#!/usr/bin/env python3
"""k=2 integer orbit structure — verify the content/elementary-divisor relationships.

Over Z the Sp-invariants (pairings) are not a complete orbit classifier; k=1 needs the
content d = gcd(F,H) (Wall: orbits classified by (N,d), d^2 | N). For k=2 the conjectured
invariant is (G, d): the 4x4 alternating Gram matrix G (6 pairings) plus d = gcd of all 16
entries, with d^2 | (every entry of G) and the elementary divisors d1 | d2 of G satisfying
d1 * d2 = Pf(G). This checks those two relationships on a random sample (integer arithmetic).

Usage: python3 k2_integer.py [n_samples]
"""
import sys, math, random

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
B = 6  # entry bound

def pairing(u, w):
    return u[0]*w[2] + u[1]*w[3] - u[2]*w[0] - u[3]*w[1]

def content(vs):
    g = 0
    for v in vs:
        for x in v:
            g = math.gcd(g, abs(x))
    return g

def gram(vs):
    G = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(i+1, 4):
            p = pairing(vs[i], vs[j])
            G[i][j] = p; G[j][i] = -p
    return G

def pf4(G):
    return G[0][1]*G[2][3] - G[0][2]*G[1][3] + G[0][3]*G[1][2]

def d1(G):
    g = 0
    for i in range(4):
        for j in range(i+1, 4):
            for k in range(4):
                for l in range(k+1, 4):
                    g = math.gcd(g, abs(G[i][k]*G[j][l] - G[i][l]*G[j][k]))
    return g

def rand_vec():
    while True:
        v = tuple(random.randint(-B, B) for _ in range(4))
        if any(v):
            return v

fails_d2 = 0
fails_pf = 0
seen = {}
for _ in range(N):
    vs = [rand_vec() for _ in range(4)]
    d = content(vs)
    G = gram(vs)
    pf = pf4(G)
    e1 = d1(G)
    ok_d2 = all(G[i][j] % (d*d) == 0 for i in range(4) for j in range(4))
    if not ok_d2:
        fails_d2 += 1
    if e1 != 0:
        if pf % e1 != 0 or (e1 * (pf // e1)) != pf:
            fails_pf += 1
    else:
        if pf != 0:
            fails_pf += 1
    seen[(tuple(tuple(r) for r in G), d)] = 1

print(f"random sample {N}: distinct (G, content) = {len(seen)}")
print(f"  d^2 | G  failures: {fails_d2}")
print(f"  d1*d2 = Pf(G)  failures: {fails_pf}")
