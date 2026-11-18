"""The real LLM generator is structurally honest — it sees only the pre-state, never the answer —
and the campaigns enforce the A -> B -> C order."""
import unittest
from unittest import mock

from pacland import benchmarks as b


class TestLlmGeneratorHonesty(unittest.TestCase):
    def _call(self, response_text, pre="the pre-state"):
        with mock.patch.object(b, "_llm_config", return_value=("http://x/v1", "", "m")):
            with mock.patch.object(b, "_ask_llm", return_value=response_text) as ask:
                out = b.llm_generator(pre)
        return out, ask.call_args[0][0]

    def test_prompt_carries_the_pre_state_not_the_answer(self):
        entry = b.DATASET["blackbody"]
        out, prompt = self._call("energy is quantised, E = h nu", pre=entry["pre"])
        # the prompt must contain the pre-state and must NOT contain the withheld jump
        self.assertIn(entry["pre"], prompt)
        self.assertNotIn(entry["jump"], prompt)

    def test_parses_numbered_and_bulleted_lines(self):
        out, _ = self._call("a first hypothesis\n- a second\n3. a third\n# a comment")
        self.assertEqual(out, ["a first hypothesis", "a second", "a third"])

    def test_refuses_without_a_model(self):
        with mock.patch.object(b, "_llm_config", return_value=("http://x/v1", "", "")):
            with self.assertRaises(RuntimeError):
                b.llm_generator("anything")


class TestCampaigns(unittest.TestCase):
    def test_order_is_calibrate_then_validate_then_frontier(self):
        self.assertEqual(list(b.CAMPAIGNS), ["A", "B", "C"])
        self.assertIn("FIRST", b.CAMPAIGNS["A"]["purpose"].upper())
        self.assertIn("frontier", b.CAMPAIGNS["C"]["purpose"].lower())

    def test_run_campaign_compares_against_the_baseline(self):
        results = b.run_campaign("A", b.five_jump_generator)
        arms = {r.arm for r in results}
        self.assertIn("untyped-baseline", arms)
        self.assertIn("llm", arms)

    def test_unknown_campaign_is_refused(self):
        with self.assertRaises(ValueError):
            b.run_campaign("Z", b.untyped_generator)


class TestSemanticMatch(unittest.TestCase):
    def test_accepts_a_paraphrase(self):
        # "photons" is shared, so a paraphrase matches even though the string differs
        self.assertTrue(b.semantic_match("photons have discrete energy packets",
                                          "light is made of quanta (photons)"))

    def test_prefix_does_not_match_a_different_word(self):
        # "photoelectric" and "photons" share a prefix but are not the same term — no match
        self.assertFalse(b.semantic_match("a granular explanation of the photoelectric threshold",
                                           "light is made of quanta (photons)"))

    def test_rejects_an_unrelated_candidate(self):
        self.assertFalse(b.semantic_match("a new long-range force",
                                          "energy is quantised, E = h nu"))


class TestCampaignBC(unittest.TestCase):
    def test_campaign_b_has_a_cross_discipline_dataset(self):
        self.assertGreaterEqual(len(b.B_DATASET), 5)
        results = b.run_campaign("B", b.untyped_generator)
        self.assertEqual({r.arm for r in results}, {"untyped-baseline", "llm"})

    def test_campaign_c_is_the_open_frontier(self):
        with self.assertRaises(ValueError):
            b.run_campaign("C", b.untyped_generator)

    def test_run_frontier_returns_proposals(self):
        proposals = b.run_frontier(lambda pre: ["proposal one", "proposal two"])
        self.assertEqual(proposals, ["proposal one", "proposal two"])


class TestJudge(unittest.TestCase):
    def test_judge_credits_a_paraphrase(self):
        cands = ["photons carry energy in discrete packets", "a new long-range force"]
        with mock.patch.object(b, "_judge_config", return_value=("http://x/v1", "", "judge")):
            with mock.patch.object(b, "_ask_llm", return_value="0"):
                matched = b.judge_matches(cands, "light is made of quanta (photons)")
        self.assertEqual(matched, [True, False])

    def test_judge_falls_back_to_full_word_without_a_model(self):
        with mock.patch.object(b, "_judge_config", return_value=("http://x/v1", "", "")):
            matched = b.judge_matches(["photons and quanta"], "light is made of quanta (photons)")
        self.assertEqual(matched, [True])


class TestGate(unittest.TestCase):
    def test_gate_passes_when_the_engine_beats_the_baseline(self):
        engine = b.ArmResult(arm="llm", suite="s", problems=10, found=7)
        baseline = b.ArmResult(arm="untyped-baseline", suite="s", problems=10, found=0)
        self.assertTrue(b.gate([engine, baseline])["passed"])

    def test_gate_fails_when_the_engine_does_not_beat_the_baseline(self):
        engine = b.ArmResult(arm="llm", suite="s", problems=10, found=0)
        baseline = b.ArmResult(arm="untyped-baseline", suite="s", problems=10, found=2)
        self.assertFalse(b.gate([engine, baseline])["passed"])


class TestJudgeCalibration(unittest.TestCase):
    def test_judge_report_counts_the_confusion_matrix(self):
        # an always-YES judge: every YES is a tp, every NO is a fp
        with mock.patch.object(b, "judge_matches", return_value=[True]):
            r = b.judge_report()
        self.assertEqual(r["tp"], 10)
        self.assertEqual(r["fp"], 10)
        self.assertEqual(r["tn"], 0)
        self.assertEqual(r["fn"], 0)
        self.assertEqual(r["precision"], 0.5)
        self.assertEqual(r["recall"], 1.0)


if __name__ == "__main__":
    unittest.main()
