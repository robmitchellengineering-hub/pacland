"""The chemistry certificate is reproducible to tolerance and refuses a tampered result."""
import json
import tempfile
import unittest
from pathlib import Path

from pacland import chemistry_certify as cc


class TestChemistryCertificate(unittest.TestCase):
    def _cert(self, sites=24, dims=(8, 16, 32)):
        d = Path(tempfile.mkdtemp())
        cert_path = d / "chem.json"
        cert = cc.certify(sites, list(dims), str(cert_path))
        return d, cert_path, cert

    def test_certify_writes_a_valid_certificate(self):
        _, cert_path, cert = self._cert()
        self.assertEqual(cert["format"], "pacland/chemistry-certificate@1")
        self.assertEqual(cert["model"]["name"], "heisenberg-chain")
        self.assertEqual(len(cert["sweep"]), 3)
        self.assertTrue(cert["convergence"]["sufficient"])

    def test_verify_accepts_a_fresh_certificate(self):
        _, cert_path, _ = self._cert()
        v = cc.verify(str(cert_path))
        self.assertTrue(v["ok"], v["failures"])

    def test_tampered_certificate_is_refused(self):
        _, cert_path, cert = self._cert()
        data = json.loads(cert_path.read_text())
        data["sweep"][-1]["energy"] += 1.0  # forge the converged energy
        cert_path.write_text(json.dumps(data))
        v = cc.verify(str(cert_path))
        self.assertFalse(v["ok"])
        self.assertTrue(any("reproducibility" in m for m in v["failures"]))

    def test_sweep_converges_toward_the_bethe_reference(self):
        _, _, cert = self._cert(sites=40, dims=(10, 20, 40, 80))
        per_site = cert["sweep"][-1]["energy_per_site"]
        exact = cert["exact_reference"]["value_per_site"]
        # finite-L energy sits above the infinite-chain value, within ~1%
        self.assertLess(abs(per_site - exact), 0.01)


if __name__ == "__main__":
    unittest.main()
