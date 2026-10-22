import importlib.util

collect_ignore = []
if importlib.util.find_spec("discopy") is None:
    collect_ignore.append("ldt/discopy_bridge.py")
for module in ("torch", "modal"):
    if importlib.util.find_spec(module) is None:
        collect_ignore += {"torch": ["ldt/lattice.py", "ldt/model.py",
                                     "ldt/train.py", "ldt/solve.py",
                                     "ldt/data.py", "ldt/enumerate.py"],
                           "modal": ["modal_app.py"]}[module]
collect_ignore.append("modal_app.py")
