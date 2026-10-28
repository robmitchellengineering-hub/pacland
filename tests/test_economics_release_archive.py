"""The Fed's release ladder: does the 37-quarter result replicate on 239 quarters?"""
import unittest

from pacland.economics import release_archive as ra


class TestLadder(unittest.TestCase):
    def test_the_bias_replicates(self):
        s = ra.summary()
        self.assertTrue(s["biased"])
        self.assertGreater(s["mean_total_pp"], 0.0)
        self.assertGreater(s["t_stat"], 2.0)

    def test_the_quarters_are_actually_239(self):
        self.assertEqual(ra.summary()["n"], 239)

    def test_every_step_is_positive(self):
        for label, s in ra.ladder().items():
            self.assertGreater(s["mean_pp"], 0.0, label)

    def test_the_steps_are_distinct(self):
        ok, msg = ra.guard_steps_are_distinguished()
        self.assertTrue(ok, msg)


class TestMemoryAndExploitability(unittest.TestCase):
    def test_no_memory(self):
        self.assertLess(abs(ra.summary()["ar1"]), 0.2)

    def test_not_exploitable(self):
        e = ra.exploitability()
        self.assertFalse(e["beats_the_print"])
        self.assertGreater(e["ratio"], 1.0)

    def test_pairing_matters(self):
        ok, msg = ra.guard_pairing_matters()
        self.assertTrue(ok, msg)

    def test_the_audit_is_green(self):
        self.assertTrue(ra.audit()["all_pass"])


if __name__ == "__main__":
    unittest.main()
