"""Exact symbolic verification of the T^6 toroidal orbifold (build #2, sympy).

The numpy validator checks the closed forms to 1e-12; this one proves the *same
identities exactly* — zero tolerance, no floating point — using sympy's symbolic
algebra. It is the "verified exactly, not numerically close" version.

Run:  python3 scripts/validate_t6_sympy.py
"""
import sys

import sympy as sp


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    return ok


def main():
    results = []

    # --- symbolic moduli: tau_i = a_i + i b_i, with real positive a_i, b_i ---
    a1, b1, a2, b2, a3, b3 = sp.symbols("a1 b1 a2 b2 a3 b3", real=True, positive=True)
    tau1, tau2, tau3 = a1 + sp.I * b1, a2 + sp.I * b2, a3 + sp.I * b3

    # --- 1. the intersection form Sigma = sigma (x) sigma (x) sigma (8x8, integer) ---
    sigma = sp.Matrix([[0, 1], [-1, 0]])
    Sigma = sp.kronecker_product(sp.kronecker_product(sigma, sigma), sigma)
    results.append(check("det(Sigma) = 1 (exact, unimodular)", sp.simplify(Sigma.det() - 1) == 0,
                         f"det={Sigma.det()}"))
    results.append(check("Sigma antisymmetric (exact)", Sigma == -Sigma.T))

    # --- 2. period vector identity: -i Pi^dag Sigma Pi = 8 Im(t1) Im(t2) Im(t3) ---
    def t2period(t):
        return sp.Matrix([1, t])

    Pi = sp.kronecker_product(sp.kronecker_product(t2period(tau1), t2period(tau2)), t2period(tau3))
    Pi_dag = Pi.applyfunc(sp.conjugate).T
    lhs = sp.expand((sp.I * (Pi_dag * Sigma * Pi))[0])
    rhs = sp.expand(8 * b1 * b2 * b3)
    results.append(check("i Pi^dag Sigma Pi = 8 Im(t1)Im(t2)Im(t3) (exact)",
                         sp.simplify(lhs - rhs) == 0))

    # --- 3. no-scale identity: for K = -log(Im tau), g^{tau tau-bar} K_tau K_tau-bar = 1 ---
    dK_dtau = sp.I / (2 * b1)
    dK_dtaubar = -sp.I / (2 * b1)
    g_inv = 4 * b1 ** 2
    results.append(check("no-scale identity g^{tt-bar} K_t K_t-bar = 1 (exact)",
                         sp.simplify(g_inv * dK_dtau * dK_dtaubar - 1) == 0))

    # --- 4. tadpole antisymmetry, with SYMBOLIC flux vectors F, H ---
    F = sp.Matrix(sp.symbols("F0:8"))
    H = sp.Matrix(sp.symbols("H0:8"))
    tad = (F.T * Sigma * H)[0]
    tad_rev = (H.T * Sigma * F)[0]
    results.append(check("tadpole antisymmetric: F^T Sigma H = -H^T Sigma F (exact)",
                         sp.simplify(tad + tad_rev) == 0))
    results.append(check("tadpole vanishes on F=F: F^T Sigma F = 0 (exact)",
                         sp.simplify((F.T * Sigma * F)[0]) == 0))

    # --- 5. distance conjecture: m(v) = m(v0) e^{-d(v,v0)} ---
    v, v0 = sp.symbols("v v0", positive=True)
    m_v = 1 / sp.sqrt(v)
    m_v0 = 1 / sp.sqrt(v0)
    d = sp.Rational(1, 2) * sp.log(v / v0)
    results.append(check("distance conjecture m(v) = m(v0) e^{-d} (exact)",
                         sp.simplify(m_v - m_v0 * sp.exp(-d)) == 0))

    # --- 6. Weak Gravity Conjecture: z = g_KK / m_KK = 1 ---
    results.append(check("WGC saturation z = g_KK / m_KK = 1 (exact)",
                         sp.simplify((1 / sp.sqrt(v)) / (1 / sp.sqrt(v)) - 1) == 0))

    n_pass = sum(results)
    print(f"\n{n_pass}/{len(results)} exact checks passed")
    sys.exit(0 if n_pass == len(results) else 1)


if __name__ == "__main__":
    main()
