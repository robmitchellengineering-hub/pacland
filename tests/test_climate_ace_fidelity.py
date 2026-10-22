"""ACE worked example — guards the headline numbers so the report cannot drift.

Known answers, from arXiv:2310.02074 Table 1 + Appendix E:
- 44 output channels = 34 prognostic + 10 diagnostic.
- 41/44 (~93%) beat the baseline — and that is model-vs-model (reference-fidelity).
- reality-fidelity m: anchor = 2 (GMST + EEI), generous = 3 (+ surface pressure),
  strict = 0 (ACE is validated against no Earth observation -> vacuous).
- radius_e(m) at delta_e = 0.025: m=2 -> ~0.960, m=3 -> ~0.784.
"""
import unittest
from math import inf

from pacland.climate.ace_fidelity import (
    ACE_OUTPUT_CHANNELS,
    N_BEATS_BASELINE,
    anchor_deficit,
    channel_summary,
    reality_deficit,
)


class TestAceChannels(unittest.TestCase):
    def test_output_channel_count_is_44(self):
        cs = channel_summary()
        self.assertEqual(cs["n_outputs"], 44)
        self.assertEqual(cs["n_prognostic"], 34)
        self.assertEqual(cs["n_diagnostic"], 10)

    def test_3d_fields_carry_8_layers(self):
        three_d = {c.symbol: c.n_layers for c in ACE_OUTPUT_CHANNELS if c.n_layers > 1}
        self.assertEqual(set(three_d), {"T_k", "q^T_k", "u_k", "v_k"})
        self.assertTrue(all(n == 8 for n in three_d.values()))

    def test_beats_baseline_is_41_of_44(self):
        cs = channel_summary()
        self.assertEqual(cs["n_beats_baseline"], N_BEATS_BASELINE)
        self.assertEqual(cs["n_beats_baseline"], 41)
        self.assertAlmostEqual(cs["reference_fidelity_pct"], 41 / 44, places=6)
        # the abstract's "over 90%" claim is this 93.2% — a model-vs-model number
        self.assertGreater(cs["reference_fidelity_pct"], 0.90)


class TestAceRealityFidelity(unittest.TestCase):
    def test_anchor_m_is_2(self):
        a = anchor_deficit()
        self.assertEqual(a.n_validation, 2)      # GMST + EEI only
        self.assertEqual(a.n_unverifiable, 2)    # OHC + GMSL absent (atmosphere-only)
        self.assertAlmostEqual(a.radius, 0.960, places=3)

    def test_generous_m_is_3(self):
        r = reality_deficit()
        self.assertEqual(r.n_validation, 3)      # GMST + EEI + surface pressure
        self.assertAlmostEqual(r.radius, 0.784, places=3)

    def test_reality_radius_exceeds_the_claimed_skill(self):
        # Even the most generous reality-fidelity radius (~78% tolerance) is a
        # *tolerance* on 3 observables, not the ">90% skillful" reference claim —
        # and the anchor radius (~96%) is worse. The point: the reference-fidelity
        # number is not a reality certificate.
        r = reality_deficit()
        self.assertGreater(r.radius, 0.78)
        self.assertLess(r.radius, 0.79)

    def test_strict_tier_is_vacuous(self):
        # ACE's own paper scores it against FV3GFS, never against the Earth, so
        # with no Earth-validation the strict reality certificate is vacuous.
        self.assertEqual(anchor_deficit().n_unverifiable, 2)
        # an empty validation set -> infinite radius (the strict m = 0 tier)
        from pacland.deficit import deficit_report
        empty = deficit_report([])
        self.assertTrue(empty.vacuous)
        self.assertEqual(empty.radius, inf)


if __name__ == "__main__":
    unittest.main()
