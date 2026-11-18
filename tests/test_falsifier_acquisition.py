"""Falsifier acquisition closes the loop: a synthesized falsifier becomes an executable test that
retries the hypothesis."""
import unittest
from unittest import mock

from pacland import falsifier_acquisition as fa
from pacland import runner


class TestBuildAndRunFalsifier(unittest.TestCase):
    def test_builds_and_runs_a_synthesized_falsifier(self):
        code = ("def falsifier():\n    x = 5\n    if x > 0:\n"
                "        return (True, 'positive value survived')\n    return (False, 'refuted')")
        with mock.patch.object(runner, "_ask_llm", return_value=code):
            out = fa.build_and_run_falsifier("the value is positive", "http://x", "", "m")
        self.assertTrue(out["ran"])
        self.assertTrue(out["survived"])
        self.assertEqual(out["evidence"], "positive value survived")
        self.assertIn("synthesized", out["note"])

    def test_refuses_without_a_model(self):
        out = fa.build_and_run_falsifier("hypothesis", "", "", "")
        self.assertFalse(out["ran"])
        self.assertIn("no LLM", out["reason"])

    def test_vacuous_falsifier_is_rejected(self):
        code = "def falsifier():\n    return (True, 'survived')"
        with mock.patch.object(runner, "_ask_llm", return_value=code):
            out = fa.build_and_run_falsifier("the value is positive", "http://x", "", "m")
        self.assertFalse(out["ran"])
        self.assertIn("vacuous", out["reason"])

    def test_crashing_code_is_reported_not_crashed(self):
        code = ("def falsifier():\n    x = 1 / 0\n    if x > 0:\n"
                "        return (True, 'positive')\n    return (False, 'refuted')")
        with mock.patch.object(runner, "_ask_llm", return_value=code):
            out = fa.build_and_run_falsifier("the value is positive", "http://x", "", "m")
        self.assertFalse(out["ran"])
        self.assertIn("failed", out["reason"])


class TestAcquireBuildRetry(unittest.TestCase):
    def test_autonomous_open_entry_carries_the_synthesized_test(self):
        cand = runner.Candidate(id="x", statement="a hypothesis", falsifier="f",
                                strategy="llm-search", source_facts=(), test="")
        with mock.patch.object(runner.LlmSearch, "generate", return_value=[cand]):
            with mock.patch.object(runner, "_falsify", return_value=(False, None, "needs a falsifier")):
                with mock.patch.object(fa, "acquire", return_value={"verdict": "no falsifier found"}):
                    with mock.patch.object(fa, "build_and_run_falsifier",
                                           return_value={"ran": True, "survived": True,
                                                         "evidence": "s", "note": "synthesized"}):
                        out = runner.run_autonomous("mass-gap")
        entry = out["rounds"][0]["open"][0]
        self.assertEqual(entry["candidate_verdict"], "survived")

    def test_unbuildable_falsifier_is_recorded_as_a_job(self):
        cand = runner.Candidate(id="x", statement="a hypothesis", falsifier="f",
                                strategy="llm-search", source_facts=(), test="")
        with mock.patch.object(runner.LlmSearch, "generate", return_value=[cand]):
            with mock.patch.object(runner, "_falsify", return_value=(False, None, "needs a falsifier")):
                with mock.patch.object(fa, "acquire", return_value={"synthesized_falsifier": "a test"}):
                    with mock.patch.object(fa, "build_and_run_falsifier",
                                           return_value={"ran": False, "reason": "code failed"}):
                        with mock.patch.object(fa, "FALSIFIER_JOBS",
                                               runner.REPO_ROOT / "runs" / "test-jobs.jsonl"):
                            out = runner.run_autonomous("mass-gap")
        entry = out["rounds"][0]["open"][0]
        self.assertIn("falsifier_job", entry)


class TestFalsifierJobs(unittest.TestCase):
    def test_record_list_and_claim_a_job(self):
        with mock.patch.object(fa, "FALSIFIER_JOBS", fa.REPO_ROOT / "runs" / "test-jobs.jsonl"):
            fa.FALSIFIER_JOBS.unlink(missing_ok=True)
            job_id = fa.record_falsifier_job("a claim", "a proposed test", "code failed")
            self.assertTrue(job_id)
            self.assertEqual(len(fa.list_falsifier_jobs("queued")), 1)
            self.assertTrue(fa.claim_falsifier_job(job_id))
            self.assertEqual(len(fa.list_falsifier_jobs("in-progress")), 1)
            self.assertTrue(fa.mark_falsifier_built(job_id, "verify_x"))
            self.assertEqual(len(fa.list_falsifier_jobs("built")), 1)
            fa.FALSIFIER_JOBS.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
