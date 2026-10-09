import torch
from torch.func import functional_call, vmap

from dc.data import Task, onehot
from dc.library import CELLS, Library
from dc.semantics import TraceFree
from dc.terms import enumerate_terms
from dc.wake import Batch, Config, fit, fit_batch

GRIDS = [(0, 3, 3, 0, 0, 5, 0), (2, 0, 0, 0, 2, 2, 0, 0, 0, 4, 4, 4), (0, 0, 7, 0, 7)]
TASKS = [Task("f", f"t{i}", tuple((g, g[::-1]) for _ in range(3)), (g[1:] + g[:1], g))
         for i, g in enumerate(GRIDS)]


def test_padded_batch_computes_what_each_task_computes():
    """Every term up to two boxes, at random weights: padding and vmap change nothing on the grid cells."""
    library, semantics, batch = Library.base(), TraceFree(), Batch.of(TASKS)
    torch.manual_seed(0)
    for term in enumerate_terms(library, 2):
        model = semantics.model(term, library)
        weights = {k: torch.randn(len(TASKS), *p.shape) for k, p in model.named_parameters()}

        def run(w, grids, mask):
            CELLS.mask = mask
            try:
                return functional_call(model, w, (grids,))
            finally:
                CELLS.mask = None

        padded = vmap(run)(weights, batch.inputs, batch.mask)
        for i, task in enumerate(TASKS):
            alone = functional_call(model, {k: w[i] for k, w in weights.items()},
                                    (onehot([a for a, _ in task.train]),))
            assert torch.allclose(padded[i, :, :task.length], alone, atol=1e-5), term


def test_fit_batch_is_fit_on_each_task():
    """One step of training, where rounding has not yet had the time to grow."""
    library, semantics, config = Library.base(), TraceFree(), Config(steps=1)
    for term in enumerate_terms(library, 2):
        batched = fit_batch(term, TASKS, Batch.of(TASKS), library, semantics, config)
        for task, b in zip(TASKS, batched):
            a = fit(term, task, library, semantics, config, 0)
            assert abs(a.dl - b.dl) < 1e-3 and a.test_prediction == b.test_prediction, term
            assert a.weights.keys() == b.weights.keys()
