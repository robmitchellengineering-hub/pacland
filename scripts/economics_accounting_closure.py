#!/usr/bin/env python3
"""Economics accounting closure on REAL US national-accounts data (recipe step 6).

The economics Rule of Three is three ledgers a model/data must close. Here they are run
on actual FRED series (downloaded 2026-10-22), so the "leak" is a *measured* number, not
a toy input — the economics analog of climate's CMIP6 conservation drift.

    Ledger 1  circular flow     income (GDI) ≡ expenditure (GDP) → the statistical
                                discrepancy is the measured gap.
    Ledger 2  sectoral balances (S−I)+(T−G)+(M−X) = 0 → closes BY CONSTRUCTION
                                (double-entry), the control that stays exact.
    Ledger 3  stock-flow        Δ(debt) = deficit → the stock-flow adjustment is the
                                measured gap.

Result (real, 2026):
    circular flow   GDI − GDP = +$189.5B  = 0.58% of GDP          (leaks)
    sectoral bal.   private + gov + foreign = $0                 (closes, by definition)
    stock-flow      Δdebt − (−deficit) = +$236.9B = 13.3% of deficit  (leaks)

So the two *measured* ledgers leak (0.6% and 13%), and only the *definitional* one closes
— exactly as climate found the atmosphere-coupled ledgers leak while the purely-ocean
ledger (salt) closes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics.guards import (  # noqa: E402
    guard_circular_flow,
    guard_sectoral_balances,
    guard_stock_flow,
)

# FRED series, billions of dollars unless noted. Source: fred.stlouisfed.org, 2026-10-22.
GDP_2026Q2 = 32563.030          # GDP (expenditure measure), 2026-04-01
GDI_2026Q2 = 32752.528          # Gross domestic income (income measure), 2026-04-01
DEFICIT_FY2025 = -1774.684      # FYFSD federal surplus/deficit, FY ending 2025-09-30
DEBT_2024_09_30 = 28859.125     # FYGFDPUN debt held by the public, 2024-09-30
DEBT_2025_09_30 = 30870.713     # FYGFDPUN debt held by the public, 2025-09-30
CURRENT_ACCOUNT_2026Q2 = -246.023  # IEABC current-account balance, 2026-04-01 (quarterly)


def main():
    # Ledger 1 — circular flow.
    resid_flow = GDI_2026Q2 - GDP_2026Q2
    ok1, msg1 = guard_circular_flow(GDI_2026Q2, GDP_2026Q2, GDP_2026Q2, tol=0.0)

    # Ledger 2 — sectoral balances (identity: private + government + foreign = 0).
    gov = DEFICIT_FY2025
    foreign = CURRENT_ACCOUNT_2026Q2
    private = -(gov) - foreign          # private balance is the residual by definition
    ok2, msg2 = guard_sectoral_balances(private, gov, foreign, tol=1e-6)

    # Ledger 3 — stock-flow.
    d_debt = DEBT_2025_09_30 - DEBT_2024_09_30
    flow = -DEFICIT_FY2025              # a deficit is a positive debt-accumulating flow
    ok3, msg3 = guard_stock_flow(d_debt, flow, tol=0.0)

    print("ECONOMICS ACCOUNTING CLOSURE — real US national accounts (FRED, 2026-10-22)")
    print("=" * 72)
    print(f"Ledger 1  circular flow   GDI − GDP = {resid_flow:+.3f} B "
          f"({resid_flow / GDP_2026Q2 * 100:.2f}% of GDP)   "
          f"{'CLOSES' if ok1 else 'LEAKS'}")
    print(f"          {msg1}")
    print(f"Ledger 2  sectoral balances  (S−I){private:+.3f} + (T−G){gov:+.3f} + "
          f"(M−X){foreign:+.3f} = 0   {'CLOSES' if ok2 else 'LEAKS'}")
    print(f"          {msg2}")
    resid_sf = d_debt - flow
    print(f"Ledger 3  stock-flow     Δdebt {d_debt:+.3f} − deficit {flow:+.3f} = "
          f"{resid_sf:+.3f} B ({resid_sf / flow * 100:.1f}% of deficit)   "
          f"{'CLOSES' if ok3 else 'LEAKS'}")
    print(f"          {msg3}")
    print()
    print("The two measured ledgers leak (0.6%, 13%); the definitional one (sectoral")
    print("balances) closes — the economics analog of climate's energy/mass leak vs salt")
    print("closing (the leak is in the measurement/coupling, not the identity).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
