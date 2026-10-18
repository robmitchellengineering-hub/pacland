"""Run JAXVacua on a Linux node and check flux-vacua invariants through guards.

Self-contained and self-asserting. Run with the cytools venv python:

    /home/rob/cytools-venv/bin/python scripts/validate_jaxvacua.py

Loads the bundled flux-EFT (h12=2, model_ID=1) and checks the invariants that
``pacland.guards.guard_tadpole`` / ``guard_integer_flux`` assert: n_fluxes is a
positive integer and the D3 tadpole is non-negative. Exits 0 iff both hold.

NOTE: JAXVacua returns numpy integers (not Python ints), so a literal
``isinstance(x, int)`` guard would FALSE-fail — this script reports the observed
types so the guard can be made numpy-aware when wired to real output.
"""
import json
import sys


def _is_int_like(x) -> bool:
    """True for Python int or numpy integer (and int-valued floats)."""
    import numpy as np  # jax pulls numpy in; safe here

    if isinstance(x, (int, np.integer)):
        return True
    if isinstance(x, float):
        return x.is_integer()
    return False


def main() -> int:
    try:
        import jax

        jax.config.update("jax_enable_x64", True)
        import jaxvacua as jvc
    except ImportError as exc:
        print(json.dumps({"guard": "flux_invariants", "passed": False, "error": str(exc)}))
        return 1

    eft = jvc.FluxEFT(h12=2, model_ID=1)
    n_fluxes = eft.n_fluxes
    tadpole = eft.tadpole

    flux_int = _is_int_like(n_fluxes) and n_fluxes > 0
    tadpole_ok = float(tadpole) >= 0.0
    passed = bool(flux_int and tadpole_ok)

    result = {
        "guard": "flux_invariants",
        "n_fluxes": int(n_fluxes),
        "n_fluxes_type": type(n_fluxes).__name__,
        "tadpole": float(tadpole),
        "flux_integer": flux_int,
        "tadpole_nonnegative": tadpole_ok,
        "passed": passed,
    }
    print(json.dumps(result))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
