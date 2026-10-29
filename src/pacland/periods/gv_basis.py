"""The GV basis convention — why "integrality" alone is not the check (B1, fixed).

#209 found that the extracted invariants came out integral on the **non-primitive** degrees only. That
symptom is a convention error, not a numerical one, and this module states the convention and the test.

The instanton part of the prepotential is

    F_inst(q) = (1/(2 pi i)^3) sum_{d>=1} n_d Li_3(q^d),     q = e^{2 pi i t}

so the coefficient of `q^m` in `F_inst` is **not** `n_m`. Expanding `Li_3(q^d) = sum_k q^(dk)/k^3` gives the
multi-cover relation

    c_m = (1/m^3) sum_{d | m} d^3 n_d

and the inversion is triangular:

    n_m = m^3 c_m - sum_{d | m, d < m} d^3 n_d

**Two consequences, and the second is the one that matters.**

1. The invariants must be extracted by the *inverse* relation, not read off as `m^3 c_m`.
2. A naive read-off still returns **integers** on composite degrees — it just returns the wrong ones
   (on the quintic, `m = 2` gives 4876875 where the truth is 609250). So **integrality is not a
   sufficient check**: it must be integrality of the correctly inverted extraction. That is exactly why
   #209's check fired where it did, and why a green "all integers" would have been misleading.

The known quintic invariants used as the anchor are the classical genus-0 values
`n_1 = 2875`, `n_2 = 609250`, `n_3 = 317206375`.

Run:        python3 scripts/gv_basis.py
Guarded by: tests/test_gv_basis.py
"""
from __future__ import annotations

from fractions import Fraction

#: Genus-0 GV invariants of the quintic — the classical integers, used as the anchor.
QUINTIC_GV = (2875, 609250, 317206375)


def divisors(m: int) -> list[int]:
    return [d for d in range(1, m + 1) if m % d == 0]


def prepotential_coefficient(m: int, n: tuple) -> Fraction:
    """`c_m` — the coefficient of `q^m` in the instanton part, from the invariants `n_d`."""
    return Fraction(sum(d ** 3 * n[d - 1] for d in divisors(m) if d <= len(n)), m ** 3)


def gv_from_coefficients(c) -> list:
    """Invert the multi-cover relation — the extraction B1 should have used."""
    n: list = []
    for m in range(1, len(c) + 1):
        # from  sum_{d|m} d^3 n_d = m^3 c_m  =>  n_m = c_m - (1/m^3) sum_{d|m, d<m} d^3 n_d
        total = Fraction(c[m - 1])
        for d in divisors(m):
            if d < m and d <= len(n):
                total -= Fraction(d ** 3 * n[d - 1], m ** 3)
        n.append(total)
    return n


def naive_readoff(c) -> list:
    """What an `n_m = m^3 c_m` read-off gives — integral at composite degrees, and wrong."""
    return [Fraction(c[m - 1]) * m ** 3 for m in range(1, len(c) + 1)]


def report(n=QUINTIC_GV) -> dict:
    """The demonstration: naive extraction returns integers, and the wrong ones."""
    c = [prepotential_coefficient(m, n) for m in range(1, len(n) + 1)]
    correct = gv_from_coefficients(c)
    naive = naive_readoff(c)
    rows = []
    for i, d in enumerate(range(1, len(n) + 1)):
        rows.append({"degree": d, "c_m": c[i], "correct": correct[i], "naive": naive[i],
                     "naive_is_integer": naive[i].denominator == 1,
                     "naive_is_wrong": naive[i] != n[i]})
    return {"coefficients": c, "rows": rows, "round_trip": correct == [Fraction(x) for x in n],
            "naive_all_integer": all(r["naive_is_integer"] for r in rows),
            "naive_any_wrong": any(r["naive_is_wrong"] for r in rows),
            "primitive_degrees": [1]}


__all__ = ["QUINTIC_GV", "divisors", "prepotential_coefficient", "gv_from_coefficients",
           "naive_readoff", "report"]
