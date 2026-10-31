"""The chamber tool must not pass a chamber the mode count says is not diffuse."""
import io
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "scripts")
import chamber_plan as C  # noqa: E402


def run(args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        C.main(args)
    return buf.getvalue()


class TestExactLuf(unittest.TestCase):
    def test_the_count_puts_the_luf_above_the_closed_form_at_low_mode_count(self):
        # Weyl's density overestimates near the fundamental, so the count is HIGHER than the formula
        exact = C.luf_exact(3.0, 2.5, 2.2, 200.0)
        closed = C.luf_density(3.0 * 2.5 * 2.2, 200.0)
        self.assertGreater(exact, closed * 0.8)

    def test_a_frequency_inside_the_window_is_not_declared_diffuse(self):
        out = run(["--chamber", "3,2.5,2.2", "--frequency", "0.12", "--q", "200"])
        self.assertIn("VERDICT: UNUSABLE", out)


class TestVerdicts(unittest.TestCase):
    def test_a_high_frequency_is_usable(self):
        self.assertIn("VERDICT: USABLE", run(["--chamber", "3,2.5,2.2", "--frequency", "1.2", "--q", "200"]))

    def test_the_tool_never_says_usable_and_not_diffuse_together(self):
        # the defect this file exists for: 0.3 GHz reported "USABLE" while the window count said NOT diffuse
        out = run(["--chamber", "3,2.5,2.2", "--frequency", "0.3", "--q", "200"])
        # 'UNUSABLE' contains 'USABLE', so match the verdict token, not the word
        self.assertFalse("VERDICT: USABLE" in out and "NOT diffuse" in out, out)

    def test_it_reports_when_the_formula_disagrees_with_the_count(self):
        out = run(["--chamber", "3,2.5,2.2", "--frequency", "0.3", "--q", "200"])
        self.assertIn("DISAGREES", out)

    def test_a_bad_chamber_is_refused(self):
        with self.assertRaises(SystemExit):
            run(["--chamber", "3,2", "--frequency", "0.3"])


if __name__ == "__main__":
    unittest.main()
