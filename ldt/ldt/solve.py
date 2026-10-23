"""
Inference: parallel stochastic search down the lattice, answers verified.

Each task gets ``chains`` states, all starting from the typed top. A round runs
the model once on every chain, kills, projects, and then:

- a chain whose state is empty, or whose conflict head fires, restarts;
- a chain whose state is a total tree runs it on the demonstrations: a
  consistent program is recorded with its test output, and the chain restarts
  to look for others;
- every other chain pins one frontier position.

The answer is never the network's word: a program is kept only when it
reproduces every demonstration. Answers are ranked by the number of programs
that give them, then by the size of the smallest. A ``uniform`` model (all
logits zero) kills nothing and pins uniformly at random: the search of the
Scott domain alone, the untrained control.
"""

from __future__ import annotations

import random
import time
from collections import defaultdict
from dataclasses import dataclass, field

import torch

from ldt.bohm import Space
from ldt.data import Task, colour_permutation, encode, label_permutation
from ldt.lattice import Typing, is_total, pin
from ldt.synth import run


@dataclass
class Result:
    name: str
    programs: dict = field(default_factory=dict)  # program -> test outputs
    first_call: int | None = None  # model calls until the first program
    calls: int = 0
    attempts: list = field(default_factory=list)
    pruned: int = 0  # chains restarted by abstract evaluation


def complete(result: Result) -> int:
    """The programs found that answer every test input."""
    return sum(None not in outputs for outputs in result.programs.values())


def rank(result: Result, space_sizes: dict, attempts: int = 2) -> list:
    """ARC's attempts: for each test input, its outputs over the consistent
    programs, by the number of programs giving them, then by the size of the
    smallest; an undefined output is never an attempt."""
    if not result.programs:
        return []
    ranked = []
    for j in range(len(next(iter(result.programs.values())))):
        votes = defaultdict(list)
        for program, outputs in result.programs.items():
            if outputs[j] is not None:
                votes[outputs[j]].append(space_sizes[program])
        ranked.append(sorted(
            votes, key=lambda o: (-len(votes[o]), min(votes[o])))[:attempts])
    return ranked


def solve(space: Space, typing: Typing, model, tasks: list[Task],
          chains: int = 32, rounds: int = 200, slots: int = 16,
          theta: float = 0.1, theta_cls: float = 0.6, temperature: float = 1.5,
          enough: int = 4, augment: bool = True, length: int = 96,
          pairs: int = 5, seed: int = 0, device="cuda",
          log=None, prune=None, free: float = 0.0):
    """Search ``tasks`` with ``slots`` tasks of ``chains`` chains at a time,
    ``rounds`` model calls per chain at most, stopping a task once ``enough``
    distinct programs are found. With ``prune`` (an
    :class:`ldt.abstract.Abstract`), a chain whose partial tree is in sound
    conflict with the demonstrations restarts before it is total. A
    fraction ``free`` of each task's chains never kills and never trusts the
    conflict head: the model only orders their pins, so they search the whole
    typed domain and an unsound kill cannot hide a program from every chain."""
    if prune is not None and not hasattr(space, "prims"):
        raise ValueError("abstract evaluation reads Böhm trees")
    # a colour permutation is undone on programs through c0..c9 only
    augment = augment and "c1" in space.index
    rng = random.Random(seed)
    gen = torch.Generator(device=device).manual_seed(seed)
    queue = list(range(len(tasks)))
    results = [Result(t.name) for t in tasks]
    B = slots * chains
    slot_task = [None] * slots
    slot_rounds = [0] * slots
    perms = [None] * B
    top = typing.top.to(device)
    x = top[None].expand(B, -1, -1).clone()
    guided = (torch.arange(B, device=device) % chains) >= round(free * chains)
    theta_row = torch.where(guided, theta, 0.0)[:, None, None]
    t0 = time.time()

    def load(s):
        if not queue:
            slot_task[s] = None
            return
        i = queue.pop(0)
        slot_task[s], slot_rounds[s] = i, 0
        rows = range(s * chains, (s + 1) * chains)
        chain_perms = [colour_permutation(rng) if augment and k else
                       list(range(10)) for k in range(chains)]
        demos[rows.start:rows.stop] = encode(
            [tasks[i]] * chains, space, 1, length, pairs,
            chain_perms)[0].to(device)
        for r, p in zip(rows, chain_perms):
            perms[r] = p
        x[rows.start:rows.stop] = top

    demos = encode(tasks[:1], space, 1, length, pairs)[0]
    demos = demos.new_zeros((B, ) + demos.shape[1:]).to(device)
    for s in range(slots):
        load(s)
    sizes = {}
    while any(t is not None for t in slot_task):
        with torch.no_grad(), torch.autocast(
                device_type="cuda", dtype=torch.bfloat16,
                enabled=device == "cuda"):
            if model is None:
                b = torch.zeros(x.shape, device=device)
                k = torch.full((B, ), -1e4, device=device)
            else:
                memory, pad = model.encode_demos(demos)
                cand, conf = model(x, memory, pad)
                b, k = cand[-1].float(), conf[-1].float()
        x1 = typing(x & ~(b.sigmoid() < theta_row))
        empty = ~x1[:, 0].any(-1)
        restart = empty | ((k.sigmoid() > theta_cls) & guided)
        total = is_total(x1) & ~restart
        if prune is not None:
            from ldt.abstract import partial_tree
            states = x1.cpu().numpy()
            for r in (~restart & ~total).nonzero()[:, 0].tolist():
                i = slot_task[r // chains]
                if i is None:
                    continue
                inverse = [0] * 10
                for c, v in enumerate(perms[r]):
                    inverse[v] = c
                tree = partial_tree(space, states[r])
                if tree is not None and prune.conflict(
                        _relabel(tree, space, inverse), tasks[i].train):
                    restart[r] = True
                    results[i].pruned += 1
        for r in total.nonzero()[:, 0].tolist():
            s = r // chains
            i = slot_task[s]
            if i is None:
                continue
            labels = x1[r].float().argmax(-1).cpu().numpy()
            inverse = [0] * 10
            for c, v in enumerate(perms[r]):
                inverse[v] = c
            labels = label_permutation(space, inverse)[labels]
            tree = space.decode(labels)
            restart[r] = True
            if tree is not None:
                tree = space.canonical(tree)
            if tree is None or tree in results[i].programs:
                continue
            f = space.compile(tree)
            if all(run(f, a) == y for a, y in tasks[i].train):
                outs = tuple(run(f, a) for a, _ in tasks[i].test)
                results[i].programs[tree] = outs
                sizes[tree] = tree.size
                if results[i].first_call is None:
                    results[i].first_call = (slot_rounds[s] + 1) * chains
        x1 = typing(pin(x1, b, typing.parent, temperature, gen, ~restart))
        x1[restart] = top
        x = x1
        for s in range(slots):
            i = slot_task[s]
            if i is None:
                continue
            slot_rounds[s] += 1
            results[i].calls += chains
            if slot_rounds[s] >= rounds or complete(results[i]) >= enough:
                results[i].attempts = rank(results[i], sizes)
                load(s)
                if log and slot_task[s] is None or (log and len(queue) % 50 == 0):
                    log({"left": len(queue), "sec": round(time.time() - t0)})
    return results


def _relabel(tree, space, perm):
    """A tree with its colour constants mapped by ``perm``."""
    if tree is None:
        return None
    head = tree.head
    if head[0] == "c" and head[1:].isdigit():
        head = f"c{perm[int(head[1:])]}"
    return type(tree)(head, tuple(_relabel(a, space, perm) for a in tree.args))


def correct(task: Task, attempts: list) -> tuple[bool, bool, float]:
    """Top-1, pass@2 (every test output among its two attempts) and the
    official per-output credit (the share of test outputs among them)."""
    truth = [y for _, y in task.test]
    if len(attempts) != len(truth):
        return False, False, 0.0
    hits = [y in a for y, a in zip(truth, attempts)]
    first = [bool(a) and a[0] == y for y, a in zip(truth, attempts)]
    return all(first), all(hits), sum(hits) / len(truth)


def score(tasks: list[Task], results: list[Result]) -> dict:
    """Top-1, pass@2 and per-output pass@2 over a benchmark."""
    rows = [correct(t, r.attempts) for t, r in zip(tasks, results)]
    return {"tasks": len(tasks), "top1": sum(r[0] for r in rows),
            "pass2": sum(r[1] for r in rows),
            "pass2_outputs": round(sum(r[2] for r in rows), 2),
            "found": sum(bool(r.programs) for r in results)}
