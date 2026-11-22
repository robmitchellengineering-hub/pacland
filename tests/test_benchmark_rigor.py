"""Benchmark rigor: cost measurement + blinded scoring (the G3 gate must be cost-aware and blind)."""
import unittest

from pacland import benchmarks as b


class TestCostMeasurement(unittest.TestCase):
    def test_run_arm_tracks_effort(self):
        # the untyped baseline emits 4 distractors per problem; cost = problems * 4
        r = b.run_arm("untyped-baseline", b.untyped_generator, "A", b.DATASET)
        self.assertEqual(r.cost, len(b.DATASET) * 4)
        self.assertGreater(r.cost, 0)

    def test_gate_reports_cost_per_found(self):
        engine = b.ArmResult("llm", "s", problems=10, found=5, cost=25)
        baseline = b.ArmResult("untyped-baseline", "s", problems=10, found=0, cost=40)
        g = b.gate([engine, baseline])
        self.assertTrue(g["passed"])
        self.assertAlmostEqual(g["engine_cost_per_found"], 5 / 25)
        self.assertIn("engine_cost_per_found", g)


class TestBlindedScoring(unittest.TestCase):
    def test_blinded_attributes_the_same_recall_as_unblinded(self):
        arms = {"llm": b.five_jump_generator, "untyped-baseline": b.untyped_generator}
        blinded = {r.arm: r for r in b.run_blinded(arms, "A", b.DATASET, seed=0)}
        plain = {r.arm: r for r in b.compare(arms, "A", b.DATASET)}
        # blinding must not change the per-arm recall — only the ORDER the scorer saw them in
        self.assertEqual(blinded["llm"].found, plain["llm"].found)
        self.assertEqual(blinded["untyped-baseline"].found, plain["untyped-baseline"].found)

    def test_blinded_tracks_cost_too(self):
        arms = {"llm": b.five_jump_generator, "untyped-baseline": b.untyped_generator}
        r = {x.arm: x for x in b.run_blinded(arms, "A", b.DATASET, seed=1)}
        self.assertGreater(r["llm"].cost, 0)
        self.assertGreater(r["untyped-baseline"].cost, 0)


class TestCapableBaseline(unittest.TestCase):
    def test_generic_llm_baseline_uses_the_neutral_prompt(self):
        from unittest import mock
        with mock.patch.object(b, "_llm_config", return_value=("http://x/v1", "", "m")):
            with mock.patch.object(b, "_ask_llm", return_value="one explanation\n- another") as ask:
                out = b.generic_llm_generator("some observation")
        prompt = ask.call_args[0][0]
        # the neutral baseline must NOT carry the discovery framing (that is the whole point)
        self.assertNotIn("scientific hypothesis generator", prompt)
        self.assertIn("Explanations:", prompt)
        self.assertEqual(out, ["one explanation", "another"])

    def test_run_llm_benchmark_compares_llm_against_generic_llm(self):
        from unittest import mock
        # stub both arms to the toy generators so the comparison runs offline
        with mock.patch.object(b, "llm_generator", b.five_jump_generator):
            with mock.patch.object(b, "generic_llm_generator", b.untyped_generator):
                out = b.run_llm_benchmark("A", judged=False)
        arms = {a["arm"]: a for a in out["arms"]}
        self.assertIn("llm", arms)
        self.assertIn("generic-llm", arms)
        self.assertIn("passed", out)
        self.assertIn("engine_cost_per_found", out)


class TestPipelineFilter(unittest.TestCase):
    def test_filter_rejects_generic_distractors(self):
        f = b.engine_with_filter(lambda pre: ["a new long-range force", "energy is quantised"])
        self.assertEqual(f("the blackbody spectrum diverges"), ["energy is quantised"])

    def test_filter_rejects_premise_restatements(self):
        f = b.engine_with_filter(lambda pre: [pre, "energy is quantised"])
        self.assertEqual(f("the blackbody spectrum diverges at short wavelength"),
                         ["energy is quantised"])

    def test_filtered_arm_has_lower_false_positives(self):
        raw = b.run_arm("llm", b.untyped_generator, "A", b.DATASET)
        filtered = b.run_arm("full-engine", b.engine_with_filter(b.untyped_generator), "A", b.DATASET)
        # the filter must not INCREASE false positives, and the untyped distractors are all filtered
        self.assertLessEqual(filtered.false_positives, raw.false_positives)

    def test_paired_uses_the_same_underlying_draw(self):
        # a deterministic generator with one right answer + one generic distractor
        calls = {"n": 0}

        def gen(pre):
            calls["n"] += 1
            return ["energy is quantised", "a new long-range force"]

        raw, filt = b.run_paired(gen, {"blackbody": b.DATASET["blackbody"]})
        # one generation, not two — the paired design removes the non-determinism confound
        self.assertEqual(calls["n"], 1)
        self.assertEqual(raw.found, filt.found)          # the filter kept the right answer
        self.assertLess(filt.false_positives, raw.false_positives)  # and dropped the distractor


if __name__ == "__main__":
    unittest.main()
