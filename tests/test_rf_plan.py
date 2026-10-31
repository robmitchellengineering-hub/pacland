"""The one command: it must run, say the required things, and refuse nonsense."""
import io
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "scripts")
sys.path.insert(0, "src")
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

    def test_every_section_carries_a_pass_mark(self):
        # the mechanism, not a specific value: every numbered section must declare its status
        out = run(["--room", "3,4,2.5"])
        self.assertIn("PASS-2", out)
        self.assertIn("PASS-1", out)          # the chamber rule comparison is still PASS-1, and says so
        for n in ("1.", "2.", "3.", "4.", "5."):
            line = next(l for l in out.splitlines() if l.strip().startswith(n))
            self.assertTrue("PASS-" in line, line)

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


class TestMeasuredLink(unittest.TestCase):
    """The plan must consume a real `iw link` capture and say whether it discriminates."""

    def _capture(self):
        import pathlib
        import tempfile
        text = ("Connected to 14:59:c0:65:57:2d (on wlp2s0)\n"
                "\tSSID: Telstra3696\n\tfreq: 2462.0\n\tsignal: -37 dBm\n"
                "\trx bitrate: 144.4 MBit/s MCS 15 short GI\n"
                "\ttx bitrate: 144.4 MBit/s MCS 15 short GI\n")
        p = pathlib.Path(tempfile.mkdtemp()) / "link.txt"
        p.write_text(text)
        return str(p)

    def test_the_measured_band_replaces_the_assumed_one(self):
        out = run(["--room", "4,5,2.4", "--antennas", "2", "--iw-link", self._capture()])
        self.assertIn("2.46 GHz", out)
        self.assertNotIn("5.18 GHz", out)

    def test_it_reports_the_streams_from_the_mcs(self):
        out = run(["--room", "4,5,2.4", "--antennas", "2", "--iw-link", self._capture()])
        self.assertIn("streams in use            2 of at most 2", out)

    def test_it_says_when_the_row_cannot_discriminate(self):
        out = run(["--room", "4,5,2.4", "--antennas", "2", "--iw-link", self._capture()])
        self.assertIn("NOT DISCRIMINATING", out)

    def test_the_falsifier_never_asks_for_a_negative_number(self):
        out = run(["--room", "4,5,2.4", "--antennas", "2", "--iw-link", self._capture()])
        self.assertNotIn("FEWER than 0", out)


class TestOneCommandCoversChambers(unittest.TestCase):
    def test_chamber_flag_adds_the_chamber_section(self):
        out = run(["--room", "3,2.5,2.2", "--band", "0.3", "--chamber"])
        self.assertIn("CHAMBER", out)
        self.assertIn("LUF by exact mode count", out)

    def test_without_the_flag_there_is_no_chamber_section(self):
        out = run(["--room", "3,2.5,2.2", "--band", "0.3"])
        self.assertNotIn("LUF by exact mode count", out)
