"""The SEXTANT runner loop: generate → test → promote/drop → record (no prose, structured)."""
import tempfile
import unittest
from pathlib import Path

from pacland import runner


class TestRunner(unittest.TestCase):
    def test_generate_combine_ou_gap(self):
        c = runner.generate(["ou-curvature", "gronwall-decay"], "combine")
        self.assertEqual(c.id, "ou-gap-lower-bound")
        self.assertEqual(c.strategy, "combine")
        self.assertEqual(c.test, "ou-gap")

    def test_generate_specialize_su2(self):
        c = runner.generate(["confinement-frontier"], "specialize")
        self.assertEqual(c.id, "su2-weak-coupling-area-law")
        self.assertEqual(c.strategy, "specialize")
        self.assertEqual(c.test, "su2-weak-coupling")

    def test_run_ou_gap_survives(self):
        c = runner.generate(["ou-curvature", "gronwall-decay"], "combine")
        v = runner.run(c)
        self.assertTrue(v.survived)
        self.assertEqual(v.verdict, "SURVIVED")
        self.assertIn("spectral gap = exactly 1", v.evidence)

    def test_advance_promotes_and_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_rec, old_disc = runner.RECORD, runner.DISCOVERIES
            runner.RECORD = Path(tmp) / "runner.jsonl"
            runner.DISCOVERIES = Path(tmp) / "discoveries.jsonl"
            try:
                v = runner.advance(["ou-curvature", "gronwall-decay"], "combine")
                self.assertTrue(v.survived)
                self.assertTrue(runner.DISCOVERIES.exists())
                self.assertTrue(runner.RECORD.exists())
                self.assertEqual(len(runner.list_discoveries()), 1)
                self.assertEqual(runner.list_discoveries()[0]["id"], "ou-gap-lower-bound")
            finally:
                runner.RECORD, runner.DISCOVERIES = old_rec, old_disc

    def test_decompose_emits_next_sublemma(self):
        c = runner.next_sublemma("ym-mass-gap")
        self.assertEqual(c.strategy, "decompose")
        self.assertIn("Dobrushin", c.statement)
        self.assertTrue(c.falsifier)
        self.assertEqual(c.source_facts, ("ym-mass-gap",))

    def test_decompose_runnable_maps_to_falsifier(self):
        # the area-law candidate of confinement-frontier has a runnable Creutz-ratio falsifier
        c = runner.generate(["confinement-frontier"], "specialize")
        self.assertEqual(c.test, "su2-weak-coupling")

    def test_manual_candidate_is_not_an_error(self):
        c = runner.next_sublemma("ym-mass-gap")
        v = runner.run(c)
        self.assertEqual(v.verdict, "MANUAL")
        self.assertIsNone(v.survived)
        self.assertIn("thinking agent", v.evidence)


class TestProveLoop(unittest.TestCase):
    """The prover loop (Level 1) — propose → check → repair → record, with a stubbed LLM and kernel
    so the wiring is tested without needing a live model or the Lean toolchain."""

    def test_prove_requires_llm_config(self):
        old = dict(runner.os.environ)
        runner.os.environ.pop("SEXTANT_LLM_MODEL", None)
        try:
            res = runner.prove("theorem x : True := by\n  sorry\n")
            self.assertFalse(res["ok"])
            self.assertIn("no LLM", res["error"])
        finally:
            runner.os.environ.clear()
            runner.os.environ.update(old)

    def test_prove_succeeds_first_try(self):
        good_code = "theorem x : True := by trivial"
        calls = {"n": 0}

        def fake_ask(prompt, endpoint, key, model):
            calls["n"] += 1
            return good_code

        def fake_check(code):
            ok = "trivial" in code and "sorry" not in code
            return (ok, "" if ok else "kernel error")

        old_ask, old_check, old_cfg = runner._ask_llm, runner._check_lean, runner._llm_config
        runner._ask_llm, runner._check_lean = fake_ask, fake_check
        runner._llm_config = lambda: ("http://x/v1", "", "m")
        try:
            res = runner.prove("theorem x : True := by\n  sorry\n")
            self.assertTrue(res["ok"])
            self.assertEqual(res["attempts"], 1)
            self.assertEqual(res["checked_by"], "lake env lean")
            self.assertEqual(calls["n"], 1)
        finally:
            runner._ask_llm, runner._check_lean, runner._llm_config = old_ask, old_check, old_cfg

    def test_prove_repairs_after_error(self):
        def fake_ask(prompt, endpoint, key, model):
            # first proposal is bad (the "sorry" survives), second is good — and the second prompt
            # must carry the kernel error (the repair signal)
            fake_ask.n += 1
            return "theorem x : True := by sorry" if fake_ask.n == 1 else "theorem x : True := by trivial"
        fake_ask.n = 0

        def fake_check(code):
            ok = "trivial" in code and "sorry" not in code
            return (ok, "" if ok else "kernel: sorry")

        old_ask, old_check, old_cfg = runner._ask_llm, runner._check_lean, runner._llm_config
        runner._ask_llm, runner._check_lean = fake_ask, fake_check
        runner._llm_config = lambda: ("http://x/v1", "", "m")
        try:
            res = runner.prove("theorem x : True := by\n  sorry\n", attempts=3)
            self.assertTrue(res["ok"])
            self.assertEqual(res["attempts"], 2)
            self.assertEqual(fake_ask.n, 2)
        finally:
            runner._ask_llm, runner._check_lean, runner._llm_config = old_ask, old_check, old_cfg

    def test_prove_gives_up_after_attempts(self):
        def fake_ask(prompt, endpoint, key, model):
            return "theorem x : True := by sorry"

        def fake_check(code):
            return (False, "kernel: sorry")

        old_ask, old_check, old_cfg = runner._ask_llm, runner._check_lean, runner._llm_config
        runner._ask_llm, runner._check_lean = fake_ask, fake_check
        runner._llm_config = lambda: ("http://x/v1", "", "m")
        try:
            res = runner.prove("theorem x : True := by\n  sorry\n", attempts=2)
            self.assertFalse(res["ok"])
            self.assertEqual(res["attempts"], 2)
            self.assertIn("sorry", res["last_error"])
        finally:
            runner._ask_llm, runner._check_lean, runner._llm_config = old_ask, old_check, old_cfg


if __name__ == "__main__":
    unittest.main()
