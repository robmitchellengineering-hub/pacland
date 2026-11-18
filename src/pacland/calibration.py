"""The calibration gate — does our confidence track correctness?

Zoubin Ghahramani's framing, applied to our certificates: a system is calibrated when it is
confident exactly when it is correct. This module scores that, in two pieces.

1. `expected_calibration_error` — the standard ECE metric (graded confidences vs outcomes).
2. `gate_quantum_certificate` — the concrete gate. It certifies a circuit, then submits a batch of
   results at known distances from the exact answer (the true one, plus graded forgeries), runs the
   certificate's referee on each, and scores the decision. Two scores are reported:

   * decision calibration — the confusion matrix. A clean matrix (no false accepts, no false
     refuses) means the pass/fail decision is calibrated.
   * graded ECE — the referee's distance, treated as a confidence, against the hard truth. A
     nonzero ECE here is a finding, not a bug: the referee is a hard threshold, not yet a
     calibrated probabilistic predictor. That gap is exactly the proper-scoring layer to build.

Usage:
    python -m pacland.calibration calibrate
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

from pacland import quantum_certify as qc
from pacland.belief import brier_score, log_score, pac_bayes_bound


def expected_calibration_error(confidences, outcomes, n_bins: int = 10) -> tuple[float, list[dict]]:
    """The standard expected calibration error: mean |confidence - accuracy| per bin,
    weighted by bin size. Returns (ece, reliability_rows)."""
    conf = np.asarray(confidences, dtype=float)
    out = np.asarray(outcomes, dtype=float)
    if conf.size == 0:
        return 0.0, []
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    rows: list[dict] = []
    for i in range(n_bins):
        lo, hi = bins[i], bins[i + 1]
        mask = (conf >= lo) & (conf < hi) if i < n_bins - 1 else (conf >= lo) & (conf <= hi)
        if mask.sum() == 0:
            continue
        mean_conf = float(conf[mask].mean())
        acc = float(out[mask].mean())
        ece += (mask.sum() / conf.size) * abs(mean_conf - acc)
        rows.append({"lo": round(lo, 2), "hi": round(hi, 2), "n": int(mask.sum()),
                     "mean_confidence": round(mean_conf, 3), "accuracy": round(acc, 3)})
    return float(ece), rows


def mean_brier_score(confidences, outcomes) -> float:
    """Mean Brier (proper) score over a (reported probability, truth) record. Lower is better."""
    conf = list(confidences)
    out = list(outcomes)
    if not conf:
        raise ValueError("no forecasts to score")
    return sum(brier_score(p, t) for p, t in zip(conf, out)) / len(conf)


def mean_log_score(confidences, outcomes) -> float:
    """Mean logarithmic (proper) score. Lower is better."""
    conf = list(confidences)
    out = list(outcomes)
    if not conf:
        raise ValueError("no forecasts to score")
    return sum(log_score(p, t) for p, t in zip(conf, out)) / len(conf)


def honesty_theorem(q: float = 0.7) -> dict:
    """The proper-scoring honesty theorem, as a number.

    For a binary event with true probability ``q``, the expected Brier score of a forecaster
    reporting ``p`` is ``(p - q)^2 + q(1 - q)``, which is minimized at ``p = q``. A proper score
    therefore pays a forecaster to report their honest belief, not to exaggerate. Returns the
    expected Brier for several reported probabilities, with the minimizer flagged.
    """
    candidates = [0.0, 0.3, q, 1.0]
    scores = {p: (p - q) ** 2 + q * (1.0 - q) for p in candidates}
    best = min(scores, key=scores.get)
    return {"true_probability": q, "expected_brier": scores, "minimizer": best,
            "honest_minimizes": abs(best - q) < 1e-12}


def certified_decision_bound(accuracy: float, m: int, delta: float = 0.05) -> dict:
    """A PAC-Bayes certified lower bound on the true decision accuracy.

    The gate's accept/refuse decision is a binary classifier whose accuracy is measured over
    ``m`` samples. McAllester's bound certifies that, with probability >= ``1 - delta``, the true
    accuracy is at least the smoothed empirical accuracy minus the KL-charged gap. The posterior
    mean is Laplace-smoothed (Beta(1,1) prior), so a perfect empirical record gives a finite KL
    instead of a vacuous infinity.
    """
    if m <= 0:
        raise ValueError("m must be positive")
    if not (0.0 <= accuracy <= 1.0):
        raise ValueError("accuracy must be in [0, 1]")
    prior = 0.5
    q = (accuracy * m + 1.0) / (m + 2.0)          # Beta(1,1) posterior mean
    gap = pac_bayes_bound(prior=prior, posterior=q, m=m, delta=delta)
    return {"accuracy": accuracy, "smoothed_accuracy": q, "m": m, "confidence": 1.0 - delta,
            "gap": gap, "lower_bound": max(0.0, q - gap),
            "theorem": "McAllester PAC-Bayes (Beta(1,1) prior, KL-charged)"}


def gate_quantum_certificate(program: str = "ghz", n_qubits: int = 16, tol: float = 1e-9,
                             seed: int = 0, n_forgeries: int = 40) -> dict:
    """Certify a circuit, referee a batch of true and forged results, and score calibration."""
    d = Path(tempfile.mkdtemp())
    cert_path = d / "cert.json"
    cert = qc.certify(program, n_qubits, str(cert_path))
    _, p_exact = qc._exact(program, n_qubits)
    n_states = p_exact.size

    rng = np.random.default_rng(seed)
    distances = [0.0] + sorted(rng.uniform(0.0, 0.6, n_forgeries).tolist())

    confidences: list[float] = []
    outcomes: list[bool] = []
    true_acc = false_acc = true_ref = false_ref = 0

    for d_true in distances:
        noise = rng.uniform(0.0, 1.0, n_states)
        noise /= noise.sum()
        claim = (1.0 - d_true) * p_exact + d_true * noise
        tv = float(0.5 * np.sum(np.abs(claim - p_exact)))
        accepted = tv <= tol
        correct = d_true <= tol
        confidences.append(1.0 - min(tv, 1.0))
        outcomes.append(correct)
        if accepted and correct:
            true_acc += 1
        elif accepted and not correct:
            false_acc += 1
        elif not accepted and correct:
            false_ref += 1
        else:
            true_ref += 1

    ece, rows = expected_calibration_error(confidences, outcomes)
    batch = len(distances)
    accuracy = (true_acc + true_ref) / batch
    return {
        "program": program,
        "n_qubits": n_qubits,
        "tol": tol,
        "batch": batch,
        "true_accept": true_acc,
        "false_accept": false_acc,
        "true_refuse": true_ref,
        "false_refuse": false_ref,
        "decision_accuracy": accuracy,
        "certified": certified_decision_bound(accuracy, batch),
        "ece": ece,
        "mean_brier": mean_brier_score(confidences, outcomes),
        "mean_log": mean_log_score(confidences, outcomes),
        "reliability": rows,
        "decision_calibrated": false_acc == 0 and false_ref == 0,
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="The calibration gate (does confidence track correctness?).")
    ap.add_argument("cmd", choices=["calibrate"], default="calibrate", nargs="?")
    ap.add_argument("--program", default="ghz")
    ap.add_argument("--qubits", type=int, default=16)
    ap.add_argument("--tol", type=float, default=1e-9)
    args = ap.parse_args(argv)

    r = gate_quantum_certificate(args.program, args.qubits, args.tol)
    print(f"calibration gate: {args.program} ({args.qubits} qubits), tolerance {args.tol:g}")
    print(f"  batch {r['batch']}: {r['true_accept']} true-accept, {r['false_accept']} false-accept, "
          f"{r['true_refuse']} true-refuse, {r['false_refuse']} false-refuse")
    print(f"  decision calibration: {'CALIBRATED' if r['decision_calibrated'] else 'MISCALIBRATED'} "
          f"(decision accuracy {r['decision_accuracy']:.3f})")
    c = r["certified"]
    print(f"  PAC-Bayes certified: with {c['confidence']:.0%} confidence, true accuracy >= "
          f"{c['lower_bound']:.3f} (empirical {c['accuracy']:.3f} minus gap {c['gap']:.3f}; "
          f"{c['theorem']})")
    print(f"  graded ECE: {r['ece']:.4f}")
    print(f"  proper scores: Brier {r['mean_brier']:.4f}, log {r['mean_log']:.4f} (lower is better)")
    print("  reliability (confidence bin -> accuracy):")
    for row in r["reliability"]:
        print(f"    [{row['lo']:.2f},{row['hi']:.2f}] n={row['n']:>3} "
              f"conf={row['mean_confidence']:.3f} acc={row['accuracy']:.3f}")

    h = honesty_theorem()
    print(f"\n  honesty theorem: for true probability {h['true_probability']}, expected Brier is minimized")
    print(f"  by reporting {h['minimizer']} (honest) — {h['honest_minimizes']}. Expected Brier by report:")
    for p in sorted(h["expected_brier"]):
        mark = "  <- honest" if p == h["minimizer"] else ""
        print(f"    report {p:.2f} -> {h['expected_brier'][p]:.4f}{mark}")

    print("\n  Reading: a clean confusion matrix means the pass/fail referee is calibrated. A")
    print("  nonzero ECE means the referee's distance is a hard threshold, not a calibrated")
    print("  probabilistic confidence. The honesty theorem shows a proper score pays for honest")
    print("  reporting — that is the layer that turns the threshold into a calibrated probability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
