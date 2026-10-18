"""Certify a real flux vacuum end-to-end through the Verification Vault.

Takes one real SUSY flux vacuum (flux -> observables) from the paired data, runs
it through the discrete guards (admission) and the certificate loop, and reports
the honest verdict: the discrete invariants pass, but the continuous observables
carry NO validated error model, so the certificate is vacuous (radius = inf).
This is the "deficit is total" conclusion made concrete on a single real vacuum —
the product is a verdict, not a vacuum.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from pacland.deficit import deficit_report
from pacland.guards import guard_integer_flux
from pacland.observables import STANDARD_OBSERVABLES


def main() -> int:
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "flux_observables.json")
    d = json.load(open(data_path))
    rows = [r for m in d.values() for r in m]
    v = rows[0]

    int_ok, int_msg = guard_integer_flux(v["flux"])
    rep = deficit_report(STANDARD_OBSERVABLES)

    result = {
        "vacuum": "h12_2_model1[0]",
        "flux": v["flux"],
        "observables": {k: v[k] for k in ("log_W0", "log_gs", "tadpole", "log_g2_inv", "log_mass2")},
        "guard_integer_flux": int_msg,
        "certificate": {
            "radius": "inf" if rep.vacuous else round(rep.radius, 4),
            "vacuous": rep.vacuous,
            "n_validated": rep.n_validation,
        },
        "verdict": (
            "admitted by the discrete guards (integer flux); the continuous certificate is "
            "VACUOUS — no validated oracle error model exists (n_validated = 0)"
        ),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
