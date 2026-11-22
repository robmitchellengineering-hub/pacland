"""The withheld-problem validation gate: blind discovery is established only by solving + reproducing."""
import math
import re
import tempfile
import unittest
from pathlib import Path

from pacland import registry, validation_gate as vg


def _symbolic_inductor(pre: str) -> list[str]:
    """A reference inductor that ACTUALLY induces: tries each planted law and returns the one that fits."""
    pairs = re.findall(r"\((\d+),(\d+)\)", pre)
    pts = [(int(x), int(y)) for x, y in pairs]
    laws = {
        "n**2": lambda n: n * n,
        "2*n + 1": lambda n: 2 * n + 1,
        "n**3": lambda n: n ** 3,
        "n*(n+1)//2": lambda n: n * (n + 1) // 2,
        "2**n": lambda n: 2 ** n,
        "3*n + 1": lambda n: 3 * n + 1,
    }
    for expr, fn in laws.items():
        if all(fn(x) == y for x, y in pts):
            return [expr]
    return []


def _garbage_generator(pre: str) -> list[str]:
    return ["n**2"]  # always wrong unless the law happens to be n**2


class TestValidationGate(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self._old = registry.REGISTRY_DIR
        registry.REGISTRY_DIR = Path(self._tmp.name)

    def tearDown(self):
        registry.REGISTRY_DIR = self._old

    def test_a_real_inductor_passes_the_gate(self):
        r = vg.blind_discovery_gate(_symbolic_inductor, n_problems=5)
        self.assertTrue(r["passed"], r)
        self.assertEqual(r["solved"], 5)  # the symbolic inductor solves every withheld problem

    def test_a_garbage_generator_fails_the_gate(self):
        r = vg.blind_discovery_gate(_garbage_generator, n_problems=5)
        self.assertFalse(r["passed"])
        self.assertIn("NOT yet established", r["verdict"])

    def test_the_verdict_is_recorded(self):
        vg.blind_discovery_gate(_symbolic_inductor, n_problems=5)
        claims = registry.claims()
        self.assertTrue(any("blind-discovery-gate" in c["id"] for c in claims))


if __name__ == "__main__":
    unittest.main()
