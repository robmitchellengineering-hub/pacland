#!/usr/bin/env python3
"""Fast joint Sp(2n) x SL(2) invariant dimensions via prime-modular rank (numpy).

Same math as joint_pairings.py (verified), but the rank is computed mod several large
primes (Gaussian elimination over GF(p)), so it scales to k=4 degree 4.

Usage: python3 joint_fast.py <k> <max_degree>
"""
import sys
import numpy as np

K = int(sys.argv[1]) if len(sys.argv) > 1 else 4
MAXD = int(sys.argv[2]) if len(sys.argv) > 2 else 4
PRIMES = [1_000_000_007, 1_000_000_009, 998_244_353]

# symbol layout: P block (i<j), Q block (i<j), N block (all i,j)
Ps, Qs, Ns = [], [], []
for i in range(K):
    for j in range(i + 1, K):
        Ps.append((i, j)); Qs.append((i, j))
for i in range(K):
    for j in range(K):
        Ns.append((i, j))
NV = len(Ps) + len(Qs) + len(Ns)
pidx = {p: i for i, p in enumerate(Ps)}
qidx = {q: i + len(Ps) for i, q in enumerate(Qs)}
nidx = {n: i + len(Ps) + len(Qs) for i, n in enumerate(Ns)}

# h-weight: P +2, Q -2, N 0
W = np.zeros(NV, dtype=np.int64)
for p in Ps: W[pidx[p]] = 2
for q in Qs: W[qidx[q]] = -2

def enumerate_exps(deg, filt=None):
    out = []
    def rec(start, left, ex):
        if left == 0:
            if filt is None or filt(ex):
                out.append(tuple(ex))
            return
        for i in range(start, NV):
            ex[i] += 1; rec(i, left - 1, ex); ex[i] -= 1
    rec(0, deg, [0] * NV)
    return out

def rank_mod_p(M, p):
    A = (M % p).astype(np.int64)
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i, c] % p != 0:
                piv = i; break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c] % p), p - 2, p)
        A[r] = (A[r] * inv) % p
        for i in range(rows):
            if i != r and A[i, c] % p != 0:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
        if r == rows:
            break
    return r

def dim(deg):
    ans = enumerate_exps(deg, filt=lambda ex: int(sum(ex[i] * W[i] for i in range(NV))) == 0)
    if not ans:
        return 0, 0
    outb = enumerate_exps(deg)
    outb_idx = {e: i for i, e in enumerate(outb)}
    nrows = 2 * len(outb)
    M = np.zeros((nrows, len(ans)), dtype=np.int64)

    for ai, ex in enumerate(ans):
        ex = np.array(ex, dtype=np.int64)
        # ---- e: F->H, H->0 ----
        for (a, b) in Ps:
            e = ex[pidx[(a, b)]]
            if e:
                base = ex.copy(); base[pidx[(a, b)]] -= 1
                x = base.copy(); x[nidx[(a, b)]] += 1
                M[outb_idx[tuple(x)], ai] += e
                y = base.copy(); y[nidx[(b, a)]] += 1
                M[outb_idx[tuple(y)], ai] -= e
        for (a, b) in Ns:
            e = ex[nidx[(a, b)]]
            if e and a != b:
                base = ex.copy(); base[nidx[(a, b)]] -= 1
                if a < b:
                    z = base.copy(); z[qidx[(a, b)]] += 1
                    M[outb_idx[tuple(z)], ai] += e
                else:
                    z = base.copy(); z[qidx[(b, a)]] += 1
                    M[outb_idx[tuple(z)], ai] -= e
        # ---- f: F->0, H->F ----
        for (a, b) in Qs:
            e = ex[qidx[(a, b)]]
            if e:
                base = ex.copy(); base[qidx[(a, b)]] -= 1
                x = base.copy(); x[nidx[(a, b)]] += 1
                M[len(outb) + outb_idx[tuple(x)], ai] += e
                y = base.copy(); y[nidx[(b, a)]] += 1
                M[len(outb) + outb_idx[tuple(y)], ai] -= e
        for (a, b) in Ns:
            e = ex[nidx[(a, b)]]
            if e and a != b:
                base = ex.copy(); base[nidx[(a, b)]] -= 1
                if a < b:
                    z = base.copy(); z[pidx[(a, b)]] += 1
                    M[len(outb) + outb_idx[tuple(z)], ai] += e
                else:
                    z = base.copy(); z[pidx[(b, a)]] += 1
                    M[len(outb) + outb_idx[tuple(z)], ai] -= e

    rank = max(rank_mod_p(M, p) for p in PRIMES)
    return len(ans) - rank, len(ans)

if __name__ == "__main__":
    print(f"k={K}, pairings = {NV}")
    dims = []
    for d in range(1, MAXD + 1):
        null, na = dim(d)
        dims.append(null)
        print(f"  degree {d}: dim = {null}  (ansatz {na})", flush=True)
    print("  sequence:", dims)
