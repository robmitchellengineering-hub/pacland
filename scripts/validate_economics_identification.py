#!/usr/bin/env python3
"""Economics set-identification — the theoretical axis (axis 2), validated exactly.

Proves, with Fraction arithmetic (zero floating point):

  G1  Gorman non-identification — two different endowment distributions with the same
      total produce the same aggregate excess demand (the distribution drops out).
  G2  the total IS identified — a different total produces a different aggregate.
  G3  a point claim about the distribution is over-claiming — the guard fails it.
  G4  a point claim about the total is justified — the guard passes it.
  G5  the sectoral identity identifies the private BALANCE (S−I) but not S vs I.
"""
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics.identification import (  # noqa: E402
    aggregate_from_distribution,
    cobb_douglas_aggregate_excess_demand,
    constraint_set_model,
    guard_point_identified,
    sectoral_balance_set,
)


def main():
    checks = []

    # G1 — two distributions, same total -> same aggregate (non-identification).
    d1 = [(F(1), F(0)), (F(0), F(1))]
    d2 = [(F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))]
    checks.append(("G1 Gorman: two distributions, one aggregate",
                   aggregate_from_distribution(d1, F(2)) == aggregate_from_distribution(d2, F(2))))

    # G2 — the total IS identified (different total -> different aggregate).
    z_total = cobb_douglas_aggregate_excess_demand((F(1), F(1)), F(2))
    z_other = cobb_douglas_aggregate_excess_demand((F(2), F(1)), F(2))
    checks.append(("G2 total identified (different total, different z)",
                   z_total != z_other))

    # G3 — a point claim about the distribution is over-claiming -> guard fails.
    ok, _ = guard_point_identified({"distribution": d1}, [{"distribution": d2}])
    checks.append(("G3 guard fails a distribution point-claim", not ok))

    # G4 — a point claim about the total is justified -> guard passes.
    ok, _ = guard_point_identified({"total": (F(1), F(1))}, [])
    checks.append(("G4 guard passes a total point-claim", ok))

    # G5 — sectoral identity: private balance identified, S vs I not.
    private, _ = sectoral_balance_set(F("-1774.684"), F("-246.023"))
    checks.append(("G5 private balance identified (S−I = +2020.707)", private == F("2020.707")))

    all_ok = True
    for name, ok in checks:
        all_ok &= ok
        print(f"{name:56s} {'PASS' if ok else 'FAIL'}")

    print()
    print("=" * 68)
    print(f"Economics set-identification: {sum(1 for _, ok in checks if ok)}/{len(checks)} pass.")
    model = constraint_set_model(F("-1774.684"), F("-246.023"))
    print("The better model emits:", model["identified"], "and refuses point forecasts.")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
