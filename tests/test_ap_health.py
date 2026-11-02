"""The health table is an INVENTORY, and these tests hold it to that.

The first version had a "suspect" verdict based on the spread of levels across spots. Its own docstring said that if the
suspects turned out to be the APs from the furthest rooms, the metric would be measuring distance rather than health - and
on the first real run the top two suspects were Rob's two working access points. These tests exist so that mistake cannot
come back quietly.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ah", ROOT / "scripts" / "ap_health.py")


def _module():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


def scan(spot: str, *bss):
    return {"spot": spot, "source": f"scan-{spot}", "bss": [
        {"ssid": s, "bssid": f"bss-{s}", "channel": 1, "band": "2.4 GHz", "rssi": r} for s, r in bss
    ]}


class TestApHealth(unittest.TestCase):

    def test_a_working_ap_that_falls_off_with_distance_is_not_flagged(self):
        # the exact case that broke the first version: -30 near, -70 far, and it is FINE
        rows = _module().table([scan("room a", ("home", -30)), scan("room b", ("home", -70))])
        self.assertEqual(rows[0]["verdict"], "heard")
        self.assertEqual(rows[0]["spread"], 40)

    def test_an_ap_quiet_everywhere_is_named(self):
        rows = _module().table([scan("room a", ("dead", -84)), scan("room b", ("dead", -86))])
        self.assertEqual(rows[0]["verdict"], "weak everywhere")

    def test_one_sighting_is_stated_as_one_sighting(self):
        rows = _module().table([scan("room a", ("rare", -40))])
        self.assertEqual(rows[0]["verdict"], "one sighting")
        self.assertEqual(rows[0]["sightings"], 1)

    def test_the_strongest_reading_per_scan_is_the_one_counted(self):
        # the same AP twice in one scan (two radios, same SSID) must not be counted as two sightings
        s = {"spot": "room a", "source": "s1", "bss": [
            {"ssid": "x", "bssid": "same", "channel": 1, "band": "2.4 GHz", "rssi": -70},
            {"ssid": "x", "bssid": "same", "channel": 1, "band": "2.4 GHz", "rssi": -55},
        ]}
        rows = _module().table([s])
        self.assertEqual(rows[0]["sightings"], 1)
        self.assertEqual(rows[0]["best"], -55)

    def test_every_row_carries_where_it_was_loudest_and_quietest(self):
        rows = _module().table([scan("near", ("a", -35)), scan("far", ("a", -75))])
        self.assertEqual(rows[0]["loudest"][0], "near")
        self.assertEqual(rows[0]["quietest"][0], "far")


if __name__ == "__main__":
    unittest.main()
