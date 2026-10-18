"""Measure which constraints eliminate the most vacua (Q2).

Applies physically-meaningful constraints to the real flux-vacua sample and
reports each elimination fraction with a confidence interval. This is the
"eliminate by verified constraint" step of docs/new-approach.md: a constraint
that eliminates a large, certified fraction is a real narrowing of the landscape.
"""
import json
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.constraints import elimination_certificate  # noqa: E402

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "vacua_sample.json",
)


def main() -> int:
    with open(DATA) as f:
        data = json.load(f)

    vacua = []
    for d in data.values():
        for w, g in zip(d["log_W0"], d["log_gs"]):
            vacua.append({"log_W0": w, "log_gs": g})

    constraints = {
        "weak coupling (gs < 1)": lambda v: v["log_gs"] < 0.0,
        "small W0 (|W0| < 1)": lambda v: v["log_W0"] < 0.0,
        "both (gs<1 AND |W0|<1)": lambda v: v["log_gs"] < 0.0 and v["log_W0"] < 0.0,
    }

    print(f"vacua: {len(vacua)}")
    for name, keep in constraints.items():
        c = elimination_certificate(vacua, keep)
        print(
            f"{name:26s} eliminates {c['eliminated'] * 100:5.1f}%  "
            f"[{c['lower'] * 100:.1f}%, {c['upper'] * 100:.1f}%]"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
