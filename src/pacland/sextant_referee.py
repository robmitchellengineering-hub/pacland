"""SEXTANT hardware referee — classify a quantum *device* against the kernel-checked QM tower.

The CATALOG in `sextant.py` classifies *claims* (forced / free / impossible). This module
classifies a *device's* shot statistics against the same kernel-checked bounds — the "ready for
real quantum hardware" half of SEXTANT. Today it consumes simulated or recorded data; when a
domestic NISQ QPU exists, the same referee certifies or refuses its output.

Qubit capacity is RAM-bounded, not a fixed count (D41). The referee fixes no qubit number: the
simulator (Phantom) runs whatever the machine's RAM holds, and the three backends scale
differently — Clifford/stabilizer (Stim) polynomial (thousands, ~free); tensor-network
(Quimb/MERA) bond-dimension; full state vector (QuEST) 2^n (~30-40 q per few GB). The referee
classifies whatever a device reports, at whatever scale.

Verdict discipline (rule 67): a device is UNKNOWN unless a circuit's statistics actually ran.
A result is IMPOSSIBLE only when it exceeds a kernel-checked bound by a stated significance —
which is what separates noise from fraud.
"""
from __future__ import annotations

import math

# Kernel-checked bounds (pacland-proof/PaclandProof/QM/CHSH.lean, Tsirelson.lean).
BELL = 2.0
TSIRELSON = 2.0 * math.sqrt(2.0)  # 2.828427...

IMPOSSIBLE, FORCED, UNKNOWN = "IMPOSSIBLE", "FORCED", "UNKNOWN"
CERTIFIED, REFUSED = "CERTIFIED", "REFUSED"


def chsh_s(exp: dict[str, float]) -> float:
    """CHSH correlator S = E(0,0) + E(0,1) + E(1,0) - E(1,1)."""
    return exp["00"] + exp["01"] + exp["10"] - exp["11"]


def chsh_sigma(exp: dict[str, float], shots: int) -> float:
    """Standard error of S. v0 model: each E is a +-1-observable estimator,
    Var(E) ~ (1 - E^2)/N with independent terms."""
    var = sum((1.0 - e * e) for e in exp.values()) / max(shots, 1)
    return math.sqrt(max(var, 0.0))


def classify_chsh(s: float, sigma: float, k: float = 5.0) -> tuple[str, str]:
    """Classify a device's CHSH result against the kernel-checked bounds, by significance.

    Returns (verdict, why). The significance `k` (default 5 sigma) is the whole point: a bound is
    only "exceeded" when the excess is statistically real, otherwise noise would read as fraud.
    """
    if s > TSIRELSON + k * sigma:
        return IMPOSSIBLE, (
            f"S={s:.3f} exceeds Tsirelson 2√2 by {s - TSIRELSON:.3f} ({k}σ): "
            "no quantum state does this — noise miscalibration or fraud (QM.Tsirelson)")
    if s > BELL + k * sigma:
        return FORCED, (
            f"S={s:.3f} violates the Bell wall 2 by >{k}σ: entanglement certified "
            "(QM.CHSH + QM.Entanglement — LOCC cannot produce it)")
    return UNKNOWN, (
        f"S={s:.3f} within {k}σ of the classical wall 2: no quantum evidence — "
        "a classical device could have produced this (rule 67)")


def referee(device: dict, k: float = 5.0) -> dict:
    """Referee one device's shot record.

    `device` is ``{"circuits": {"chsh": {"expectations": {"00","01","10","11"}, "shots": N}}}``.
    Summary is CERTIFIED / REFUSED / UNKNOWN; each ran circuit gets a certificate with its
    verdict, measured value, significance, theorem and falsifier.
    """
    circuits = device.get("circuits", {})
    if not circuits:
        return {"verdict": UNKNOWN, "certificates": [],
                "reason": "no circuits ran — absent evidence is not green (rule 67)"}

    certificates: list[dict] = []
    rec = circuits.get("chsh")
    if rec:
        exp, shots = rec["expectations"], rec["shots"]
        s, sigma = chsh_s(exp), chsh_sigma(exp, shots)
        verdict, why = classify_chsh(s, sigma, k)
        certificates.append({
            "circuit": "chsh",
            "S": round(s, 4), "sigma": round(sigma, 4), "shots": shots,
            "theorem": "QM.Tsirelson (S <= 2√2) / QM.CHSH (Bell wall 2)",
            "falsifier": f"S > 2√2 + {k}σ",
            "verdict": verdict, "why": why,
        })

    verdicts = {c["verdict"] for c in certificates}
    if IMPOSSIBLE in verdicts:
        summary = REFUSED
    elif FORCED in verdicts:
        summary = CERTIFIED
    else:
        summary = UNKNOWN
    return {"verdict": summary, "certificates": certificates,
            "reason": f"{len(certificates)} circuit(s) ran; per-circuit {sorted(verdicts)}"}


def probe_devices() -> dict[str, dict]:
    """The synthetic devices the falsifier tests run: one to certify, one to refuse, one to
    refuse-to-certify, and one empty (UNKNOWN)."""
    e = 1.0 / math.sqrt(2.0)
    chsh = lambda a, b, c, d: {"circuits": {"chsh": {  # noqa: E731
        "expectations": {"00": a, "01": b, "10": c, "11": d}, "shots": 10**6}}}
    return {
        "quantum": chsh(e, e, e, -e),     # S = 2√2 -> CERTIFIED
        "cheating": chsh(0.75, 0.75, 0.75, -0.75),  # S = 3.0 -> REFUSED
        "classical": chsh(0.5, 0.5, 0.5, -0.5),     # S = 2.0 -> UNKNOWN
        "empty": {},
    }
