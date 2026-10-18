"""Validate the flux guards on real JAXVacua-sampled flux vacua (local, no jax).

Reads ``data/vacua_sample.json`` (163 SUSY flux vacua, two h12=2 models, sampled
by JAXVacua) and runs the flux guards from ``pacland.guards`` on the real flux
vectors:

- ``guard_integer_flux``   must pass on all 163 (real flux quanta are integers);
- ``guard_no_sl2z_redundancy`` reports whether the sample holds SL(2,Z)-redundant
  (exact- or sign-flip-duplicate) vectors — a real finding about the sampler;
- the D3 tadpole sum(f^2) is reported as a range (the bound itself comes from the
  CY geometry via JAXVacua's ``tadpole`` attribute).

Exits 0 iff integer_flux passes on every vector. Prints one JSON summary.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.guards import guard_integer_flux, guard_no_sl2z_redundancy


def main() -> int:
    data_path = Path(__file__).resolve().parents[1] / "data" / "vacua_sample.json"
    d = json.loads(data_path.read_text())

    fluxes = []
    for model in d.values():
        fluxes.extend(model["flux"])

    n = len(fluxes)
    int_failures = [f for f in fluxes if not guard_integer_flux(f)[0]]
    tadpoles = [sum(x * x for x in f) for f in fluxes]
    redundant_ok, redundant_msg = guard_no_sl2z_redundancy(fluxes)

    result = {
        "guard": "flux_invariants",
        "n_flux_vacua": n,
        "integer_flux_passed": len(int_failures) == 0,
        "integer_flux_failures": len(int_failures),
        "tadpole_min": min(tadpoles),
        "tadpole_max": max(tadpoles),
        "sl2z_redundant": not redundant_ok,
        "sl2z_message": redundant_msg,
    }
    print(json.dumps(result, indent=2))
    return 0 if not int_failures else 1


if __name__ == "__main__":
    sys.exit(main())
