"""tn_backend — an exact matrix-product-state (MPS) backend for the quantum computer.

This is the tensor-network half of "low-entanglement circuits run exact and fast past the
30-qubit wall". The state-vector backend (`quantum.py`) stores 2^n amplitudes; this backend
stores an MPS — `n` site tensors whose bond dimension `D` is set by the *entanglement*, not by
`n`. For an area-law (low-entanglement) state `D` stays small, so the cost is `~n·D²` instead
of `2^n`, and the state is represented **exactly**: every gate is applied by contracting the
relevant site tensors and re-splitting via a **full-rank SVD** (no truncation — singular values
are dropped only when numerically zero, at 1e-13 × the largest, i.e. exact to machine precision).
The MPS therefore contracts to the identical state the state-vector backend holds.

The machine-checked area law (`QM.MERA`: entanglement across a cut = the cut area `D^m`,
exactly — see `pacland-proof/PaclandProof/QM/MERA.lean` and `docs/sextant.md`) is what makes
"low D is exact" a theorem rather than a heuristic. `report()` is the **area-law gate**: it
prints the bond dimension, so a volume-law circuit (where `D` must grow toward `2^(n/2)`) is
*visible* instead of silently truncating or exploding.

Convention: qubit 0 is the least-significant bit of a measured string, matching `QuantumCircuit`.
"""
from __future__ import annotations

import math

import numpy as np

# --- single-qubit gates ----------------------------------------------------------------
_H = np.array([[1, 1], [1, -1]], dtype=complex) / math.sqrt(2)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_S = np.array([[1, 0], [0, 1j]], dtype=complex)
_T = np.array([[1, 0], [0, np.exp(1j * math.pi / 4)]], dtype=complex)
GATES = {"H": _H, "X": _X, "Y": _Y, "Z": _Z, "S": _S, "T": _T}

# --- two-qubit gates, in the |left right> basis (index = 2*left + right) ---------------
CNOT_STD = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)  # control=left
CNOT_REV = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], dtype=complex)  # control=right
_CZ = np.diag([1, 1, 1, -1]).astype(complex)
_SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)


def _cphase(angle: float) -> np.ndarray:
    return np.diag([1, 1, 1, np.exp(1j * angle)]).astype(complex)


def _svd_split(M: np.ndarray):
    """Full-rank SVD split, dropping only numerically-zero singular values (exact to machine
    precision). Returns (U, sVh) with sVh = diag(s) @ Vh already folded together."""
    U, s, Vh = np.linalg.svd(M, full_matrices=False)
    if s.size:
        tol = 1e-13 * s[0]
        keep = s > tol
        U, s, Vh = U[:, keep], s[keep], Vh[keep, :]
    return U, s[:, None] * Vh


class TNQuantumCircuit:
    """An exact MPS quantum circuit. Same gate interface as `QuantumCircuit`, but the state is
    a matrix product state, so low-entanglement circuits scale past the 2^n state-vector wall."""

    def __init__(self, n_qubits: int):
        self.n = n_qubits
        # each site tensor: shape (chi_left, 2, chi_right); |0…0> has all bond dims 1
        self.sites = [np.zeros((1, 2, 1), dtype=complex) for _ in range(n_qubits)]
        for s in self.sites:
            s[0, 0, 0] = 1.0  # amplitude of |0>

    # ---- single-qubit gates -----------------------------------------------------------
    def apply_gate(self, name: str, target: int):
        G = GATES[name]
        self.sites[target] = np.einsum("bB,lbr->lBr", G, self.sites[target])
        return self

    # ---- two-qubit gates ---------------------------------------------------------------
    def _apply_adjacent(self, gate4, left: int, right: int):
        """Apply a 4×4 gate (|left right> basis, left more significant) to adjacent sites."""
        A, B = self.sites[left], self.sites[right]
        theta = np.einsum("lam,mbr->labr", A, B)                       # (l, a, b, r)
        theta = np.einsum("ABab,labr->lABr", gate4.reshape(2, 2, 2, 2), theta)
        l, _, _, r = theta.shape
        M = theta.reshape(l * 2, 2 * r)
        U, sVh = _svd_split(M)
        k = U.shape[1]
        self.sites[left] = U.reshape(l, 2, k)
        self.sites[right] = sVh.reshape(k, 2, r)
        return self

    def _swap(self, left: int, right: int):
        return self._apply_adjacent(_SWAP, left, right)

    def _apply_2q_sym(self, gate4, a: int, b: int):
        """Symmetric two-qubit gate (CZ, CPhase, SWAP): the |11> phase / swap does not care
        which qubit is 'control'."""
        if a == b:
            raise ValueError("two-qubit gate needs distinct qubits")
        if b == a + 1:
            return self._apply_adjacent(gate4, a, b)
        if a == b + 1:
            return self._apply_adjacent(gate4, b, a)
        if b > a:
            for q in range(b, a + 1, -1):          # bring b down to a+1
                self._swap(q - 1, q)
            self._apply_adjacent(gate4, a, a + 1)
            for q in range(a + 1, b):
                self._swap(q, q + 1)
        else:
            for q in range(b, a - 1):              # bring b up to a-1
                self._swap(q, q + 1)
            self._apply_adjacent(gate4, a - 1, a)
            for q in range(a - 1, b, -1):
                self._swap(q - 1, q)
        return self

    def apply_cnot(self, control: int, target: int):
        if control == target:
            raise ValueError("control == target")
        if target == control + 1:
            return self._apply_adjacent(CNOT_STD, control, target)
        if target == control - 1:
            return self._apply_adjacent(CNOT_REV, target, control)
        if target > control:
            for q in range(target, control + 1, -1):
                self._swap(q - 1, q)
            self._apply_adjacent(CNOT_STD, control, control + 1)
            for q in range(control + 1, target):
                self._swap(q, q + 1)
        else:
            for q in range(target, control - 1):
                self._swap(q, q + 1)
            self._apply_adjacent(CNOT_REV, control - 1, control)
            for q in range(control - 1, target, -1):
                self._swap(q - 1, q)
        return self

    def apply_cz(self, a: int, b: int):
        return self._apply_2q_sym(_CZ, a, b)

    def apply_cphase(self, control: int, target: int, angle: float):
        return self._apply_2q_sym(_cphase(angle), control, target)

    # ---- readout -----------------------------------------------------------------------
    def amplitude(self, bits) -> complex:
        """<bits|ψ> for a bit list (bits[0] = qubit 0). Exact contraction, O(n·D²)."""
        L = np.array([1.0 + 0j])
        for i, b in enumerate(bits):
            L = L @ self.sites[i][:, b, :]          # (chi_right,)
        return complex(L[0])

    def statevector(self) -> np.ndarray:
        if self.n > 20:
            raise ValueError("statevector is 2^n — use sample()/amplitude() past ~20 qubits")
        return np.array(
            [self.amplitude([(i >> q) & 1 for q in range(self.n)]) for i in range(2 ** self.n)],
            dtype=complex,
        )

    def probabilities(self) -> np.ndarray:
        sv = self.statevector()
        p = np.real(sv * sv.conj())
        return p / p.sum()

    def probability_of(self, bits) -> float:
        a = self.amplitude(bits)
        return float(np.real(a * a.conj()))

    def measure_qubit(self, target: int) -> int:
        """Measure one qubit (marginal) and project. Uses the full state vector, so it is meant
        for small n (teleport, etc.); for large n use `sample`."""
        if self.n > 20:
            raise ValueError("measure_qubit on >20 qubits is not implemented; use sample()")
        sv = self.statevector()
        p = np.real(sv * sv.conj())
        p /= p.sum()
        p0 = sum(p[i] for i in range(2 ** self.n) if ((i >> target) & 1) == 0)
        outcome = int(np.random.choice(2, p=[p0, 1.0 - p0]))
        # project onto |outcome> (keep physical dim 2, zero the other entry — exact P_outcome |ψ>)
        self.sites[target][:, 1 - outcome, :] = 0.0
        return outcome

    # ---- exact MPS sampling ------------------------------------------------------------
    def _sample_one(self) -> list[int]:
        """Sample one bitstring from |amp|² exactly (left-canonical form, no truncation)."""
        sites = [s.copy() for s in self.sites]
        for i in range(self.n - 1):
            l, _, r = sites[i].shape
            U, sVh = _svd_split(sites[i].reshape(l * 2, r))
            k = U.shape[1]
            sites[i] = U.reshape(l, 2, k)
            sites[i + 1] = np.einsum("kr,rbs->kbs", sVh, sites[i + 1])
        bits: list[int] = []
        L = np.array([1.0 + 0j])
        for i in range(self.n):
            v = np.einsum("l,lbr->br", L, sites[i])          # (2, chi_right)
            p = np.real(np.einsum("br,br->b", v, v.conj()))
            p = p / p.sum()
            b = int(np.random.choice(2, p=p))
            bits.append(b)
            L = v[b] / np.linalg.norm(v[b])
        return bits

    def measure(self, shots: int = 1):
        """Sample `shots` bitstrings (qubit 0 = LSB, same format as QuantumCircuit.measure).
        Returns (bitstrings, probabilities-or-None) — probabilities only when n <= 20."""
        samples = [self._sample_one() for _ in range(shots)]
        out = []
        for s in samples:
            r = 0
            for i, b in enumerate(s):
                r |= b << i
            out.append(format(r, f"0{self.n}b"))
        probs = self.probabilities() if self.n <= 20 else None
        return out, probs

    # ---- the area-law gate --------------------------------------------------------------
    def report(self) -> dict:
        """The area-law gate: report the bond dimension so volume-law growth is visible."""
        max_d = max(s.shape[0] for s in self.sites)
        max_d = max(max_d, self.sites[-1].shape[2])
        cut = self.n // 2
        central_rank = self.sites[cut - 1].shape[2] if cut > 0 else self.sites[0].shape[2]
        mps_bytes = sum(s.size for s in self.sites) * 16
        sv_bytes = (2 ** self.n) * 16
        volume_law = 2 ** (self.n // 2)
        return {
            "n_qubits": self.n,
            "max_bond_dim": max_d,
            "central_cut_schmidt_rank": central_rank,
            "mps_bytes": mps_bytes,
            "statevector_bytes": sv_bytes,
            "volume_law_ceiling": volume_law,
            "low_entanglement": max_d <= 64,  # D bounded by a small constant -> area-law regime
        }
