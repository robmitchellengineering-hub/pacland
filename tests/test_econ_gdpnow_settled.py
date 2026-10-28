"""GDPNow against the settled number: the edge must survive both targets and dropping 2020."""
import unittest

from pacland.economics import gdpnow as G


class TestSettled(unittest.TestCase):
    def test_both_targets_are_scored_on_the_same_vintages(self):
        c = G.settled_comparison()
        for target in G.TARGETS:
            for exclude in (False, True):
                self.assertIn((target, exclude), c["rows"])
                self.assertEqual(c["rows"][(target, exclude)]["n"],
                                 c["rows"][(target, exclude)]["n"])

    def test_the_edge_survives_the_settled_target(self):
        c = G.settled_comparison()
        self.assertTrue(c["beats_null_everywhere"], c["verdict"])
        self.assertLess(c["rows"][("final", False)]["ratio"], 1.0)

    def test_the_edge_survives_dropping_2020(self):
        c = G.settled_comparison()
        self.assertLess(c["rows"][("final", True)]["ratio"], 1.0)

    def test_the_margin_narrows_and_says_so(self):
        c = G.settled_comparison()
        self.assertGreater(c["rows"][("final", True)]["ratio"],
                           c["rows"][("advance", False)]["ratio"])
        self.assertIn("narrows", c["verdict"])

    def test_the_guard_is_green(self):
        ok, msg = G.guard_settled_skill_is_not_a_covid_artefact()
        self.assertTrue(ok, msg)


class TestCertificate(unittest.TestCase):
    def test_gdpnow_is_verified_now(self):
        from pacland.certify.dossiers import gdpnow
        c = gdpnow()
        self.assertEqual(c.grade, "VERIFIED")
        self.assertEqual(c.score["satisfied"], len(c.findings))

    def test_the_headline_states_both_targets(self):
        from pacland.certify.dossiers import gdpnow
        h = gdpnow().headline
        self.assertIn("advance", h)
        self.assertIn("settled", h)


if __name__ == "__main__":
    unittest.main()
