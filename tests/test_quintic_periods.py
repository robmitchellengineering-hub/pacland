"""F2 M1 — the quintic's PF operator, its Frobenius coefficients, its monodromy, and its radius.

What is verified here is what is *verifiable* today. The conifold period is deliberately **not** claimed:
#210's rule is that the Γ-value must be pinned from a citable source before any number is used, and it
has not been. The finding this milestone does deliver is that the series at z = 0 **cannot** certify the
conifold at all, because the conifold sits exactly on the radius of convergence.
"""
import math
import unittest

import mpmath as mp

from pacland.periods import quintic as Q


class TestFrobeniusCoefficients(unittest.TestCase):
    def test_the_recursion_reproduces_the_closed_form_exactly(self):
        # c_n(0) = (5n)!/(n!)^5 — the literature coefficient, from the operator's own recursion
        mp.mp.dps = 30
        js = Q.coeff_jets(10)
        for n in range(11):
            self.assertAlmostEqual(
                float(js[n][0] / Q.closed_form_coeff(n)), 1.0, places=25,
                msg=f"n={n}")

    def test_the_first_coefficients_are_the_known_integers(self):
        mp.mp.dps = 30
        c = Q.coeffs(3)
        self.assertEqual(int(c[0]), 1)
        self.assertEqual(int(c[1]), 120)              # 5!/1
        self.assertEqual(int(c[2]), 113400)           # 10!/(2!)^5
        self.assertEqual(int(c[3]), math.factorial(15) // math.factorial(3) ** 5)


class TestMonodromy(unittest.TestCase):
    def test_it_is_one_unipotent_block_of_index_four(self):
        mp.mp.dps = 30
        M = Q.monodromy_zero_point()
        n = 4
        I = [[mp.mpf(1) if i == j else mp.mpf(0) for j in range(n)] for i in range(n)]

        def mul(a, b):
            return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

        N = [[M[i][j] - I[i][j] for j in range(n)] for i in range(n)]
        N2, N3, N4 = mul(N, N), mul(mul(N, N), N), mul(mul(mul(N, N), N), N)
        self.assertTrue(all(abs(x) < 1e-20 for r in N4 for x in r), "N^4 must vanish")
        self.assertTrue(any(abs(x) > 1e-12 for r in N3 for x in r), "N^3 must NOT vanish: index 4")
        self.assertTrue(all(abs(M[i][j]) < 1e-20 for i in range(n) for j in range(n) if j > i),
                        "the monodromy is lower triangular: no term with j > i")


class TestRadius(unittest.TestCase):
    def test_the_series_is_bounded_inside_the_radius(self):
        mp.mp.dps = 30
        b = Q.tail_bound(60, mp.mpf("0.0001"))
        self.assertNotEqual(b, mp.inf)
        self.assertLess(float(b), 1e-20)

    def test_the_ratio_tends_to_the_radius(self):
        mp.mp.dps = 30
        r = Q.ratios(200, Q.Z_CONIFOLD * mp.mpf("0.5"))
        self.assertAlmostEqual(float(r[-1]), 0.5, delta=0.02)
        r1 = Q.ratios(300, Q.Z_CONIFOLD)
        self.assertGreater(float(r1[-1]), 0.99)        # at the conifold the ratio test is exhausted

    def test_the_bound_degrades_by_orders_of_magnitude_at_the_conifold(self):
        # the finding: at z_c the ratio r -> 1, so the geometric bound degrades like 1/(1-r) and no
        # practical number of terms certifies the conifold. Measured, not asserted:
        mp.mp.dps = 30
        inside = float(Q.tail_bound(300, Q.Z_CONIFOLD / 2))
        at = float(Q.tail_bound(300, Q.Z_CONIFOLD))
        self.assertGreater(at, 1000 * inside)
        self.assertGreater(float(Q.ratios(300, Q.Z_CONIFOLD)[-1]), 0.99)
        st = Q.radius_study(120)
        self.assertGreater(st["1.0"]["tail_bound"], 1e3 * st["0.5"]["tail_bound"])


if __name__ == "__main__":
    unittest.main()
