"""Trust board — guards the per-model scoring and the trusted set.

Known answers (full 53-model Zelinka table, sensitivity_tier fixed to both
bounds of the IPCC likely range 2.5-4.0 K):
- board() scores 53 models.
- 17 have conservation drift data.
- 15 pass sensitivity + forcing.
- 14 are trusted (pass every available axis): MPI-ESM1-2-HR is dropped by
  conservation; GISS-E2-2-G (2.43 K) and NorESM2-MM (2.49 K) are excluded by
  the lower-bound fix.
"""
import unittest

from pacland.climate.trust_board import board, summary, trusted


class TestTrustBoard(unittest.TestCase):
    def test_board_scores_53(self):
        self.assertEqual(len(board()), 53)

    def test_17_have_conservation_data(self):
        with_drift = [r for r in board() if r["ledgers_failed"] is not None]
        self.assertEqual(len(with_drift), 17)

    def test_15_pass_sensitivity_and_forcing(self):
        sf = [r for r in board()
              if "sensitivity" not in r["axes_failed"] and "forcing" not in r["axes_failed"]]
        self.assertEqual(len(sf), 15)

    def test_trusted_is_14(self):
        self.assertEqual(len(trusted()), 14)

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
        self.assertGreaterEqual(len(fams), 10)

    def test_summary_mentions_trusted_count(self):
        self.assertIn("trusted (pass all available axes): 14", summary())


if __name__ == "__main__":
    unittest.main()
