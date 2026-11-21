"""P1 — unify memory + registries: one evidence/claim architecture with failure tracking.

Validates that the runner's learned knowledge (survivors AND failures) lands in the unified registry as
queryable claims — so research compounds across campaigns and SEXTANT can say a direction failed.
"""
import tempfile
import unittest
from pathlib import Path

from pacland import registry, runner


class TestUnifiedClaims(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old_reg = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)
        self._old = (runner.RECORD, runner.DISCOVERIES, runner.REJECTED,
                     runner.MEMORY, runner.EXPERIMENTS)
        runner.RECORD = Path(self._tmp.name) / "runner.jsonl"
        runner.DISCOVERIES = Path(self._tmp.name) / "discoveries.jsonl"
        runner.REJECTED = Path(self._tmp.name) / "rejected.jsonl"
        runner.MEMORY = Path(self._tmp.name) / "memory.jsonl"
        runner.EXPERIMENTS = Path(self._tmp.name) / "experiments.jsonl"

    def tearDown(self):
        registry.REGISTRY_DIR = self._old_reg
        (runner.RECORD, runner.DISCOVERIES, runner.REJECTED,
         runner.MEMORY, runner.EXPERIMENTS) = self._old

    def test_failed_direction_is_recorded_and_queryable(self):
        runner._append_rejected("mass-gap", "the mass gap is a power law in beta", "falsified")
        failed = registry.failed_directions()
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["payload"]["status"], "failed")
        self.assertIn("power law", failed[0]["payload"]["statement"])

    def test_gated_out_is_a_distinct_disposition(self):
        runner._append_rejected("mass-gap", "some unjustified claim", "gated-out: assumption-audit")
        self.assertEqual(len(registry.claims("gated-out")), 1)
        self.assertEqual(len(registry.claims("failed")), 0)  # gated-out is not falsified

    def test_survivor_becomes_a_claim_with_the_checklist(self):
        c = runner.generate(["ou-curvature", "gronwall-decay"], "combine")
        runner.prove_and_record(c, "OU spectral gap = exactly 1")
        survived = registry.claims("survived")
        self.assertEqual(len(survived), 1)
        p = survived[0]["payload"]
        self.assertIn("spectral gap", p["statement"])
        self.assertEqual(p["status"], "survived")
        self.assertEqual(p["test"], "ou-gap")

    def test_known_unknown_disproven_tallies(self):
        runner._append_rejected("mass-gap", "a falsified claim", "falsified")
        c = runner.generate(["ou-curvature", "gronwall-decay"], "combine")
        runner.prove_and_record(c, "evidence")
        tally = registry.known_unknown_disproven()
        self.assertEqual(tally["failed"], 1)
        self.assertEqual(tally["survived"], 1)
        self.assertEqual(tally["total"], 2)

    def test_memory_prefix_reads_from_registry(self):
        runner._append_rejected("mass-gap", "the mass gap is a power law in beta", "falsified")
        prefix = runner._memory_prefix("mass-gap")
        self.assertIn("FALSIFIED", prefix)
        self.assertIn("power law", prefix)


if __name__ == "__main__":
    unittest.main()
