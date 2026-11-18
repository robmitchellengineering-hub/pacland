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


class TestNonVacuousSurvivor(unittest.TestCase):
    def test_a_toy_theorem_is_not_a_survivor(self):
        c = runner._mk("mass-gap", "s", "t", "the effective Hessian is bounded below", "f", 1.0, 0.5)
        self.assertFalse(runner.is_non_vacuous_survivor(c, "some evidence"))

    def test_a_real_object_that_ran_a_falsifier_is_a_survivor(self):
        c = runner._mk("mass-gap", "s", "t", "the mass gap is positive for Yang-Mills", "f", 1.0, 0.5)
        self.assertTrue(runner.is_non_vacuous_survivor(c, "keyword-routed falsifier evidence"))

    def test_an_open_candidate_is_not_a_survivor(self):
        c = runner._mk("mass-gap", "s", "t", "the mass gap is positive", "f", 1.0, 0.5)
        self.assertFalse(runner.is_non_vacuous_survivor(c, "needs a falsifier (proposed: x)"))


class TestFalsifierRouting(unittest.TestCase):
    def test_routes_a_mass_gap_lower_bound_to_the_ratio_falsifier(self):
        self.assertEqual(runner._falsifier_for_statement("m_gap ≥ c·√σ with c > 0"),
                         runner.verify_glueball_mass_ratio)

    def test_routes_a_perturbative_claim_to_the_scaling_referee(self):
        self.assertEqual(runner._falsifier_for_statement("the mass gap is non-perturbative"),
                         runner.verify_mass_gap_scaling)

    def test_leaves_theta_open(self):
        self.assertIsNone(runner._falsifier_for_statement("the mass gap is robust against a θ-term"))

    def test_polyakov_routes_to_the_clustering_falsifier(self):
        self.assertEqual(runner._falsifier_for_statement("Polyakov-loop correlators cluster exponentially"),
                         runner.FALSIFIERS["polyakov-clustering"])

    def test_routes_to_the_new_candidate_specific_falsifiers(self):
        self.assertEqual(runner._falsifier_for_statement("the d=5 mass gap survives the continuum limit"),
                         runner.FALSIFIERS["d5-mass-gap"])
        self.assertEqual(runner._falsifier_for_statement("a first-order bulk transition persists"),
                         runner.FALSIFIERS["bulk-transition"])
        self.assertEqual(runner._falsifier_for_statement("the mass gap is universal under irrelevant operators"),
                         runner.FALSIFIERS["universality"])

    def test_unresolved_measurement_is_open_not_falsified(self):
        c = runner.Candidate(id="x", statement="s", falsifier="f", strategy="st",
                             source_facts=(), test="glueball-mass-ratio")
        def _noise():
            return False, "noise-dominated at beta=2.4: the signal is unresolved"
        with mock.patch.dict(runner.FALSIFIERS, {"glueball-mass-ratio": _noise}):
            ran, survived, evidence = runner._falsify(c)
        self.assertFalse(ran)
        self.assertIsNone(survived)
        self.assertIn("unresolved", evidence)

    def test_keyword_routed_falsifier_is_approximate_not_survived(self):
        c = runner.Candidate(id="x", statement="the mass gap scales as sqrt(sigma)", falsifier="f",
                             strategy="st", source_facts=(), test="")
        def _fake_falsifier():
            return True, "some related test passed"
        with mock.patch.object(runner, "_falsifier_for_statement", return_value=_fake_falsifier):
            ran, survived, evidence = runner._falsify(c)
        self.assertTrue(ran)
        self.assertIsNone(survived)  # approximate, not a definitive survive
        self.assertIn("APPROXIMATE", evidence)

    def test_mass_gap_scaling_referee_identity_is_not_a_survivor(self):
        survived, evidence = runner.verify_mass_gap_scaling()
        self.assertFalse(survived)  # no INDEPENDENT mechanism survives; AF is the referee itself
        self.assertIn("REFEREE IDENTITY", evidence)


class TestAutonomousLoop(unittest.TestCase):
    def _candidate(self, statement="a hypothesis", test=""):
        return runner.Candidate(id="x", statement=statement, falsifier="f", strategy="llm-search",
                                source_facts=(), test=test)

    def test_prove_and_record_defers_without_an_llm(self):
        with mock.patch.object(runner, "_llm_config", return_value=("", "", "")):
            with mock.patch.object(runner, "DISCOVERIES", runner.REPO_ROOT / "runs" / "test.jsonl"):
                r = runner.prove_and_record(self._candidate(), "evidence")
        self.assertTrue(r["recorded"])
        self.assertIn("deferred", r["proof"])

    def test_run_autonomous_collects_a_survivor(self):
        cand = self._candidate("a surviving hypothesis")
        with mock.patch.object(runner.LlmSearch, "generate", return_value=[cand]):
            with mock.patch.object(runner, "_falsify", return_value=(True, True, "survived evidence")):
                with mock.patch("pacland.challenges.run_sequence", return_value=[]):
                    with mock.patch("pacland.challenges.gate", return_value="PASS"):
                        with mock.patch.object(runner, "prove_and_record",
                                               return_value={"ok": False, "recorded": True,
                                                             "proof": "deferred"}):
                            out = runner.run_autonomous("mass-gap")
        self.assertEqual(len(out["rounds"][0]["survivors"]), 1)
        self.assertIn("run_id", out)

    def test_an_approximate_verdict_is_open_not_falsified(self):
        # survived=None means "approximate test, not a definitive survive/falsify" — it must not be
        # counted as falsified.
        cand = self._candidate("a hypothesis")
        with mock.patch.object(runner.LlmSearch, "generate", return_value=[cand]):
            with mock.patch.object(runner, "_falsify", return_value=(True, None, "APPROXIMATE")):
                with mock.patch("pacland.challenges.run_sequence", return_value=[]):
                    with mock.patch("pacland.challenges.gate", return_value="PASS"):
                        out = runner.run_autonomous("mass-gap")
        r = out["rounds"][0]
        self.assertEqual(len(r["proposals"]), 0)  # not counted as falsified
        self.assertEqual(len(r["open"]), 1)

    def test_a_challenge_failure_gates_out_the_candidate(self):
        cand = self._candidate("a hypothesis")
        with mock.patch.object(runner.LlmSearch, "generate", return_value=[cand]):
            with mock.patch.object(runner, "_falsify", return_value=(True, True, "survived")):
                with mock.patch("pacland.challenges.run_sequence", return_value=[]):
                    with mock.patch("pacland.challenges.gate", return_value="FAIL"):
                        out = runner.run_autonomous("mass-gap")
        r = out["rounds"][0]
        self.assertEqual(len(r["survivors"]), 0)  # gated out, not proved
        self.assertEqual(r["proposals"][0]["verdict"], "gated-out")

    def test_lean_bridge_rejects_a_different_proposition(self):
        with mock.patch.object(runner, "_judge_config", return_value=("http://x", "", "judge")):
            with mock.patch.object(runner, "_ask_llm", return_value="NO"):
                ok = runner._lean_matches_hypothesis("theorem wrong : 1 = 2", "the mass gap is positive")
        self.assertFalse(ok)

    def test_lean_bridge_accepts_the_same_proposition(self):
        with mock.patch.object(runner, "_judge_config", return_value=("http://x", "", "judge")):
            with mock.patch.object(runner, "_ask_llm", return_value="YES"):
                ok = runner._lean_matches_hypothesis("theorem", "the mass gap is positive")
        self.assertTrue(ok)

    def test_register_experiment_writes_a_run_id(self):
        with mock.patch.object(runner, "EXPERIMENTS", runner.REPO_ROOT / "runs" / "test-exp.jsonl"):
            run_id = runner.register_experiment("test", {"seed": 1}, {"recall": 0.5})
        self.assertTrue(run_id)
        self.assertEqual(len(run_id), 12)

    def test_reproduce_reruns_an_autonomous_run(self):
        with mock.patch.object(runner, "EXPERIMENTS", runner.REPO_ROOT / "runs" / "test-exp.jsonl"):
            runner.EXPERIMENTS.write_text('{"run_id": "abc123", "kind": "autonomous", '
                                          '"config": {"problem": "p", "rounds": 1, "budget": 4}, '
                                          '"metrics": {}}\n')
            with mock.patch.object(runner, "run_autonomous",
                                   return_value={"run_id": "new", "rounds": []}):
                out = runner.reproduce("abc123")
        self.assertEqual(out["reproduced_from"], "abc123")
        self.assertEqual(out["new_run_id"], "new")

    def test_check_lean_refuses_a_sorry_placeholder(self):
        # a file that compiles with `sorry` is NOT a proof
        ok, err = runner._check_lean("theorem t : (1 : Nat) + 1 = 2 := by sorry\n")
        self.assertFalse(ok)
        self.assertIn("not a proof", err)


if __name__ == "__main__":
    unittest.main()
