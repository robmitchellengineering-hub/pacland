"""The trust board — aggregation across disciplines."""
import unittest

from pacland.trust import board, summary


class TestTrustBoard(unittest.TestCase):
    def test_board_counts(self):
        s = summary()
        self.assertEqual(s["n_artifacts"], 29)
        self.assertEqual(s["n_broken"], 7)
        self.assertEqual(s["n_weak"], 11)
        self.assertEqual(s["n_clean"], 11)

    def test_broken_are_the_double_flagged(self):
        broken = summary()["broken"]
        self.assertIn("CMIP6 CNRM-ESM2-1", broken)
        self.assertIn("CMIP6 UKESM1-0-LL", broken)
        self.assertEqual(len(broken), 7)

    def test_clean_are_the_giss_family(self):
        clean = [e.artifact for e in board()
                 if e.tier == "clean" and e.discipline == "climate"]
        self.assertEqual(sorted(clean), ["CMIP6 GISS-E2-1-G", "CMIP6 GISS-E2-1-G-CC"])

    def test_e3sm_is_weak_not_clean(self):
        e = next(e for e in board() if e.artifact == "CMIP6 E3SM-1-1")
        self.assertEqual(e.tier, "weak")  # clean but hot

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
