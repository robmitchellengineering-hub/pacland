"""SW linearised model tests — parsing, the steady-state check, and the fixture."""
import json
import pathlib
import unittest

from pacland.economics import sw2007, sw_linear as L

FIXTURE = pathlib.Path(__file__).resolve().parents[1] / "data" / "economics" / "sw_mod.json"

#: A miniature model block with the same shapes the real file uses: two equilibrium
#: conditions, one measurement equation with a constant, and a #definition.
TINY = """
parameters calfa cbeta ctou constepinf ctrend;
calfa=.3;
cbeta=.99;
ctou=.025;
constepinf=0.5;
ctrend=0.4;
model(linear);
#crk=(cbeta^(-1))*(1+ctrend/100)^1 - (1-ctou);
#cky=calfa/crk;
  y = calfa*k + (1-calfa)*lab ;
  inv = k - k(-1) + ctou ;
  pinfobs = pinf + constepinf ;
end;
"""


class TestParser(unittest.TestCase):
    def test_it_splits_equations_and_definitions(self):
        p = L.parse(TINY, use_posterior=False)
        self.assertEqual(len(p.equations), 3)
        self.assertEqual(len(p.equilibrium), 2)
        self.assertEqual(len(p.measurement), 1)

    def test_definitions_are_evaluated(self):
        p = L.parse(TINY, use_posterior=False)
        self.assertIn("crk", p.definitions)
        self.assertAlmostEqual(p.definitions["crk"], 1 / 0.99 * 1.004 - 0.975, places=9)

    def test_timing_notation_is_translated(self):
        self.assertEqual(L.to_python("x = a*y(-1) + b*z(+1)"), "x = a*y_lag + b*z_lead")

    def test_no_model_block_is_refused(self):
        with self.assertRaises(ValueError):
            L.parse("nothing here")


class TestFixture(unittest.TestCase):
    def setUp(self):
        self.f = json.loads(FIXTURE.read_text())

    def test_counts(self):
        self.assertEqual(self.f["n_equations"], 40)
        self.assertEqual(self.f["n_equilibrium"], 34)
        self.assertEqual(self.f["n_measurement"], 6)

    def test_no_equilibrium_equation_failed(self):
        self.assertEqual(self.f["equilibrium_bad"], [])

    def test_rates_match_the_paper_and_this_repo(self):
        r = self.f["rates"]
        self.assertLess(abs(r["real_annual_pct"] - 3.0), 0.6)
        self.assertLess(abs(r["nominal_annual_pct"] - 6.0), 0.6)
        self.assertLess(abs(r["nominal_annual_pct"] - sw2007.nominal_rate_annual_pct()), 0.05)

    def test_shares_sum_to_one(self):
        self.assertAlmostEqual(self.f["rates"]["shares_sum"], 1.0, places=9)

    def test_the_source_is_pinned(self):
        self.assertIn("Smets_Wouters_2007", self.f["source"])
        self.assertEqual(len(self.f["sha256"]), 64)


class TestTheInjectedFault(unittest.TestCase):
    def test_a_broken_steady_state_is_detected(self):
        # the seeded fault: a definition that no longer matches the equations
        p = L.parse(TINY, overrides={"ctou": 0.5}, use_posterior=False)
        res = L.check(p)
        self.assertFalse(res["ok"])
        self.assertTrue(res["equilibrium_bad"])


if __name__ == "__main__":
    unittest.main()
