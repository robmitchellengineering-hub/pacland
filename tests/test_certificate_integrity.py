"""Integrity of the certificate set: signature, hashes, and a reproduction that can actually fail.

The point of these tests is the second half of each: not that the honest case passes, but that the
dishonest case fails. A tamper that does not change the bytes makes a test vacuous, so each one
asserts the tamper landed before asserting the rejection.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pacland.certify.integrity import (  # noqa: E402
    CERT_DIR, SIG_NAME, SIGNERS_NAME, compare_trees, verify_set, verify_signature,
)

CERT = ROOT / CERT_DIR
HAVE_KEYGEN = shutil.which("ssh-keygen") is not None


class TestTheCommittedSet(unittest.TestCase):
    def test_the_signature_and_public_key_are_committed(self):
        self.assertTrue((CERT / SIG_NAME).is_file(), "no manifest signature is committed")
        self.assertTrue((CERT / SIGNERS_NAME).is_file(), "no allowed_signers is committed")

    @unittest.skipUnless(HAVE_KEYGEN, "ssh-keygen not available")
    def test_the_committed_set_verifies_offline(self):
        result = verify_set(ROOT)
        self.assertTrue(result["ok"], "\n".join(result["failures"]))
        messages = " / ".join(message for _, message in result["checks"])
        self.assertIn("signature", messages)
        self.assertIn("hash", messages)


class TestTampering(unittest.TestCase):
    @unittest.skipUnless(HAVE_KEYGEN, "ssh-keygen not available")
    def test_a_tampered_manifest_breaks_the_signature(self):
        original = (CERT / "MANIFEST.json").read_bytes()
        doc = json.loads(original)
        name = sorted(doc["artifacts"])[0]
        # always a real change: a sha256 of zeros is never a real hash, and a grade may already be
        # the one we would "tamper" to (which is exactly how a vacuous test is born)
        doc["artifacts"][name]["sha256"] = "0" * 64
        tampered = (json.dumps(doc, indent=2) + "\n").encode()
        self.assertNotEqual(tampered, original,
                            "the tamper did not change the bytes — this test would prove nothing")
        ok, why = verify_signature(tampered, CERT / SIG_NAME, CERT / SIGNERS_NAME)
        self.assertFalse(ok, "a tampered manifest verified")
        self.assertIn("signature", why.lower())

    @unittest.skipUnless(HAVE_KEYGEN, "ssh-keygen not available")
    def test_a_tampered_artifact_breaks_its_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            shutil.copytree(CERT, root / CERT_DIR)
            target = root / CERT_DIR / "gdpnow.json"
            original = target.read_bytes()
            target.write_bytes(original + b"\n")
            self.assertNotEqual(target.read_bytes(), original, "the tamper did not change the bytes")
            result = verify_set(root)
        self.assertFalse(result["ok"], "a tampered artifact verified")
        self.assertTrue(any("gdpnow" in failure for failure in result["failures"]), result["failures"])


class TestReproduction(unittest.TestCase):
    def test_a_fresh_issue_reproduces_the_committed_bytes(self):
        env = {"PYTHONPATH": str(ROOT / "src"),
               "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin"}
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "issue_vvs.py"), "--out", tmp],
                capture_output=True, env=env, cwd=str(ROOT),
            )
            self.assertEqual(proc.returncode, 0,
                             proc.stderr.decode("utf-8", "replace")[-2000:])
            problems = compare_trees(CERT, pathlib.Path(tmp) / CERT_DIR)
        self.assertEqual(problems, [], "\n".join(problems))

    def test_the_comparison_can_fail(self):
        # the mutation proof for the gate itself: if this cannot fail, a green run means nothing
        with tempfile.TemporaryDirectory() as tmp:
            fresh = pathlib.Path(tmp) / CERT_DIR
            shutil.copytree(CERT, fresh)
            target = fresh / "gdpnow.json"
            target.write_bytes(target.read_bytes() + b"\n")
            problems = compare_trees(CERT, fresh)
        self.assertTrue(problems, "a one-byte difference was not reported")


if __name__ == "__main__":
    unittest.main()
