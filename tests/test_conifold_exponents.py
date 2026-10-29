"""F2 M2a — the conifold's local exponents, computed exactly."""
import unittest

import sympy as sp

from pacland.periods import conifold as C


class TestIndicial(unittest.TestCase):
    def test_the_indicial_polynomial_is_s_s_minus_1_squared_s_minus_2(self):
        p = C.indicial_polynomial()
        s = C.S
        self.assertEqual(sp.simplify(p - s * (s - 1) ** 2 * (s - 2)), 0)

    def test_the_exponents_are_0_1_1_2(self):
        self.assertEqual([sp.Rational(e) for e in C.exponents()],
                         [sp.Integer(0), sp.Integer(1), sp.Integer(1), sp.Integer(2)])

    def test_all_exponents_are_integers_so_the_monodromy_is_unipotent(self):
        r = C.structure()
        self.assertTrue(r["all_integer"])
        self.assertTrue(r["unipotent"])
        self.assertEqual(r["double_root"], ["1"])

    def test_the_regular_singular_structure(self):
        # at u = 0 the leading coefficient has a simple zero: lowest index is one above the order
        Lf = C.apply_L_at_conifold()
        self.assertEqual(min(Lf), -3)

    def test_a_wrong_zc_breaks_the_polynomial(self):
        # the exponents are a property of z_c = 1/5^5, not of the method
        Lf = C.apply_L_at_conifold(zc=sp.Rational(1, 5 ** 4))
        s = C.S
        p = sp.Poly(Lf[min(Lf)], s)
        self.assertNotEqual(sp.simplify(p.as_expr() - s * (s - 1) ** 2 * (s - 2)), 0)


if __name__ == "__main__":
    unittest.main()


class TestResonances(unittest.TestCase):
    """Integral exponents mean the recursion collapses at integer orders — computed, not assumed."""

    def test_the_resonance_orders(self):
        self.assertEqual(C.resonances(0), [1, 2])
        self.assertEqual(C.resonances(1), [1])
        self.assertEqual(C.resonances(2), [])

    def test_only_the_top_exponent_is_a_plain_power_series(self):
        w = C.which_branch_is_clean()
        self.assertTrue(w["2"]["clean"])
        self.assertFalse(w["0"]["clean"])
        self.assertFalse(w["1"]["clean"])

    def test_this_is_why_the_connection_needs_the_log_algebra(self):
        # two of the three exponent branches are resonantly degenerate (0 and 1); with the double root
        # at 1 that is three of the four solutions carrying logarithms, and only s=2 clean. Stated as a
        # test so the next session does not discover it the hard way.
        w = C.which_branch_is_clean()
        self.assertEqual(sum(1 for v in w.values() if not v["clean"]), 2)
        self.assertEqual(sorted(k for k, v in w.items() if v["clean"]), ["2"])
