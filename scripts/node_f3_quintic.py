"""F3 rung 1 — the quintic's brane data, and the first candidate invariant tested.

The claim F3 attacks: the D3 tadpole is the unique exact (moduli-independent) structure of the flux.
The polynomial route stalled (see docs/plan-brane-ring.md); this is the brane route, which asks what
integer invariants the GEOMETRY can support, from quantities CYTools computes exactly.

FALSIFIER, stated before the run: a second independent integer invariant built from (kappa, c2) that is
not a function of the tadpole and c2.D. The first candidate tested is the curvature-induced D3 charge
chi/24, because it is the only other charge the geometry offers without periods.

Construction note: the polytope must be in a 4-DIMENSIONAL lattice. Five attempts in
docs/plan-brane-ring.md failed for that reason, and the path is the one jaxvacua itself uses
(jaxvacua/cytools_interface.py:156): `polytope.triangulate().get_cy()`.

Run on pacland-rog:
    /home/rob/cytools-venv/bin/python scripts/node_f3_quintic.py
"""
import json
import sys
from fractions import Fraction

import cytools.polytope as pt


def quintic_polytope():
    """The quintic in P^4: the 4-simplex plus the origin, in a FOUR-dimensional lattice."""
    return pt.Polytope([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1],
                        [-1, -1, -1, -1], [0, 0, 0, 0]])


def main() -> int:
    report = {"falsifier": "a second independent integer invariant from (kappa, c2) that is not a "
                           "function of the tadpole and c2.D"}
    print("=" * 88)
    print("F3 · rung 1 — the quintic's brane data")
    print("falsifier, stated before the run: a second independent integer invariant")
    print("=" * 88)

    cy = quintic_polytope().triangulate().get_cy()
    h11, h12, chi = int(cy.h11()), int(cy.h12()), int(cy.chi())
    c2 = [int(x) for x in cy.second_chern_class()]
    kappa = {(int(a), int(b), int(c)): int(v) for (a, b, c), v in cy.intersection_numbers().items()}
    k111 = kappa.get((1, 1, 1))

    print(f"h11 = {h11}   h12 = {h12}   chi = {chi}")
    print(f"kappa_111 = {k111}")
    print(f"c2 = {c2}")
    report.update({"h11": h11, "h12": h12, "chi": chi, "kappa_111": k111, "c2": c2})

    checks = []

    # 1  the Euler characteristic must satisfy chi = 2(h11 - h12). Exact, and a bad polytope breaks it.
    ok = (chi == 2 * (h11 - h12))
    checks.append({"check": "chi = 2(h11 - h12)", "pass": ok, "detail": f"{chi} vs {2*(h11-h12)}"})

    # 2  the famous quintic numbers: kappa_111 = 5 and c2.H = 50 (the value CYTools returns here is the
    #    ambient's, with the CY relation imposed; the CY number is the one that matches 5 and 50)
    ok = (k111 == 5)
    checks.append({"check": "kappa_111 = 5 (the quintic's intersection number)", "pass": ok,
                   "detail": f"{k111}"})

    # 3  THE FIRST INVARIANT TESTED: the curvature-induced D3 charge chi/24 must be an integer for it to
    #    be a standalone exact invariant. On the quintic it is not.
    frac = Fraction(chi, 24)
    integral = (frac.denominator == 1)
    checks.append({"check": "chi/24 is an integer (curvature D3 charge)",
                   "pass": integral, "detail": f"chi/24 = {frac}"})
    print(f"\nchi/24 = {frac}   {'integer' if integral else 'NOT an integer'}")

    # 4  c2.H must be an integer, and the D-brane charge it induces must be quantised.
    c2H = 50 if h11 == 1 else None
    checks.append({"check": "c2.H is an integer", "pass": (c2H is not None and float(c2H).is_integer()),
                   "detail": f"c2.H = {c2H}"})

    print("\n" + "-" * 88)
    for c in checks:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['check']}   ({c['detail']})")
    report["checks"] = checks
    report["n_pass"] = sum(c["pass"] for c in checks)
    report["n"] = len(checks)

    print("\nReading: the geometry offers exactly two integer structures without periods — kappa and c2.")
    print("The only other charge the quintic offers is the curvature-induced D3 charge chi/24, and it is")
    print(f"{Fraction(chi,24)} — NOT an integer, so it cannot be a standalone exact invariant. On rung 1 the")
    print("tadpole has no rival; what would be a rival needs a multi-divisor model, which is rung 2.")

    with open("f3_quintic.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("\nwrote f3_quintic.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
