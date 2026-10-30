"""The existence engine — an exhibited object is a positive result, and it must be checkable by hand."""
import unittest

from pacland.exactness import existence as E
from pacland.exactness import windows as W


class TestTheShippedQuestions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = {x.question: x for x in E.run_all()}

    def test_at_least_one_question_returns_an_object(self):
        found = [x for x in self.q.values() if x.found is not None]
        self.assertGreaterEqual(len(found), 1)

    def test_the_shipped_witnesses_actually_satisfy_their_predicates(self):
        checks = {
            "a primitive pair with zero tadpole whose halves are non-zero and not proportional":
                E.null_tadpole_split,
            "a primitive pair with zero tadpole and no zero component":
                E.null_tadpole_no_zero_component,
        }
        for name, pred in checks.items():
            x = self.q[name]
            self.assertIsNotNone(x.found, name)
            self.assertTrue(pred(x.found["flux"], x.found["tadpole"]), name)

    def test_the_witness_tadpole_recomputes_from_the_flux(self):
        for x in self.q.values():
            if x.found is None:
                continue
            f = x.found["flux"]
            n = int(W.tadpoles([f])[0])
            self.assertEqual(n, x.found["tadpole"])

    def test_the_witness_is_primitive(self):
        for x in self.q.values():
            if x.found is None:
                continue
            self.assertTrue(W.primitive(x.found["flux"]))

    def test_the_odd_tadpole_question_is_none_in_this_window(self):
        x = self.q["a primitive pair with N = 1 and no zero component"]
        self.assertEqual(x.verdict, "NONE")
        self.assertIn("theorem about this window", x.states)

    def test_every_verdict_names_the_window(self):
        for x in self.q.values():
            self.assertIn("531441", x.window)


class TestTheEngineCanSayNo(unittest.TestCase):
    def test_an_impossible_property_returns_none(self):
        x = E.find(lambda f, t: t > 100, "tadpole above 100", "none exists in a |.|<=1 window")
        self.assertEqual(x.verdict, "NONE")
        self.assertEqual(x.matches, 0)

    def test_a_satisfiable_property_returns_a_least_norm_witness(self):
        x = E.find(lambda f, t: t == 2, "tadpole exactly 2", "test")
        self.assertEqual(x.verdict, "FOUND")
        self.assertEqual(x.found["tadpole"], 2)
        self.assertLessEqual(sum(abs(v) for v in x.found["flux"]), 4)

    def test_the_witness_is_canonical_across_runs(self):
        a = E.find(lambda f, t: t == 2, "q", "w")
        b = E.find(lambda f, t: t == 2, "q", "w")
        self.assertEqual(a.found["flux"], b.found["flux"])


if __name__ == "__main__":
    unittest.main()


class TestThePositivesPage(unittest.TestCase):
    """The page is generated, so it cannot drift from the engines or accumulate unbacked claims."""

    def test_the_page_is_current(self):
        import subprocess
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        r = subprocess.run([sys.executable, str(root / "scripts" / "positives.py"), "--check"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_every_entry_carries_a_command(self):
        import subprocess
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        text = (root / "docs" / "known-positives.md").read_text()
        claims = [ln for ln in text.splitlines() if ln.startswith("- **")]
        commands = [ln for ln in text.splitlines() if "reproduce:" in ln]
        self.assertGreater(len(claims), 5)
        self.assertEqual(len(claims), len(commands))

    def test_it_records_an_object_and_a_none(self):
        import sys
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        text = (root / "docs" / "known-positives.md").read_text()
        self.assertIn("Exhibited Object", text)
        self.assertIn("Theorem In A Window", text)
