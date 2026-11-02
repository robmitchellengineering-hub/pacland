"""H-E: results published without a stated falsifier are the ones that get demoted."""
import unittest

from pacland.exactness import killing_tests as K


class TestThePattern(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = K.audit()

    def test_the_pattern_holds(self):
        self.assertTrue(self.a["pattern_holds"])

    def test_no_demoted_result_had_a_stated_falsifier(self):
        self.assertEqual(self.a["demoted_with_a_stated_falsifier"], [])

    def test_no_survivor_lacks_one(self):
        self.assertEqual(self.a["survived_without_one"], [])

    def test_every_result_is_classified(self):
        self.assertEqual(len(self.a["demoted"]) + len(self.a["survived"]), self.a["results"])


class TestTheHypothesesAreDifferent(unittest.TestCase):
    def test_every_hypothesis_states_a_falsifier(self):
        for name, kind, stated, status, test in K.hypotheses():
            self.assertTrue(stated, name)
            self.assertGreater(len(test), 10, name)

    def test_the_refuted_ones_are_successes_not_failures(self):
        # a hypothesis dying cleanly in one run is the system working
        verdicts = K.audit()["hypothesis_verdicts"]
        self.assertIn("refuted", verdicts.values())
        self.assertIn("supported", verdicts.values())


class TestTheStatement(unittest.TestCase):
    def test_the_narrow_form_is_stated(self):
        self.assertIn("H-E SUPPORTED", K.audit()["verdict"])
        self.assertIn("narrow form", K.audit()["verdict"])


if __name__ == "__main__":
    unittest.main()
