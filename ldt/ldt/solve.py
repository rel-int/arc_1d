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


def rank(result: Result, space_sizes: dict) -> list:
    votes = defaultdict(list)
    for program, outputs in result.programs.items():
        votes[outputs].append(space_sizes[program])
    return sorted(votes, key=lambda o: (-len(votes[o]), min(votes[o])))


def solve(space: Space, typing: Typing, model, tasks: list[Task],
          chains: int = 32, rounds: int = 200, slots: int = 16,
          theta: float = 0.1, theta_cls: float = 0.6, temperature: float = 1.5,
          enough: int = 4, augment: bool = True, length: int = 96,
          pairs: int = 5, seed: int = 0, device="cuda", log=None):
    """Search ``tasks`` with ``slots`` tasks of ``chains`` chains at a time,
    ``rounds`` model calls per chain at most, stopping a task once ``enough``
    distinct programs are found."""
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
    inputs = outputs = None
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
        inp, out, _, _ = encode([tasks[i]] * chains, space, 1, length, pairs,
                                chain_perms)
        inputs[rows.start:rows.stop] = inp.to(device)
        outputs[rows.start:rows.stop] = out.to(device)
        for r, p in zip(rows, chain_perms):
            perms[r] = p
        x[rows.start:rows.stop] = top

    inputs = torch.zeros(B, pairs, length, dtype=torch.long, device=device)
    outputs = torch.zeros_like(inputs)
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
                memory, pad = model.encode_demos(inputs, outputs)
                cand, conf = model(x, memory, pad)
                b, k = cand[-1].float(), conf[-1].float()
        x1 = typing(x & ~(b.sigmoid() < theta))
        empty = ~x1[:, 0].any(-1)
        restart = empty | (k.sigmoid() > theta_cls)
        total = is_total(x1) & ~restart
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
            if slot_rounds[s] >= rounds or len(results[i].programs) >= enough:
                results[i].attempts = rank(results[i], sizes)[:2]
                load(s)
                if log and slot_task[s] is None or (log and len(queue) % 50 == 0):
                    log({"left": len(queue), "sec": round(time.time() - t0)})
    return results


def score(tasks: list[Task], results: list[Result]) -> dict:
    """Top-1 and pass@2 (every test output right among two attempts)."""
    top1 = pass2 = 0
    for task, result in zip(tasks, results):
        truth = tuple(y for _, y in task.test)
        top1 += bool(result.attempts) and result.attempts[0] == truth
        pass2 += truth in result.attempts[:2]
    return {"tasks": len(tasks), "top1": top1, "pass2": pass2,
            "found": sum(bool(r.programs) for r in results)}
