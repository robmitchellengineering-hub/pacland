"""P0 #2 — the end-to-end autonomous test: proposal → falsify → challenge gate → evidence → record.

Validates the WHOLE loop in one shot, not the pieces: a candidate that the falsifier actually tests
and that survives must make it through the eight-stage challenge gate to the evidence/discovery
record — it must NOT be gated-out on a bad falsifier lookup. This is the test that would have caught
the name-vs-id regression (the challenge sequence dropping a candidate the runner had already tested).
"""
import tempfile
import unittest
from pathlib import Path

from pacland import runner


class TestEndToEndAutonomous(unittest.TestCase):
    def _run(self, tmp: str) -> dict:
        # isolate every persistent store so the test never touches the real record
        old = (runner.RECORD, runner.DISCOVERIES, runner.REJECTED, runner.MEMORY, runner.EXPERIMENTS)
        runner.RECORD = Path(tmp) / "runner.jsonl"
        runner.DISCOVERIES = Path(tmp) / "discoveries.jsonl"
        runner.REJECTED = Path(tmp) / "rejected.jsonl"
        runner.MEMORY = Path(tmp) / "memory.jsonl"
        runner.EXPERIMENTS = Path(tmp) / "experiments.jsonl"

        # the LLM search returns the deterministic grounded candidate (a REAL falsifier: ou-gap)
        def fake_generate(self, problem, budget):
            return [runner.generate(["ou-curvature", "gronwall-decay"], "combine")]

        old_gen = runner.LlmSearch.generate
        runner.LlmSearch.generate = fake_generate
        old_env = dict(runner.os.environ)
        runner.os.environ.pop("SEXTANT_LLM_MODEL", None)  # no LLM → prove defers, survivor still recorded
        try:
            return runner.run_autonomous("confinement-frontier", rounds=1, budget=1)
        finally:
            (runner.RECORD, runner.DISCOVERIES, runner.REJECTED,
             runner.MEMORY, runner.EXPERIMENTS) = old
            runner.LlmSearch.generate = old_gen
            runner.os.environ.clear()
            runner.os.environ.update(old_env)

    def test_survivor_reaches_the_evidence_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._run(tmp)
        round0 = out["rounds"][0]
        survivors = round0["survivors"]
        self.assertTrue(survivors, f"a falsifier-tested candidate was not recorded as a survivor: {round0}")
        # the survivor entry carries the statement (the evidence record) — a proposal reached evidence
        self.assertIn("spectral gap", survivors[0]["statement"])

    def test_survivor_is_not_gated_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._run(tmp)
        gated = [p for p in out["rounds"][0]["proposals"] if p.get("verdict") == "gated-out"]
        self.assertFalse(gated, f"a falsifier-tested candidate was gated out: {gated}")

    def test_challenge_gate_passes_on_a_tested_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self._run(tmp)
        survivor = out["rounds"][0]["survivors"][0]
        self.assertEqual(survivor["gate"], "PASS")
        # the gate's own record shows the falsifier result was used, not a failed lookup
        challenges = survivor["challenges"]
        boundary = challenges.get("boundary-testing")
        self.assertEqual(boundary, "PASS")


if __name__ == "__main__":
    unittest.main()
