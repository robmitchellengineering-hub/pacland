"""Carrier A, rung 1 — the Einstein–Hilbert truncation, checked against its own closed form.

The point of these tests is not that a fixed point exists. It is that **this solver reproduces a
published closed form and a published pair of complex critical exponents**, so that when the next rung
of the truncation ladder disagrees with this one, the disagreement is about the truncation and not about
a bug in the solver.

The mutation test at the end is the one that matters: it re-runs the solver with the `+2` dropped from
`P2` — the exact reading the mangled PDF text suggested — and shows the answer moves. That variant
looked completely plausible and would have shipped.
"""
import cmath
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.energy import frg  # noqa: E402


class TestAgainstTheClosedForm(unittest.TestCase):
    """Litim hep-th/0312114, eq. gtilde-inf and the d=4 critical exponents."""

    def test_lambda_star_at_four_dimensions_is_one_quarter(self):
        """The closed form is 0/0 at d=4; the paper gives the limit in words, and so does this."""
        lam, _ = frg.solve(4.0)
        self.assertAlmostEqual(lam, 0.25, places=10)

    def test_g_star_at_four_dimensions_matches_the_reinserted_cd(self):
        _, g = frg.solve(4.0)
        g_phys = g * frg.cd(4.0)
        self.assertAlmostEqual(g_phys, 1.1780972451, places=8)

    def test_the_beta_functions_vanish_at_the_fixed_point(self):
        lam, g = frg.solve(4.0)
        self.assertAlmostEqual(frg.beta_lambda(lam, g, 4.0), 0.0, places=10)
        self.assertAlmostEqual(frg.beta_g(lam, g, 4.0), 0.0, places=10)

    def test_eta_at_the_fixed_point_is_two_minus_d(self):
        """The paper: beta_g = 0 implies eta* = 2 - d. An internal consistency check, not a citation."""
        for d in (4.0, 5.0, 6.0):
            lam, g = frg.solve(d)
            self.assertAlmostEqual(frg.eta(lam, g, d), 2.0 - d, places=6, msg=f"d={d}")

    def test_the_closed_form_matches_the_solver_above_four_dimensions(self):
        for d in (5.0, 6.0, 8.0, 10.0):
            lam, g = frg.solve(d)
            lam_ref, g_phys_ref = frg.fixed_point_closed_form(d)
            self.assertAlmostEqual(lam, lam_ref, places=7, msg=f"d={d}")
            self.assertAlmostEqual(g * frg.cd(d), g_phys_ref, places=5, msg=f"d={d}")


class TestTheCriticalExponents(unittest.TestCase):
    def test_at_four_dimensions_they_are_the_published_complex_pair(self):
        """theta_pm = (5 +/- i sqrt(167))/3, i.e. 1.6667 +/- 4.3076 i."""
        th = frg.critical_exponents(4.0)
        exact = (5.0 + 1j * 167 ** 0.5) / 3.0
        self.assertAlmostEqual(th[0].real, exact.real, places=4)
        self.assertAlmostEqual(abs(th[0].imag), exact.imag, places=3)

    def test_they_are_complex_rather_than_refused(self):
        """A solver that raises on complex exponents fails on the known answer - this one did."""
        th = frg.critical_exponents(4.0)
        self.assertTrue(all(isinstance(t, complex) for t in th))
        self.assertGreater(abs(th[0].imag), 1.0)

    def test_the_pair_is_conjugate(self):
        th = frg.critical_exponents(4.0)
        self.assertAlmostEqual(th[0].real, th[1].real, places=6)
        self.assertAlmostEqual(th[0].imag, -th[1].imag, places=6)


class TestTheComplexityBoundary(unittest.TestCase):
    """The paper: the exponents stay complex for 2.56 < d < 21.4. That is a third known answer."""

    def test_complex_inside_the_window(self):
        for d in (3.0, 4.0, 10.0, 21.0):
            self.assertGreater(abs(frg.critical_exponents(d)[0].imag), 1e-6, msg=f"d={d}")

    def test_real_above_the_window(self):
        for d in (21.5, 22.0, 25.0):
            self.assertLess(abs(frg.critical_exponents(d)[0].imag), 1e-9, msg=f"d={d}")

    def test_the_boundary_sits_between_21_and_22(self):
        self.assertGreater(abs(frg.critical_exponents(21.0)[0].imag), 1e-6)
        self.assertLess(abs(frg.critical_exponents(22.0)[0].imag), 1e-9)


class TestTheMutation(unittest.TestCase):
    def test_dropping_the_plus_two_from_p2_moves_the_answer(self):
        """The mangled-PDF reading of P2 gave a cubic where the paper says quadratic.

        This is not a hypothetical: it is the near-miss this rung was built out of. If the `+2` were
        cosmetic, the closed-form check would pass either way and the source would not matter.
        """
        def p2_no_plus_two(lam, g, d):
            return 8.0 * (lam ** 2 - lam - d * g)

        def beta_lam_variant(lam, g, d):
            return frg.p1(lam, g, d) / (p2_no_plus_two(lam, g, d) + 4.0 * (d + 2.0) * g)

        def beta_g_variant(lam, g, d):
            return (d - 2.0) * g * p2_no_plus_two(lam, g, d) / (
                p2_no_plus_two(lam, g, d) + 4.0 * (d + 2.0) * g)

        # beta_g = 0 with the wrong P2 forces g = lambda (lambda - 1) / d
        lam, g = 0.6, None
        g = lam * (lam - 1.0) / 4.0
        self.assertLess(g, 0.0, "the wrong reading drives g negative - unphysical, and still 'solves'")
        self.assertNotAlmostEqual(g, frg.solve(4.0)[1], places=3)


class TestTheVerdict(unittest.TestCase):
    def test_the_rung_one_verdict_is_that_a_fixed_point_exists(self):
        v = frg.verdict(4.0)
        self.assertTrue(v["matches_closed_form"])
        self.assertAlmostEqual(v["eta_star"], -2.0, places=6)

    def test_the_verdict_says_what_it_is_not(self):
        """One truncation is not the ladder: the docstring must not claim survival."""
        doc = frg.__doc__ or ""
        self.assertIn("one truncation", doc.lower())
        self.assertIn("not evidence", doc.lower())


if __name__ == "__main__":
    unittest.main()
