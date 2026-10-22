"""
The recurrent transformer that reads a lattice state and the demonstrations.

Tokens are the tree addresses, each the linear embedding of its alive labels
plus a learned address embedding, and one CLS token for the conflict logit. A
stack of ``layers`` blocks (self-attention, cross-attention to the encoded
demonstrations, padding cells included as ``PAD`` tokens so that attention
needs no mask, feed-forward) is unrolled ``loops`` times; the lattice encoding
is re-injected at every loop and every loop emits its own logits, as in the
paper. The demonstrations are encoded once per call: one token per cell of a
one-dimensional pair, carrying the input colour, the output colour (or a mask
for the test input), the cell's position and the pair's index.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.checkpoint import checkpoint

PAD, MASK = 10, 11  # colour codes beyond 0-9


@dataclass
class Config:
    dim: int = 128
    heads: int = 4
    layers: int = 4
    loops: int = 8
    demo_layers: int = 2
    max_length: int = 96
    max_pairs: int = 6
    dropout: float = 0.1
    checkpoint: bool = True


class Attention(nn.Module):
    """Multi-head attention through ``scaled_dot_product_attention``, so that
    no attention matrix is kept for the backward pass."""

    def __init__(self, c: Config):
        super().__init__()
        self.heads, self.dropout = c.heads, c.dropout
        self.q = nn.Linear(c.dim, c.dim)
        self.kv = nn.Linear(c.dim, 2 * c.dim)
        self.out = nn.Linear(c.dim, c.dim)

    def forward(self, h, memory):
        B, N, D = h.shape
        split = lambda t: t.view(B, -1, self.heads, D // self.heads)\
            .transpose(1, 2)  # noqa: E731
        q = split(self.q(h))
        k, v = (split(t) for t in self.kv(memory).chunk(2, -1))
        a = F.scaled_dot_product_attention(
            q, k, v, dropout_p=self.dropout if self.training else 0.0)
        return self.out(a.transpose(1, 2).reshape(B, N, D))


class Block(nn.Module):
    def __init__(self, c: Config):
        super().__init__()
        self.norm1, self.norm2, self.norm3 = (nn.LayerNorm(c.dim) for _ in "123")
        self.attn, self.cross = Attention(c), Attention(c)
        self.ff = nn.Sequential(nn.Linear(c.dim, 4 * c.dim), nn.GELU(),
                                nn.Dropout(c.dropout), nn.Linear(4 * c.dim, c.dim))

    def forward(self, h, memory):
        a = self.norm1(h)
        h = h + self.attn(a, a)
        h = h + self.cross(self.norm2(h), memory)
        return h + self.ff(self.norm3(h))


class LDT(nn.Module):
    def __init__(self, n_positions: int, n_labels: int, config: Config):
        super().__init__()
        c = self.config = config
        self.colour_in = nn.Embedding(12, c.dim)
        self.colour_out = nn.Embedding(12, c.dim)
        self.cell = nn.Embedding(c.max_length, c.dim)
        self.pair = nn.Embedding(c.max_pairs, c.dim)
        self.demo = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(c.dim, c.heads, 4 * c.dim, c.dropout,
                                       batch_first=True, norm_first=True),
            c.demo_layers, enable_nested_tensor=False)
        self.lattice = nn.Linear(n_labels, c.dim)
        self.address = nn.Parameter(torch.randn(n_positions + 1, c.dim) * 0.02)
        self.blocks = nn.ModuleList(Block(c) for _ in range(c.layers))
        self.norm = nn.LayerNorm(c.dim)
        self.candidate = nn.Linear(c.dim, n_labels)
        self.conflict = nn.Linear(c.dim, 1)

    def encode_demos(self, inputs, outputs):
        """``inputs``, ``outputs``: (batch, pairs, length) colour codes, PAD
        beyond a grid's length, MASK for the unknown test output."""
        B, M, L = inputs.shape
        h = (self.colour_in(inputs) + self.colour_out(outputs)
             + self.cell.weight[:L] + self.pair.weight[:M, None])
        pad = inputs == PAD
        h = self.demo(h.reshape(B, M * L, -1),
                      src_key_padding_mask=pad.reshape(B, M * L))
        return h, pad.reshape(B, M * L)

    def forward(self, x, memory, memory_pad, loops: int | None = None):
        """Candidate logits (loops, batch, positions, labels) and conflict
        logits (loops, batch) of a batch of states ``x``."""
        B = x.shape[0]
        inject = torch.cat([
            self.lattice(x.to(self.address.dtype)),
            self.lattice.weight.new_zeros(B, 1, self.config.dim)], 1)
        inject = inject + self.address
        h = torch.zeros_like(inject)
        candidates, conflicts = [], []
        for _ in range(loops or self.config.loops):
            h = h + inject
            if self.training and self.config.checkpoint:
                h = checkpoint(self._blocks, h, memory, use_reentrant=False)
            else:
                h = self._blocks(h, memory)
            out = self.norm(h)
            candidates.append(self.candidate(out[:, :-1]))
            conflicts.append(self.conflict(out[:, -1])[:, 0])
        return torch.stack(candidates), torch.stack(conflicts)

    def _blocks(self, h, memory):
        for block in self.blocks:
            h = block(h, memory)
        return h
