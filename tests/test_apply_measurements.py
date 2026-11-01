"""The consumer's REFUSALS are the feature; these tests lock them.

`scripts/apply_measurements.py` turns ARCore measurements into room dimensions. It is easy to write a version that fills
the template eagerly and hard to notice that it has invented a room, so the cases that matter are the ones where it does
NOT write.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("am", ROOT / "scripts" / "apply_measurements.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


def _write_payload(root: Path, name: str, room: str, metres: list[float]) -> None:
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "capability": "measure",
        "room": room,
        "count": len(metres),
        "measurements": [
            {"room": room, "metres": m, "from": [0, 0, 0], "to": [m, 0, 0]} for m in metres
        ],
    }
    (d / "stdout.txt").write_text(json.dumps(payload))


class TestApplyMeasurements(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # A COPY of the template: a test that writes the repository's own layout file is a test with a side effect, and
        # the first version of this file did exactly that.
        self.layout = self.root / "layout.json"
        self.layout.write_text((ROOT / "docs" / "data" / "layout-template.json").read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def test_two_walls_in_one_scan_make_a_room(self):
        # two walls in ONE payload - one session, which is the only way two lengths describe the same room
        _write_payload(self.root, "measure-1", "kitchen", [3.42, 2.61])
        rooms = _module().load_measurements(str(self.root))
        self.assertEqual(len(rooms["kitchen"]), 2)
        pair = _module().room_from_walls(rooms["kitchen"])
        self.assertEqual(pair, (2.61, 3.42))

    def test_one_measurement_is_not_a_room(self):
        _write_payload(self.root, "measure-1", "kitchen", [3.42])
        self.assertEqual(_module().main(["x", "--root", str(self.root)]), 1,
                         "one line cannot describe a room, and saying so is the point")

    def test_a_square_room_is_allowed(self):
        # a square room is 4.0 x 4.0; the duplicate case is caught from the coordinates, not from the lengths
        a = {"metres": 4.0, "from": [0, 0, 0], "to": [4, 0, 0], "source": "s"}
        b = {"metres": 4.0, "from": [0, 0, 0], "to": [0, 0, 4], "source": "s"}
        self.assertEqual(_module().room_from_walls([a, b]), (4.0, 4.0))

    def test_the_same_wall_twice_is_caught_from_the_coordinates(self):
        first = {"from": [0, 0, 0], "to": [3.42, 0, 0]}
        second = {"from": [0, 0, 0.02], "to": [3.41, 0, 0.01]}      # the same wall, tapped again
        reversed_second = {"from": [3.41, 0, 0.01], "to": [0, 0, 0.02]}
        other_wall = {"from": [0, 0, 0], "to": [0, 0, 2.61]}
        self.assertTrue(_module().same_line(first, second))
        self.assertTrue(_module().same_line(first, reversed_second), "direction must not matter")
        self.assertFalse(_module().same_line(first, other_wall))

    def test_a_good_room_and_a_bad_one_refuse_the_whole_file(self):
        _write_payload(self.root, "measure-1", "kitchen", [3.42])
        _write_payload(self.root, "measure-2", "kitchen", [2.61])
        _write_payload(self.root, "measure-3", "hallway", [4.10])
        _write_payload(self.root, "measure-4", "hallway", [4.05])
        self.assertEqual(_module().main(["x", "--root", str(self.root), "--layout", str(self.layout), "--write"]), 1,
                         "the bad room must refuse the write for every room")

    def test_a_label_matches_its_room_despite_case_and_spacing(self):
        rooms = json.loads((ROOT / "docs" / "data" / "layout-template.json").read_text())["rooms"]
        mod = _module()
        self.assertEqual(mod.resolve_room("Kitchen", rooms), "kitchen")
        self.assertEqual(mod.resolve_room("  kitchen  ", rooms), "kitchen")
        self.assertEqual(mod.resolve_room("the kitchen", rooms), "kitchen")

    def test_an_unrelated_label_is_not_forced_onto_a_room(self):
        rooms = json.loads((ROOT / "docs" / "data" / "layout-template.json").read_text())["rooms"]
        self.assertIsNone(_module().resolve_room("garage", rooms))

    def test_a_mismatched_label_refuses_the_write_and_says_so(self):
        _write_payload(self.root, "measure-1", "garage", [3.42])
        _write_payload(self.root, "measure-2", "garage", [2.61])
        result = _module().main(["x", "--root", str(self.root), "--layout", str(self.layout), "--write"])
        self.assertEqual(result, 1, "an unmatched room must not be written silently")

    def test_two_walls_from_different_sessions_are_not_a_room(self):
        # ARCore's world coordinates are relative to the session, so lengths from two scans are unrelated numbers - they
        # might even be the same wall. This must refuse rather than multiply two guesses together.
        _write_payload(self.root, "measure-a", "kitchen", [4.15])
        _write_payload(self.root, "measure-b", "kitchen", [4.73])
        result = _module().main(["x", "--root", str(self.root), "--layout", str(self.layout), "--write"])
        self.assertEqual(result, 1)

    def test_nothing_on_the_hub_is_not_an_error(self):
        self.assertEqual(_module().main(["x", "--root", str(self.root)]), 0)

    def test_a_corrupt_payload_in_the_directory_does_not_stop_the_others(self):
        bad = self.root / "measure-bad"
        bad.mkdir()
        (bad / "stdout.txt").write_text("{not json")
        _write_payload(self.root, "measure-1", "kitchen", [3.42])
        rooms = _module().load_measurements(str(self.root))
        self.assertEqual(list(rooms), ["kitchen"])


if __name__ == "__main__":
    unittest.main()
