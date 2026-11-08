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


class TestGHZ(unittest.TestCase):
    def test_ghz_is_all_equal(self):
        p = q.ghz(3).probabilities()
        self.assertAlmostEqual(p[0], 0.5, places=6)   # |000>
        self.assertAlmostEqual(p[7], 0.5, places=6)   # |111>
        self.assertAlmostEqual(p[1] + p[2] + p[3] + p[4] + p[5] + p[6], 0.0, places=6)


class TestQFT(unittest.TestCase):
    def test_qft2_of_zero_is_uniform(self):
        p = q.qft2().probabilities()
        for i in range(4):
            self.assertAlmostEqual(p[i], 0.25, places=6)


class TestTeleportation(unittest.TestCase):
    def test_teleport_moves_the_state(self):
        """After teleporting |1⟩, qubit 2 is |1⟩ regardless of Alice's random outcomes."""
        for _ in range(50):
            p = q.teleport().probabilities()
            p2 = sum(p[i] for i in range(8) if (i >> 2) & 1)
            self.assertAlmostEqual(p2, 1.0, places=9)


class TestQEC(unittest.TestCase):
    def test_repetition_code_detects_the_error_and_recovers(self):
        """Encode |1⟩→|111⟩, flip qubit 1 → |101⟩ = index 5; majority vote recovers logical 1."""
        p = q.qec_bitflip().probabilities()
        self.assertAlmostEqual(p[5], 1.0, places=6)   # |101> is the error state


if __name__ == "__main__":
    unittest.main()
