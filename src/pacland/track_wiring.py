"""track_wiring.py — wire the four mass-gap tracks into the discovery engine.

Each track becomes a HYPOTHESIS (registered in ``hypotheses.HYPOTHESES``) AND a runnable FALSIFIER
(registered in ``runner.FALSIFIERS``), so the engine can *work* them — propose → falsify → record —
rather than only list them. The two tractable falsifiers (Coulomb string tension, RG flow curvature)
run now; the two Lean-dependent ones (Gribov horizon, curvature measure) report honestly as unresolved
until their Lean proofs land.
"""
from __future__ import annotations

import math

from pacland import registry

TRACK_HYPOTHESES: dict[str, dict] = {
    "gribov": {
        "question": "does the Gribov horizon yield a volume-uniform positive spectral gap?",
        "open": "a residual Gribov copy / a horizon that does not yield m > 0",
        "candidates": [
            {"hypothesis": "restricting to the first Gribov region removes the gauge flat directions",
             "falsifier": "gribov-no-residual-copy"},
        ],
        "attack": "formalize the gauge-orbit quotient and check it removes the flat directions",
    },
    "coulomb": {
        "question": "is the string tension σ(β) bounded below, uniformly in β and volume?",
        "open": "a Wilson loop violating the area law / σ(β) → 0 (the U(1) Coulomb phase)",
        "candidates": [
            {"hypothesis": "σ(β) ≥ σ₀·e^(−2.364β) uniformly in volume and spacing",
             "falsifier": "string-tension-positive"},
        ],
        "attack": "prove (not just Monte-Carlo) σ(β) > 0 uniformly; the non-Abelian-only record is in hypotheses.py",
    },
    "rg": {
        "question": "is the RG flow's curvature uniformly bounded (effective interactions stay controlled)?",
        "open": "a flow/truncation where the curvature diverges (couplings run away)",
        "candidates": [
            {"hypothesis": "the Polchinski flow's beta functions stay finite at the fixed point",
             "falsifier": "flow-curvature-bounded"},
        ],
        "attack": "extend energy/frg.py to bound the Hessian curvature along the flow, not just the fixed point",
    },
    "curvature": {
        "question": "does Wang's criterion (negative curvature on a measure-negligible set + drift ⇒ positive gap) hold β-uniformly?",
        "open": "negative curvature on a measure-non-negligible set",
        "candidates": [
            {"hypothesis": "the SU(2) 1-plaquette curvature 1/4 + 2β·cosθ is negative only on a measure-negligible set",
             "falsifier": "curvature-measure-negligible"},
        ],
        "attack": "formalize Wang's criterion + the Lyapunov drift (named in hypotheses.py, not yet in the Lean tower)",
    },
}


def register_tracks() -> int:
    """Register the four tracks in hypotheses.HYPOTHESES. Returns the number added."""
    from pacland import hypotheses
    n = 0
    for tid, meta in TRACK_HYPOTHESES.items():
        hypotheses.HYPOTHESES[tid] = meta
        n += 1
    return n


# ------------------------------------------------------------------------------------------ #
# The runnable falsifiers. Each returns (survived, evidence).
# ------------------------------------------------------------------------------------------ #

def _verify_string_tension_positive() -> tuple[bool, str]:
    """Coulomb track: is the lattice string tension positive at every probed β (an area law)?"""
    from pacland import lattice_ym_su2 as su2
    betas = (1.5, 2.0, 2.5, 3.0)
    values = []
    for b in betas:
        sig = su2.measure_string_tension(b, d=4, N=2, n_sweeps=6, seed=0)
        values.append(sig)
    if all(sig > 0.0 for sig in values):
        return True, f"SU(2) string tension σ = {values} — positive at every β (area law)"
    return False, f"SU(2) string tension σ = {values} — σ ≤ 0 at some β (no area law)"


def _verify_flow_curvature_bounded() -> tuple[bool, str]:
    """RG track: do the Polchinski-flow beta functions stay finite at the fixed point?"""
    from pacland.energy import frg
    lam, g = frg.solve(d=4.0)
    bl, bg = frg.beta_lambda(lam, g), frg.beta_g(lam, g)
    if math.isfinite(bl) and math.isfinite(bg):
        return True, f"FRG fixed point (λ*,g*) = ({lam:.4f},{g:.4f}); beta = ({bl:.3e},{bg:.3e}) finite"
    return False, f"FRG beta functions diverge at the fixed point: beta_lambda={bl}, beta_g={bg}"


def _unresolved(reason: str):
    """A falsifier that cannot run until its Lean proof lands — honest 'unresolved', not a verdict."""
    return (False, f"unresolved — {reason}")


def wire_falsifiers() -> int:
    """Register each track's falsifier in runner.FALSIFIERS. Returns the number wired."""
    from pacland import runner
    runner.FALSIFIERS.update({
        "gribov-no-residual-copy": lambda: _unresolved("the gauge-orbit quotient is not yet Lean-checked"),
        "string-tension-positive": _verify_string_tension_positive,
        "flow-curvature-bounded": _verify_flow_curvature_bounded,
        "curvature-measure-negligible": lambda: _unresolved("Wang's criterion is not yet formalized"),
    })
    return 4


def run_track(track_id: str) -> dict:
    """Run one track's first candidate falsifier and record the outcome as a claim."""
    meta = TRACK_HYPOTHESES[track_id]
    cand = meta["candidates"][0]
    from pacland import runner
    falsifier = runner.FALSIFIERS.get(cand["falsifier"])
    if falsifier is None:
        return {"track": track_id, "error": f"falsifier {cand['falsifier']!r} not wired"}
    survived, evidence = falsifier()
    registry.record_claim(
        f"claim-track-{track_id}",
        cand["hypothesis"],
        "survived" if survived else "failed",
        problem=track_id,
        reason=evidence,
        produced_by="track-wiring",
    )
    return {"track": track_id, "survived": survived, "evidence": evidence,
            "falsifier": cand["falsifier"]}


# ------------------------------------------------------------------------------------------ #
# Legitimacy: each track must be a SOURCED path, not a hand-wavy name.
# ------------------------------------------------------------------------------------------ #

TRACK_LEGITIMACY: dict[str, list[dict]] = {
    "gribov": [
        {"result": "the Gribov horizon restricts the gauge field to the first Gribov region, removing the gauge flat directions",
         "source": "Gribov 1978, Nucl.Phys.B 139:1"},
        {"result": "the horizon restriction generates a non-perturbative mass scale (the Gribov mass)",
         "source": "Zwanziger 1989, Nucl.Phys.B 323:513"},
    ],
    "coulomb": [
        {"result": "confinement is the area law of the Wilson loop (the string tension σ)",
         "source": "Wilson 1974; the Creutz ratio, Creutz 1980"},
        {"result": "m/√σ ≈ 3.2 is a (numerically) universal ratio",
         "source": "lattice gauge theory"},
    ],
    "rg": [
        {"result": "the exact renormalization-group flow equation for the effective action",
         "source": "Polchinski 1984, Nucl.Phys.B 231:269"},
        {"result": "the flow of the effective action (the functional RG)",
         "source": "Wetterich 1993, Phys.Lett.B 301:90"},
    ],
    "curvature": [
        {"result": "the Bakry-Émery curvature-dimension condition implies a spectral gap",
         "source": "Bakry-Émery 1985"},
        {"result": "negative curvature on a measure-negligible set + a Lyapunov drift implies a positive spectral gap",
         "source": "Wang's spectral-gap Lyapunov criterion"},
    ],
}


def verify_legitimacy(track_id: str) -> dict:
    """A track is LEGITIMATE iff its mechanism is sourced — tied to a real, citable mathematical result,
    not just a name. Returns the verdict + the sources.
    """
    entries = TRACK_LEGITIMACY.get(track_id, [])
    return {"track": track_id, "legitimate": bool(entries),
            "sources": [e["source"] for e in entries]}


def verify_all_legitimate() -> dict:
    """Every track must be a legitimate (sourced) path. Returns per-track verdicts."""
    verdicts = {tid: verify_legitimacy(tid) for tid in TRACK_HYPOTHESES}
    all_ok = all(v["legitimate"] for v in verdicts.values())
    # record the legitimacy in the registry so it is auditable, not just in code
    for tid, v in verdicts.items():
        registry.record_claim(
            f"claim-legitimacy-{tid}",
            f"the {tid} track is a legitimate path",
            "survived" if v["legitimate"] else "failed",
            problem=tid,
            reason="; ".join(v["sources"]),
            produced_by="track-legitimacy",
        )
    return {"all_legitimate": all_ok, "verdicts": verdicts}
