"""P2 — the supervisor: identify missing lemmas, track failed approaches, choose the next frontier."""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, supervisor


class TestSupervisor(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_identify_missing_lemmas_from_a_temp_tree(self):
        d = Path(self._tmp.name) / "proof"
        d.mkdir(parents=True)
        (d / "Gap.lean").write_text("theorem gap_theorem : True := by\n  sorry\n")
        (d / "Done.lean").write_text("theorem done_theorem : True := by trivial\n")
        gaps = supervisor.identify_missing_lemmas(proof_dir=d)
        self.assertIn("gap_theorem (Gap.lean)", gaps)
        self.assertFalse(any("done_theorem" in g for g in gaps))

    def test_failed_approaches_reads_claims(self):
        registry.record_claim("claim-x", "a failed thing", "failed", reason="no")
        self.assertEqual(len(supervisor.failed_approaches()), 1)

    def test_choose_next_frontier_returns_a_problem(self):
        f = supervisor.choose_next_frontier()
        self.assertTrue(f.get("problem"))
        self.assertTrue(f.get("next_sublemma"))

    def test_frontier_skips_failed_sublemmas(self):
        # a failed sub-lemma of a known open problem is skipped when choosing the frontier
        from pacland import hypotheses, runner
        # record the top problem's FIRST candidate as failed, then verify the frontier skips it
        top = runner.rank_open_by_eig()[0][0]
        first = hypotheses.HYPOTHESES[top]["candidates"][0]["hypothesis"]
        registry.record_claim("claim-fail", first, "failed", reason="falsified")
        f = supervisor.choose_next_frontier()
        if f.get("problem") == top:
            self.assertNotEqual(f.get("next_sublemma"), first)

    def test_report_is_consolidated(self):
        r = supervisor.supervisor_report()
        self.assertIn("missing_lemmas", r)
        self.assertIn("failed_approaches", r)
        self.assertIn("frontier", r)


if __name__ == "__main__":
    unittest.main()
