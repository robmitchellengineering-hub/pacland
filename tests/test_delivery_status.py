"""The delivery status doc cannot drift from the code.

The stale "supervisor to build" / "model still training" cells in TOOL-SEXTANT-DELIVERY.md were
quoted as truth. This test pins the doc to the live check so that can't happen again: if a component
is built in the code but the doc still says "to build" / "still training", the test fails.
"""
import unittest

from pacland.delivery_status import live_status, REPO

STALE_MARKERS = ("to build", "still training", "training not finished", "not finished")


class TestDeliveryStatus(unittest.TestCase):
    def test_all_bundle_components_are_built(self):
        status = live_status()
        for component, info in status.items():
            if component.startswith("_"):
                continue
            self.assertTrue(info["built"], f"{component} is not fully built: missing {info['missing']}")

    def test_doc_does_not_mark_a_built_component_as_to_build(self):
        doc = (REPO / "docs" / "TOOL-SEXTANT-DELIVERY.md").read_text(encoding="utf-8")
        status = live_status()
        built = [c for c, i in status.items() if not c.startswith("_") and i["built"]]
        for line in doc.splitlines():
            low = line.lower()
            if any(m in low for m in STALE_MARKERS):
                # if the line names a built component, it's the stale pattern
                for component in built:
                    if component.replace("-", " ") in low or component in low:
                        self.fail(
                            f"stale marker in the delivery doc for a built component "
                            f"({component}): {line.strip()!r}")
