"""The VVS named-gate certificate: five fields per gate, and a verified flag that cannot lie."""
import json
import pathlib
import unittest

from pacland.certify import dossiers as D

ROOT = pathlib.Path(__file__).resolve().parents[1]
VVS = ROOT / "certificates" / "vvs"


class TestFormat(unittest.TestCase):
    def test_the_named_gate_contract_has_five_fields(self):
        v = D.gdpnow().to_vvs()
        self.assertEqual(v["format"], "valiant-verification/named-gate@1")
        for gate in v["gates"]:
            for field in ("gate", "result", "evidence", "evidence_path", "producer", "falsifier"):
                self.assertIn(field, gate)
                self.assertTrue(str(gate[field]).strip(), f"{field} is empty")

    def test_a_pass_without_a_falsifier_is_not_allowed_to_be_silent(self):
        for gate in D.smets_wouters().to_vvs()["gates"]:
            self.assertTrue(gate["falsifier"].strip())

    def test_verified_means_every_gate_passed(self):
        # the invariant is checked on the two verified parts plus a constructed failing one, rather
        # than re-running every dossier (which re-solves a DSGE and re-checks five theorems)
        from pacland.certify.certificate import (Certificate, Finding, SATISFIED, FAILING)
        made = Certificate(subject="s", issuer="i", issued="d", headline="h", limitations=(),
                           provenance=(), sector="x", findings=(
                               Finding("c", "q1", "a", "e", SATISFIED),
                               Finding("c", "q2", "a", "e", FAILING)))
        v = made.to_vvs()
        self.assertEqual((v["gates_passed"], v["gates_required"], v["verified"]), (1, 2, False))
        for name in ("gdpnow", "physics_theorems"):
            v = getattr(D, name)().to_vvs()
            self.assertTrue(v["verified"], name)
            self.assertEqual(v["gates_required"], len(v["gates"]))


class TestPhysics(unittest.TestCase):
    def test_the_theorem_tower_is_verified(self):
        c = D.physics_theorems()
        self.assertEqual(c.grade, "VERIFIED")
        self.assertTrue(c.to_vvs()["verified"])

    def test_every_theorem_names_its_validator(self):
        for f in D.physics_theorems().findings:
            self.assertIn("scripts/validate_", f.evidence)


class TestManifest(unittest.TestCase):
    def test_the_manifest_carries_a_hash_per_artifact(self):
        manifest = json.loads((VVS / "MANIFEST.json").read_text())
        self.assertEqual(manifest["format"], "valiant-verification/manifest@1")
        for name, rec in manifest["artifacts"].items():
            self.assertRegex(rec["sha256"], r"^[0-9a-f]{64}$", name)
            self.assertIn(rec["grade"], ("VERIFIED", "QUALIFIED", "RESTRICTED", "REFUSED"))

    def test_three_of_five_are_verified(self):
        # the set is asserted exactly, so a certificate that silently starts or stops passing is a
        # test failure rather than a quiet change on the page
        manifest = json.loads((VVS / "MANIFEST.json").read_text())
        verified = [n for n, r in manifest["artifacts"].items() if r["verified"]]
        self.assertEqual(sorted(verified), ["gdpnow", "physics", "riemann-zeros"])


if __name__ == "__main__":
    unittest.main()
