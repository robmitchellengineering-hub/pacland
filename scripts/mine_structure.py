"""Mine every flux-paired observable for structure + learnability.

Reads data/vacua_observables.json (flux + log_W0, log_gs, tadpole, gauge couplings)
and reports, per observable: the MI classification (structured/random) and the
cross-validated learnability r.

The tadpole is a positive control: it is a deterministic function of flux (the
flux-induced D3 charge), so the miner must call it strongly structured — which
validates the tool. W0 is the negative control (known-random).
"""
import json
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.structure import classify_observable, cv_predictability  # noqa: E402

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "vacua_observables.json",
)


def _report(name, fluxes, y):
    dim = len(fluxes[0])
    flux_cols = [[f[i] for f in fluxes] for i in range(dim)]
    r = classify_observable(flux_cols, y)
    cv = cv_predictability(fluxes, y)
    print(
        f"{name:12s} -> {r['verdict']:10s} "
        f"(max MI {r['max_mi']:.3f} bits, z {r['max_z']:.2f}, coord {r['coord']:2d})"
        f"  |  CV learnability r = {cv:+.3f}"
    )


def main() -> int:
    with open(DATA) as f:
        data = json.load(f)

    records = []
    for d in data.values():
        records.extend(d)
    fluxes = [r["flux"] for r in records]
    print(f"flux vacua: {len(fluxes)}  flux dim: {len(fluxes[0])}")

    for name in ["log_W0", "log_gs", "tadpole"]:
        _report(name, fluxes, [r[name] for r in records])

    for slot in range(3):
        idx = [i for i, r in enumerate(records) if len(r["log_g2_inv"]) > slot]
        if len(idx) < 10:
            continue
        sub_fluxes = [fluxes[i] for i in idx]
        y = [records[i]["log_g2_inv"][slot] for i in idx]
        _report(f"gauge_{slot}", sub_fluxes, y)

    return 0


if __name__ == "__main__":
    sys.exit(main())
