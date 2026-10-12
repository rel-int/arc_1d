"""
Selection: which of a task's kept candidates answers its test pair.

Each selector re-ranks the kept candidates, the first being the answer. Two
rank the candidates themselves:

- ``dl``: least description length;
- ``loo``: most training pairs predicted when fitted on the others, then least DL.

The others are votes: every kept candidate gives a weight to the test
prediction it makes, and the candidates predicting the heaviest one come
first, in the order of ``loo``. Candidates agreeing on an output pool their
evidence, where a ranking hears only the best of them.

- ``bma``: weight ``2^-DL``, i.e. the posterior of a candidate under the MDL
  prior, so that the vote is Bayesian model averaging over the kept ones;
- ``vote_loo``: weight ``loo + 1``, the held-out evidence alone;
- ``vote``: weight ``2^-DL`` times ``(loo + 1) / (pairs + 2)``, the
  prior times Laplace's estimate of the chance to predict an unseen pair.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dc.wake import Solution

PAIRS = 3  # training pairs per task in 1D-ARC, the most a candidate can predict held out


def weight(solution: Solution, best_dl: float, rule: str) -> float:
    """The weight of a candidate's vote, its prior relative to the best one's so that it never underflows."""
    prior = 2. ** (best_dl - solution.dl)
    if rule == "bma":
        return prior
    if rule == "vote_loo":
        return solution.loo + 1
    return prior * (solution.loo + 1) / (PAIRS + 2)


def select(solutions: list[Solution], rule: str) -> list[Solution]:
    """The kept candidates of one task, re-ranked by ``rule``."""
    by_loo = sorted(solutions, key=lambda s: (-(s.loo or 0), s.dl))
    if rule == "dl":
        return sorted(solutions, key=lambda s: s.dl)
    if rule == "loo":
        return by_loo
    best_dl = min(s.dl for s in solutions)
    score = defaultdict(float)
    for solution in solutions:
        score[solution.test_prediction] += weight(solution, best_dl, rule)
    return sorted(by_loo, key=lambda s: -score[s.test_prediction])


SELECTORS = ("dl", "loo", "bma", "vote_loo", "vote")
NEEDS_LOO = {"loo", "vote_loo", "vote"}
