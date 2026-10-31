"""Acceptance: every delivered command runs, and says the things the docs promise.

The objective's completion criterion is 'a wireless engineer can run one command and get a prediction with a stated
uncertainty, and a measurement either confirms it or falsifies it'. That is only true if the commands work together
— so this test runs them the way a user would.
"""
import io
import json
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "scripts")
sys.path.insert(0, "src")

import chamber_plan  # noqa: E402
import rf_plan  # noqa: E402
import rf_survey_from_iw  # noqa: E402
import validate_streams  # noqa: E402


def capture(fn, argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn(argv)
    return buf.getvalue()


REAL_LINK = """Connected to 14:59:c0:65:57:2d (on wlp2s0)
\tSSID: Telstra3696
\tfreq: 2462.0
\tsignal: -37 dBm
\trx bitrate: 144.4 MBit/s MCS 15 short GI
\ttx bitrate: 144.4 MBit/s MCS 15 short GI
"""


class TestTheSuiteRuns(unittest.TestCase):
    def test_room_plan_prints_a_prediction_and_a_falsifier(self):
        out = capture(rf_plan.main, ["--room", "3,4,2.5", "--antennas", "4"])
        self.assertIn("RF PLAN", out)
        self.assertIn("WHAT WOULD FALSIFY", out)
        self.assertIn("One measurement settles it", out)

    def test_chamber_plan_reaches_a_verdict(self):
        out = capture(chamber_plan.main, ["--chamber", "3,2.5,2.2", "--frequency", "0.3"])
        self.assertIn("VERDICT:", out)

    def test_the_real_link_capture_parses_to_two_streams(self):
        link = rf_survey_from_iw.parse_link(REAL_LINK)
        self.assertEqual(link["nss"], 2)
        self.assertEqual(link["band"], "2.4 GHz")

    def test_the_plan_consumes_that_capture_and_declines_to_overclaim(self):
        p = pathlib.Path(tempfile.mkdtemp()) / "link.txt"
        p.write_text(REAL_LINK)
        out = capture(rf_plan.main, ["--room", "4,5,2.4", "--antennas", "2", "--iw-link", str(p)])
        self.assertIn("streams in use            2 of at most 2", out)
        self.assertIn("NOT DISCRIMINATING", out)

    def test_validation_refuses_to_call_one_row_a_confirmation(self):
        p = pathlib.Path(tempfile.mkdtemp()) / "v.csv"
        p.write_text("x,y,z,nss,snr_db\n0.5,1.2,0.9,2,20.0\n")
        out = capture(validate_streams.main,
                      ["--room", "3,4,2.5", "--data", str(p)])
        self.assertIn("VERDICT:", out)
        # one row can be consistent; it must never say FALSIFIED without evidence
        self.assertNotIn("FALSIFIED — a measurement beat", out)

    def test_json_is_machine_readable_with_statuses(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rf_plan.main(["--room", "3,4,2.5", "--json"])
        out = buf.getvalue()
        d = json.loads(out[out.index("{"):])
        self.assertEqual(d["format"], "rf-plan@1")
        for block in ("modes", "streams", "chamber", "thermal"):
            self.assertIn("status", d[block])


if __name__ == "__main__":
    unittest.main()
