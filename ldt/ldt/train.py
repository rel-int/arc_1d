"""
On-policy training: the paper's Solve loop over a pool of states.

Each step runs the model on the pool, takes one optimiser step on the loss
against the alpha targets, then moves every state one step down the lattice:
kill the labels whose sigmoid is below ``theta``, project onto the well-typed
trees, and, unless the state is truly conflicted or solved (both checked
against ``Y``, and a total tree outside ``Y`` by running it on the
demonstrations), pin one frontier position. Finished or stale states are
replaced by fresh tasks under a random colour permutation.

The conflict target is "no solution of ``Y`` survives in ``x``", not "some
position is empty in the union of the survivors", which differ once K > 1.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import asdict, dataclass

import torch
import torch.nn.functional as F

from ldt.bohm import Space
from ldt.data import (Task, colour_permutation, encode, label_permutation,
                      permute)
from ldt.lattice import alpha, consistent, is_total, pin
from ldt.model import LDT, Config


@dataclass
class TrainConfig:
    steps: int = 20000
    batch: int = 256
    lr: float = 1e-3
    weight_decay: float = 0.1
    warmup: float = 0.05
    clip: float = 1.0
    w_pos: float = 4.0
    w_neg: float = 0.5
    l_cls: float = 0.1
    l_ce: float = 0.2
    theta: float = 0.1
    temperature: float = 1.5
    max_age: int = 100
    max_solutions: int = 16
    length: int = 96
    pairs: int = 5
    seed: int = 0
    log_every: int = 100
    augment: bool = True  # colour permutations of each task drawn


def verify(space: Space, labels, train) -> bool:
    """Whether a total label vector is a program consistent with ``train``."""
    from ldt.synth import run
    tree = space.decode(labels)
    if tree is None or not space.check(tree):
        return False
    f = space.compile(tree)
    return all(run(f, x) == y for x, y in train)


def losses(cand, conf, x, target, conflicted, c: TrainConfig):
    """The paper's loss (1), averaged over the loops."""
    alive = x.float()
    tgt = target.float()
    singleton = (target.sum(-1) == 1) & (x.sum(-1) > 1)
    label = target.float().argmax(-1)
    total = 0.0
    parts = {"bce": 0.0, "cls": 0.0, "ce": 0.0}
    for b, k in zip(cand, conf):
        b = b.float()
        weight = alive * (c.w_pos * tgt + c.w_neg * (1 - tgt))
        bce = (F.binary_cross_entropy_with_logits(b, tgt, reduction="none")
               * weight).sum() / alive.sum().clamp(min=1)
        cls = F.binary_cross_entropy_with_logits(k.float(), conflicted.float())
        if singleton.any():
            masked = b.masked_fill(~x, -1e4)[singleton]
            ce = F.cross_entropy(masked, label[singleton])
        else:
            ce = b.sum() * 0
        total = total + bce + c.l_cls * cls + c.l_ce * ce
        parts["bce"] += bce.item() / len(cand)
        parts["cls"] += cls.item() / len(cand)
        parts["ce"] += ce.item() / len(cand)
    return total / len(cand), parts


class Pool:
    """A batch of states in flight, each with its task."""

    def __init__(self, space: Space, typing: torch.nn.Module, tasks: list[Task],
                 c: TrainConfig, device):
        self.space, self.typing, self.tasks, self.c = space, typing, tasks, c
        self.device = device
        self.rng = random.Random(c.seed)
        B = c.batch
        self.task = [None] * B
        self.demos = None
        self.Y = torch.zeros(B, c.max_solutions, space.n_positions,
                             dtype=torch.long, device=device)
        self.valid = torch.zeros(B, c.max_solutions, dtype=torch.bool,
                                 device=device)
        self.x = typing.top[None].expand(B, -1, -1).clone().to(device)
        self.prev = self.x.clone()
        self.age = torch.zeros(B, dtype=torch.long, device=device)
        self.perm = [None] * B
        self.train = [None] * B  # the demonstrations in the permuted frame
        self.refill(torch.ones(B, dtype=torch.bool, device=device))

    def refill(self, rows: torch.Tensor):
        index = rows.nonzero()[:, 0].tolist()
        if not index:
            return
        tasks = [self.rng.choice(self.tasks) for _ in index]
        perms = [self.permutation(t) for t in tasks]
        demos, Y, valid = encode(
            tasks, self.space, self.c.max_solutions, self.c.length,
            self.c.pairs, perms)
        if self.demos is None:
            self.demos = demos.new_zeros(
                (self.c.batch, ) + demos.shape[1:]).to(self.device)
        idx = torch.tensor(index, device=self.device)
        self.demos[idx] = demos.to(self.device)
        self.Y[idx] = Y.to(self.device)
        self.valid[idx] = valid.to(self.device)
        self.x[idx] = self.typing.top.to(self.device)
        self.prev[idx] = self.typing.top.to(self.device)
        self.age[idx] = 0
        for i, t, p in zip(index, tasks, perms):
            self.task[i], self.perm[i] = t, p
            self.train[i] = permute(t.train, p)

    def permutation(self, task: Task) -> list[int]:
        """A random colour permutation, unless the task's program does not
        commute with it (some primitives break ties by colour index), in
        which case the identity."""
        if not self.c.augment:
            return list(range(10))
        perm = colour_permutation(self.rng)
        labels = label_permutation(self.space, perm)[task.solutions[0]]
        if verify(self.space, labels, permute(task.train, perm)):
            return perm
        return list(range(10))


def schedule(step, c: TrainConfig):
    warm = max(1, int(c.warmup * c.steps))
    if step < warm:
        return step / warm
    progress = (step - warm) / max(1, c.steps - warm)
    return 0.05 + 0.95 * 0.5 * (1 + math.cos(math.pi * progress))


def train(space: Space, tasks: list[Task], config: Config, c: TrainConfig,
          device="cuda", log=print, checkpoint=None, validate=None,
          resume: dict | None = None):
    """Train from scratch, or from ``resume`` (a checkpoint's state, whose
    pool is drawn afresh), saving ``checkpoint[1](state)`` every
    ``checkpoint[0]`` steps and once more at the end, a run of no steps
    included."""
    torch.manual_seed(c.seed)
    typing = space.typing().to(device)
    model = LDT(space.n_positions, len(space.vocab), config).to(device)
    decay = [p for n, p in model.named_parameters() if p.dim() >= 2]
    rest = [p for n, p in model.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": c.weight_decay},
                             {"params": rest, "weight_decay": 0.0}],
                            lr=c.lr, betas=(0.9, 0.95))
    start = 0
    if resume is not None:
        model.load_state_dict(resume["model"])
        opt.load_state_dict(resume["optimizer"])
        start = resume["step"]
        log({"resumed": start})
    pool = Pool(space, typing, tasks, c, device)
    gen = torch.Generator(device=device).manual_seed(c.seed)

    def snapshot(step):
        return {"model": model.state_dict(), "optimizer": opt.state_dict(),
                "config": asdict(config), "train": asdict(c), "step": step}

    stats, t0 = {}, time.time()
    amp = torch.autocast(device_type="cuda", dtype=torch.bfloat16)\
        if device == "cuda" else torch.autocast("cpu", enabled=False)
    for step in range(start, c.steps):
        for g in opt.param_groups:
            g["lr"] = c.lr * schedule(step, c)
        model.train()
        x = pool.x
        target, conflicted = alpha(x, pool.Y, pool.valid)
        target = torch.where(conflicted[:, None, None], x & pool.prev, target)
        pool.prev = torch.where(conflicted[:, None, None], pool.prev, target)
        with amp:
            memory, pad = model.encode_demos(pool.demos)
            cand, conf = model(x, memory, pad)
            loss, parts = losses(cand, conf, x, target, conflicted, c)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), c.clip)
        opt.step()
        with torch.no_grad():
            b = cand[-1].float()
            killed = x & (b.sigmoid() < c.theta)
            unsound = (killed & target).any(-1).any(-1) & ~conflicted
            x1 = typing(x & ~killed)
            ok = consistent(x1, pool.Y, pool.valid).any(1)
            total = is_total(x1)
            # a total tree outside Y may still be consistent with the demos
            for i in (total & ~ok).nonzero()[:, 0].tolist():
                labels = x1[i].float().argmax(-1).cpu().numpy()
                if verify(space, labels, pool.train[i]):
                    ok[i] = True
            solved = total & ok
            truly_conflicted = ~ok
            branch = ~solved & ~truly_conflicted
            x2 = typing(pin(x1, b, typing.parent, c.temperature, gen, branch))
            pool.x = x2
            pool.age += 1
            done = solved | truly_conflicted | (pool.age > c.max_age)
            for k, v in [("loss", loss.item()), *parts.items(),
                         ("solved", solved.float().mean().item()),
                         ("conflict", truly_conflicted.float().mean().item()),
                         ("unsound", unsound.float().mean().item()),
                         ("cls_acc", ((conf[-1] > 0) == conflicted)
                          .float().mean().item()),
                         ("alive", x1.sum(-1).float().mean().item())]:
                stats[k] = stats.get(k, 0.0) + v
            pool.refill(done)
        if (step + 1) % c.log_every == 0:
            n = c.log_every
            msg = {k: round(v / n, 4) for k, v in stats.items()}
            msg.update(step=step + 1, lr=round(opt.param_groups[0]["lr"], 6),
                       sec=round(time.time() - t0, 1))
            log(msg)
            stats = {}
        if validate is not None and (step + 1) % validate[0] == 0:
            log({"step": step + 1, "validation": validate[1](model, typing)})
        if checkpoint is not None and (step + 1) % checkpoint[0] == 0:
            checkpoint[1](snapshot(step + 1))
    if checkpoint is not None:
        checkpoint[1](snapshot(c.steps))
    return model, typing
