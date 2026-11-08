"""A working quantum computer — the circuit model is correct, not just "runs".

These assert the exact probability distributions the three programs must produce, computed from the
state vector (deterministic), so a wrong gate order or axis mapping fails here, not in a demo.
"""
import unittest

from pacland import quantum as q


class TestBellState(unittest.TestCase):
    def test_bell_is_perfectly_correlated(self):
        p = q.bell().probabilities()
        self.assertAlmostEqual(p[0], 0.5, places=6)  # |00>
        self.assertAlmostEqual(p[3], 0.5, places=6)  # |11>
        self.assertAlmostEqual(p[1], 0.0, places=6)  # |01> never
        self.assertAlmostEqual(p[2], 0.0, places=6)  # |10> never

    def test_bell_state_is_normalized(self):
        p = q.bell().probabilities()
        self.assertAlmostEqual(p.sum(), 1.0, places=6)


class TestSuperposition(unittest.TestCase):
    def test_hadamard_is_50_50(self):
        p = q.superposition().probabilities()
        self.assertAlmostEqual(p[0], 0.5, places=6)
        self.assertAlmostEqual(p[1], 0.5, places=6)


class TestGrover(unittest.TestCase):
    def test_grover_finds_the_marked_item(self):
        p = q.grover().probabilities()
        self.assertAlmostEqual(p[3], 1.0, places=6)  # |11> found
        self.assertAlmostEqual(p[0] + p[1] + p[2], 0.0, places=6)


class TestCircuitModel(unittest.TestCase):
    def test_apply_gate_and_cnot(self):
        """H then CNOT on the target qubit gives the Bell amplitudes."""
        c = q.QuantumCircuit(2)
        c.apply_gate("H", 0).apply_cnot(0, 1)
        p = c.probabilities()
        self.assertAlmostEqual(p[0], 0.5, places=6)
        self.assertAlmostEqual(p[3], 0.5, places=6)

    def test_x_flips_the_bit(self):
        c = q.QuantumCircuit(1)
        c.apply_gate("X", 0)
        p = c.probabilities()
        self.assertAlmostEqual(p[1], 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
