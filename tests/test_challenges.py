"""The graded challenge sequence must not pass vacuously — no catalog match is NOT_APPLICABLE, and
formal-verification requires a real theorem declaration."""
import unittest
from unittest import mock

from pacland import challenges as ch


class TestKnownResults(unittest.TestCase):
    def test_no_catalog_match_is_not_applicable_not_pass(self):
        # a bare hypothesis that names no catalog claim must be NOT_APPLICABLE, not PASS
        class _Sextant:
            CATALOG = {}

        with mock.patch.object(ch, "_import_sextant", return_value=(_Sextant(), None)):
            results = ch.run_sequence(ch.Candidate("bare", "some new hypothesis"))
        kr = next(r for r in results if r.name == "known-results")
        self.assertEqual(kr.verdict, "NOT_APPLICABLE")

    def test_named_forced_claim_is_failed(self):
        class _Sextant:
            CATALOG = {"chsh": {"verdict": "FORCED", "claim": "the quantum bound is 2√2"}}

        with mock.patch.object(ch, "_import_sextant", return_value=(_Sextant(), None)):
            results = ch.run_sequence(ch.Candidate("chsh", "chsh is wrong"))
        kr = next(r for r in results if r.name == "known-results")
        self.assertEqual(kr.verdict, "FAIL")


class TestLeanCheck(unittest.TestCase):
    def test_no_target_is_not_applicable(self):
        v, _ = ch._lean_check("")
        self.assertEqual(v, "NOT_APPLICABLE")

    def test_undeclared_theorem_is_inconclusive_not_pass(self):
        v, ev = ch._lean_check("DefinitelyNotARealTheoremName")
        self.assertEqual(v, "INCONCLUSIVE")
        self.assertIn("not declared", ev)


class TestModelJudge(unittest.TestCase):
    def test_logical_consistency_passes_when_consistent(self):
        with mock.patch.object(ch, "_ask_judge", return_value="INTERNALLY CONSISTENT"):
            v, ev = ch._model_judge("logical-consistency", "a hypothesis")
        self.assertEqual(v, "PASS")

    def test_logical_consistency_fails_when_contradictory(self):
        with mock.patch.object(ch, "_ask_judge", return_value="CONTRADICTORY"):
            v, ev = ch._model_judge("logical-consistency", "a hypothesis")
        self.assertEqual(v, "FAIL")

    def test_is_inconclusive_without_a_judge(self):
        with mock.patch.object(ch, "_ask_judge", return_value=None):
            v, ev = ch._model_judge("alternative-explanation", "a hypothesis")
        self.assertEqual(v, "INCONCLUSIVE")

    def test_run_sequence_uses_the_judge_for_model_stages(self):
        with mock.patch.object(ch, "_import_sextant", return_value=(None, None)):
            with mock.patch.object(ch, "_ask_judge",
                                   side_effect=["INTERNALLY CONSISTENT", "JUSTIFIED", "NO"]):
                results = ch.run_sequence(ch.Candidate("bare", "some hypothesis"))
        verdicts = {r.name: r.verdict for r in results}
        self.assertEqual(verdicts["logical-consistency"], "PASS")
        self.assertEqual(verdicts["assumption-audit"], "PASS")
        self.assertEqual(verdicts["alternative-explanation"], "PASS")  # NO -> no simpler theory


if __name__ == "__main__":
    unittest.main()
