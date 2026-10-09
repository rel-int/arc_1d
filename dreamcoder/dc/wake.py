"""
Wake: fit every candidate term to a task's training pairs and score it by
description length.

``DL = structure + parameters + data``, all in bits:

- structure: ``-log2`` of the term under the library's grammar
  (:func:`dc.terms.structure_bits`);
- parameters: every parameter's deviation from its prior value, quantised
  (:meth:`dc.semantics.Model.param_bits`);
- data: ``-log2`` of the training outputs under the fitted model, summed
  over every cell of every training pair (:func:`dc.semantics.nll_bits`).

The test pair is never seen here: it is only predicted, by ``dc.run``.
"""

from __future__ import annotations

import zlib
from dataclasses import dataclass, replace

import torch
from torch.func import functional_call, vmap

from dc.data import Task, onehot
from dc.library import CELLS, Library
from dc.semantics import Semantics, nll_bits
from dc.terms import Term, structure_bits


@dataclass
class Config:
    max_size: int = 3
    max_candidates: int = 80
    steps: int = 100
    lr: float = 0.05
    delta: float = 0.01  # quantum of the parameter code
    shrink: float = 0.5  # proximal step after each Adam step, as a fraction of lr
    stop_bits: float = 0.1  # stop fitting once the training pairs fit exactly within this many bits
    quotas: str = ""  # e.g. "3:57,4:50,5:43": the most probable 57 of size <= 3, 50 of size 4, 43 of size 5
    keep: int = 3
    seed: int = 0
    restarts: int = 1  # starts per candidate with --batched: the prior, then perturbations of it
    noise: float = 0.1  # scale of the Gaussian perturbation of a restart
    select: str = "dl"  # "dl", or "loo" to re-rank the kept candidates by leave-one-out with --batched


@dataclass
class Solution:
    term: Term
    structure: float
    params: float
    data: float
    train_exact: bool
    weights: dict  # parameter name -> trained value, for abstraction
    test_prediction: tuple[int, ...]
    loo: int | None = None  # training pairs predicted when fitted on the others, if selected by it

    @property
    def dl(self) -> float:
        return self.structure + self.params + self.data

    def rank(self, select: str) -> tuple:
        """The sort key of a selector: least DL, or most pairs held out and predicted then least DL."""
        return (self.dl,) if select == "dl" else (-self.loo, self.dl)


def seed_for(*keys) -> int:
    return zlib.crc32("/".join(map(str, keys)).encode())


def fit(term: Term, task: Task, library: Library, semantics: Semantics, config: Config,
        iteration: int) -> Solution:
    """
    Fit the parameters of one candidate on the training pairs: Adam on the
    data bits, each step followed by a proximal step shrinking every
    deviation from the prior towards zero, so that a parameter the data does
    not consistently push stays exactly at its prior and costs nothing. Stop
    early once the training pairs fit exactly within ``stop_bits``, since
    further steps only buy confidence. Then round the deviations below half a
    quantum back to the prior and score.
    """
    torch.manual_seed(seed_for(config.seed, iteration, task.name, term))
    model = semantics.model(term, library)
    inputs = onehot([i for i, _ in task.train])
    targets = torch.tensor([o for _, o in task.train])
    parameters = list(model.parameters())
    if parameters:
        optimiser = torch.optim.Adam(parameters, lr=config.lr)
        for step in range(config.steps):
            optimiser.zero_grad()
            output = model(inputs)
            data = nll_bits(output, targets)
            if step % 10 == 9 and data < config.stop_bits and (output.argmax(-1) == targets).all():
                break
            data.backward()
            optimiser.step()
            model.shrink(config.shrink * config.lr)
        model.snap(config.delta)
    with torch.no_grad():
        output = model(inputs)
        prediction = model(onehot([task.test[0]])).argmax(-1)[0]
        return Solution(
            term=term, structure=structure_bits(term, library),
            params=float(model.param_bits(config.delta)), data=float(nll_bits(output, targets)),
            train_exact=bool((output.argmax(-1) == targets).all()),
            weights={name: p.detach().clone() for name, p in model.slot_parameters()},
            test_prediction=tuple(prediction.tolist()))


def candidates(library: Library, config: Config) -> list[Term]:
    """
    The terms of highest prior probability up to ``max_size`` boxes: the
    ``max_candidates`` best overall, or with ``quotas`` the best few of each
    size bucket, so that a search budget reaches the larger sizes at all.
    """
    from dc.terms import enumerate_terms
    ranked = sorted(enumerate_terms(library, config.max_size),
                    key=lambda t: (structure_bits(t, library), str(t)))
    if not config.quotas:
        return ranked[:config.max_candidates]
    chosen, low = [], 1
    for bucket in config.quotas.split(","):
        high, count = map(int, bucket.split(":"))
        chosen += [t for t in ranked if low <= t.size <= high][:count]
        low = high + 1
    return chosen


def wake(task: Task, terms: list[Term], library: Library, semantics: Semantics, config: Config,
         iteration: int) -> list[Solution]:
    """The ``keep`` candidates of least description length on this task, best first."""
    torch.set_num_threads(1)
    solutions = [fit(t, task, library, semantics, config, iteration) for t in terms]
    return sorted(solutions, key=lambda s: s.dl)[:config.keep]


@dataclass
class Batch:
    """
    Tasks padded to one length with background: training inputs
    ``(tasks, pairs, length, 10)``, targets and grid cells ``(tasks, pairs,
    length)``, and the test inputs and cells with one pair each.
    """
    inputs: torch.Tensor
    targets: torch.Tensor
    mask: torch.Tensor
    test: torch.Tensor
    test_mask: torch.Tensor

    @classmethod
    def of(cls, tasks: list[Task]) -> Batch:
        length = max(t.length for t in tasks)
        pad = lambda grid: list(grid) + [0] * (length - len(grid))
        cells = lambda grid: [c < len(grid) for c in range(length)]
        return cls(
            inputs=torch.stack([onehot([pad(i) for i, _ in t.train]) for t in tasks]),
            targets=torch.tensor([[pad(o) for _, o in t.train] for t in tasks]),
            mask=torch.tensor([[cells(i) for i, _ in t.train] for t in tasks]),
            test=torch.stack([onehot([pad(t.test[0])]) for t in tasks]),
            test_mask=torch.tensor([[cells(t.test[0])] for t in tasks]))


def masked_bits(output: torch.Tensor, targets: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """:func:`dc.semantics.nll_bits` of each task of a batch, over its grid cells alone."""
    p = output.gather(-1, targets[..., None]).squeeze(-1).clamp(min=1e-9)
    return torch.where(mask, -torch.log2(p), 0.).sum((1, 2))


def starts(prior: dict, config: Config, iteration: int, term: Term) -> dict:
    """
    ``config.restarts`` starting points per parameter, stacked: the prior,
    then the prior plus Gaussian noise of scale ``noise``, drawn from a
    generator seeded by ``(seed, iteration, term)`` and the same for every task,
    so that a task's fit does not depend on what else is in its batch.
    """
    generator = torch.Generator().manual_seed(seed_for(config.seed, iteration, term))
    noise = lambda p: config.noise * torch.randn(
        config.restarts - 1, *p.shape, generator=generator, device="cpu")
    return {k: torch.cat([p[None], p + noise(p).to(p.device)]) for k, p in prior.items()}


def fit_batch(term: Term, tasks: list[Task], batch: Batch, library: Library,
              semantics: Semantics, config: Config, iteration: int = 0) -> list[Solution]:
    """
    :func:`fit` on every task at once, from each of :func:`starts`: one
    model, its parameters stacked along a leading axis of tasks times starts
    and the forward pass vmapped over it, with one Adam over the stack,
    which, being elementwise, is one Adam per task and start. An instance
    that fits within ``stop_bits`` is frozen at the step where :func:`fit`
    would have stopped. Each task keeps the start of least DL, the first on a tie.
    """
    model = semantics.model(term, library)
    slot = {id(p): name for name, p in model.slot_parameters()}
    named = dict(model.named_parameters())
    restarts = config.restarts if named else 1
    tasks_by_start = lambda x: x.repeat_interleave(restarts, 0)
    origin = starts({k: p.detach() for k, p in named.items()}, replace(config, restarts=restarts),
                    iteration, term)
    prior = {k: p.detach().expand(len(tasks) * restarts, *p.shape).clone() for k, p in named.items()}
    params = {k: p.repeat(len(tasks), *[1] * (p.dim() - 1)).requires_grad_() for k, p in origin.items()}
    inputs, targets, mask = map(tasks_by_start, (batch.inputs, batch.targets, batch.mask))

    def run(weights, grids, cells):
        CELLS.mask = cells
        try:
            return functional_call(model, weights, (grids,))
        finally:
            CELLS.mask = None

    forward = vmap(run)
    exact = lambda output, targets, mask: ((output.argmax(-1) == targets) | ~mask).flatten(1).all(1)
    if params:
        optimiser = torch.optim.Adam(params.values(), lr=config.lr)
        active = torch.ones(len(inputs), dtype=torch.bool)
        frozen = {k: p.detach().clone() for k, p in params.items()}
        for step in range(config.steps):
            optimiser.zero_grad()
            output = forward(params, inputs, mask)
            data = masked_bits(output, targets, mask)
            if step % 10 == 9:
                done = active & (data < config.stop_bits) & exact(output, targets, mask)
                for k, p in params.items():
                    frozen[k][done] = p.detach()[done]
                active &= ~done
                if not active.any():
                    break
            data.sum().backward()
            optimiser.step()
            with torch.no_grad():
                step_size = config.shrink * config.lr
                for k, p in params.items():
                    d = p - prior[k]
                    p.copy_(prior[k] + d.sign() * (d.abs() - step_size).clamp(min=0))
                    p[~active] = frozen[k][~active]
        with torch.no_grad():
            for k, p in params.items():
                small = (p - prior[k]).abs() < config.delta / 2
                p[small] = prior[k][small]
    with torch.no_grad():
        output = forward(params, inputs, mask)
        data = masked_bits(output, targets, mask)
        fits = exact(output, targets, mask)
        predictions = forward(params, *map(tasks_by_start, (batch.test, batch.test_mask))).argmax(-1)[:, 0]
        bits = sum((torch.log2(1 + (p - prior[k]).abs() / config.delta).flatten(1).sum(1)
                    for k, p in params.items()), torch.zeros(len(inputs)))
    structure = structure_bits(term, library)
    chosen = (bits + data).view(len(tasks), restarts).argmin(1) + torch.arange(len(tasks)) * restarts
    return [Solution(
        term=term, structure=structure, params=float(bits[i]), data=float(data[i]),
        train_exact=bool(fits[i]),
        weights={slot[id(p)]: params[k][i].detach().cpu().clone() for k, p in named.items()},
        test_prediction=tuple(predictions[i, :task.length].tolist()))
        for i, task in zip(chosen.tolist(), tasks)]


def folds(task: Task) -> list[Task]:
    """The task fitted on all its training pairs but one and tested on that one, for each one."""
    return [Task(task.family, task.name, task.train[:k] + task.train[k + 1:], task.train[k])
            for k in range(len(task.train))]


def leave_one_out(term: Term, tasks: list[Task], library: Library, semantics: Semantics,
                  config: Config, iteration: int) -> list[int]:
    """For each task, how many of its training pairs ``term`` predicts when fitted on the others."""
    held_out = [fold for task in tasks for fold in folds(task)]
    solutions = fit_batch(term, held_out, Batch.of(held_out), library, semantics,
                          replace(config, restarts=1), iteration)
    hits = [s.test_prediction == fold.test[1] for s, fold in zip(solutions, held_out)]
    per_task = len(held_out) // len(tasks)
    return [sum(hits[i:i + per_task]) for i in range(0, len(hits), per_task)]


def wake_batch(tasks: list[Task], terms: list[Term], library: Library, semantics: Semantics,
               config: Config, iteration: int = 0, device: str = "cpu",
               progress=None) -> dict[str, list[Solution]]:
    """
    :func:`wake` on every task, one term at a time over all of them, keeping
    the ``keep`` candidates of least description length on each as it goes;
    the sort is stable, so ties fall as in :func:`wake`. With ``select`` set
    to ``loo``, the kept candidates are then fitted once more per training
    pair, on the other pairs, and re-ranked by how many they predict.
    """
    best = {t.name: [] for t in tasks}
    with torch.device(device):
        batch = Batch.of(tasks)
        for n, term in enumerate(terms):
            solutions = fit_batch(term, tasks, batch, library, semantics, config, iteration)
            for task, solution in zip(tasks, solutions):
                best[task.name] = sorted(best[task.name] + [solution], key=lambda s: s.dl)[:config.keep]
            if progress:
                progress(n + 1, len(terms))
        if config.select == "loo":
            by_term = {}
            for task in tasks:
                for solution in best[task.name]:
                    by_term.setdefault(solution.term, []).append((task, solution))
            for term, kept in by_term.items():
                hits = leave_one_out(term, [t for t, _ in kept], library, semantics, config, iteration)
                for (_, solution), hit in zip(kept, hits):
                    solution.loo = hit
            for name in best:
                best[name].sort(key=lambda s: s.rank(config.select))
    return best
