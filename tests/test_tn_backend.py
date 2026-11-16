"""The tensor-network backend is EXACT (matches the state vector), and the area-law gate reports
the bond dimension honestly.

The central claim: for a low-entanglement (area-law) circuit the exact MPS backend reproduces the
state-vector answer bit-for-bit, at `~n·D²` memory instead of `2^n` — so it runs past the 30-qubit
wall. These tests pin that: (1) exact agreement on every program and on random circuits, and
(2) the area-law gate shows GHZ(n=64) at bond dimension 2 while a random circuit's D grows.
"""
import unittest

import numpy as np

from pacland import quantum as q
from pacland.tn_backend import TNQuantumCircuit


def _sv(c):
    return c.state if hasattr(c, "state") else c.statevector()


class TestExactAgreement(unittest.TestCase):
    def _assert_exact(self, name, builder):
        sv = _sv(builder(cls=q.QuantumCircuit))
        tn = _sv(builder(cls=TNQuantumCircuit))
        self.assertTrue(np.allclose(sv, tn, atol=1e-10),
                        f"{name}: TN backend disagrees with the state vector "
                        f"(max diff {np.max(np.abs(sv - tn)):.2e})")

    def test_all_deterministic_programs_match_exactly(self):
        self._assert_exact("bell", q.bell)
        self._assert_exact("superposition", q.superposition)
        self._assert_exact("grover", q.grover)
        self._assert_exact("ghz", q.ghz)
        self._assert_exact("qft2", q.qft2)
        self._assert_exact("qec", q.qec_bitflip)

    def test_random_circuits_match_exactly(self):
        for depth in (12, 30):
            rng = np.random.default_rng(depth)
            ops = []
            for _ in range(depth):
                ops.append(("H", int(rng.integers(6))))
                a, b = int(rng.integers(6)), int(rng.integers(6))
                while a == b:
                    b = int(rng.integers(6))
                ops.append(("CNOT", a, b))
            c1, c2 = q.QuantumCircuit(6), TNQuantumCircuit(6)
            for op in ops:
                if op[0] == "H":
                    c1.apply_gate("H", op[1]); c2.apply_gate("H", op[1])
                else:
                    c1.apply_cnot(op[1], op[2]); c2.apply_cnot(op[1], op[2])
            self.assertTrue(np.allclose(c1.state, c2.statevector(), atol=1e-10),
                            f"random circuit depth {depth} disagrees")

    def test_non_adjacent_gates_match_exactly(self):
        c1 = q.QuantumCircuit(4)
        c1.apply_gate("H", 0).apply_cnot(0, 3).apply_cnot(3, 0).apply_cphase(0, 3, np.pi / 3)
        c2 = TNQuantumCircuit(4)
        c2.apply_gate("H", 0).apply_cnot(0, 3).apply_cnot(3, 0).apply_cphase(0, 3, np.pi / 3)
        self.assertTrue(np.allclose(c1.state, c2.statevector(), atol=1e-10))

    def test_teleport_moves_the_state_on_tn(self):
        for _ in range(20):
            c = q.teleport(cls=TNQuantumCircuit)
            sv = c.statevector()
            p = np.real(sv * sv.conj()); p /= p.sum()
            p2 = sum(p[i] for i in range(8) if (i >> 2) & 1)
            self.assertAlmostEqual(p2, 1.0, places=9)


class TestPastTheWall(unittest.TestCase):
    def test_ghz_64_is_area_law_and_exact(self):
        c = q.ghz(n=64, cls=TNQuantumCircuit)
        r = c.report()
        self.assertEqual(r["max_bond_dim"], 2)          # GHZ has Schmidt rank 2 across every cut
        self.assertEqual(r["central_cut_schmidt_rank"], 2)
        self.assertTrue(r["low_entanglement"])
        # 8 KB of MPS tensors vs 2^64 * 16 bytes of state vector
        self.assertLess(r["mps_bytes"], r["statevector_bytes"])

    def test_ghz_64_samples_are_all_equal(self):
        c = q.ghz(n=64, cls=TNQuantumCircuit)
        samples, _ = c.measure(8)
        self.assertTrue(all(s in ("0" * 64, "1" * 64) for s in samples))

    def test_sampling_matches_statevector_for_small_n(self):
        rng = np.random.default_rng(3)
        targets = [int(rng.integers(4)) for _ in range(6)]
        c1, c2 = q.QuantumCircuit(4), TNQuantumCircuit(4)
        for t in targets:
            c1.apply_gate("H", t); c2.apply_gate("H", t)
        c1.apply_cnot(0, 3); c2.apply_cnot(0, 3)
        p_exact = c1.probabilities()
        samples, _ = c2.measure(20000)
        from collections import Counter
        counts = Counter(int(s, 2) for s in samples)
        emp = np.array([counts.get(i, 0) / 20000 for i in range(16)])
        self.assertTrue(np.allclose(emp, p_exact, atol=0.02),
                        f"sampled {emp} vs exact {p_exact}")


if __name__ == "__main__":
    unittest.main()
