"""F1 — the measure engine: a family of measures, one exact lattice, and a spread that is the result.

The acceptance test is not a number, it is an identity: on a symmetric window the tadpole flips sign
under `(F, H) -> (-F, H)`, so every measure that sees `N` only through `|N|` must give

    fraction(N > 0) == (1 - fraction(N == 0)) / 2

exactly. A broken weight fails it, which is how the engine is proved able to go red.
"""
import unittest

import numpy as np

from pacland.exactness import measures as M
from pacland.exactness import windows as W


class TestAntisymmetry(unittest.TestCase):
    def test_the_identity_holds_for_every_symmetric_measure(self):
        r = M.antisymmetry()
        self.assertTrue(r["all_pass"], [c for c in r["checks"] if not c["pass"]])
        for c in r["checks"]:
            self.assertLess(c["residual"], 1e-12, c["measure"])

    def test_the_identity_can_fail(self):
        # a weight that is NOT invariant under N -> -N must break the identity
        fluxes = W.enumerate_window(6, 1)
        n_vals = W.tadpoles(fluxes)
        asymmetric = np.abs(n_vals.astype(float) + 3.0)      # depends on the sign of N
        asymmetric = asymmetric / asymmetric.sum()
        lhs = M.fraction(n_vals > 0, asymmetric)
        rhs = (1.0 - M.fraction(n_vals == 0, asymmetric)) / 2.0
        self.assertGreater(abs(lhs - rhs), 1e-3)


class TestMeasures(unittest.TestCase):
    def test_every_measure_is_a_distribution(self):
        fluxes = W.enumerate_window(6, 1)
        n_vals = W.tadpoles(fluxes)
        for kind in M.MEASURES:
            if kind in ("log-N", "tadpole-weighted"):
                continue                                    # zero weight on N = 0 by construction
            w = M.weights(kind, fluxes, n_vals)
            self.assertAlmostEqual(float(w.sum()), 1.0, places=12, msg=kind)
            self.assertTrue(np.all(w >= 0), kind)

    def test_an_unknown_measure_is_refused(self):
        fluxes = W.enumerate_window(6, 1)
        with self.assertRaises(ValueError):
            M.weights("wishful", fluxes)


class TestTable(unittest.TestCase):
    def test_the_table_reports_its_window_and_its_exactness(self):
        t = M.table()
        self.assertEqual(t["window"], "b3=6, |F_i|,|H_i| <= 1")
        self.assertTrue(t["exact"])
        self.assertEqual(t["pairs"], 531441)

    def test_the_fraction_moves_by_a_factor_of_five(self):
        # the fact F1 exists to produce: on ONE lattice, one question, five reasonable measures
        t = M.table()
        row = {r["property"]: r for r in t["rows"]}["0 < N <= 1"]
        self.assertAlmostEqual(row["values"]["tadpole-uniform"], 0.0714, places=3)
        self.assertAlmostEqual(row["values"]["log-N"], 0.3609, places=3)
        self.assertGreater(row["ratio"], 5.0)

    def test_a_measure_with_no_support_is_flagged_not_averaged(self):
        t = M.table()
        row = {r["property"]: r for r in t["rows"]}["prop_zero"]
        self.assertEqual(sorted(row["zero_support"]), ["log-N", "tadpole-weighted"])
        self.assertAlmostEqual(row["values"]["flux-uniform"], 0.2407, places=3)


class TestSmallLattice(unittest.TestCase):
    def test_flux_uniform_is_the_plain_count(self):
        fluxes = W.enumerate_window(2, 1)                   # 3^4 = 81 pairs
        n_vals = W.tadpoles(fluxes)
        w = M.weights("flux-uniform", fluxes, n_vals)
        direct = float((n_vals > 0).sum()) / len(n_vals)
        self.assertAlmostEqual(M.fraction(n_vals > 0, w), direct, places=12)
        self.assertEqual(len(fluxes), 81)


if __name__ == "__main__":
    unittest.main()
