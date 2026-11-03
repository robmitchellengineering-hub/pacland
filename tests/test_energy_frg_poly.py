"""Rung 2 tests — a ladder that reproduces one rung and refuses to flatter the rest.

The value of this file is the second test. Anyone can make `n=1` match a table; what matters is that the
`n>=2` rows are reported as **not matching**, with the missing term named, rather than being tuned into
agreement. A truncation ladder that silently omits a term looks exactly like a converging ladder.
"""
import pathlib
import sys
import unittest

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from pacland.energy import frg_poly as M  # noqa: E402


class TestSeriesArithmetic(unittest.TestCase):
    def test_geometric_series(self):
        """1/(1-x) = 1 + x + x^2 + ... — the inverse must reproduce it exactly to the truncation order."""
        n = 4
        denom = M._poly(n, [(0, 1.0), (1, -1.0)])
        got = M._inv(denom, n)
        self.assertTrue(np.allclose(got, np.ones(n + 1)))

    def test_multiplication_truncates(self):
        n = 2
        a = M._poly(n, [(0, 1.0), (1, 2.0), (2, 3.0)])
        b = a.copy()
        prod = M._mul(a, b, n)
        self.assertAlmostEqual(prod[0], 1.0)
        self.assertAlmostEqual(prod[1], 4.0)
        self.assertAlmostEqual(prod[2], 10.0)

    def test_derivative_of_a_polynomial(self):
        n = 3
        f = M._poly(n, [(0, 5.0), (1, 7.0), (2, 11.0)])
        df = M._deriv(f, n)
        self.assertAlmostEqual(df[0], 7.0)
        self.assertAlmostEqual(df[1], 22.0)
        self.assertAlmostEqual(df[2], 0.0)


class TestTheKnownAnswer(unittest.TestCase):
    def test_n1_reproduces_the_published_fixed_point(self):
        """Table 3 of arXiv:0712.0445: u0* = 0.00523, u1* = -0.0202."""
        u, res = M.find_fixed_point(1)
        self.assertLess(res, 1e-10)
        self.assertAlmostEqual(u[0], 0.00523, places=5)
        self.assertAlmostEqual(u[1], -0.02020, places=4)

    def test_the_beta_functions_actually_vanish_there(self):
        u, _ = M.find_fixed_point(1)
        self.assertLess(float(np.max(np.abs(M.betas(u, 1)))), 1e-10)

    def test_the_paper_table_is_transcribed_not_invented(self):
        self.assertEqual(M.PAPER_TABLE_3[1][0], 0.00523)
        self.assertEqual(len(M.PAPER_TABLE_3[6]), 7)


class TestTheLadderRefusesToFlatterItself(unittest.TestCase):
    def test_n2_and_n3_do_not_match_the_paper(self):
        """They must be reported as mismatches. Tuning them into agreement is the failure mode."""
        rows = {r["n"]: r for r in M.ladder(3)}
        self.assertTrue(rows[1]["matches_paper"])
        self.assertFalse(rows[2]["matches_paper"])
        self.assertFalse(rows[3]["matches_paper"])

    def test_every_row_still_reaches_a_fixed_point(self):
        """A mismatch is a statement about the truncation, not a solver failure: the flow still vanishes."""
        for row in M.ladder(3):
            self.assertLess(row["residual"], 1e-8, f"n={row['n']}")

    def test_the_missing_term_is_named(self):
        self.assertIn("D_1(d,0)", M.MISSING_TERM)
        self.assertIn("single", M.__doc__.lower())

    def test_the_module_forbids_a_convergence_claim(self):
        doc = M.__doc__ or ""
        self.assertIn("claim a ladder exists", doc.lower())


if __name__ == "__main__":
    unittest.main()
