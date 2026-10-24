"""Trust board — guards the per-model scoring and the trusted set.

Known answers (full 53-model Zelinka table, sensitivity_tier fixed to both
bounds of the IPCC likely range 2.5-4.0 K), after the conservation-widening:
- board() scores 53 models.
- 44 have conservation data (17 Irving 3-ledger + 27 widened energy-only).
- 15 pass sensitivity + forcing.
- 6 are trusted: the widened (raw second-source) energy drift drops 22 more
  models; this is flagged preliminary until cross-validated.
"""
import unittest

from pacland.climate.trust_board import board, summary, trusted


class TestTrustBoard(unittest.TestCase):
    def test_board_scores_53(self):
        self.assertEqual(len(board()), 53)

    def test_44_have_conservation_data(self):
        with_drift = [r for r in board() if r["ledgers_failed"] is not None]
        self.assertEqual(len(with_drift), 44)

    def test_27_widened_energy_only(self):
        widened = [r for r in board() if r.get("conservation_scope") == "energy-only (widened)"]
        self.assertEqual(len(widened), 27)

    def test_15_pass_sensitivity_and_forcing(self):
        sf = [r for r in board()
              if "sensitivity" not in r["axes_failed"] and "forcing" not in r["axes_failed"]]
        self.assertEqual(len(sf), 15)

    def test_trusted_is_6(self):
        self.assertEqual(len(trusted()), 6)

    def test_conservation_drops_mpi_esm1_2_hr(self):
        # passes sensitivity + forcing, but leaks one ledger -> not trusted
        self.assertNotIn("MPI-ESM1-2-HR", trusted())

    def test_lower_bound_excludes_low_ecs_models(self):
        # the sensitivity_tier fix: below-2.5-K models must not be trusted
        self.assertNotIn("GISS-E2-2-G", trusted())
        self.assertNotIn("NorESM2-MM", trusted())

    def test_trusted_is_multi_family(self):
        import re
        fams = {re.split(r"\d", m)[0].rstrip("-") for m in trusted()}
        self.assertGreaterEqual(len(fams), 4)

    def test_summary_flags_the_caveat(self):
        self.assertIn("RAW second-source", summary())


if __name__ == "__main__":
    unittest.main()
