"""The discovery engine runs all strategies, falsifies, scores, and the typed jump framework
generates the true historical jump (retrodiction)."""
import unittest
from unittest import mock

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

    def test_unavailable_falsifier_is_open_not_a_crash(self):
        # a falsifier that needs a missing dependency (e.g. stim in CI) returns OPEN, not a raise
        def _raises():
            raise ImportError("No module named 'stim'")

        runner.FALSIFIERS["__raises__"] = _raises
        try:
            c = runner.Candidate(id="x", statement="s", falsifier="f", strategy="st",
                                 source_facts=(), test="__raises__")
            ran, survived, evidence = runner._falsify(c)
            self.assertFalse(ran)
            self.assertIsNone(survived)
            self.assertIn("unavailable", evidence)
        finally:
            runner.FALSIFIERS.pop("__raises__", None)


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


class TestLineage(unittest.TestCase):
    def test_candidate_carries_its_ancestry(self):
        parent = runner._mk("mass-gap", "conceptual-jump", "anomaly", "parent hypothesis",
                            "a falsifier", 2.0, 0.3)
        child = runner._mk("mass-gap", "conceptual-jump", "inversion", "child hypothesis",
                           "a falsifier", 2.0, 0.3, ancestry=(parent.id,))
        self.assertIn(parent.id, child.ancestry)
        self.assertEqual(runner.lineage(child), f"{parent.id} → {child.id}")

    def test_lineage_retains_the_dead_end_parent(self):
        # G4: an unsuccessful branch is retained in the child's ancestry, not re-discovered.
        dead = runner._mk("mass-gap", "computational-search", "counterexample", "dead end",
                          "a falsifier", 1.0, 0.4)
        child = runner._mk("mass-gap", "computational-search", "counterexample", "modified",
                           "a falsifier", 1.0, 0.4, ancestry=(dead.id,))
        self.assertEqual(child.ancestry, (dead.id,))
        self.assertIn(dead.id, runner.lineage(child))


class TestLlmSearch(unittest.TestCase):
    def test_llm_search_is_a_registered_strategy(self):
        self.assertIn("llm-search", {s.name for s in runner.SEARCH_STRATEGIES})

    def test_returns_nothing_without_a_model(self):
        s = runner.LlmSearch()
        self.assertEqual(s.generate("mass-gap", 4), [])

    def test_parses_hypothesis_falsifier_lines(self):
        s = runner.LlmSearch()
        with mock.patch.object(runner, "_llm_config", return_value=("http://x/v1", "", "m")):
            with mock.patch.object(runner, "_ask_llm",
                                   return_value="a hypothesis | a falsifier\nanother | its falsifier"):
                out = s.generate("mass-gap", 4)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].statement, "a hypothesis")
        self.assertEqual(out[0].falsifier, "a falsifier")


if __name__ == "__main__":
    unittest.main()
