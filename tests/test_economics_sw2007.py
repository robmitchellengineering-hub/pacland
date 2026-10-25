"""Smets–Wouters (2007) record tests — provenance checks and their seeded faults."""
import unittest

from pacland.economics import sw2007


class TestDerivations(unittest.TestCase):
    def test_beta_from_the_reported_number(self):
        self.assertAlmostEqual(sw2007.beta(), 1 / 1.0016, places=12)

    def test_detrended_discount_factor_is_below_beta(self):
        self.assertLess(sw2007.beta_tilde(), sw2007.beta())

    def test_implied_rates(self):
        self.assertAlmostEqual(sw2007.real_rate_annual_pct(), 3.019, places=3)
        self.assertAlmostEqual(sw2007.inflation_annual_pct(), 3.12, places=6)

    def test_fisher_holds_as_an_identity(self):
        gap = sw2007.nominal_rate_annual_pct() - (
            sw2007.real_rate_annual_pct() + sw2007.inflation_annual_pct()
        )
        self.assertAlmostEqual(gap, 0.0, places=9)

    def test_calvo_slope_from_published_stickiness(self):
        self.assertAlmostEqual(sw2007.calvo_kappa(), 0.1777, places=4)


class TestDeterminacy(unittest.TestCase):
    def test_published_rule_is_determinate(self):
        d = sw2007.determinacy()
        self.assertTrue(d["determinate"])
        self.assertGreater(d["margin"], 0.0)

    def test_boundary_is_near_one_at_the_published_output_response(self):
        d = sw2007.determinacy()
        self.assertAlmostEqual(d["boundary"], 0.9966, places=4)

    def test_smoothing_weakens_the_contemporaneous_response_only(self):
        d = sw2007.determinacy()
        self.assertAlmostEqual(d["contemporaneous_response"], 0.3876, places=4)
        self.assertEqual(d["r_pi"], 2.04)

    def test_scope_is_stated(self):
        self.assertIn("excludes", sw2007.determinacy()["scope"])


class TestGuards(unittest.TestCase):
    def test_provenance_guard_green(self):
        ok, msg = sw2007.guard_provenance_consistency()
        self.assertTrue(ok, msg)
        self.assertIn("worst gap", msg)

    def test_provenance_guard_red_on_a_transcription_error(self):
        saved = dict(sw2007.PUBLISHED_STRUCTURAL)
        try:
            sw2007.PUBLISHED_STRUCTURAL["tau"] = 0.63   # would imply a ~5.7% real rate
            ok, msg = sw2007.guard_provenance_consistency()
        finally:
            sw2007.PUBLISHED_STRUCTURAL.clear()
            sw2007.PUBLISHED_STRUCTURAL.update(saved)
        self.assertFalse(ok)
        self.assertIn("provenance", msg)

    def test_determinacy_guard_red_on_a_passive_rule(self):
        ok, msg = sw2007.guard_determinacy(r_pi=0.5)
        self.assertFalse(ok)
        self.assertIn("INDETERMINATE", msg)

    def test_observation_set_is_seven(self):
        ok, msg = sw2007.guard_observation_set()
        self.assertTrue(ok, msg)


class TestDeficit(unittest.TestCase):
    def test_ceiling_is_seven_observables(self):
        ceiling, _ = sw2007.deficit()
        self.assertEqual(ceiling.n_validation, 7)

    def test_ceiling_radius(self):
        ceiling, _ = sw2007.deficit(0.025)
        self.assertAlmostEqual(ceiling.radius, 0.513, places=3)

    def test_out_of_sample_is_vacuous(self):
        _, oos = sw2007.deficit()
        self.assertEqual(oos.n_validation, 0)
        self.assertTrue(oos.vacuous)

    def test_in_sample_count_is_the_published_seven(self):
        self.assertEqual(sw2007.IN_SAMPLE_VALIDATED, 7)


class TestPublishedRecord(unittest.TestCase):
    def test_the_benchmark_is_a_var_not_a_random_walk(self):
        # the honest correction: SW's table favours the DSGE against a VAR(1), and does
        # not contain the no-change null at all.
        rec = sw2007.out_of_sample_vs_random_walk()
        self.assertEqual(rec["benchmark"], "VAR(1)")
        self.assertFalse(rec["random_walk_present"])

    def test_dsge_gains_are_positive_at_every_horizon(self):
        rec = sw2007.out_of_sample_vs_random_walk()
        self.assertTrue(rec["dsge_beats_var1_at_every_horizon"])
        for h, gain in sw2007.PUBLISHED_OUT_OF_SAMPLE["DSGE"].items():
            self.assertGreater(gain, 0.0, f"horizon {h}")

    def test_published_numbers_are_recorded_verbatim(self):
        self.assertEqual(sw2007.PUBLISHED_OUT_OF_SAMPLE["DSGE"][12], 13.51)
        self.assertEqual(sw2007.PUBLISHED_OUT_OF_SAMPLE["BVAR(4)"][12], -9.84)

    def test_source_names_the_tables(self):
        self.assertIn("Tables 1a/1b", sw2007.SOURCE)
        self.assertIn("Table 3", sw2007.SOURCE)

    def test_summary_states_the_untested_null(self):
        self.assertIn("VAR(1)", sw2007.summary())


if __name__ == "__main__":
    unittest.main()
