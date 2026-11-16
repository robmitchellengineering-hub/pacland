"""The quantum certificate is reproducible, tamper-evident, and refuses a wrong answer."""
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from pacland import quantum_certify as qc


class TestQuantumCertificate(unittest.TestCase):
    def _cert(self, program="ghz", n=8):
        d = Path(tempfile.mkdtemp())
        cert_path = d / "cert.json"
        cert = qc.certify(program, n, str(cert_path))
        return d, cert_path, cert

    def test_certify_writes_a_valid_certificate(self):
        _, cert_path, cert = self._cert()
        self.assertEqual(cert["format"], "pacland/quantum-certificate@1")
        self.assertEqual(cert["circuit"]["program"], "ghz")
        self.assertEqual(cert["evidence"]["max_bond_dim"], 2)  # GHZ is area-law
        data = json.loads(cert_path.read_text())
        self.assertEqual(data["result"]["sha256"], cert["result"]["sha256"])

    def test_integrity_re_run_accepts(self):
        _, cert_path, _ = self._cert()
        v = qc.verify(str(cert_path))
        self.assertTrue(v["ok"], v["failures"])

    def test_forged_uniform_claim_is_refused(self):
        d, cert_path, cert = self._cert("ghz", 8)
        n = 2 ** 8
        claim = d / "forged.json"
        claim.write_text(json.dumps({"probabilities": [1.0 / n] * n}))
        v = qc.verify(str(cert_path), against=str(claim))
        self.assertFalse(v["ok"])
        self.assertTrue(any("total-variation" in m for m in v["failures"]))

    def test_true_claim_is_accepted(self):
        d, cert_path, _ = self._cert("ghz", 8)
        _, p = qc._exact("ghz", 8)
        claim = d / "true.json"
        claim.write_text(json.dumps({"probabilities": p.tolist()}))
        v = qc.verify(str(cert_path), against=str(claim))
        self.assertTrue(v["ok"], v["failures"])

    def test_tampered_certificate_is_refused(self):
        _, cert_path, _ = self._cert("ghz", 8)
        data = json.loads(cert_path.read_text())
        data["result"]["sha256"] = "0" * 64
        cert_path.write_text(json.dumps(data))
        v = qc.verify(str(cert_path))
        self.assertFalse(v["ok"])
        self.assertTrue(any("integrity" in m for m in v["failures"]))

    def test_non_ghz_program_certifies(self):
        _, cert_path, cert = self._cert("bell", 2)
        self.assertEqual(cert["circuit"]["n_qubits"], 2)
        v = qc.verify(str(cert_path))
        self.assertTrue(v["ok"])


if __name__ == "__main__":
    unittest.main()
