"""The Lean-repo and CSV adapters: external theorems and tabular data land as registry entries."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, ingest


EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


class TestExternalAdapters(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_lean_repo_theorems_land_as_tier1_properties(self):
        out = ingest.ingest_lean_repo(str(EXAMPLES / "external_lean"), source="geo-lean")
        self.assertEqual(out["lean_theorems"], 2)
        p = registry.get("property", "ext:geo-lean:lean-darcy_flow_conservation")
        self.assertEqual(p["payload"]["tier"], 1)
        self.assertEqual(p["provenance"]["source"], "geo-lean")

    def test_csv_rows_land_as_evidence(self):
        out = ingest.ingest_csv(str(EXAMPLES / "external_data.csv"), source="geo-data")
        self.assertEqual(out["rows"], 2)
        e = registry.get("evidence", "ext:geo-data:evidence-0")
        self.assertEqual(e["payload"]["dataset"], "Theis 1935")
        self.assertEqual(e["provenance"]["method"], "csv")

    def test_csv_kind_is_configurable(self):
        ingest.ingest_csv(str(EXAMPLES / "external_data.csv"), source="geo-data", kind="property")
        self.assertIsNotNone(registry.get("property", "ext:geo-data:property-0"))


if __name__ == "__main__":
    unittest.main()
