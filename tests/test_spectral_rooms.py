"""Room modes: Weyl's law as an oracle, and the correction verified away from the seat it was tuned at."""
import unittest

from pacland.spectral import rooms as R


class TestWeyl(unittest.TestCase):
    def test_the_box_mode_count_matches_weyl_with_the_surface_term(self):
        for box in ((6.0, 4.5, 3.0), (5.0, 5.0, 2.5), (8.0, 3.0, 2.8)):
            w = R.weyl_convergence(*box)
            self.assertTrue(w["pass"], (box, w["verdict"]))
            self.assertLess(abs(w["final_error"]), 1e-2)

    def test_it_converges_rather_than_sitting_still(self):
        w = R.weyl_convergence(6.0, 4.5, 3.0)
        errors = [abs(r["error"]) for r in w["rows"]]
        self.assertLess(errors[-1], errors[0])

    def test_degeneracies_are_many_and_are_collapsed(self):
        raw = R.box_modes(6.0, 4.5, 3.0, 2000.0)
        d = R.distinct(raw)
        self.assertGreater(len(raw) - len(d), 10000)      # 62,075 measured
        self.assertTrue(all(b - a > 0 for a, b in zip(d, d[1:])))


class TestCorrection(unittest.TestCase):
    def test_the_correction_reduces_ripple_at_the_tuned_seat(self):
        r = R.correction_report(6.0, 4.5, 3.0, (2.0, 1.5, 1.2))
        self.assertTrue(r["pass"])
        self.assertGreater(r["improvement_db"], 3.0)
        self.assertLess(r["max_gain_db"], 13.0)          # bounded boost
        self.assertGreater(r["min_gain_db"], -19.0)

    def test_single_point_eq_is_seat_specific(self):
        r = R.spatial_report(6.0, 4.5, 3.0, (2.0, 1.5, 1.2),
                             [(1.0, 3.0, 2.0), (3.0, 2.2, 1.6), (4.5, 1.0, 0.9)])
        self.assertTrue(r["single_helps_tuned"])
        # the tuned seat improves far more than the worst other seat: the fix does not travel
        tuned = r["rows"][0]["single_delta"]
        worst = max(row["single_delta"] for row in r["rows"][1:])
        self.assertLess(tuned, worst)

    def test_multi_point_eq_helps_the_whole_room(self):
        r = R.spatial_report(6.0, 4.5, 3.0, (2.0, 1.5, 1.2),
                             [(1.0, 3.0, 2.0), (3.0, 2.2, 1.6), (4.5, 1.0, 0.9)])
        self.assertTrue(r["multi_helps_all"], r["verdict"])


if __name__ == "__main__":
    unittest.main()
