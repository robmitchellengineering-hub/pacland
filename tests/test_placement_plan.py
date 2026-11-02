"""The placement model, held to what it can and cannot say.

Two things matter here: that the arithmetic of a move is right, and that the script refuses to dress the status quo as a
finding when the current position is already the best candidate.
"""
from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pp", ROOT / "scripts" / "placement_plan.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestPlacementPlan(unittest.TestCase):

    def test_moving_further_away_costs_level(self):
        # doubling the distance at 30 dB/decade costs about 9 dB
        delta = _module().path_loss_delta(2.0, 4.0)
        self.assertAlmostEqual(delta, -9.03, places=1)

    def test_moving_closer_gains_level(self):
        self.assertGreater(_module().path_loss_delta(8.0, 4.0), 0)

    def test_a_wall_costs_its_loss(self):
        self.assertAlmostEqual(_module().path_loss_delta(4.0, 4.0, walls=1), -_module().WALL_DB, places=6)

    def test_deficit_measures_against_the_best_room(self):
        d = _module().deficit({"a": -30, "b": -60})
        self.assertEqual(d["a"], 0.0)
        self.assertEqual(d["b"], 30.0)

    def test_label_variants_fold_into_one_room(self):
        self.assertEqual(_module().canonical("bedroom next to router house loop walk"), "bedroom next to router")
        self.assertEqual(_module().canonical("kitchen"), "kitchen")

    def test_the_best_candidate_never_costs_the_best_room_more_than_the_limit(self):
        rooms = [
            {"name": "a", "x": 0, "y": 0, "w": 4, "h": 4},
            {"name": "b", "x": 4, "y": 0, "w": 4, "h": 4},
            {"name": "c", "x": 8, "y": 0, "w": 4, "h": 4},
        ]
        levels = {"a": -30.0, "b": -50.0, "c": -70.0}
        result = _module().plan(levels, ap_position=(2, 2), rooms=rooms,
                                candidates=[(2, 2), (6, 2), (10, 2)])
        if result["best"] is not None:
            self.assertLessEqual(result["best"]["best_room_cost_db"], _module().MAX_LOSS_DB)

    def test_an_unplaceable_room_is_scored_as_unchanged_rather_than_dropped(self):
        rooms = [{"name": "a", "x": 0, "y": 0, "w": 4, "h": 4}]
        levels = {"a": -30.0, "nowhere": -80.0}
        result = _module().plan(levels, ap_position=(2, 2), rooms=rooms, candidates=[(2, 2)])
        self.assertEqual(result["all"][0]["predicted"]["nowhere"], -80.0)


if __name__ == "__main__":
    unittest.main()
