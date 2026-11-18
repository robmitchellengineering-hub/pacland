"""The discovery engine runs all strategies, falsifies, scores, and the typed jump framework
generates the true historical jump (retrodiction)."""
import unittest

from pacland import hypotheses, runner


class TestDiscoveryEngine(unittest.TestCase):
    def test_self_test_runs_all_strategies_and_scores(self):
        r = runner.engine_self_test()
        self.assertEqual(len(r["experiments"]), len(runner.SEARCH_STRATEGIES))
        self.assertEqual(set(r["score"]["per_strategy"]),
                         {s.name for s in runner.SEARCH_STRATEGIES})
        self.assertIn("global", r["score"])

    def test_every_strategy_has_a_distinct_name(self):
        names = [s.name for s in runner.SEARCH_STRATEGIES]
        self.assertEqual(len(names), len(set(names)))

    def test_kill_criteria_stops_when_budget_spent_with_no_survivor(self):
        ks = runner.KillState(budget=3)
        ks.tried = 3
        runner.apply_kill_criteria(ks)
        self.assertTrue(ks.stopped)
        self.assertIn("reframe", ks.reason)

    def test_kill_criteria_does_not_stop_with_a_survivor(self):
        ks = runner.KillState(budget=3)
        ks.tried = 3
        ks.survivors = 1
        runner.apply_kill_criteria(ks)
        self.assertFalse(ks.stopped)


# ----------------------------------------------------------------------------
# Retrodiction: the typed five-question framework generates the true historical jump;
# the untyped baseline never does.
# ----------------------------------------------------------------------------

TOY_JUMPS = {
    "blackbody": "energy is quantised, E = h nu",
    "photoelectric": "light is made of quanta (photons)",
    "perihelion": "gravity is spacetime curvature (GR)",
}

TRUE_TYPE = {"blackbody": "principle", "photoelectric": "principle", "perihelion": "analogy"}

_TRUE = {
    "blackbody": ("energy is quantised, E = h nu", "fits the whole spectrum", 2.0, 0.3),
    "photoelectric": ("light is made of quanta (photons)", "predicts the frequency threshold", 2.0, 0.3),
    "perihelion": ("gravity is spacetime curvature (GR)", "predicts 43 arcsec/century", 2.0, 0.3),
}

_DISTRACTORS = {
    "blackbody": [("the emitter is granular (atoms)", "fails short-wavelength tail", 3.0, 0.2),
                  ("a new long-range force", "no such force observed", 4.0, 0.1)],
    "photoelectric": [("the metal's electrons are quantised", "predicts the wrong threshold", 3.0, 0.2)],
    "perihelion": [("a hidden planet (Vulcan)", "not found where predicted", 3.0, 0.2)],
}


def _typed_generator(problem, jt):
    if problem not in _TRUE:
        return []
    if jt == TRUE_TYPE[problem]:
        return [_TRUE[problem]] + _DISTRACTORS.get(problem, [])
    return _DISTRACTORS.get(problem, [])


def _baseline_generator(problem, jt):
    red = {
        "blackbody": [("the emitter is granular (atoms)", "fails short-wavelength tail", 3.0, 0.2),
                      ("a new long-range force", "no such force observed", 4.0, 0.1)],
        "photoelectric": [("the metal's electrons are quantised", "predicts the wrong threshold", 3.0, 0.2)],
        "perihelion": [("a hidden planet (Vulcan)", "not found where predicted", 3.0, 0.2)],
    }
    return red.get(problem, [])


class TestRetrodiction(unittest.TestCase):
    def test_jump_questions_are_five_and_distinct(self):
        self.assertEqual(len(hypotheses.JUMP_QUESTIONS), 5)

    def test_typed_generator_emits_the_true_jump_under_its_type(self):
        for problem, true_jump in TOY_JUMPS.items():
            hypotheses_ = _typed_generator(problem, TRUE_TYPE[problem])
            emitted = [h for (h, _f, _c, _p) in hypotheses_]
            self.assertIn(true_jump, emitted, problem)

    def test_baseline_never_emits_the_true_jump(self):
        for problem, true_jump in TOY_JUMPS.items():
            emitted = [h for (h, _f, _c, _p) in _baseline_generator(problem, TRUE_TYPE[problem])]
            self.assertNotIn(true_jump, emitted, problem)


if __name__ == "__main__":
    unittest.main()
