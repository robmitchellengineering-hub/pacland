"""Report tests — the CLI views cannot drift from the artifacts they describe."""
import sys
import unittest
from io import StringIO
from unittest import mock

from pacland.economics import report


class TestModelsReport(unittest.TestCase):
    def setUp(self):
        self.text = report.models_report()

    def test_every_roster_row_appears(self):
        from pacland.economics.model_roster import ROSTER

        for m in ROSTER:
            self.assertIn(m.name[:20], self.text)

    def test_it_states_the_outcome_rule(self):
        self.assertIn("taking the test is not passing it", self.text)

    def test_it_carries_the_audit_verdict(self):
        self.assertIn("audit:", self.text)


class TestConstraintsReport(unittest.TestCase):
    def test_rank_and_count_are_printed(self):
        text = report.constraints_report()
        self.assertIn("independent rank 8", text)
        self.assertIn("constraints 11", text)


class TestRealtimeReport(unittest.TestCase):
    def setUp(self):
        self.text = report.realtime_report()

    def test_all_three_sections_are_present(self):
        self.assertIn("statistical benchmarks", self.text)
        self.assertIn("published nowcast", self.text)
        self.assertIn("no-change", self.text)

    def test_the_falsification_is_reported(self):
        self.assertIn("FALSIFIED", self.text)

    def test_the_nowcast_ratio_matches_the_module(self):
        from pacland.economics import gdpnow

        self.assertIn(f"{gdpnow.evaluate()['ratio']['mae']:.2f}x", self.text)


class TestCli(unittest.TestCase):
    def _run(self, argv):
        from pacland import cli

        buf = StringIO()
        with mock.patch.object(sys, "argv", argv), mock.patch("sys.stdout", buf):
            cli.main()
        return buf.getvalue()

    def test_models_flag(self):
        out = self._run(["pacland", "economics", "--models"])
        self.assertIn("MODEL ROSTER", out)

    def test_constraints_flag(self):
        out = self._run(["pacland", "economics", "--constraints"])
        self.assertIn("CONSTRAINT SET", out)

    def test_realtime_flag(self):
        out = self._run(["pacland", "economics", "--realtime"])
        self.assertIn("REAL-TIME RESULTS", out)

    def test_default_is_still_the_deficit(self):
        out = self._run(["pacland", "economics"])
        self.assertIn("ECONOMICS VERIFICATION DEFICIT", out)


if __name__ == "__main__":
    unittest.main()
