import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import unittest

from pacland.solve import constraint_set, solve

DATA = Path(__file__).resolve().parents[1] / "data" / "vacua_observables.json"


class TestSolve(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(DATA) as f:
            raw = json.load(f)
        cls.records = [r for d in raw.values() for r in d]

    def test_constraint_set_has_three_real_constraints(self):
        cs = constraint_set()
        self.assertEqual(len(cs), 3)

    def test_solve_on_real_data(self):
        r = solve(self.records)
        self.assertEqual(r["n"], len(self.records))
        self.assertEqual(len(r["per"]), 3)
        self.assertGreater(r["joint"], 0.9)
        self.assertGreaterEqual(r["n_survive"], 0)
        self.assertIn("log_W0", r["narrowing"])
        # with ~1 survivor the narrowing must be unmeasurable, not faked 0%
        self.assertIsNone(r["narrowing"]["log_W0"])

    def test_gauge_constraint_rejects_strong_coupling(self):
        keep = dict(constraint_set())["perturbative gauge (g^2 < 4pi)"]
        self.assertTrue(keep({"log_g2_inv": [1.0, 2.0]}))     # weak: passes
        self.assertFalse(keep({"log_g2_inv": [1.0, -5.0]}))   # one strong: fails
        self.assertTrue(keep({"log_g2_inv": []}))             # unknown: passes


if __name__ == "__main__":
    unittest.main()
