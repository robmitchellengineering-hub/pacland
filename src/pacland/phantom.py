"""Phantom — the simulated quantum computer (SEXTANT's substrate).

Rung 2: computes the actual quantum facts. A small state-vector simulator (numpy) handles the
general case; Stim handles the Clifford/stabilizer class (millions of qubits) once installed.
The CHSH game is the canonical end-to-end: the Bell state |Φ⁺⟩ under the four optimal
measurement settings gives S = 2√2, which is the "quantum-simulated" value that QM.Tsirelson
certifies as the exact bound.
"""

from __future__ import annotations

import numpy as np

Z = np.array([[1, 0], [0, -1]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)


def chsh_value() -> float:
    """S = E(0,0) + E(0,1) + E(1,0) − E(1,1) for the optimal quantum strategy (Bell state).

    Alice measures Z (x=0) or X (x=1); Bob measures (Z+X)/√2 (y=0) or (Z−X)/√2 (y=1).
    The result is 2√2 — the Tsirelson bound, the FORCED maximum."""
    bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)  # |Φ⁺⟩ = (|00⟩+|11⟩)/√2
    A = [Z, X]
    B = [(Z + X) / np.sqrt(2), (Z - X) / np.sqrt(2)]

    def expectation(x: int, y: int) -> float:
        obs = np.kron(A[x], B[y])
        return float(np.real(bell.conj() @ obs @ bell))

    return expectation(0, 0) + expectation(0, 1) + expectation(1, 0) - expectation(1, 1)


def stim_version() -> str | None:
    """The installed Stim version, or None if the Clifford engine is not installed yet."""
    try:
        import stim

        return stim.__version__
    except Exception:
        return None


if __name__ == "__main__":
    s = chsh_value()
    print(f"CHSH (quantum-simulated) = {s:.6f}  (2√2 = {2 * np.sqrt(2):.6f})")
    print(f"Stim (Clifford engine) = {stim_version()}")


def clifford_scaling(n_qubits: int = 1000) -> str:
    """Stim simulates a Clifford circuit on `n_qubits` in polynomial time (the stabilizer tableau
    is O(n²) Pauli terms, not 2ⁿ amplitudes). This is the practical evidence behind
    QM.Stabilizer.clifford_normalizes_pauli — the Clifford class is classically simulable."""
    import time

    import stim

    s = stim.TableauSimulator()
    t0 = time.perf_counter()
    for i in range(n_qubits):
        s.h(i)
    for i in range(n_qubits - 1):
        s.cnot(i, i + 1)
    dt = time.perf_counter() - t0
    return (
        f"Stim ran an H/CNOT Clifford circuit on {n_qubits} qubits in {dt * 1000:.1f} ms "
        f"(polynomial tableau — the T gate is the single thing that escapes it to 2^{n_qubits})"
    )
