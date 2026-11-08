"""A working quantum computer — the general circuit model, simulated on existing hardware.

Phantom computes *specific* quantum facts and runs their falsifiers; this is the *general*
interface a person can program: allocate qubits, apply gates, measure, get results. It runs on a
state-vector simulator (numpy) today — RAM-bounded (D41): n qubits = 2^n complex amplitudes, so
~20–30 qubits on a laptop; the Clifford class already runs in polynomial time (Stim). The same
circuit model is what real quantum hardware will execute, so programs written here run unchanged
when a QPU exists.

Honest limits (rule 67): this is a CLASSICAL simulation, not a quantum speedup. It is a quantum
computer you can *use* — write circuits, run real algorithms (superposition, entanglement, search),
and read the measurement statistics — to develop, test, learn and verify before hardware arrives.

Usage:
    python -m pacland.quantum bell --shots 1000
    python -m pacland.quantum grover
    python -m pacland.quantum superposition --shots 1000
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np

H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
T = np.array([[1, 0], [0, np.exp(1j * math.pi / 4)]], dtype=complex)

GATES = {"H": H, "X": X, "Y": Y, "Z": Z, "S": S, "T": T}


class QuantumCircuit:
    """A general n-qubit circuit. Qubit 0 is the least-significant bit of the measured string."""

    def __init__(self, n_qubits: int):
        if n_qubits > 30:
            raise ValueError(f"{n_qubits} qubits = {2 ** n_qubits} amplitudes — RAM-bounded (D41)")
        self.n = n_qubits
        self.state = np.zeros(2 ** n_qubits, dtype=complex)
        self.state[0] = 1.0  # |0…0>

    def apply_gate(self, name: str, target: int):
        """Apply a single-qubit gate (H/X/Y/Z/S/T) to `target`."""
        g = GATES[name]
        sv = self.state.reshape((2,) * self.n)
        axis = self.n - 1 - target  # reshape axis 0 = most-significant qubit
        sv = np.moveaxis(sv, axis, 0)
        sv = np.tensordot(g, sv, axes=(1, 0))
        sv = np.moveaxis(sv, 0, axis)
        self.state = sv.reshape(2 ** self.n)
        return self

    def apply_cnot(self, control: int, target: int):
        """CNOT: flip `target` where `control` is |1>."""
        idx = np.arange(2 ** self.n)
        ctrl = ((idx >> control) & 1) << target
        new_idx = idx ^ ctrl
        out = np.zeros_like(self.state)
        out[new_idx] = self.state
        self.state = out
        return self

    def apply_cz(self, a: int, b: int):
        """Controlled-Z between qubits a,b (flips the sign of |11>) — H CNOT H."""
        self.apply_gate("H", b)
        self.apply_cnot(a, b)
        self.apply_gate("H", b)
        return self

    def probabilities(self) -> np.ndarray:
        p = np.real(self.state * np.conj(self.state))
        return p / p.sum()

    def measure(self, shots: int = 1):
        """Sample `shots` bitstrings from the |amplitude|^2 distribution."""
        p = self.probabilities()
        out = np.random.choice(2 ** self.n, size=shots, p=p)
        return [format(r, f"0{self.n}b") for r in out], p


def bell():
    """The Bell state (|00⟩+|11⟩)/√2 — the simplest entanglement, measured perfectly correlated."""
    c = QuantumCircuit(2)
    c.apply_gate("H", 0).apply_cnot(0, 1)
    return c


def superposition():
    """One Hadamard — a single qubit in equal superposition of |0⟩ and |1⟩."""
    c = QuantumCircuit(1)
    c.apply_gate("H", 0)
    return c


def grover(iterations: int = 1):
    """Grover's search on 2 qubits (4 items) for the marked state |11⟩. One iteration
    amplifies |11⟩ to probability 1."""
    c = QuantumCircuit(2)
    c.apply_gate("H", 0).apply_gate("H", 1)          # uniform superposition
    for _ in range(iterations):
        c.apply_cz(0, 1)                              # oracle: phase-flip |11⟩ (the mark)
        # diffusion: H X⊗X CZ X⊗X H (reflects about the mean)
        c.apply_gate("H", 0).apply_gate("H", 1)
        c.apply_gate("X", 0).apply_gate("X", 1)
        c.apply_cz(0, 1)
        c.apply_gate("X", 0).apply_gate("X", 1)
        c.apply_gate("H", 0).apply_gate("H", 1)
    return c


PROGRAMS = {"bell": bell, "superposition": superposition, "grover": grover}


def _run(program: str, shots: int) -> int:
    c = PROGRAMS[program]()
    results, probs = c.measure(shots)
    counts: dict[str, int] = {}
    for r in results:
        counts[r] = counts.get(r, 0) + 1
    print(f"{program}: {shots} shots on {c.n} qubit(s)")
    for bits, p in sorted(zip([format(i, f'0{c.n}b') for i in range(2 ** c.n)], probs),
                          key=lambda t: -t[1]):
        got = counts.get(bits, 0)
        print(f"  |{bits}>  P={p:.4f}   observed {got}/{shots} ({got/shots:.4f})")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="A working quantum computer (simulated).")
    ap.add_argument("program", choices=sorted(PROGRAMS))
    ap.add_argument("--shots", type=int, default=1000)
    args = ap.parse_args(argv)
    return _run(args.program, args.shots)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
