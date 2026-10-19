#!/usr/bin/env python3
"""Constraint-First Theorem — the tadpole F^T J H generates the ENTIRE ring of
symplectic invariants of the flux pair (F,H), for any b3.

Why this matters:
    Mitchell's Uniqueness Theorem (validate_mitchell_uniqueness.py) proves the
    DEGREE-2 slice — F^T J H is the unique BILINEAR symplectic invariant.  That is
    one point.  The constraint-first conjecture needs the whole curve: "the ONLY
    exact structure is the constraint", i.e. there is NO invariant of any degree
    other than the tadpole and its powers.

    This is exactly the First Fundamental Theorem of invariant theory for the
    symplectic group (H. Weyl, "The Classical Groups", 1939), specialized to
    k = 2 copies of the defining representation:

        C[(C^{2n})^2]^{Sp(2n)}  =  C[ F^T J H ].

    So the conjecture was ALREADY PROVEN in 1939 — we only had to identify the flux
    pair (F,H) as the k = 2 case.  This script verifies the completeness direction
    computationally at every low degree d: the space of Sp(6)-invariant homogeneous
    polynomials in (F,H) has

        dim = 1 if d is even  (spanned by (F^T J H)^{d/2})
        dim = 0 if d is odd.

Method (standard invariant-theory move):
    1. An Sp-invariant polynomial is in particular torus-invariant; the torus acts
       diagonally, so a polynomial is torus-invariant iff every monomial is.  This
       collapses the INPUT ansatz: degree-d inputs satisfy a_i + b_i = a_{i+3} + b_{i+3}
       (i = 0,1,2) — a few dozen to a few hundred monomials instead of C(12+d-1, d).
    2. Annihilation X.p = 0 by the FULL sp(6) algebra (21 basis elements) is imposed
       on the FULL degree-d output space (torus + off-torus monomials), because a
       generator maps a torus-invariant monomial to an off-torus one.  This gives a
       tall-thin integer system (21 * C_out) x C_in; its nullity is the invariant
       dimension.  Rank is computed exactly over several large primes (max over primes
       = rank over Q for any prime avoiding the finitely many minor determinants), and
       cross-checked against sympy's exact rref for the low degrees.
"""

import sys
import itertools
import sympy as sp
import numpy as np

B3 = 6          # b3 = 6 for T^6; 2n = b3 -> n = 3
N = B3 // 2     # n = 3
PRIMES = [1_000_000_007, 1_000_000_009, 998_244_353]


def symplectic_form():
    I = sp.eye(N)
    Z = sp.zeros(N)
    return sp.Matrix([[Z, I], [-I, Z]])


def sp_basis():
    """Basis of sp(2n) = {X : X^T J + J X = 0} as blocks [[A, B],[C, -A^T]],
    B, C symmetric.  dim = n^2 + n(n+1)/2 + n(n+1)/2 = n(2n+1) = 21 for n=3."""
    basis = []
    for i in range(N):                     # A-type: n^2 = 9
        for j in range(N):
            M = sp.zeros(B3)
            M[i, j] += 1
            M[j + N, i + N] += -1
            basis.append(M)
    for i in range(N):                     # B-type (symmetric): n(n+1)/2 = 6
        for j in range(i, N):
            M = sp.zeros(B3)
            M[i, j + N] += 1
            M[j, i + N] += 1
            basis.append(M)
    for i in range(N):                     # C-type (symmetric): n(n+1)/2 = 6
        for j in range(i, N):
            M = sp.zeros(B3)
            M[i + N, j] += 1
            M[j + N, i] += 1
            basis.append(M)
    return basis


def all_monomials(d):
    nvars = 2 * B3
    for combo in itertools.combinations_with_replacement(range(nvars), d):
        e = [0] * nvars
        for v in combo:
            e[v] += 1
        yield tuple(e)


def torus_invariant_monomials(d):
    """Degree-d monomials with a_i + b_i = a_{i+3} + b_{i+3} (i = 0,1,2)."""
    if d % 2 != 0:
        return []
    half = d // 2
    out = []
    for o0 in range(half + 1):
        for o1 in range(half - o0 + 1):
            o2 = half - o0 - o1
            occ = (o0, o1, o2)
            choices = []
            for i in range(N):
                o = occ[i]
                pair = [(ai, o - ai, a3, o - a3) for ai in range(o + 1) for a3 in range(o + 1)]
                choices.append(pair)
            for c0 in choices[0]:
                for c1 in choices[1]:
                    for c2 in choices[2]:
                        e = [0] * (2 * B3)
                        for i, (ai, bi, a3, b3) in enumerate((c0, c1, c2)):
                            e[i], e[B3 + i] = ai, bi
                            e[i + N], e[B3 + i + N] = a3, b3
                        out.append(tuple(e))
    return out


def act_on_monomial(X, e):
    """X acting on (F, H) as two copies of the defining rep; returns {exponent: coeff}."""
    res = {}
    for i in range(B3):
        ai = e[i]
        if ai > 0:
            for j in range(B3):
                c = X[i, j]
                if c != 0:
                    e2 = list(e); e2[i] -= 1; e2[j] += 1
                    key = tuple(e2); res[key] = res.get(key, 0) + ai * c
        bi = e[B3 + i]
        if bi > 0:
            for j in range(B3):
                c = X[i, j]
                if c != 0:
                    e2 = list(e); e2[B3 + i] -= 1; e2[B3 + j] += 1
                    key = tuple(e2); res[key] = res.get(key, 0) + bi * c
    return res


def rank_mod(A, p):
    """Rank of integer matrix A over F_p by Gaussian elimination (vectorised)."""
    A = (A % p).astype(np.int64)
    m, n = A.shape
    r = 0
    for c in range(n):
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0:
            continue
        piv = r + int(nz[0])
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        below = np.nonzero(A[r + 1:, c])[0]
        if below.size:
            rows = r + 1 + below
            A[rows] = (A[rows] - A[rows, c][:, None] * A[r]) % p
        r += 1
    return r


def invariant_dim(d, exact_check=False):
    """Dimension of the space of Sp(6)-invariant homogeneous degree-d polynomials."""
    inputs = torus_invariant_monomials(d)
    C_in = len(inputs)
    if C_in == 0:
        return 0
    outputs = list(all_monomials(d))
    C_out = len(outputs)
    out_idx = {m: k for k, m in enumerate(outputs)}
    basis = sp_basis()

    # dense (21 * C_out) x C_in integer matrix, built from sparse triples
    dense = np.zeros((len(basis) * C_out, C_in), dtype=np.int64)
    for xi, X in enumerate(basis):
        for ci, m in enumerate(inputs):
            for e2, coeff in act_on_monomial(X, m).items():
                dense[xi * C_out + out_idx[e2], ci] += coeff

    max_rank = max(rank_mod(dense, p) for p in PRIMES)
    if exact_check and C_in <= 80:         # sympy exact rref cross-check on small cases
        rank_exact = sp.Matrix(dense.tolist()).rank()
        assert rank_exact == max_rank, f"exact rank {rank_exact} != modular {max_rank}"
    return C_in - max_rank


def main():
    J = symplectic_form()
    basis = sp_basis()
    assert len(basis) == N * (2 * N + 1) == 21, f"basis size {len(basis)} != 21"
    for X in basis:
        assert (X.T * J + J * X).is_zero_matrix, "non-symplectic basis element"
    print(f"sp(6) basis verified: {len(basis)} elements, all satisfy X^T J + J X = 0\n")

    F = sp.Matrix(sp.symbols("F0:6"))
    H = sp.Matrix(sp.symbols("H0:6"))
    tadpole = sp.expand((F.T * J * H)[0])
    for X in basis:
        XF = X * F
        XH = X * H
        lie = sum((XF)[i] * sp.diff(tadpole, F[i]) for i in range(B3)) + \
              sum((XH)[i] * sp.diff(tadpole, H[i]) for i in range(B3))
        assert sp.expand(lie) == 0, "tadpole not annihilated by sp(6)"
    print("tadpole F^T J H =", tadpole)
    print("tadpole is sp(6)-invariant (annihilated by all 21 generators): PASS\n")

    results = []
    for d in range(1, 6):
        dim = invariant_dim(d, exact_check=(d <= 4))
        expected = 1 if (d % 2 == 0) else 0
        ok = (dim == expected)
        results.append((d, dim, expected, ok))
        print(f"degree {d}: invariant space dim = {dim}  (FFT predicts {expected})  "
              f"{'PASS' if ok else 'FAIL'}")

    all_ok = all(r[3] for r in results)
    print(f"\n{'=' * 68}")
    print(f"Constraint-First completeness: {sum(r[3] for r in results)}/{len(results)} "
          f"degrees match the FFT pattern (dim 1 at even, 0 at odd).")
    print("Sequence 0,1,0,1,0 = the ONLY invariants are 1, tadpole, tadpole^2, ...")
    print("Combined with Mitchell's Uniqueness Theorem (degree-2) and the classical")
    print("First Fundamental Theorem (Weyl 1939), the tadpole is the UNIQUE exact")
    print("structure: every duality-invariant exact polynomial in flux is a power of")
    print("F^T J H.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
