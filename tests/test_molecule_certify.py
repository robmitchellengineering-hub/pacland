"""The molecule certificate: H2's ground energy, from integrals to a value that matches FCI."""
import json
import tempfile
import unittest
from pathlib import Path

from pacland import molecule_certify as mc

try:
    import openfermion  # noqa: F401
    import pyscf  # noqa: F401
    _HAVE_DEPS = True
except ImportError:
    _HAVE_DEPS = False


@unittest.skipUnless(_HAVE_DEPS, "pyscf/openfermion not installed (optional chemistry deps)")
class TestMoleculeCertificate(unittest.TestCase):
    def _cert(self):
        d = Path(tempfile.mkdtemp())
        cert_path = d / "h2.json"
        cert = mc.certify(str(cert_path))
        return cert_path, cert

    def test_certify_writes_a_valid_certificate(self):
        _, cert = self._cert()
        self.assertEqual(cert["format"], "pacland/molecule-certificate@1")
        self.assertEqual(cert["molecule"]["name"], "H2")
        self.assertEqual(cert["molecule"]["n_qubits"], 4)
        self.assertEqual(cert["hamiltonian"]["n_terms"], 15)

    def test_energy_matches_fci(self):
        _, cert = self._cert()
        self.assertLess(abs(cert["result"]["energy"] - cert["result"]["reference_energy"]), 1e-10)

    def test_verify_accepts(self):
        cert_path, _ = self._cert()
        v = mc.verify(str(cert_path))
        self.assertTrue(v["ok"], v["failures"])

    def test_forged_energy_is_refused(self):
        cert_path, _ = self._cert()
        data = json.loads(cert_path.read_text())
        data["result"]["energy"] += 0.1  # forge a lower energy than the pipeline actually gives
        cert_path.write_text(json.dumps(data))
        v = mc.verify(str(cert_path))
        self.assertFalse(v["ok"])
        self.assertTrue(any("reproducibility" in m for m in v["failures"]))


if __name__ == "__main__":
    unittest.main()
