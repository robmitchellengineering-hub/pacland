"""Provisional placement: sizes measured, positions guessed, and the guess is labelled.

The danger this guards is not a wrong number - it is a provisional layout being mistaken for a floor plan, so the tests
check the LABEL as much as the arithmetic.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pr", ROOT / "scripts" / "place_rooms.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestPlaceRooms(unittest.TestCase):

    def setUp(self):
        self.rooms = [
            {"name": "a", "w": 3.0, "h": 2.5},
            {"name": "b", "w": 2.0, "h": 2.5},
            {"name": "c", "w": None, "h": None},
        ]

    def test_unmeasured_rooms_are_not_placed(self):
        placed = _module().place(self.rooms)
        self.assertEqual([r["name"] for r in placed], ["a", "b"])
        # an unmeasured room is not touched at all, rather than being given a position with no size behind it
        self.assertNotIn("x", self.rooms[2])

    def test_placed_rooms_touch_and_do_not_overlap(self):
        placed = _module().place(self.rooms)
        a, b = placed
        self.assertEqual(a["x"] + a["w"], b["x"], "rooms share a wall")
        self.assertEqual(a["y"], b["y"], "same shelf")

    def test_every_placed_room_is_labelled_provisional(self):
        for r in _module().place(self.rooms):
            self.assertEqual(r["placement"], "provisional")

    def test_it_wraps_to_a_new_shelf_instead_of_running_off(self):
        rooms = [{"name": f"r{i}", "w": 5.0, "h": 3.0} for i in range(4)]
        placed = _module().place(rooms)
        self.assertLessEqual(max(r["x"] + r["w"] for r in placed), _module().SHELF_WIDTH)
        self.assertGreater(max(r["y"] for r in placed), 0.0, "four 5 m rooms cannot fit on one shelf")

    def test_a_layout_with_nothing_measured_reports_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "l.json"
            p.write_text(json.dumps({"rooms": [{"name": "a", "w": None, "h": None}]}))
            before = p.read_text()
            self.assertEqual(_module().main(["x", "--layout", str(p), "--write"]), 0)
            self.assertEqual(p.read_text(), before)

    def test_write_records_positions_and_the_provisional_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "l.json"
            p.write_text(json.dumps({"rooms": [{"name": "a", "w": 3.0, "h": 2.5}]}))
            _module().main(["x", "--layout", str(p), "--write"])
            out = json.loads(p.read_text())
            self.assertEqual(out["rooms"][0]["x"], 0.0)
            self.assertIn("PROVISIONAL", out["_note"])


if __name__ == "__main__":
    unittest.main()
