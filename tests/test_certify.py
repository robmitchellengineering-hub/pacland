"""Certificates: the grade follows the findings, and every number is computed at issue time."""
import unittest

from pacland.certify import dossiers as D
from pacland.certify.certificate import (Certificate, Finding, FAILING, NOT_DEMONSTRATED,
                                         PARTIAL, SATISFIED)


def make(statuses):
    findings = tuple(Finding("clause", "q", "a", "e", s) for s in statuses)
    return Certificate(subject="s", issuer="i", issued="d", findings=findings, headline="h",
                       limitations=(), provenance=())


class TestGrade(unittest.TestCase):
    def test_all_satisfied_is_verified(self):
        self.assertEqual(make([SATISFIED, SATISFIED]).grade, "VERIFIED")

    def test_a_partial_is_qualified(self):
        self.assertEqual(make([SATISFIED, PARTIAL]).grade, "QUALIFIED")

    def test_a_gap_is_restricted(self):
        self.assertEqual(make([SATISFIED, NOT_DEMONSTRATED]).grade, "RESTRICTED")

    def test_a_failure_is_refused(self):
        self.assertEqual(make([SATISFIED, FAILING]).grade, "REFUSED")


class TestDossiers(unittest.TestCase):
    def test_gdpnow_is_verified_and_beats_the_null_on_both_targets(self):
        # it was QUALIFIED while only the advance estimate had been scored; the settled-number
        # comparison closed the last finding, and this test now pins the stronger claim
        c = D.gdpnow()
        self.assertEqual(c.grade, "VERIFIED")
        self.assertIn("lower MAE", c.headline)
        self.assertIn("settled", c.headline)

    def test_smets_wouters_is_refused_for_a_stated_reason(self):
        c = D.smets_wouters()
        self.assertEqual(c.grade, "REFUSED")
        self.assertIn("observable", c.headline)
        self.assertTrue(any(f.status == FAILING for f in c.findings))

    def test_cmip6_names_a_model_and_cites_a_number(self):
        c = D.cmip6()
        self.assertIn("CMIP6", c.subject)
        self.assertIn("W/m2", c.headline)
        self.assertEqual(c.grade, "REFUSED")

    def test_every_dossier_has_evidence_and_limitations(self):
        for name, fn in D.DOSSIERS.items():
            c = fn()
            self.assertGreaterEqual(len(c.findings), 4, name)
            self.assertTrue(c.provenance, name)
            self.assertTrue(c.limitations, name)

    def test_marksdown_and_json_render(self):
        c = D.gdpnow()
        md, js = c.to_markdown(), c.to_json()
        self.assertIn("Model risk certificate", md)
        self.assertIn('"grade"', js)


if __name__ == "__main__":
    unittest.main()
