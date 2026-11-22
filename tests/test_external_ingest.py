"""External data integration — other people's data lands in the same registry, namespaced + auditable."""
import json
import tempfile
import unittest
from pathlib import Path

from pacland import registry, ingest


CONTRIBUTION = {
    "source": "hydro-project",
    "description": "a test contribution",
    "domain": "geology",
    "structures": [{"id": "aquifer", "type": "conservation", "definition": "water mass balance"}],
    "properties": [{"id": "darcy-law", "statement": "q = -K grad h", "tier": 1}],
    "evidence": [{"id": "pumping-test", "test": "tests/test_darcy.py"}],
    "mappings": [{"from": "aquifer", "to": "heat-equation", "mapping": "flow is diffusion"}],
}


class TestExternalIngest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_external_structures_land_namespaced(self):
        n = ingest.ingest_external(CONTRIBUTION)
        self.assertEqual(n["structures"], 1)
        self.assertIsNotNone(registry.get("structure", "ext:hydro-project:aquifer"))
        # the raw id is NOT used — external data cannot collide with the internal catalog
        self.assertIsNone(registry.get("structure", "aquifer"))

    def test_external_mapping_resolves_own_structure_and_keeps_internal(self):
        ingest.ingest_external(CONTRIBUTION)
        m = registry.get("mapping", "ext:hydro-project:mapping-aquifer-heat-equation")
        self.assertIsNotNone(m)
        self.assertEqual(m["payload"]["from"], "ext:hydro-project:aquifer")
        self.assertEqual(m["payload"]["to"], "heat-equation")  # internal structure kept as-is

    def test_provenance_records_the_source(self):
        ingest.ingest_external(CONTRIBUTION)
        s = registry.get("structure", "ext:hydro-project:aquifer")
        self.assertEqual(s["provenance"]["produced_by"], "external")
        self.assertEqual(s["provenance"]["source"], "hydro-project")

    def test_external_does_not_overwrite_internal(self):
        # seed an internal structure with the SAME raw id, then ingest external — both survive
        registry.add(registry.Entry(id="aquifer", kind="structure",
                                    payload={"type": "conservation"}, provenance={"produced_by": "internal"}))
        ingest.ingest_external(CONTRIBUTION)
        self.assertIsNotNone(registry.get("structure", "aquifer"))               # internal untouched
        self.assertIsNotNone(registry.get("structure", "ext:hydro-project:aquifer"))  # external present

    def test_sample_file_ingests(self):
        sample = Path(__file__).resolve().parent.parent / "examples" / "external-contribution.json"
        if not sample.exists():
            self.skipTest("sample file not present")
        n = ingest.ingest_external(json.loads(sample.read_text()))
        self.assertGreaterEqual(n["structures"], 2)
        self.assertGreaterEqual(n["mappings"], 1)


if __name__ == "__main__":
    unittest.main()
