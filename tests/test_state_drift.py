"""The committed live-state files cannot drift from the code.

Regenerates the delivery status from the code and fails if the committed
``web/delivery-status.json`` differs — so a code change that makes the state stale is caught by the
suite (the CI gate), not by a reader of the site.
"""
import json
import unittest

from pacland.delivery_status import live_status, REPO


class TestStateDrift(unittest.TestCase):
    def test_delivery_status_matches_code(self):
        committed = json.loads((REPO / "web" / "delivery-status.json").read_text(encoding="utf-8"))
        live = live_status()
        self.assertEqual(
            committed, live,
            "web/delivery-status.json is stale — run `python3 scripts/build_delivery_status.py` "
            "and commit the result")


if __name__ == "__main__":
    unittest.main()
