"""Verification Vault guards — approach #1.

Each guard asserts one physical invariant a string-theory computation must
satisfy, following the Valiant Verification discipline:

  - a violation fails LOUDLY (a silent pass is a fail),
  - each guard has a seeded-fault mutation test in ``tests/test_guards.py``
    proving it goes red on the fault it exists to catch.

The real oracle outputs plug into these guards: CYTools Hodge numbers
(``oracle/adapters.py::CyToolsAdapter``), JAXVacua flux vacua
(``JaxVacuaAdapter``), cymetric metrics (``CymetricAdapter``). Until those run,
the guards are exercised on exact/toy data — same contract, no physics tools.
"""
from __future__ import annotations


def guard_hodge_numbers(h11: int, h21: int, expected: tuple[int, int] = (1, 101)) -> tuple[bool, str]:
    """Known-answer guard: the quintic threefold has h11=1, h21=101.

    Fails if the CY topology computation does not reproduce the known answer —
    the class of bug where a solver returns plausible-but-wrong numbers.
    """
    ok = (h11, h21) == expected
    return ok, f"h11={h11} h21={h21} (expected {expected})"


def guard_tadpole(flux, bound: int) -> tuple[bool, str]:
    """Invariant guard: the D3 tadpole sum(f^2) must not exceed the bound.

    Fails on a vacuum whose flux exceeds the tadpole bound — a physically
    inconsistent state that must never enter the certificate loop.
    """
    s = sum(f * f for f in flux)
    return s <= bound, f"tadpole={s} (bound {bound})"


def guard_integer_flux(flux) -> tuple[bool, str]:
    """Discrete-data guard: flux quanta are integers, never floats.

    ``docs/encoding.md`` §5: no floating-point encoding of discrete data. A
    float in a flux vector is the class of bug that silently corrupts counts
    and inflates the class size.
    """
    bad = [f for f in flux if not isinstance(f, int)]
    return not bad, f"non-integer flux entries: {bad}"


def _canon(f: tuple) -> tuple:
    """Canonical form of a flux vector under the -1 element of SL(2,Z)."""
    neg = tuple(-x for x in f)
    return min(f, neg)


def guard_no_sl2z_redundancy(fluxes) -> tuple[bool, str]:
    """No-double-counting guard (toy): no duplicate or sign-flip-duplicate flux
    vectors — SL(2,Z)-equivalent vacua must be quotiented, not double-counted.

    ``docs/evolvability.md`` §8.3: un-quotiented redundancy inflates the
    effective class size and wrecks the SQ/VC-dimension estimate. This is the
    smallest honest version of that guard (exact dup + the -1 element).
    """
    seen = set()
    for f in fluxes:
        key = _canon(tuple(f))
        if key in seen:
            return False, f"SL(2,Z)-redundant flux {f}"
        seen.add(key)
    return True, "no redundant flux vectors"


def guard_ricci_flat(sigma: float, tol: float = 1e-2) -> tuple[bool, str]:
    """Accuracy guard: the CY metric's Ricci-flatness residual must be small.

    cymetric reports sigma ~ 1e-3..1e-4 vs Fubini-Study ~0.4. Fails on a metric
    that is not actually Ricci-flat — the dominant systematic error of L2 stage 1.
    """
    return sigma <= tol, f"sigma={sigma} (tol {tol})"


__all__ = [
    "guard_hodge_numbers",
    "guard_tadpole",
    "guard_integer_flux",
    "guard_no_sl2z_redundancy",
    "guard_ricci_flat",
]
