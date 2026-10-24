"""Conservation repair — guards the drift-correction result against drift.

Known answers (data/climate/cmip6_drift.json, Irving et al. 2021):
- 19 models, 12 leak energy (net TOA beyond 0.1 W/m2).
- The leak is localized to the atmosphere-ocean coupling (salt conserved).
- Drift-correction makes every model conserve by construction.
- Post-fix: the strict gate reduces to sensitivity+forcing -> 15 models, ~3.08 K.
"""
import unittest

from pacland.climate.drift_correction import (
    correction_proof,
    correction_proof_all,
    full_repair,
    leak,
    leak_map,
    post_fix_prediction,
    repair,
    repair_report,
    retrospective,
    retrospective_rule_of_three,
    zonal_drift_available,
)


class TestRepairReport(unittest.TestCase):
    def test_19_models(self):
        self.assertEqual(repair_report()["n_models"], 19)

    def test_12_leak_energy(self):
        n_energy = sum(1 for m in repair_report()["models"] if m["energy_leaks"])
        self.assertEqual(n_energy, 12)

    def test_leak_localized_to_coupling(self):
        # more models leak at the coupling (energy/mass) than at the ocean (salt)
        rp = repair_report()
        self.assertGreater(rp["n_coupling_leak"], rp["n_models"] - rp["n_coupling_leak"])

    def test_all_correctable(self):
        self.assertTrue(repair_report()["all_correctable"])


class TestRepair(unittest.TestCase):
    def test_repair_conserves_by_construction(self):
        self.assertTrue(repair("CNRM-ESM2-1")["conserves_after_fix"])

    def test_repair_is_the_negated_leak(self):
        lk = leak("CNRM-ESM2-1")
        rp = repair("CNRM-ESM2-1")
        self.assertAlmostEqual(rp["correct_energy_by_Wm2"], -lk["energy_Wm2"], places=4)

    def test_repair_names_what_it_does_not_fix(self):
        self.assertIn("spatial", repair("CNRM-ESM2-1")["what_it_does_not_fix"])


class TestPostFixPrediction(unittest.TestCase):
    def test_post_fix_ecs_is_sens_forc(self):
        p = post_fix_prediction()
        self.assertAlmostEqual(p["after_fix_ECS_K"], 3.08, places=2)
        self.assertEqual(p["after_fix_models"], 15)

    def test_before_fix_is_giss(self):
        self.assertAlmostEqual(post_fix_prediction()["before_fix_strict_ECS_K"], 2.71, places=2)


class TestFullRepair(unittest.TestCase):
    def test_full_repair_is_global_plus_zonal(self):
        fr = full_repair("CNRM-ESM2-1")
        self.assertIn("zonal", fr["full_fix"])
        self.assertTrue(fr["conserves_after_fix"])

    def test_zonal_tier_reports_status(self):
        z = full_repair("CNRM-ESM2-1")["zonal"]
        # either a leak map (mesh data present) or a pending status (data not yet produced)
        self.assertTrue("model" in z or "status" in z)

    def test_leak_map_handles_missing_data(self):
        lm = leak_map("CNRM-ESM2-1")
        if zonal_drift_available():
            self.assertIn("max_leak_lat", lm)
        else:
            self.assertIsNone(lm)


class TestCorrectionProof(unittest.TestCase):
    def test_hadgem3_leaks_then_conserves(self):
        p = correction_proof("HadGEM3-GC31-LL")
        self.assertFalse(p["before"]["conserves_energy"])   # leaks today
        self.assertTrue(p["after"]["conserves"])            # conserves after
        self.assertEqual(p["after"]["netTOA_Wm2"], 0.0)

    def test_correction_is_the_negated_leak(self):
        p = correction_proof("HadGEM3-GC31-LL")
        self.assertAlmostEqual(p["correction"]["energy_Wm2"], -p["before"]["netTOA_Wm2"], places=4)

    def test_error_removed_is_quantified(self):
        p = correction_proof("HadGEM3-GC31-LL")
        self.assertGreater(p["error_removed"]["ratio_to_eei"], 0)
        lo, hi = p["error_removed"]["spurious_warming_K"]
        self.assertGreater(hi, lo)


class TestCorrectionProofAll(unittest.TestCase):
    def test_all_19_conserve_after(self):
        r = correction_proof_all()
        self.assertEqual(r["n_models"], 19)
        self.assertEqual(r["n_failed_before"], 12)   # 12 leak energy
        self.assertEqual(r["n_failed_after"], 0)     # all conserve after the fix

    def test_every_row_conserves_exactly(self):
        r = correction_proof_all()
        self.assertTrue(all(m["after_netTOA_Wm2"] == 0.0 for m in r["models"]))

    def test_max_imbalance_is_the_worst_leaker(self):
        r = correction_proof_all()
        worst = max(r["models"], key=lambda m: abs(m["before_netTOA_Wm2"]))
        self.assertAlmostEqual(r["max_imbalance_removed_K"], abs(worst["before_netTOA_Wm2"]) * 0.5, places=2)


class TestRetrospective(unittest.TestCase):
    def test_correction_lands_inside_observed_range(self):
        self.assertTrue(retrospective()["ecs_corrected_in_range"])

    def test_naive_ensemble_is_hot_biased(self):
        self.assertGreater(retrospective()["ecs_naive_bias_K"], 0.5)

    def test_correction_reduces_ecs_bias(self):
        r = retrospective()
        self.assertLess(abs(r["ecs_corrected_bias_K"]), abs(r["ecs_naive_bias_K"]))


class TestRetrospectiveRuleOfThree(unittest.TestCase):
    def test_three_independent_arms(self):
        r = retrospective_rule_of_three()
        self.assertEqual(r["n_arms"], 3)
        sources = {a["source"] for a in r["arms"]}
        self.assertEqual(len(sources), 3)   # three distinct observational sources

    def test_each_arm_has_a_finding(self):
        r = retrospective_rule_of_three()
        self.assertTrue(all(a["finding"] for a in r["arms"]))


if __name__ == "__main__":
    unittest.main()
