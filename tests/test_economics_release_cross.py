"""Two archives, one 'first release': do they agree, and does the disagreement change a headline?"""
import unittest

from pacland.economics import release_cross as rc


class TestAgreement(unittest.TestCase):
    def test_most_quarters_agree(self):
        a = rc.agreement()
        self.assertGreaterEqual(a["n_within"], a["n"] - 2)
        self.assertGreaterEqual(a["n"], 30)

    def test_the_disagreements_are_the_covid_quarters(self):
        a = rc.agreement()
        names = [r["quarter"] for r in a["outside"]]
        for o in rc.OUTLIERS:
            self.assertIn(o.replace(":", ""), names)

    def test_the_worst_gap_is_reported_not_averaged(self):
        a = rc.agreement()
        self.assertGreater(a["worst_gap"], 3.0)
        self.assertLess(a["mean_abs_gap"], 1.0)


class TestSensitivity(unittest.TestCase):
    def test_the_37_quarter_headline_is_not_stable(self):
        s = rc.sensitivity()
        self.assertFalse(s["stable"])
        self.assertGreater(s["swing"], 0.2)

    def test_all_three_variants_are_positive(self):
        s = rc.sensitivity()
        for k in ("all", "excluded", "fed_values"):
            self.assertGreater(s[k], 0.0, k)


class TestGuards(unittest.TestCase):
    def test_misalignment_breaks_the_agreement(self):
        ok, msg = rc.guard_misalignment()
        self.assertTrue(ok, msg)

    def test_outliers_must_be_named(self):
        ok, msg = rc.guard_outliers_are_named()
        self.assertTrue(ok, msg)

    def test_the_audit_is_green(self):
        self.assertTrue(rc.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
