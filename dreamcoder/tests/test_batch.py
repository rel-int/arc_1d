import torch
from torch.func import functional_call, vmap

from dc.data import Task, onehot
from dc.library import CELLS, Entry, Library
from dc.semantics import TraceFree
from dc.terms import X, Term, enumerate_terms
from dc.wake import Batch, Config, fit, fit_batch, folds, leave_one_out, starts

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


def test_fit_batch_is_fit_with_a_learned_box():
    """A box carrying trained weights compiles to a nested model, which the vmap must reach too."""
    library, semantics = Library.base(), TraceFree()
    body = Term.parse("recolour(paint(x, segment(x)))")
    torch.manual_seed(1)
    weights = {k: p.detach() + 0.1 * torch.randn_like(p) for k, p in semantics.model(body, library).slot_parameters()}
    library.entries["f0a"] = Entry("f0a", ("Grid",), "Grid", body=body, weights=weights)
    library.weights["f0a"] = 3.
    for steps in (0, 1):
        for term in [t for t in enumerate_terms(library, 2) if "f0a" in str(t)]:
            batched = fit_batch(term, TASKS, Batch.of(TASKS), library, semantics, Config(steps=steps))
            for task, b in zip(TASKS, batched):
                a = fit(term, task, library, semantics, Config(steps=steps), 0)
                assert abs(a.dl - b.dl) < 1e-3 and a.test_prediction == b.test_prediction, (steps, term)


def test_restart_zero_is_the_prior_and_the_others_follow_the_seed():
    prior = {"w": torch.zeros(4)}
    first, again = (starts(prior, Config(restarts=3), 0, X) for _ in range(2))
    other = starts(prior, Config(restarts=3, seed=1), 0, X)
    assert torch.equal(first["w"][0], prior["w"]) and torch.equal(first["w"], again["w"])
    assert not torch.equal(first["w"][1:], other["w"][1:])


def test_restarts_never_fit_worse_than_the_prior_alone():
    library, semantics, batch = Library.base(), TraceFree(), Batch.of(TASKS)
    for term in enumerate_terms(library, 2)[:12]:
        one = fit_batch(term, TASKS, batch, library, semantics, Config(steps=20))
        many = fit_batch(term, TASKS, batch, library, semantics, Config(steps=20, restarts=4))
        assert all(b.dl <= a.dl + 1e-3 for a, b in zip(one, many)), term


def test_leave_one_out_counts_the_held_out_pairs_predicted():
    library, semantics, config = Library.base(), TraceFree(), Config(steps=20)
    assert all(len(f.train) == 2 and f.test == t.train[k] for t in TASKS for k, f in enumerate(folds(t)))
    reverse = leave_one_out(Term("reflect", (X,)), TASKS, library, semantics, config, 0)
    identity = leave_one_out(Term("shift", (X,)), TASKS, library, semantics, config, 0)
    assert reverse == [3, 3, 3] and identity == [0, 0, 0]
