#!/usr/bin/env python3
"""The k>=1 joint invariant ring of Sp(2n) x SL(2) on flux pairs — Weyl FFT at the pairings level.

For k=1 the joint ring is C[N], N = F^T J H (the tadpole; SL(2)-invariant). For k>=2 the
cross-pairings appear and SL(2) acts non-trivially; the joint ring is the genuinely open case.

Method (independent of b3, since the SL(2) action on the pairings does not depend on it):
  1. By Weyl's FFT the Sp(2n)-invariants of k pairs (F_i, H_i) are the pairings
        P_ij = F_i^T J F_j (i<j),  Q_ij = H_i^T J H_j (i<j),  N_ij = F_i^T J H_j (all i,j).
  2. SL(2) acts on these pairings via the standard 2-dim rep on each (F_i, H_i).
  3. The joint invariants are the SL(2)-invariants of C[pairings]: torus-ansatz (#P == #Q)
     plus annihilation by the sl(2) generators e, f.  Nullity = invariant dimension.

k=2 result (proved below and asserted in --self-test): the joint ring is
    C[N_11, N_22, S, D],   S = N_12 + N_21,   D = P_12 Q_12 - (N_12 - N_21)^2 / 4,
a polynomial ring in 3 quadratics (flux degree 2) and 1 quartic (flux degree 4).  At the
pairings level the Hilbert series is 1/((1-t)^3 (1-t^2)): dims 3, 7, 13, 22 at pairing
degrees 1..4 (= flux degrees 2, 4, 6, 8).

Usage: python3 validate_k2_joint.py [k [max_degree]] | --self-test
"""
import sys
import sympy as sp

def pairing_symbols(k):
    P, Q, N = {}, {}, {}
    sym = []
    for i in range(k):
        for j in range(i + 1, k):
            P[(i, j)] = sp.Symbol(f"P{i}{j}"); sym.append(P[(i, j)])
            Q[(i, j)] = sp.Symbol(f"Q{i}{j}"); sym.append(Q[(i, j)])
    for i in range(k):
        for j in range(k):
            N[(i, j)] = sp.Symbol(f"N{i}{j}"); sym.append(N[(i, j)])
    return P, Q, N, sym

def antisym(a, b, d):
    """P and Q are antisymmetric in (a,b): d[b,a] = -d[a,b], d[a,a] = 0."""
    if a < b: return d[(a, b)]
    if a > b: return -d[(b, a)]
    return sp.Integer(0)

def sl2_e(s, P, Q, N):
    for (a, b), v in P.items():
        if s == v: return N[(a, b)] - N[(b, a)]
    for (a, b), v in Q.items():
        if s == v: return sp.Integer(0)
    for (a, b), v in N.items():
        if s == v: return antisym(a, b, Q)
    return sp.Integer(0)

def sl2_f(s, P, Q, N):
    for (a, b), v in P.items():
        if s == v: return sp.Integer(0)
    for (a, b), v in Q.items():
        if s == v: return N[(a, b)] - N[(b, a)]
    for (a, b), v in N.items():
        if s == v: return antisym(a, b, P)
    return sp.Integer(0)

def hweight(s, P, Q):
    return 2 if s in P.values() else (-2 if s in Q.values() else 0)

def invariant_dims(k, maxdeg):
    P, Q, N, sym = pairing_symbols(k)
    nv = len(sym)
    idx = {s: i for i, s in enumerate(sym)}

    def deriv(act):
        lin = {s: sp.expand(act(s)) for s in sym}
        def op(p):
            r = sp.Integer(0)
            for s, lf in lin.items():
                if lf != 0:
                    r += lf * sp.diff(p, s)
            return sp.expand(r)
        return op

    e_op = deriv(lambda s: sl2_e(s, P, Q, N))
    f_op = deriv(lambda s: sl2_f(s, P, Q, N))

    def monomial(exp):
        r = sp.Integer(1)
        for s in sym:
            e = exp[idx[s]]
            if e: r *= s ** e
        return r

    dims = []
    for deg in range(1, maxdeg + 1):
        # torus ansatz: #P == #Q
        ans = []
        def rec1(start, left, exps):
            if left == 0:
                w = sum(exps[idx[s]] * hweight(s, P, Q) for s in sym)
                if w == 0: ans.append(tuple(exps))
                return
            for i in range(start, nv):
                exps[i] += 1; rec1(i, left - 1, exps); exps[i] -= 1
        rec1(0, deg, [0] * nv)

        outb = []
        def rec2(start, left, exps):
            if left == 0:
                outb.append(tuple(exps)); return
            for i in range(start, nv):
                exps[i] += 1; rec2(i, left - 1, exps); exps[i] -= 1
        rec2(0, deg, [0] * nv)

        M = sp.zeros(2 * len(outb), len(ans))
        for oi, op in enumerate((e_op, f_op)):
            for ai, exp in enumerate(ans):
                q = op(monomial(exp))
                pd = sp.Poly(q, *sym).as_dict() if q != 0 else {}
                for oo, e2 in enumerate(outb):
                    M[oi * len(outb) + oo, ai] = pd.get(e2, 0)
        dims.append(len(ans) - M.rank())
    return dims

if __name__ == "__main__":
    if "--self-test" in sys.argv:
        # k=1: C[N] -> pairing dims 1,1,1,1 (flux 2,4,6,8)
        d1 = invariant_dims(1, 4)
        assert d1 == [1, 1, 1, 1], f"k=1 fail: {d1}"
        # k=2: C[N11,N22,S,D] -> pairing dims 3,7,13,22
        d2 = invariant_dims(2, 4)
        assert d2 == [3, 7, 13, 22], f"k=2 fail: {d2}"
        # k=3 (fast, low degree): 6 quadratics + 6 quartics -> [6, 27]
        d3 = invariant_dims(3, 2)
        assert d3 == [6, 27], f"k=3 fail: {d3}"
        print(f"k-joint self-test: k=1 {d1} (C[N]); k=2 {d2} (C[N11,N22,S,D]); "
              f"k=3 {d3} (6 quadratics + 6 quartics) — OK")
        sys.exit(0)
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    print(f"k={k}: pairing-level invariant dims (degrees 1..{maxd} = flux degrees 2..{2*maxd}):")
    print("  ", invariant_dims(k, maxd))
