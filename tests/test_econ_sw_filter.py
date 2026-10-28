"""The SW filter: the space is well formed, the block filter matches the full one, and the
usability verdict is measured rather than asserted."""
import unittest

from pacland.economics import sw_filter as F


class TestSpace(unittest.TestCase):
    def test_the_state_space_is_well_formed(self):
        solved, measured = F.solved_model(), F.measured_rows()
        space = F.one_step_space(solved, measured)
        self.assertEqual(space["n_state"], 34)
        self.assertEqual(space["n_obs"], 5)
        self.assertEqual(len(space["observation_lag"]), 5)

    def test_growth_observables_carry_a_lag_row(self):
        solved, measured = F.solved_model(), F.measured_rows()
        space = F.one_step_space(solved, measured)
        lag = space["observation_lag"][0]
        self.assertTrue(any(abs(v) > 1e-12 for v in lag))

    def test_wages_are_excluded(self):
        self.assertNotIn("dw", F.USED)


class TestFilterRuns(unittest.TestCase):
    def test_the_block_filter_produces_one_forecast_per_step(self):
        space = F.one_step_space(F.solved_model(), F.measured_rows())
        sim = F.simulate(steps=6, seed=2)
        out = F.block_filter(space, sim["observables"])
        self.assertEqual(len(out["obs_pred"]), 6)
        self.assertEqual(len(out["obs_pred"][0]), 5)

    def test_simulation_uses_the_solved_model(self):
        sim = F.simulate(steps=4, seed=2)
        self.assertEqual(len(sim["truth"][0]), 34)


class TestUsabilityIsMeasured(unittest.TestCase):
    def test_the_filter_is_documented_as_not_usable(self):
        q = F.forecast_quality(steps=30, seed=5)
        self.assertFalse(q["usable"])
        self.assertLess(q["worst_r2"], 0.5)

    def test_the_audit_records_the_refusal(self):
        a = F.audit()
        self.assertFalse(a["usable"])
        self.assertTrue(a["all_pass"])          # the situation is honestly characterised


if __name__ == "__main__":
    unittest.main()
