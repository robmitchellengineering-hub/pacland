"""The sweep — minimal check-set for a claim's failure modes."""
import unittest

from pacland.climate.guards import guard_energy_budget, guard_ocean_mass, guard_ocean_salt
from pacland.verification_config import measure_coverage, minimal_cover, sweep


class TestSweep(unittest.TestCase):
    def test_climate_three_ledger_sweep(self):
        # claim: "the model conserves"; three failure modes, three checks, 1:1
        base = {"nettoa": 0.0, "mass": 0.0, "salt": 0.0}
        checks = [
            ("energy", lambda m: guard_energy_budget(m["nettoa"], 0.0, tol=0.1)),
            ("mass", lambda m: guard_ocean_mass(m["mass"], tol_mm_per_yr=0.3)),
            ("salt", lambda m: guard_ocean_salt(m["salt"], tol=1e-5)),
        ]
        modes = [
            ("energy leak", lambda m: {**m, "nettoa": 0.5}),
            ("mass leak", lambda m: {**m, "mass": 0.5}),
            ("salt leak", lambda m: {**m, "salt": 1e-4}),
        ]
        r = sweep(checks, modes, base)
        self.assertTrue(r["complete"])
        self.assertEqual(sorted(r["names"]), ["energy", "mass", "salt"])
        self.assertEqual(r["n_checks"], 3)

    def test_redundant_check_is_dropped(self):
        # claim: "x is a positive even small number"; positive_dup is a copy of positive
        base = 10
        checks = [
            ("positive", lambda x: (x > 0, "non-positive")),
            ("even", lambda x: (x % 2 == 0, "odd")),
            ("small", lambda x: (x < 1000, "huge")),
            ("positive_dup", lambda x: (x > 0, "non-positive")),
        ]
        modes = [
            ("negative", lambda x: -x),
            ("odd", lambda x: x + 1),
            ("huge", lambda x: 1000000),
        ]
        r = sweep(checks, modes, base)
        self.assertTrue(r["complete"])
        self.assertEqual(r["n_checks"], 3)
        self.assertEqual(len(set(r["names"]) & {"positive", "positive_dup"}), 1)
        self.assertIn("even", r["names"])
        self.assertIn("small", r["names"])

    def test_uncovered_mode_is_reported_loudly(self):
        # a failure mode no check catches must NOT read as a pass
        base = 10
        checks = [("positive", lambda x: (x > 0, "non-positive"))]
        modes = [("negative", lambda x: -x), ("odd", lambda x: x + 1)]
        r = sweep(checks, modes, base)
        self.assertFalse(r["complete"])
        self.assertEqual(r["uncovered_modes"], ["odd"])

    def test_measure_coverage_shape(self):
        base = 10
        checks = [("positive", lambda x: (x > 0, "!")), ("even", lambda x: (x % 2 == 0, "!"))]
        modes = [("negative", lambda x: -x), ("odd", lambda x: x + 1)]
        C = measure_coverage(checks, modes, base)
        self.assertEqual(C, [[1, 0], [0, 1]])

    def test_minimal_cover_returns_none_when_blind(self):
        # no check catches mode 1 -> None (not a silent empty cover)
        C = [[1, 0], [1, 0]]
        self.assertIsNone(minimal_cover(C))


if __name__ == "__main__":
    unittest.main()
