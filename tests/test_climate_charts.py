"""The climate figure page must be regenerated, not hand-edited."""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("bcc", ROOT / "scripts" / "build_climate_charts.py")


def _builder():
    mod = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(mod)
    return mod


class TestFiguresAreCurrent(unittest.TestCase):
    def test_committed_page_matches_the_data(self):
        committed = (ROOT / "web" / "climate.html").read_text()
        self.assertEqual(committed, _builder().page(),
                         "web/climate.html is stale — run python3 scripts/build_climate_charts.py")

    def test_every_chart_is_drawn_from_the_data(self):
        html = (ROOT / "web" / "climate.html").read_text()
        self.assertGreaterEqual(html.count("<svg"), 3, "expected three drawn charts")
        self.assertIn("measured imbalance", html)
        # the numbers in the prose must be the numbers in the data
        self.assertIn("0.77", html)
        self.assertIn("GISS-E2-1-G", html)

    def test_the_reference_line_survives_the_bars(self):
        html = (ROOT / "web" / "climate.html").read_text()
        self.assertIn('stroke="#ffffff" stroke-width="4.5"', html,
                      "the 0.77 W/m2 reference line needs its white halo or it vanishes over the bars")

    def test_no_chart_library_and_no_scripts(self):
        html = (ROOT / "web" / "climate.html").read_text()
        self.assertNotIn("<script", html, "figures must render without JavaScript")
        self.assertNotIn("cdn.", html)


if __name__ == "__main__":
    unittest.main()
