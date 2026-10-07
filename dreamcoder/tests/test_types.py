import itertools

import pytest
import torch

from discopy.utils import AxiomError

from dc.library import FEAT, GRID, TYPES, Library, equivariant
from dc.terms import X, Term, enumerate_terms, structure_bits, to_diagram


@pytest.fixture
def library():
    return Library.base()


def well_typed(term, library, expected="Grid"):
    if term.head == "x":
        return expected == "Grid"
    entry = library[term.head]
    return entry.cod == expected and len(term.args) == len(entry.dom) and all(
        well_typed(a, library, t) for a, t in zip(term.args, entry.dom))


def test_types_are_distinct():
    assert GRID != FEAT and TYPES == {"Grid": GRID, "Feat": FEAT}


def test_enumeration_is_well_typed(library):
    terms = enumerate_terms(library, 3)
    assert len(terms) == len(set(terms)) == 57
    for term in terms:
        assert well_typed(term, library) and 1 <= term.size <= 3
        diagram = to_diagram(term, library)
        assert diagram.dom == diagram.cod == GRID
        assert len([b for b in diagram.boxes if b.name in library.entries]) == term.size


def test_enumeration_prunes_idempotents(library):
    names = {str(t) for t in enumerate_terms(library, 2)}
    assert "reflect(reflect(x))" not in names and "shift(shift(x))" in names


def test_ill_typed_terms_are_refused(library):
    with pytest.raises((AxiomError, TypeError)):
        to_diagram(Term("paint", (X, X)), library)
    with pytest.raises((AxiomError, TypeError)):
        to_diagram(Term("recolour", (Term("scan", (X,)),)), library)


def test_prior_is_a_distribution(library):
    total = sum(2 ** -structure_bits(t, library) for t in enumerate_terms(library, 6))
    assert 0.3 < total <= 0.5  # x alone has the other half; pruning and the tail lose the rest


def test_equivariant_commutes_with_foreground_permutations():
    m = equivariant(torch.randn(5))
    for perm in itertools.islice(itertools.permutations(range(1, 10)), 50):
        p = torch.eye(10)[[0, *perm]]
        assert torch.allclose(p @ m, m @ p, atol=1e-6)


def test_terms_read_back_from_their_print(library):
    for term in enumerate_terms(library, 3):
        assert Term.parse(str(term)) == term
