"""The first GDP print: bias, exploitability, and the target that changes the answer."""
import unittest

from pacland.economics import revisions as rv


class TestBias(unittest.TestCase):
    def test_the_advance_estimate_revises_upward(self):
        s = rv.summary()
        self.assertGreater(s["mean_revision_pp"], 0.0)
        self.assertGreater(s["share_upward"], 0.5)
        self.assertGreater(s["t_stat"], 2.0)

    def test_but_the_revisions_have_no_memory(self):
        self.assertLess(abs(rv.summary()["ar1"]), 0.2)

    def test_the_bias_is_a_property_of_the_values(self):
        ok, msg = rv.guard_bias_is_not_an_artefact()
        self.assertTrue(ok, msg)


class TestExploitability(unittest.TestCase):
    def test_a_bias_correction_does_not_beat_the_print_out_of_sample(self):
        e = rv.exploitability()
        self.assertFalse(e["beats_the_print"])
        self.assertGreater(e["ratio"], 1.0)

    def test_the_loss_is_reported_rather_than_hidden(self):
        self.assertIn("not exploitable", rv.exploitability()["verdict"])


class TestTargets(unittest.TestCase):
    def test_the_official_print_beats_the_nowcast_against_the_final_number(self):
        b = rv.benchmarks()
        self.assertLess(b["advance_vs_final"], b["nowcast_vs_final"])

    def test_the_nowcast_does_beat_the_null(self):
        b = rv.benchmarks()
        self.assertLess(b["nowcast_over_null"], 1.0)
        self.assertLess(b["print_over_null"], 1.0)

    def test_the_two_targets_are_distinguished(self):
        ok, msg = rv.guard_target_is_not_confused()
        self.assertTrue(ok, msg)

    def test_the_audit_is_green(self):
        self.assertTrue(rv.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
