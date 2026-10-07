> Goal: a first, minimal experiment for a diagrammatic DreamCoder on 1D-ARC. We want to know whether a wake/abstract loop over string diagrams, with no LLM anywhere, can solve 1D-ARC tasks and grow a useful library. Keep the scope small. This is a feasibility run.
>
> Before writing code:
> - Read the repo and tell me what DisCoPy version and which modules (monoidal, closed, rewriting) are available. You can base your work on open PRs for discopy.neural so you don't need to reimplement the category of neural networks
> - Check out the arc_1d repo for the 1D-ARC dataset (Xu et al. 2023, on GitHub). Report its task families and how many tasks each has.
> - Write a plan for an initial experiment as a PR description on that repo.
>
> Design constraints:
>
> 1. Types and library.
>    - A 1D grid is a sequence of colour cells.
>    - Define a small base library of typed constants (boxes) in DisCoPy, each parameterised by a small neural net (a tiny MLP or 1D conv).
>    - Keep it to roughly 5–10 boxes with clear types: per-cell maps, shifts, reflection, object segmentation, fill. Also include copy/discard and composition structure.
>    - Write the boxes so that a later library entry can carry its trained weights.
>
> 2. Semantics.
>    - Implement evaluation as a functor from the free monoidal category on the library into PyTorch modules.
>    - Start trace-free, since most 1D-ARC tasks need no recursion.
>    - Put the functor behind a clean interface, so we can swap in neural GoI (Int(NN), with trace as a fixpoint) later without touching the search code.
>
> 3. Wake (search).
>    - Enumerate small diagrams up to a size bound, type-correct by construction, under a simple prior over diagram size and box frequency.
>    - For each candidate, fit the box weights on the task's training pairs with a short inner loop.
>    - Score each candidate by description length = structure cost + parameter cost + training loss.
>    - Parameter cost must be charged. Otherwise the nets absorb everything and any structure fits.
>    - Keep the top few candidates per task.
>
> 4. Abstract.
>    - Skip e-graphs for now.
>    - Mine frequent subdiagrams across the best solutions.
>    - Add the top few as new library boxes, initialising their weights from the trained solutions.
>
> 5. Loop.
>    - Run 3–5 wake/abstract iterations.
>    - Hold out each task's test pair and only ever fit on its training pairs.
>
> Report, per iteration:
> - Exact-match accuracy on test pairs, overall and per task family.
> - Library size, and the new boxes with their types.
> - Mean description length of solutions.
> - Wall-clock time.
>
> Also show 3 solved and 3 failed tasks with their diagrams drawn.
>
> Engineering:
> - Make it run on a single GPU or CPU in under about an hour at default settings, with a --quick flag for a few-minute smoke test.
> - Fix seeds, log configs, and write results to a markdown file.
> - Write tests for type-checking and for the functor on a hand-built diagram.
>
> Flag anywhere you had to make a design choice I didn't specify, rather than deciding silently.

- [x] report DisCoPy version and modules, base on discopy.neural (#743)
- [x] report 1D-ARC families and task counts
- [x] plan as the PR description
- [x] types and base library (`dc/library.py`)
- [x] trace-free functor behind `Semantics` (`dc/semantics.py`)
- [x] wake: typed enumeration, inner fit, DL with parameter cost (`dc/wake.py`)
- [x] abstract: mine subdiagrams, inherit weights (`dc/abstract.py`)
- [x] loop, report, `--quick` (`dc/run.py`)
- [x] tests: type-checking, functor on hand-built diagrams
- [ ] default run, results committed and summarised on the PR
