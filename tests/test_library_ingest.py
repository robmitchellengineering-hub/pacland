"""External LIBRARY integration — a Python module's CONTRIBUTION + FALSIFIERS become usable by the engine."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, ingest, runner


class TestLibraryIngest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def _sample(self):
        return ingest.load_module_from_path(
            str(Path(__file__).resolve().parent.parent / "examples" / "external_library.py"))

    def test_library_contribution_ingests(self):
        out = ingest.ingest_library(self._sample())
        self.assertIn("contribution", out)
        self.assertIsNotNone(registry.get("structure", "ext:hydrogeology-project:darcy-flow"))

    def test_library_falsifiers_registered_in_runner(self):
        out = ingest.ingest_library(self._sample())
        self.assertEqual(out["falsifiers"], 2)
        key = "ext:hydrogeology-project:darcy-diffusivity-positive"
        self.assertIn(key, runner.FALSIFIERS)
        survived, evidence = runner.FALSIFIERS[key]()
        self.assertTrue(survived)

    def test_library_falsifier_recorded_as_evidence(self):
        ingest.ingest_library(self._sample())
        ev = registry.get("evidence", "ext:hydrogeology-project:evidence-darcy-diffusivity-positive")
        self.assertIsNotNone(ev)
        self.assertEqual(ev["provenance"]["source"], "hydrogeology-project")


if __name__ == "__main__":
    unittest.main()
