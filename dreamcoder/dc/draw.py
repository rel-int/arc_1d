"""
Draw the best solutions of a finished run from its ``history.json``.

    uv run python -m dc.draw results/default 1d_hollow_23 1d_pcopy_mc_12
"""

import json
import sys
from pathlib import Path

from dc.library import Entry, Library
from dc.terms import Term, to_diagram


def library_of(history: list[dict]) -> Library:
    """The library a run ended with, without the weights: enough to draw with."""
    library = Library.base()
    for record in history:
        for signature, body, _ in record["new_boxes"]:
            name, cod = signature.split(" : ")[0], signature.split(" -> ")[1]
            library.entries[name] = Entry(name, ("Grid",), cod, body=Term.parse(body))
            library.weights[name] = 1.
    return library


def main(out: Path, *names: str):
    history = json.loads((out / "history.json").read_text())
    library = library_of(history)
    for name in names:
        term = Term.parse(history[-1]["solutions"][name][0])
        path = out / "figures" / f"{name}.png"
        to_diagram(term, library).draw(path=str(path), figsize=(5, 4))
        print(f"{name}: {term} -> {path}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), *sys.argv[2:])
