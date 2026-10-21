"""The trust board — aggregation across disciplines."""
import unittest

from pacland.trust import board, summary


class TestTrustBoard(unittest.TestCase):
    def test_board_counts(self):
        s = summary()
        self.assertEqual(s["n_artifacts"], 26)
        self.assertEqual(s["n_broken"], 2)
        self.assertEqual(s["n_weak"], 10)
        self.assertEqual(s["n_clean"], 14)

    def test_broken_are_the_two_cnrm_models(self):
        self.assertEqual(summary()["broken"],
                         ["CMIP6 CNRM-ESM2-1", "CMIP6 CNRM-CM6-1"])

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
