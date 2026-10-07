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
from dataclasses import dataclass

import torch

from dc.data import Task, onehot
from dc.library import Library
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
    keep: int = 3
    seed: int = 0


@dataclass
class Solution:
    term: Term
    structure: float
    params: float
    data: float
    train_exact: bool
    weights: dict  # parameter name -> trained value, for abstraction
    test_prediction: tuple[int, ...]

    @property
    def dl(self) -> float:
        return self.structure + self.params + self.data


def seed_for(*keys) -> int:
    return zlib.crc32("/".join(map(str, keys)).encode())


def fit(term: Term, task: Task, library: Library, semantics: Semantics, config: Config,
        iteration: int) -> Solution:
    """
    Fit the parameters of one candidate on the training pairs: Adam on the
    data bits, each step followed by a proximal step shrinking every
    deviation from the prior towards zero, so that a parameter the data does
    not consistently push stays exactly at its prior and costs nothing. Then
    round the deviations below half a quantum back to the prior and score.
    """
    torch.manual_seed(seed_for(config.seed, iteration, task.name, term))
    model = semantics.model(term, library)
    inputs = onehot([i for i, _ in task.train])
    targets = torch.tensor([o for _, o in task.train])
    parameters = list(model.parameters())
    if parameters:
        optimiser = torch.optim.Adam(parameters, lr=config.lr)
        for _ in range(config.steps):
            optimiser.zero_grad()
            nll_bits(model(inputs), targets).backward()
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
    """The ``max_candidates`` terms of highest prior probability, up to ``max_size`` boxes."""
    from dc.terms import enumerate_terms
    terms = enumerate_terms(library, config.max_size)
    return sorted(terms, key=lambda t: (structure_bits(t, library), str(t)))[:config.max_candidates]


def wake(task: Task, terms: list[Term], library: Library, semantics: Semantics, config: Config,
         iteration: int) -> list[Solution]:
    """The ``keep`` candidates of least description length on this task, best first."""
    torch.set_num_threads(1)
    solutions = [fit(t, task, library, semantics, config, iteration) for t in terms]
    return sorted(solutions, key=lambda s: s.dl)[:config.keep]
