"""The competing-programmes structure: four tracks, the A1-A5 metric, and the leaderboard."""
import unittest

from pacland import research_program as rp


class TestResearchProgram(unittest.TestCase):
    def test_four_tracks_are_present(self):
        self.assertEqual({t.id for t in rp.TRACKS}, {"gribov", "coulomb", "rg", "curvature"})

    def test_each_track_bets_on_different_assumptions(self):
        # the heavy-lifting assumptions are what distinguish the tracks — they must not be identical
        bets = {t.id: set(t.heavy_lifting) for t in rp.TRACKS}
        self.assertNotEqual(bets["gribov"], bets["coulomb"])
        self.assertNotEqual(bets["coulomb"], bets["rg"])
        self.assertNotEqual(bets["rg"], bets["curvature"])

    def test_track_score_counts_cleared_assumptions(self):
        # coulomb must clear A1, A3, A4; clearing all three = score 3
        self.assertEqual(rp.track_score("coulomb", {"A1", "A3", "A4"}), 3)
        self.assertEqual(rp.track_score("coulomb", {"A4"}), 1)

    def test_leaderboard_ranks_closest_first(self):
        lb = rp.leaderboard({"coulomb": {"A1", "A3", "A4"}, "gribov": {"A4"}})
        self.assertEqual(lb[0]["track"], "coulomb")  # 3/3 beats 1/2
        self.assertEqual(lb[0]["cleared"], 3)
        self.assertEqual(lb[0]["of"], 3)

    def test_report_names_the_leader(self):
        r = rp.report({"coulomb": {"A1", "A3", "A4"}, "rg": {"A1"}})
        self.assertEqual(r["leader"], "coulomb")
        self.assertTrue(r["any_full"])  # coulomb is 3/3 = full

    def test_missing_assumptions_are_reported(self):
        lb = rp.leaderboard({"coulomb": {"A4"}})
        self.assertIn("A1", lb[0]["missing"])
        self.assertIn("A3", lb[0]["missing"])


if __name__ == "__main__":
    unittest.main()
