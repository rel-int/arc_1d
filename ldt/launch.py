"""
Launch jobs on the deployed app, so that they outlive the shell that started
them (a ``modal run`` client that dies takes its app down with it).

    modal deploy modal_app.py
    python launch.py generate --name d3 --dsl 2d --max-size 12 --exact 5
    python launch.py train --name r1 --data d1 --gpu H100 --steps 20000
    python launch.py evaluate --run r1 --bench 1darc --evaluate '{"free": 0.5}'

A training job writes its log on the volume, read back with
``modal run modal_app.py::fetch --path runs/<name>/log.jsonl``; an
evaluation writes ``runs/<run>/eval-<bench><tag>.json``, an enumeration
``enum/<name>.json`` (``enum/<bench>-<budget>.json`` without ``--name``)
and a generation only its shards, ``data/<name>/``.
"""

import argparse
import json

import modal

EVALUATE = '{"chains": 32, "rounds": 100, "slots": 32, "free": 0.5}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", default="ldt-arc")
    sub = parser.add_subparsers(dest="job", required=True)
    train = sub.add_parser("train")
    train.add_argument("--name", required=True)
    train.add_argument("--data", required=True)
    train.add_argument("--gpu", default="H100")
    train.add_argument("--model", default="{}")
    train.add_argument("--steps", type=int, default=20000)
    train.add_argument("--batch", type=int, default=256)
    train.add_argument("--extra", default='{"log_every": 200}')
    train.add_argument("--validation", type=int, default=512)
    train.add_argument("--evaluate", default=EVALUATE)
    train.add_argument("--dsl", default="1d")
    train.add_argument("--benches", default="1darc")
    train.add_argument("--unseal", default="")
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--run", required=True)
    evaluate.add_argument("--bench", default="1darc")
    evaluate.add_argument("--evaluate", default=EVALUATE)
    evaluate.add_argument("--unseal", default="")
    evaluate.add_argument("--prune", type=int, default=0)
    evaluate.add_argument("--uniform", type=int, default=0)
    evaluate.add_argument("--dsl", default="1d")
    evaluate.add_argument("--tag", default="")
    generate = sub.add_parser("generate")
    generate.add_argument("--name", required=True)
    generate.add_argument("--shards", type=int, default=250)
    generate.add_argument("--per-shard", type=int, default=400)
    generate.add_argument("--dsl", default="1d")
    generate.add_argument("--max-size", type=int, default=20)
    generate.add_argument("--exact", type=int, default=0)
    generate.add_argument("--mutants", type=float, default=0.5)
    enum = sub.add_parser("enumerate")
    enum.add_argument("--budget", type=int, default=20000)
    enum.add_argument("--bench", default="1darc")
    enum.add_argument("--dsl", default="1d")
    enum.add_argument("--unseal", default="")
    enum.add_argument("--name", default="")
    a = parser.parse_args()
    if a.job == "enumerate":
        call = modal.Function.from_name(a.app, "enumerate_all").spawn(
            a.budget, a.bench, a.dsl, a.unseal, 10, a.name)
    elif a.job == "generate":
        call = modal.Function.from_name(a.app, "generate_all").spawn(
            a.name, a.shards, a.per_shard, 0, a.dsl, a.max_size, a.exact,
            a.mutants)
    elif a.job == "train":
        fn = modal.Function.from_name(a.app, f"train_{a.gpu.lower()}")
        train_json = json.dumps({"steps": a.steps, "batch": a.batch}
                                | json.loads(a.extra))
        call = fn.spawn(a.name, a.data, a.model, train_json, a.validation,
                        a.evaluate, a.dsl, a.benches, a.unseal)
    else:
        fn = modal.Function.from_name(a.app, "evaluate_remote")
        call = fn.spawn(a.run, a.bench, a.evaluate, a.unseal, bool(a.prune),
                        bool(a.uniform), a.dsl, a.tag)
    print(call.object_id)


if __name__ == "__main__":
    main()
