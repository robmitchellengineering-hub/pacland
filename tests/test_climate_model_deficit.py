"""Per-model climate deficit — a failed test costs an observable, not a fraction."""
import unittest

from pacland.climate import model_deficit as D


class TestPerModel(unittest.TestCase):
    def test_the_clean_model_has_three(self):
        r = D.model_deficit("GISS-E2-1-G")
        self.assertEqual(r.m, 3)
        self.assertTrue(r.ecs_validated and r.erf2x_validated and r.conservation_validated)

    def test_the_leaking_model_has_two(self):
        r = D.model_deficit("MPI-ESM1-2-HR")
        self.assertEqual(r.m, 2)
        self.assertFalse(r.conservation_validated)

    def test_the_failing_model_has_one(self):
        r = D.model_deficit("UKESM1-0-LL")
        self.assertEqual(r.m, 1)
        self.assertFalse(r.ecs_validated)

    def test_the_radius_falls_with_m(self):
        a = D.model_deficit("GISS-E2-1-G").radius
        b = D.model_deficit("UKESM1-0-LL").radius
        self.assertLess(a, b)

    def test_matches_the_trust_board(self):
        from pacland.climate.trust_board import board

        rows = {r["model"]: r for r in board()}
        r = D.model_deficit("MPI-ESM1-2-HR")
        self.assertFalse(r.conservation_validated)
        self.assertIn("conservation", rows["MPI-ESM1-2-HR"]["axes_failed"])


class TestReport(unittest.TestCase):
    def test_three_rows(self):
        self.assertEqual(len(D.board_rows()), 3)

    def test_summary_explains_the_marking(self):
        s = D.summary()
        for token in ("+  validated", "x  failed", "—  no data"):
            self.assertIn(token, s)


if __name__ == "__main__":
    unittest.main()
