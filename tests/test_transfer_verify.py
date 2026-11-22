"""P1 — generalise transfer verification: any registry mapping is verifiable (or honestly unverified)."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, transfer_verify
from pacland import fields, known_unifications


class TestGeneralisedTransferVerify(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)
        fields.seed_fields()
        registry.seed_known_unifications()   # the specific mappings (heat-diffusion-walk, markov-population, gauge-connection)
        known_unifications.record()

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_specific_checker(self):
        r = transfer_verify.verify_transfer("heat-diffusion-walk")
        self.assertTrue(r["verified"])
        self.assertIn("ratio", r["result"])

    def test_type_checker_markov(self):
        # markov-chain-monte-carlo ↔ wright-fisher share the 'markov' type → spectral-gap invariant
        r = transfer_verify.verify_transfer("markov-population")
        self.assertTrue(r["verified"])
        self.assertIn("spectral gap", r["result"]["invariant"])

    def test_unverifiable_mapping_is_honest(self):
        # gauge-connection has no specific checker and no shared-type checker → UNVERIFIED, not a crash
        r = transfer_verify.verify_transfer("gauge-connection")
        self.assertFalse(r["verified"])
        self.assertEqual(r.get("status"), "unverified")

    def test_unknown_mapping_reports_error(self):
        r = transfer_verify.verify_transfer("does-not-exist")
        self.assertFalse(r["verified"])
        self.assertIn("unknown mapping", r.get("error", ""))

    def test_verifiable_mappings_lists_coverage(self):
        v = transfer_verify.verifiable_mappings()
        self.assertIn("heat-diffusion-walk", v)
        self.assertIn("markov-population", v)


if __name__ == "__main__":
    unittest.main()
