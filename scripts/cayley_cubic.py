#!/usr/bin/env python3
"""Extract the SL(2)-invariants of 3 copies of Sym^2(C^2) — the mixed part of k=3.

Each copy is (P,Q,A) with the standard Sym^2 action. Expect degree-2 dim 6 and
degree-3 dim 1 (the Cayley cubic). Extracts and prints the cubic.
"""
import sympy as sp

PAIRS = ['12', '13', '23']
NAMES = [f'{c}{ij}' for ij in PAIRS for c in 'PQA']
syms = sp.symbols(' '.join(NAMES))
S = {v: syms[i] for i, v in enumerate(NAMES)}

def hw(v):  # torus weight
    return {'P': 2, 'Q': -2, 'A': 0}[v[0]]

def eact(v):
    c, ij = v[0], v[1:]
    if c == 'P': return S['A' + ij]
    if c == 'Q': return sp.Integer(0)
    return 2 * S['Q' + ij]

def fact(v):
    c, ij = v[0], v[1:]
    if c == 'P': return sp.Integer(0)
    if c == 'Q': return S['A' + ij]
    return 2 * S['P' + ij]

def deriv(act):
    lin = {S[v]: sp.expand(act(v)) for v in NAMES}
    def op(p):
        r = sp.Integer(0)
        for s, lf in lin.items():
            if lf:
                r += lf * sp.diff(p, s)
        return sp.expand(r)
    return op

e_op, f_op = deriv(eact), deriv(fact)
NV = len(syms)
IDX = {s: i for i, s in enumerate(syms)}

def monomial(exp):
    r = sp.Integer(1)
    for s in syms:
        e = exp[IDX[s]]
        if e:
            r *= s ** e
    return r

def dim_and_null(deg):
    ans = []
    def r1(start, left, ex):
        if left == 0:
            w = sum(ex[IDX[s]] * hw(NAMES[IDX[s]]) for s in syms)
            if w == 0:
                ans.append(tuple(ex))
            return
        for i in range(start, NV):
            ex[i] += 1; r1(i, left - 1, ex); ex[i] -= 1
    r1(0, deg, [0] * NV)
    outb = []
    def r2(start, left, ex):
        if left == 0:
            outb.append(tuple(ex)); return
        for i in range(start, NV):
            ex[i] += 1; r2(i, left - 1, ex); ex[i] -= 1
    r2(0, deg, [0] * NV)
    M = sp.zeros(2 * len(outb), len(ans))
    for oi, op in enumerate((e_op, f_op)):
        for ai, ex in enumerate(ans):
            q = op(monomial(ex))
            pd = sp.Poly(q, *syms).as_dict() if q else {}
            for oo, e2 in enumerate(outb):
                M[oi * len(outb) + oo, ai] = pd.get(e2, 0)
    null = len(ans) - M.rank()
    return null, (M.nullspace(), ans) if null else ([], [])

d2, _ = dim_and_null(2)
d3, (ns, ans) = dim_and_null(3)
print(f"degree 2 dim = {d2} (expect 6)")
print(f"degree 3 dim = {d3} (expect 1 — the Cayley cubic)")
for k, vec in enumerate(ns):
    poly = sp.factor(sp.expand(sum(c * monomial(ex) for c, ex in zip(vec, ans))))
    print(f"  cubic invariant: {poly}")
