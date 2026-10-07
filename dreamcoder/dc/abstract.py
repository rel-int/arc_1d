"""
Abstract: grow the library from the best solutions.

No e-graphs and no refactoring: a fragment is a subterm with at least two
boxes of the best solution of a task that the solution fits exactly on its
training pairs. Every such subterm is a closed function of ``x``, i.e. a
subdiagram ``Grid -> T``, so it becomes a box ``Grid -> T`` as it is. A
fragment is scored by the boxes it saves, ``(support - 1) * (size - 1)``,
where its support is the number of tasks using it, and the best few with
support at least two join the library.

The new box carries trained weights: those of the occurrence closest to all
the others in L1, i.e. the medoid of its occurrences, so that a task needing
what most of them learned starts there and pays nothing for it.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import torch

from dc.library import Entry, Library
from dc.terms import Term
from dc.wake import Solution


@dataclass
class Fragment:
    term: Term
    occurrences: list[dict]  # the weights of the fragment in each task using it
    tasks: list[str]

    @property
    def saving(self) -> int:
        return (len(self.tasks) - 1) * (self.term.size - 1)


def rename(weights: dict, path: str) -> dict:
    """The weights of the subterm at ``path``, renamed as if it were the root ``r``."""
    return {"r" + name[len(path):]: w for name, w in weights.items()
            if name.startswith(path + ".") or name.startswith(path + "_")}


def fragments(best: dict[str, Solution]) -> list[Fragment]:
    found: dict[Term, Fragment] = {}
    for task, solution in sorted(best.items()):
        if not solution.train_exact:
            continue
        seen = set()
        for path, sub in solution.term.subterms():
            if sub.size < 2 or sub in seen:
                continue
            seen.add(sub)
            fragment = found.setdefault(sub, Fragment(sub, [], []))
            fragment.occurrences.append(rename(solution.weights, path))
            fragment.tasks.append(task)
    return sorted(found.values(), key=lambda f: (-f.saving, str(f.term)))


def medoid(occurrences: list[dict]) -> dict:
    flat = [torch.cat([w[k].flatten() for k in sorted(w)]) if w else torch.zeros(0)
            for w in occurrences]
    cost = [sum(float((a - b).abs().sum()) for b in flat) for a in flat]
    return occurrences[min(range(len(flat)), key=cost.__getitem__)]


def uses(term: Term) -> list[str]:
    return [sub.head for _, sub in term.subterms() if sub.head != "x"]


def abstract(library: Library, best: dict[str, Solution], new_boxes: int,
             iteration: int) -> list[Entry]:
    """
    Add the ``new_boxes`` fragments saving the most boxes, then re-estimate
    the weight of every entry as one plus its uses in the best solutions
    that fit their training pairs, a new entry counting its support.
    """
    bodies = {e.body for e in library.entries.values() if not e.is_primitive}
    added = []
    for fragment in fragments(best):
        if len(added) == new_boxes:
            break
        if len(fragment.tasks) < 2 or fragment.term in bodies:
            continue
        cod = library[fragment.term.head].cod
        name = f"f{iteration}{'abcdefghij'[len(added)]}"
        entry = Entry(name, ("Grid",), cod, body=fragment.term,
                      weights=medoid(fragment.occurrences), iteration=iteration)
        library.entries[name] = entry
        library.weights[name] = 1. + len(fragment.tasks)
        added.append(entry)
    counts = defaultdict(int)
    for solution in best.values():
        if solution.train_exact:
            for head in uses(solution.term):
                counts[head] += 1
    for name in library.entries:
        if name not in {e.name for e in added}:
            library.weights[name] = 1. + counts[name]
    return added
