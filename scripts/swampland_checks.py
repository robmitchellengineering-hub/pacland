"""Run the swampland-connection report against the data we already hold.

Prints, per conjecture: what is computed, the Rule-of-Three verdict against flux,
and the TESTABLE-NOW / NEEDS-BIGGER-MACHINE classification. Pure stdlib + pacland.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pacland.swampland import swampland_report  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(path):
    with open(os.path.join(ROOT, path)) as fh:
        return json.load(fh)


def main():
    vacua_obs = load("data/vacua_observables.json")
    # concatenate both h12=2 models into one sample
    vacua = []
    for mk, entries in vacua_obs.items():
        for p in entries:
            if "flux" in p and "log_g2_inv" in p and p["log_g2_inv"]:
                vacua.append(p)

    rich = load("data/rich_sample.json")["points"]

    rep = swampland_report(vacua, rich)

    print(f"Swampland-connection report  (n_vacua = {rep['n_vacua']})\n")
    for name, body in rep["conjectures"].items():
        print(f"[{name}]  {body['status']}")
        for k, v in body.items():
            if k == "status":
                continue
            print(f"    {k}: {v}")
        print()


if __name__ == "__main__":
    main()
