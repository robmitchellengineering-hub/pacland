"""Pin the verification-deficit arithmetic (guards the headline numbers).

The certificate radius is ``sqrt(ln(1/delta_e) / (2m))``. The repo once quoted
"~19 measured points -> ~43% radius", which is wrong: 43% is the *m = 10* case
(the ten-observable toy set); *m = 19* (the SM free-parameter count) gives ~31%.
This script recomputes the numbers from the certificate module and asserts them,
so the conflation cannot recur silently — the guard-for-the-docs pattern.

Run:  python3 scripts/verify_deficit_numbers.py
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from pacland.certificate import finite_d_certificate, hoeffding_radius

DELTA_E = 0.025

CASES = {
    10: 0.4295,  # ten-observable toy set
    19: 0.3116,  # ~19 SM free parameters
    25: 0.2716,  # upper end of the ~19-25 range
}

fails: list[str] = []

print("one-sided Hoeffding radius  sqrt(ln(1/delta_e)/(2m))  at delta_e = 0.025")
for m, expected in CASES.items():
    r = hoeffding_radius(m, DELTA_E)
    print(f"  m={m:2d}  radius={r:.4f}  ({r*100:.1f}%)  expected ~{expected*100:.1f}%")
    if not math.isclose(r, expected, abs_tol=5e-4):
        fails.append(f"m={m}: got {r:.4f}, expected {expected:.4f}")

m_for_1pct = math.log(1.0 / DELTA_E) / (2.0 * 0.01 ** 2)
print(f"  m needed for a 1% radius: {m_for_1pct:.0f}  (expect ~18,444)")
if not math.isclose(m_for_1pct, 18444, abs_tol=10):
    fails.append(f"m-for-1%: got {m_for_1pct:.0f}, expected ~18444")

# cross-check the finite-D certificate emits the same oracle-validation radius
cert = finite_d_certificate(p_g_exact=0.0, p_hat_e=0.0, m=19, delta_e=DELTA_E)
print(f"  finite_d_certificate(m=19): radius_e={cert.radius_e:.4f}, bound={cert.bound:.4f}, confidence={cert.confidence:.3f}")

if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)

print("OK: deficit arithmetic pinned (m=19 -> 31%, m=10 -> 43%, 1% needs ~18.4k).")
