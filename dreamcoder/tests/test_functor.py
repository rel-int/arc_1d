import torch

from discopy.neural.network import Box, Network

from dc.abstract import abstract, rename
from dc.data import onehot
from dc.library import FEAT, GRID, Library, Paint, Reflect, Scan, Segment
from dc.semantics import TraceFree
from dc.terms import X, Slot, Term
from dc.wake import Solution


def symbolic(name, dom, cod, path):
    return Box(name, dom, cod, module=Slot(name, path))


GRIDS = onehot([[0, 3, 0, 0, 3, 0, 0], [5, 5, 0, 2, 0, 0, 7]])


def test_functor_on_hand_built_diagram():
    """copy x three ways, discard one, reflect another, paint the third with its scan."""
    library = Library.base()
    reflect = symbolic("reflect", GRID, GRID, "a")
    scan = symbolic("scan", GRID, FEAT, "b")
    paint = symbolic("paint", GRID @ FEAT, GRID, "c")
    diagram = (Network.copy(GRID, 3)
               >> Network.discard(GRID) @ reflect @ scan >> paint)
    assert diagram.dom == diagram.cod == GRID
    compiled, slots = TraceFree().compile(diagram, library)
    assert set(slots) == {"a", "b", "c"}
    assert isinstance(slots["a"], Reflect) and isinstance(slots["c"], Paint)
    with torch.no_grad():
        slots["c"].theta.copy_(torch.randn(5))
        expected = slots["c"](GRIDS.flip(1), slots["b"](GRIDS))
        assert torch.allclose(compiled(GRIDS), expected)


def test_functor_preserves_composition():
    library = Library.base()
    f, g = symbolic("reflect", GRID, GRID, "f"), symbolic("segment", GRID, FEAT, "g")
    compiled, slots = TraceFree().compile(f >> g, library)
    assert torch.equal(compiled(GRIDS), slots["g"](slots["f"](GRIDS)))
    assert isinstance(slots["g"], Segment)


def test_occurrences_get_their_own_modules():
    model = TraceFree().model(Term("shift", (Term("shift", (X,)),)), Library.base())
    assert len(model.slots) == 2 and model.slots["r"] is not model.slots["r_0"]
    assert len(list(model.parameters())) == 2


def test_model_starts_at_its_prior_and_pays_for_deviations():
    model = TraceFree().model(Term("paint", (X, Term("scan", (X,)))), Library.base())
    assert model.param_bits(0.01).item() == 0
    assert torch.equal(model(GRIDS).argmax(-1), GRIDS.argmax(-1))  # paint starts as the identity
    with torch.no_grad():
        model.slots["r"].bias[3] += 1.
    assert abs(model.param_bits(0.01).item() - torch.log2(torch.tensor(101.)).item()) < 1e-4
    model.shrink(0.4)
    assert abs(model.slots["r"].bias[3].item() - 0.6) < 1e-6
    model.snap(2.)
    assert model.param_bits(0.01).item() == 0


def test_abstraction_carries_trained_weights():
    library, semantics = Library.base(), TraceFree()
    body = Term("paint", (X, Term("segment", (X,))))
    trained = semantics.model(body, library)
    with torch.no_grad():
        trained.slots["r"].bias.fill_(0.5)
    weights = {name: p.detach().clone() for name, p in trained.slot_parameters()}
    best = {name: Solution(body, 0., 0., 0., True, weights, ()) for name in ("t1", "t2")}
    assert rename(weights, "r") == weights
    added = abstract(library, best, 1, iteration=0)
    assert [e.signature() for e in added] == ["f0a : Grid -> Grid"]
    reused = semantics.model(Term("f0a", (X,)), library)
    assert reused.param_bits(0.01).item() == 0  # inherited weights are its prior
    assert torch.allclose(reused(GRIDS), trained(GRIDS))
    assert library.weights["f0a"] == 3 and library.weights["paint"] == 3 and library.weights["shift"] == 1
