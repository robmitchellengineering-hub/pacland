"""The energy claims: the two computed ones are arithmetic that can be wrong; the three registered ones
must refuse rather than print a number they have not earned.

The refusal tests matter more than the arithmetic ones: a registered claim whose script happily produces
a verdict would be exactly the "gate that cannot fail" this repository exists to avoid.
"""
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import energy_li_s_ceiling as LIS  # noqa: E402
import energy_lithium_ceiling as LIC  # noqa: E402
import energy_drift_ecs as EDE  # noqa: E402


class TestLiSCeiling(unittest.TestCase):
    def test_the_asymptote_at_r_equal_3_is_680_wh_kg(self):
        self.assertAlmostEqual(LIS.asymptote(3.0), 680.0, delta=3.0)

    def test_a_finite_cell_cannot_reach_the_asymptote(self):
        # the correction this run produced: 680 is a q -> infinity limit, never a reachable cell
        self.assertLess(LIS.ceiling(3.0), LIS.asymptote(3.0))

    def test_the_ceiling_falls_as_electrolyte_rises(self):
        values = [LIS.asymptote(r) for r in (2.0, 3.0, 4.0, 6.0)]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_1600_wh_kg_is_impossible_by_arithmetic(self):
        self.assertLess(LIS.ceiling(3.0, q_max=20.0), 1600.0 / 2)


class TestLithiumCeiling(unittest.TestCase):
    def test_lfp_needs_0_41_kg_lce_per_kwh(self):
        self.assertAlmostEqual(LIC.lce_per_kwh(1.75), 0.41, delta=0.01)

    def test_the_2024_supply_caps_deployment_near_3_2_twh(self):
        self.assertAlmostEqual(LIC.deployment_ceiling_twh(1.3e6, 0.41), 3.17, delta=0.1)

    def test_a_leakier_chemistry_lowers_the_ceiling(self):
        self.assertLess(LIC.deployment_ceiling_twh(1.3e6, LIC.lce_per_kwh(1.9)),
                        LIC.deployment_ceiling_twh(1.3e6, LIC.lce_per_kwh(1.75)))


class TestClimateTransfer(unittest.TestCase):
    def _table(self):
        return json.loads((ROOT / "data" / "climate" / "cmip6_ecs_models.json").read_text())["models"]

    def test_forcing_does_not_predict_ecs_across_models(self):
        # the refutation this run produced: the slope is negative, so 0.76 K per W/m2 is not a slope
        models = self._table()
        slope = EDE.ols_slope([m["erf2x_wm2"] for m in models], [m["ecs_K"] for m in models])
        self.assertLess(slope, 0.3, f"slope {slope:.3f} no longer refutes the draft claim")

    def test_the_drift_join_covers_most_of_the_ledger(self):
        models = {m["model"]: m["ecs_K"] for m in self._table()}
        drift = json.loads((ROOT / "data" / "climate" / "cmip6_drift.json").read_text())["models"]
        joined = [r for r in drift if r["model"] in models]
        self.assertGreaterEqual(len(joined), 15, f"only {len(joined)} models join drift to ECS")


class TestRegisteredClaimsRefuse(unittest.TestCase):
    def _run(self, script: str, *args: str):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                              capture_output=True, text=True, timeout=120)

    def test_fusion_refuses_without_the_itpa_database(self):
        r = self._run("energy_fusion_exponent.py", "--data", "/nonexistent/itpa.csv")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("REFUSED", r.stdout)
        self.assertIn("Falsifier", r.stdout)

    def test_climate_refuses_without_the_ecs_column(self):
        r = self._run("energy_drift_ecs.py", "--ecs", "/nonexistent/ecs.json")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("REFUSED", r.stdout)
        self.assertIn("ECS", r.stdout)

    def test_verification_energy_refuses_without_a_measurement(self):
        r = self._run("energy_verify_joules.py", "--data", "/nonexistent/energy.json")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn("REFUSED", r.stdout)
        self.assertIn("10^4", r.stdout)


class TestEveryProgrammeScriptRunsOrRefuses(unittest.TestCase):
    """A registered claim whose script neither runs nor refuses cleanly is a dead entry in the registry."""

    PROGRAMME = {
        "lithium-mass-ceiling", "li-s-electrolyte-ceiling", "fusion-confinement-exponent",
        "climate-drift-ecs-transfer", "verification-joule-floor", "ecs-per-forcing-slope",
    }

    def test_each_script_terminates_with_a_verdict_or_a_refusal(self):
        reg = json.loads((ROOT / "docs" / "claims.json").read_text())
        for c in reg["claims"]:
            if c["id"] not in self.PROGRAMME:
                continue
            with self.subTest(claim=c["id"]):
                r = subprocess.run([sys.executable, str(ROOT / c["script"])],
                                   capture_output=True, text=True, timeout=900)
                self.assertIn(r.returncode, (0, 2),
                              f"{c['id']}: {c['script']} exited {r.returncode}: {r.stderr[-400:]}")
                self.assertTrue(r.returncode == 0 or "REFUSED" in r.stdout,
                                f"{c['id']}: exit 2 without a REFUSED line")


if __name__ == "__main__":
    unittest.main()
