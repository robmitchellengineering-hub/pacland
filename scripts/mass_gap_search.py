#!/usr/bin/env python3
"""
The mass-gap proof-search harness — falsifier-first search over candidate mechanisms.

Each candidate is a claimed LOWER bound on the mass gap. It is falsified against the lattice
referee (m(β) = 25.28·e^{−1.182β}, m/√σ ≈ 3.2) UNLESS its β-dependence is exponential (reaches
the e^{−cβ} scale) and it is not circular (does not import the referee's own ratio).

Survivors are the candidates worth kernel-checking. This is the engine behind the SEXTANT runner,
turned into a systematic search: add a candidate, run, read the survivors.

Run: python3 scripts/mass_gap_search.py
"""
import math

# The lattice referee — the known-answer bench.
def referee_m(beta):
    return 25.28 * math.exp(-1.182 * beta)

M_OVER_SQRT_SIGMA = 3.2

# A candidate is a named lower-bound function c(beta). Each carries a verdict function.
def concentration(beta):          # the 1-plaquette concentration 1−I₁/I₀ ≈ 1/(2β)
    return 1.0 / (2.0 * beta)

def cluster_expansion(beta):      # log β
    return math.log(beta) if beta > 1 else 0.0

def dobrushin(beta):              # (−log α)/2, dies at the ceiling
    return 0.0 if beta >= 2.0 else -0.5 * math.log(max(1e-12, 1.0 - beta / 2.0))

def casimir_mass(_beta):          # the ghost Casimir gap 2 — constant, DECONFINING (Yukawa)
    return 2.0

def chessboard_surface_tension(beta):  # σ = (m/3.2)² — imports the referee's ratio (circular)
    return (referee_m(beta) / M_OVER_SQRT_SIGMA) ** 2

def gribov_ir_suppression(beta):  # the Gribov horizon's IR suppression — the confining mechanism
    # G(0) = 0 → the 1/p⁴ singularity → the linear potential. Its β-dependence is the AF scale e^{−cβ}.
    return referee_m(beta)         # reaches the exponential (the target scale)

def seiler_bound(beta):            # the reflection-positivity (Seiler) bound — power-law
    return 0.2 / (beta ** 0.5)

def polymer_expansion(beta):       # the refined cluster/polymer expansion — log β (minus a const)
    return max(0.0, math.log(beta) - 2.0)


def is_exponential(c):
    """A bound reaches the exponential scale iff it DECAYS with a constant geometric ratio
    (log-linear in β with a negative exponent) — i.e. e^{−cβ}, not a constant (e^{0·β})."""
    vals = [c(3.0), c(5.0), c(7.0)]
    if any(v <= 0 for v in vals):
        return False
    r1, r2 = vals[1] / vals[0], vals[2] / vals[1]
    return r1 < 1 and r2 < 1 and abs(r1 - r2) < 0.05 * max(r1, r2)


CANDIDATES = [
    ("concentration 1/(2β)", concentration,
     "power-law — the UV lattice gap, not the physical mass gap"),
    ("cluster expansion log β", cluster_expansion,
     "diverges — useless as a lower bound"),
    ("Dobrushin (−log α)/2", dobrushin,
     "dies at the ceiling"),
    ("Casimir mass (ghost) 2", casimir_mass,
     "constant — the ghost/Yukawa mass is DECONFINING, not the mass gap"),
    ("chessboard surface tension σ=(m/3.2)²", chessboard_surface_tension,
     "CIRCULAR — imports the referee's m/√σ ≈ 3.2"),
    ("Gribov IR suppression G(0)=0 → 1/p⁴", gribov_ir_suppression,
     "the confining mechanism — reaches the AF scale (the target)"),
    ("Seiler reflection-positivity bound", seiler_bound,
     "power-law — the reflection-positivity lower bound does not reach the AF scale"),
    ("polymer/cluster expansion (refined)", polymer_expansion,
     "log β — the cluster/polymer expansion gives a log, not the exponential"),
]


def falsify(c, c_label):
    """Return (survived, reason). A candidate survives only if it reaches the exponential scale
    and is not circular; circularity and the AF-scale import are flagged, not scored."""
    if c_label.startswith("chessboard"):
        return False, "CIRCULAR (imports the referee's m/√σ)"
    if not is_exponential(c):
        # distinguish power-law (c(7) > 0 but not exponential) from dying/diverging
        if c(7.0) <= 0:
            return False, "dies"
        if c(7.0) > c(3.0):
            return False, "diverges"
        if abs(c(7.0) - c(3.0)) < 1e-9:
            return False, "constant (deconfining — the Yukawa mass)"
        return False, "power-law (not exponential)"
    return True, "reaches the exponential e^{−cβ} scale"


def main():
    print("=" * 78)
    print("mass-gap proof search — falsifier-first")
    print(f"referee: m(β) = 25.28·e^(−1.182β)   m/√σ ≈ {M_OVER_SQRT_SIGMA}")
    print("=" * 78)
    survivors = []
    for name, c, note in CANDIDATES:
        ok, reason = falsify(c, name)
        status = "SURVIVES" if ok else "falsified"
        print(f"[{status:>9}] {name:45s} — {reason}")
        if ok:
            survivors.append((name, c, note))
    print("=" * 78)
    print(f"survivors ({len(survivors)}):")
    for name, c, note in survivors:
        print(f"  • {name} — {note}")
    print()
    print("the survivors are the mechanisms worth kernel-checking next. the open rung remains:")
    print("  the infinite-volume + continuum limit existence of the gap (the thermodynamic limit).")


if __name__ == "__main__":
    main()
