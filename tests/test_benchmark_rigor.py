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


if __name__ == "__main__":
    unittest.main()
