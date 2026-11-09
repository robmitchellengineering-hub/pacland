"""STRATA (NVIDIA) — km-scale emulator, run through the two-level certificate.

Known answers, all from primary sources (arXiv:2606.31248 abstract; the released
huggingface.co/nvidia/strata config.json / channels.json / train_config.json):

- 331,664,906 parameters (config.json).
- 7 prognostic + 3 diagnostic output variables, 4 forcing inputs, 24 levels
  (level_start 8, level_end 32) -> 145 prognostic scalar channels + 3 = 148.
- No top-of-atmosphere radiative flux in any output channel -> EEI is not
  computable -> the anchor reality-fidelity count is m=1 (GMST only), below
  ACE's m=2; the generous tier (GMST + surface pressure) is m=2.
- radius_e(m) at delta_e=0.025: m=1 -> ~1.358, m=2 -> ~0.960, m=0 -> inf.
- The energy headline is throughput: 48 sim-days/MWh (~50x SCREAM), 741
  sim-days/wall-clock day @ 512 H100 — efficiency, not fidelity.
"""
import unittest
from math import inf

from pacland.climate.strata_fidelity import (
    ENERGY_FACTOR_VS_SCREAM,
    FLOP_FACTOR_PER_GRIDPOINT,
    N_LEVELS,
    N_PARAMETERS,
    RESOLUTION_KM,
    SIM_DAYS_PER_MWH,
    SIM_DAYS_PER_WALLCLOCK_DAY,
    STRATA_OUTPUT_CHANNELS,
    STRATA_FORCING,
    TRAINING_DAYS,
    anchor_deficit,
    channel_summary,
    eei_computable,
    efficiency_summary,
    reality_deficit,
)


class TestStrataChannels(unittest.TestCase):
    def test_seven_prognostic_three_diagnostic_variables(self):
        cs = channel_summary()
        self.assertEqual(cs["n_prognostic_vars"], 7)
        self.assertEqual(cs["n_diagnostic_vars"], 3)
        self.assertEqual(cs["n_forcing_vars"], 4)

    def test_six_prognostic_fields_carry_24_levels(self):
        three_d = {c.symbol for c in STRATA_OUTPUT_CHANNELS if c.n_levels == N_LEVELS}
        self.assertEqual(three_d, {"PotentialTemperature", "U", "V", "z_mid", "omega", "qv"})
        self.assertEqual(N_LEVELS, 24)

    def test_148_scalar_channels_by_the_ace_convention(self):
        cs = channel_summary()
        self.assertEqual(cs["n_prognostic_channels"], 145)  # 6 x 24 + T_2m
        self.assertEqual(cs["n_diagnostic_channels"], 3)
        self.assertEqual(cs["n_outputs"], 148)

    def test_parameter_count_is_331_664_906(self):
        self.assertEqual(N_PARAMETERS, 331_664_906)
        self.assertEqual(channel_summary()["n_parameters"], 331_664_906)

    def test_training_facts_from_the_abstract(self):
        self.assertEqual(TRAINING_DAYS, 17)
        self.assertEqual(RESOLUTION_KM, 4.9)
        self.assertEqual(channel_summary()["n_grid_cells"], 25_000_000)
        self.assertEqual(len(STRATA_FORCING), 4)


class TestNoToaFlux(unittest.TestCase):
    def test_no_output_channel_is_a_radiative_flux(self):
        # the sharp finding: the released checkpoint emits no TOA flux, so EEI
        # is not computable from it
        self.assertFalse(eei_computable())

    def test_eei_is_measured_but_not_computable(self):
        a = anchor_deficit()
        self.assertEqual(a.n_measured, 4)       # all four anchors are measured
        self.assertEqual(a.n_computable, 1)     # only GMST is computable
        self.assertEqual(a.n_unverifiable, 3)   # EEI, OHC, GMSL


class TestStrataRealityFidelity(unittest.TestCase):
    def test_anchor_m_is_1_gmst_only(self):
        a = anchor_deficit()
        self.assertEqual(a.n_validation, 1)     # GMST only; EEI not computable
        self.assertAlmostEqual(a.radius, 1.358, places=3)

    def test_generous_m_is_2(self):
        r = reality_deficit()
        self.assertEqual(r.n_validation, 2)     # GMST + surface pressure
        self.assertAlmostEqual(r.radius, 0.960, places=3)

    def test_anchor_radius_is_looser_than_ace(self):
        # STRATA's anchor (m=1) radius ~1.358 is *looser* than ACE's anchor (m=2)
        # ~0.960, because STRATA cannot reach EEI — the finer emulator verifies
        # worse on the reality axis even as it wins on resolution.
        a = anchor_deficit()
        self.assertGreater(a.radius, 0.96)

    def test_strict_tier_is_vacuous(self):
        # STRATA's own paper validates it against SCREAM, never the Earth, so with
        # no Earth-validation the strict reality certificate is vacuous.
        from pacland.deficit import deficit_report

        empty = deficit_report([])
        self.assertTrue(empty.vacuous)
        self.assertEqual(empty.radius, inf)


class TestTheEfficiencyHeadline(unittest.TestCase):
    def test_efficiency_numbers_from_the_abstract(self):
        e = efficiency_summary()
        self.assertEqual(SIM_DAYS_PER_MWH, 48)
        self.assertEqual(ENERGY_FACTOR_VS_SCREAM, 50)
        self.assertEqual(SIM_DAYS_PER_WALLCLOCK_DAY, 741)
        self.assertEqual(FLOP_FACTOR_PER_GRIDPOINT, 10)
        self.assertEqual(e["sim_days_per_mwh"], 48)
        self.assertEqual(e["h100_count"], 512)

    def test_efficiency_is_not_fidelity(self):
        # the headline number is a throughput claim against the reference (SCREAM),
        # not a fidelity claim against the Earth
        self.assertIn("throughput", efficiency_summary()["verdict"])


if __name__ == "__main__":
    unittest.main()
