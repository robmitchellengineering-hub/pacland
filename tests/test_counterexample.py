"""The counterexample engine — and the proof that it can find what it claims to look for."""
import unittest

from pacland.exactness import counterexample as C


class TestTheShippedSearches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = {x.conjecture: x for x in C.run_all()}

    def test_known_answer_controls_find_a_counterexample(self):
        # these MUST break: if they do not, the engine cannot report a broken conjecture at all
        for name in ("tadpole is always positive", "tadpole is never zero"):
            v = self.v[name]
            self.assertIsNotNone(v.counterexample, f"{name} found nothing -- the engine is blind")
            self.assertEqual(v.verdict, "BROKEN")

    def test_the_false_bound_is_broken_in_the_window(self):
        v = self.v["tadpole N <= 3"]
        self.assertIsNotNone(v.counterexample)
        self.assertGreater(v.counterexample["tadpole"], 3)

    def test_the_true_bound_is_not_broken_in_the_window(self):
        v = self.v["tadpole N <= 6"]
        self.assertIsNone(v.counterexample)
        self.assertEqual(v.verdict, "no counterexample")

    def test_a_clean_verdict_states_what_it_does_not_prove(self):
        v = self.v["tadpole N <= 6"]
        self.assertIn("nothing outside it", v.proves)
        self.assertIn("b3=6", v.window)

    def test_a_broken_verdict_quotes_the_object(self):
        v = self.v["tadpole N <= 3"]
        self.assertIn("FALSE", v.proves)
        self.assertIn("flux", v.counterexample)


class TestTheEngineCanFail(unittest.TestCase):
    def test_a_planted_counterexample_is_found(self):
        # a predicate that is true everywhere except one planted object
        target = None

        def planted(flux, t):
            nonlocal target
            if target is None and t == 2:
                target = flux
                return False
            return True

        v = C.search(planted, "planted at a known object", limit=1)
        self.assertIsNotNone(v.counterexample)
        self.assertEqual(v.counterexample["flux"], target)

    def test_a_predicate_true_everywhere_returns_nothing(self):
        v = C.search(lambda flux, t: True, "always true")
        self.assertIsNone(v.counterexample)
        self.assertEqual(v.searched, 531441)

    def test_the_scope_is_always_stated(self):
        for v in C.run_all():
            self.assertIn("does NOT prove", v.scope)


if __name__ == "__main__":
    unittest.main()
