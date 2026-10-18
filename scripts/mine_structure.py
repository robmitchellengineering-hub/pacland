"""Mine the real flux-vacua data for structured (geometry-informative) observables.

Runs the non-linear structure miner (``src/pacland/structure.py``) over every
flux coordinate and the observables we have paired with flux: log|W0| and log(gs).
The fork: if any observable is ``structured``, that's a positive result (a fingerprint
that pins the geometry); if all are ``random``, that strengthens the negative result
(the map is information-theoretically empty in these coordinates).
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
    "data", "vacua_sample.json",
)


def main() -> int:
    with open(DATA) as f:
        data = json.load(f)

    fluxes, logW, loggs = [], [], []
    for d in data.values():
        fluxes.extend(d["flux"])
        logW.extend(d["log_W0"])
        loggs.extend(d["log_gs"])

    dim = len(fluxes[0])
    flux_cols = [[f[i] for f in fluxes] for i in range(dim)]

    print(f"flux vacua: {len(fluxes)}  flux dim: {dim}")
    for name, y in [("log_W0", logW), ("log_gs", loggs)]:
        r = classify_observable(flux_cols, y)
        cv = cv_predictability(fluxes, y)
        print(
            f"{name:8s} -> {r['verdict']:10s} "
            f"(max MI {r['max_mi']:.3f} bits, z {r['max_z']:.2f}, coord {r['coord']})"
            f"  |  CV learnability r = {cv:+.3f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
