"""The one command: it must run, say the required things, and refuse nonsense."""
import io
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "scripts")
import rf_plan  # noqa: E402


def run(args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        rf_plan.main(args)
    return buf.getvalue()


class TestOneCommand(unittest.TestCase):
    def test_it_produces_every_section(self):
        out = run(["--room", "3,4,2.5", "--antennas", "4", "--snr", "20"])
        for section in ("MODE STRUCTURE", "STREAMS", "PLACEMENT LEVERS", "CHAMBER QUESTION",
                        "THERMAL CEILING", "WHAT WOULD FALSIFY"):
            self.assertIn(section, out)

    def test_it_carries_pass_marks(self):
        out = run(["--room", "3,4,2.5"])
        self.assertIn("PASS-2", out)
        self.assertIn("PASS-1", out)          # the thermal bound is PASS-1 and says so

    def test_it_states_a_falsifier(self):
        self.assertIn("One measurement settles it", run(["--room", "3,4,2.5"]))

    def test_a_bad_room_is_refused(self):
        with self.assertRaises(SystemExit):
            run(["--room", "3,4"])

    def test_a_negative_dimension_is_refused(self):
        with self.assertRaises(SystemExit):
            run(["--room", "-3,4,2.5"])


if __name__ == "__main__":
    unittest.main()
