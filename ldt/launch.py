"""
Launch jobs on the deployed app, so that they outlive the shell that started
them (a ``modal run`` client that dies takes its app down with it).

    modal deploy modal_app.py
    python launch.py train --name r1 --data d1 --gpu H100 --steps 20000
    python launch.py evaluate --run r1 --bench 1darc --evaluate '{"free": 0.5}'

Each job writes its log on the volume, read back with
``modal run modal_app.py::fetch --path runs/<name>/log.jsonl``.
"""

import argparse
import json

import modal

EVALUATE = '{"chains": 32, "rounds": 100, "slots": 32, "free": 0.5}'


def main():
    parser = argparse.ArgumentParser()
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
    a = parser.parse_args()
    if a.job == "train":
        fn = modal.Function.from_name("ldt-arc", f"train_{a.gpu.lower()}")
        train_json = json.dumps({"steps": a.steps, "batch": a.batch}
                                | json.loads(a.extra))
        call = fn.spawn(a.name, a.data, a.model, train_json, a.validation,
                        a.evaluate, a.dsl, a.benches, a.unseal)
    else:
        fn = modal.Function.from_name("ldt-arc", "evaluate_remote")
        call = fn.spawn(a.run, a.bench, a.evaluate, a.unseal, bool(a.prune),
                        bool(a.uniform), a.dsl, a.tag)
    print(call.object_id)


if __name__ == "__main__":
    main()
