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
