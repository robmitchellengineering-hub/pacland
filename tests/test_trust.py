"""The trust board — aggregation across disciplines."""
import unittest

from pacland.trust import board, summary


class TestTrustBoard(unittest.TestCase):
    def test_board_counts(self):
        s = summary()
        self.assertEqual(s["n_artifacts"], 29)
        self.assertEqual(s["n_broken"], 5)
        self.assertEqual(s["n_weak"], 10)
        self.assertEqual(s["n_clean"], 14)

    def test_broken_are_the_multi_ledger_leakers(self):
        broken = summary()["broken"]
        self.assertIn("CMIP6 BCC-ESM1", broken)        # fails all three ledgers
        self.assertIn("CMIP6 CNRM-ESM2-1", broken)
        self.assertIn("CMIP6 CNRM-CM6-1", broken)
        self.assertEqual(len(broken), 5)

    def test_board_orders_broken_first(self):
        es = board()
        self.assertEqual(es[0].tier, "broken")
        self.assertEqual(es[1].tier, "broken")
        # clean entries come last
        self.assertEqual(es[-1].tier, "clean")

    def test_every_entry_has_evidence(self):
        for e in board():
            self.assertTrue(e.evidence.strip(), e.artifact)


if __name__ == "__main__":
    unittest.main()
