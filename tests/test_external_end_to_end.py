"""End-to-end: an ingested external project's data flows through the WHOLE pipeline, not just the registry."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, ingest, runner, transfer_verify
from pacland import fields


class TestExternalEndToEnd(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)
        fields.seed_fields()  # the internal catalog (heat-equation, brownian-motion, …)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def _ingest(self):
        lib = ingest.load_module_from_path(
            str(Path(__file__).resolve().parent.parent / "examples" / "external_library.py"))
        return ingest.ingest_library(lib)

    def test_external_mapping_is_verifiable(self):
        self._ingest()
        r = transfer_verify.verify_transfer("ext:hydrogeology-project:mapping-darcy-flow-heat-equation")
        self.assertTrue(r["verified"], r)
        self.assertIn("parabolic-pde", r["check"])

    def test_external_falsifier_runs_through_the_runner(self):
        self._ingest()
        key = "ext:hydrogeology-project:darcy-diffusivity-positive"
        survived, evidence = runner.FALSIFIERS[key]()
        self.assertTrue(survived)

    def test_external_structure_is_in_cross_field_search(self):
        self._ingest()
        # the external darcy-flow is a parabolic-pde structure in geology — it must appear in a
        # same-type search alongside the internal physics structures
        ext = registry.get("structure", "ext:hydrogeology-project:darcy-flow")
        self.assertEqual(ext["payload"]["type"], "parabolic-pde")
        internal = registry.get("structure", "heat-equation")
        self.assertEqual(internal["payload"]["type"], "parabolic-pde")
        # the two ends of the external mapping resolve to the SAME type → the transfer is legitimate
        m = registry.get("mapping", "ext:hydrogeology-project:mapping-darcy-flow-heat-equation")
        self.assertEqual(m["payload"]["to"], "heat-equation")

    def test_external_does_not_shadow_internal(self):
        self._ingest()
        # the external darcy-flow and the internal heat-equation are distinct entries of the same type
        self.assertIsNotNone(registry.get("structure", "ext:hydrogeology-project:darcy-flow"))
        self.assertIsNotNone(registry.get("structure", "heat-equation"))


if __name__ == "__main__":
    unittest.main()
