"""
The lattice operations of a batch of states, on the device.

A state is a boolean tensor ``x`` of shape ``(batch, positions, labels)``: the
labels still alive at each address of the Böhm tree. Shrinking ``x`` adds
information (``⊑`` in the paper's convention, Scott-above in the domain of
partial Böhm trees); an all-empty state is the bottom element, a conflict.

- :class:`Typing` is :meth:`ldt.bohm.Space.propagate` batched: the exact
  projection of the well-typed trees, run after every kill and every pin.
- :func:`alpha` is the paper's alpha operator over the solutions still
  consistent with a state.
- :func:`pin` is the branching step: one undecided position whose parent is
  decided (a frontier of the partial Böhm tree, i.e. forcing one argument) is
  pinned to a label drawn from the model's logits.
"""

from __future__ import annotations

import torch

from ldt.bohm import Space


class Typing(torch.nn.Module):
    """The typing automaton of a :class:`Space` as buffers on the device."""

    def __init__(self, space: Space):
        super().__init__()
        self.space = space
        f = lambda a: torch.as_tensor(a)  # noqa: E731
        self.register_buffer("edge_label", f(space.edge_label))
        self.register_buffer("edge_state", f(space.edge_state))
        self.register_buffer("edge_child", f(space.edge_child))
        self.register_buffer("label_matrix", f(space.edge_label_matrix).float())
        self.register_buffer("state_matrix", f(space.edge_state_matrix).float())
        self.register_buffer("child_matrix", f(space.edge_child_matrix).float())
        self.levels = [(r.start, r.stop) for r in space.levels()]
        parent = [-1] + [(a - 1) // space.arity
                         for a in range(1, space.n_positions)]
        self.register_buffer("parent", torch.tensor(parent))
        top = torch.from_numpy(space.propagate(space.top()))
        self.register_buffer("top", top)

    @torch.no_grad()
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, P, _ = x.shape
        Q, A = self.state_matrix.shape[1], self.space.arity
        support = torch.zeros(B, P, len(self.edge_label), dtype=torch.bool,
                              device=x.device)
        alive = torch.zeros(B, P, Q, dtype=torch.bool, device=x.device)
        for d in reversed(range(len(self.levels))):
            lo, hi = self.levels[d]
            ok = x[:, lo:hi][:, :, self.edge_label]
            for j in range(A):
                if d == len(self.levels) - 1:
                    child_alive = torch.zeros(B, hi - lo, Q, dtype=torch.bool,
                                              device=x.device)
                    child_alive[:, :, 0] = True
                else:
                    c_lo = A * lo + 1 + j
                    child_alive = alive[:, c_lo:A * (hi - 1) + 2 + j:A]
                ok = ok & child_alive[:, :, self.edge_child[:, j]]
            support[:, lo:hi] = ok
            alive[:, lo:hi] = (ok.float() @ self.state_matrix) > 0
        reach = torch.zeros(B, P, Q, dtype=torch.bool, device=x.device)
        reach[:, 0, self.space.root_state] = True
        out = torch.zeros_like(x)
        for d in range(len(self.levels)):
            lo, hi = self.levels[d]
            active = (support[:, lo:hi]
                      & reach[:, lo:hi][:, :, self.edge_state]).float()
            out[:, lo:hi] = (active @ self.label_matrix) > 0
            if d + 1 < len(self.levels):
                for j in range(A):
                    c_lo = A * lo + 1 + j
                    reach[:, c_lo:A * (hi - 1) + 2 + j:A] =\
                        (active @ self.child_matrix[j]) > 0
        empty = ~out[:, 0].any(-1)
        out[empty] = False
        return out


def consistent(x: torch.Tensor, Y: torch.Tensor, valid: torch.Tensor):
    """Which solutions ``Y`` (batch, K, positions) of labels are in ``gamma(x)``."""
    alive = torch.gather(x, 2, Y.transpose(1, 2).clamp(min=0))  # (B, P, K)
    return alive.all(1) & valid


def alpha(x: torch.Tensor, Y: torch.Tensor, valid: torch.Tensor):
    """``x ⊓ alpha({y in Y | y in gamma(x)})`` and which rows have none."""
    keep = consistent(x, Y, valid)  # (B, K)
    B, P, V = x.shape
    index = Y.clamp(min=0).transpose(1, 2)  # (B, P, K)
    src = keep[:, None, :].expand(B, P, Y.shape[1])
    onehot = torch.zeros(B, P, Y.shape[1], V, dtype=torch.bool,
                         device=x.device)
    onehot.scatter_(3, index[..., None], src[..., None])
    target = onehot.any(2) & x
    return target, ~keep.any(1)


def is_total(x: torch.Tensor) -> torch.Tensor:
    """Every position has exactly one label."""
    return (x.sum(-1) == 1).all(-1)


def frontier(x: torch.Tensor, parent: torch.Tensor) -> torch.Tensor:
    """Undecided positions whose parent is decided: the Omegas of the partial
    Böhm tree that forcing an argument would refine."""
    count = x.sum(-1)
    decided = count == 1
    parent_decided = torch.ones_like(decided)
    parent_decided[:, 1:] = decided[:, parent[1:]]
    return (count > 1) & parent_decided


def pin(x: torch.Tensor, logits: torch.Tensor, parent: torch.Tensor,
        temperature: float, generator: torch.Generator | None = None,
        rows: torch.Tensor | None = None) -> torch.Tensor:
    """Pin one frontier position per row (where ``rows``) to a label drawn
    from ``softmax(logits / temperature)`` over its alive labels."""
    B, P, V = x.shape
    open_ = frontier(x, parent)
    if rows is not None:
        open_ &= rows[:, None]
    has = open_.any(1)
    weights = open_.float() + (~has)[:, None].float()
    position = torch.multinomial(weights, 1, generator=generator)[:, 0]
    batch = torch.arange(B, device=x.device)
    scores = logits[batch, position].float() / temperature
    scores = scores.masked_fill(~x[batch, position], float("-inf"))
    scores = torch.where(has[:, None], scores, torch.zeros_like(scores))
    label = torch.multinomial(scores.softmax(-1).nan_to_num(1.0 / V), 1,
                              generator=generator)[:, 0]
    out = x.clone()
    row = out[batch, position]
    row = torch.where(has[:, None],
                      torch.nn.functional.one_hot(label, V).bool() & row, row)
    out[batch, position] = row
    return out
