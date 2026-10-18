"""Vault tests — the guard-enforced admission loop, plus seeded-fault mutations.

Proves the #1 invariant: a computation that fails a guard is REFUSED (no
certificate), and a computation that passes is admitted. Each guard has a
seeded fault it must catch.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import math
import unittest

from pacland.oracle import ToricBackground, exact_toric_oracle
from pacland.vault import run_vault


def guard_finite(obs):
    v = obs.get("gauge_coupling_log")
    ok = v is not None and math.isfinite(v)
    return ok, f"gauge_coupling_log={v}"


def guard_negative(obs):
    # -ln(1 + tadpole) is <= 0 for any valid toy background
    v = obs.get("gauge_coupling_log")
    ok = v is not None and v <= 0.0
    return ok, f"gauge_coupling_log={v} (must be <= 0)"


GUARDS = [("finite", guard_finite), ("nonpositive", guard_negative)]


class TestVault(unittest.TestCase):
    def test_passing_run_is_admitted(self):
        v = run_vault(exact_toric_oracle, ToricBackground("toy", (1, 0, 0)), GUARDS)
        self.assertTrue(v.passed)
        self.assertEqual(v.failures, ())

    def test_nonfinite_output_is_refused(self):
        # seeded fault: the oracle returns NaN (a numerical blow-up)
        def nan_oracle(genotype):
            return {"gauge_coupling_log": float("nan")}

        v = run_vault(nan_oracle, None, GUARDS)
        self.assertFalse(v.passed)
        self.assertIn("finite", v.failures[0])

    def test_wrong_sign_is_refused(self):
        # seeded fault: a positive coupling log (impossible for this toy)
        def wrong_oracle(genotype):
            return {"gauge_coupling_log": +0.5}

        v = run_vault(wrong_oracle, None, GUARDS)
        self.assertFalse(v.passed)
        self.assertIn("nonpositive", v.failures[0])

    def test_missing_output_is_refused_not_silent(self):
        # seeded fault: the oracle omits the observable — must fail, not pass
        def empty_oracle(genotype):
            return {}

        v = run_vault(empty_oracle, None, GUARDS)
        self.assertFalse(v.passed)
        self.assertEqual(len(v.failures), 2)

    def test_guard_that_raises_is_refused(self):
        # a guard that errors is a failure, never a silent pass
        def raising_guard(obs):
            raise RuntimeError("boom")

        v = run_vault(exact_toric_oracle, ToricBackground("toy", (1, 0, 0)),
                      [("raising", raising_guard)])
        self.assertFalse(v.passed)
        self.assertIn("guard raised RuntimeError", v.failures[0])


if __name__ == "__main__":
    unittest.main()
