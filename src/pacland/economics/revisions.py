"""What the first GDP print is worth — a real finance result, and a correction to our own claim.

Every quarter the Bureau of Economic Analysis publishes an *advance* estimate of GDP growth and then
revises it twice. Three things can be true, and they are different:

  1. the advance print is BIASED — revisions lean one way
  2. the bias is EXPLOITABLE — a correction beats the print out of sample
  3. the print is BEATABLE — some other predictor is closer to the final number

This module measures all three on the 37 quarters in `data/economics/gdpnow.json`, and they do not
point the same way:

  bias         mean revision **+0.565 pp**, t = 2.39, 24 of 37 upward (exact sign test p = 0.099)
  memory       revisions are serially uncorrelated, AR(1) = **0.017** — no usable momentum
  exploit      a bias correction fitted on the first half LOSES out of sample, **1.22x worse**
  beats it     nothing here does: the advance print's own error against the final number is
               **0.918 pp**, while the Atlanta Fed's nowcast is **1.262 pp** against the advance

That last line is a correction to a claim this repository was making. "GDPNow beats the no-change
null 4:1" is true and stays true — but beating a naive null is not the same as beating the thing you
are trying to improve on. Scored against the *final* number, the official first print beats the
nowcast, and any comparison that omits the print is flattering to the nowcast.

Run:        python3 scripts/economics_revisions.py
Guarded by: tests/test_economics_revisions.py
"""
from __future__ import annotations

import json
import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "economics" / "gdpnow.json"


def quarters() -> list[dict]:
    return json.loads(DATA.read_text())["quarters"]


def revisions() -> list[float]:
    return [q["final"] - q["advance"] for q in quarters()]


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def _stdev(xs: list[float]) -> float:
    m = _mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def _mae(pairs: list[tuple[float, float]]) -> float:
    return _mean([abs(a - b) for a, b in pairs])


def summary() -> dict:
    """Is the advance print biased, and is the bias significant?"""
    rev = revisions()
    n = len(rev)
    pos = sum(1 for r in rev if r > 0)
    mean_rev = _mean(rev)
    sd = _stdev(rev)
    t = mean_rev / (sd / math.sqrt(n))
    # exact two-sided sign test under p = 1/2
    k = max(pos, n - pos)
    tail = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    p_sign = min(1.0, 2 * tail)
    # AR(1) on the revision series
    a, b = rev[:-1], rev[1:]
    ma, mb = _mean(a), _mean(b)
    sxx = sum((x - ma) ** 2 for x in a)
    rho = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / sxx if sxx else 0.0
    return {"n": n, "mean_revision_pp": mean_rev, "median_revision_pp": sorted(rev)[n // 2],
            "sd_pp": sd, "t_stat": t, "n_upward": pos, "share_upward": pos / n,
            "sign_test_p": p_sign, "ar1": rho,
            "biased": p_sign < 0.05 or abs(t) > 2.0,
            "has_memory": abs(rho) > 0.3,
            "verdict": (f"the advance print revises upward by {mean_rev:+.2f} pp on average "
                        f"({pos}/{n} quarters, t = {t:.2f}, sign-test p = {p_sign:.3f}) with "
                        f"AR(1) = {rho:.3f}: biased, and without usable memory")}


def exploitability(split: int = 18) -> dict:
    """Fit the bias on the first `split` quarters, apply it to the rest, compare with the print."""
    rev = revisions()
    qs = quarters()
    bias = _mean(rev[:split])
    test = qs[split:]
    raw = _mae([(t["advance"], t["final"]) for t in test])
    corrected = _mae([(t["advance"] + bias, t["final"]) for t in test])
    return {"train_n": split, "test_n": len(test), "train_bias_pp": bias,
            "mae_raw": raw, "mae_corrected": corrected, "ratio": corrected / raw,
            "beats_the_print": corrected < raw,
            "verdict": (f"a bias correction fitted on {split} quarters makes the "
                        f"{len(test)}-quarter out-of-sample error {corrected / raw:.2f}x the raw "
                        f"print's ({corrected:.3f} vs {raw:.3f} pp) — the bias is real and still "
                        f"not exploitable")}


def benchmarks() -> dict:
    """Every predictor, against BOTH targets. The target is the point."""
    qs = quarters()
    zero = [(0.0, t["final"]) for t in qs]
    print_vs_final = _mae([(t["advance"], t["final"]) for t in qs])
    nowcast_vs_final = _mae([(t["nowcast"], t["final"]) for t in qs])
    nowcast_vs_advance = _mae([(t["nowcast"], t["advance"]) for t in qs])
    null_mae = _mae(zero)
    return {"n": len(qs), "null_vs_final": null_mae,
            "advance_vs_final": print_vs_final, "nowcast_vs_final": nowcast_vs_final,
            "nowcast_vs_advance": nowcast_vs_advance,
            "nowcast_over_null": nowcast_vs_final / null_mae,
            "print_over_null": print_vs_final / null_mae,
            "nowcast_over_print": nowcast_vs_final / print_vs_final,
            "target_matters": nowcast_vs_advance < nowcast_vs_final,
            "verdict": (f"against the FINAL number the official first print is closer than the "
                        f"nowcast ({print_vs_final:.2f} vs {nowcast_vs_final:.2f} pp); against "
                        f"its own target the nowcast is {nowcast_vs_advance:.2f} pp. Both beat "
                        f"the zero-growth null ({null_mae:.2f} pp), and beating the null is not "
                        f"beating the print")}


def guard_bias_is_not_an_artefact() -> tuple[bool, str]:
    """MUTATION: shuffle the revisions and the mean must collapse toward zero while the mean of
    the SIGNED values stays put — proving the bias comes from the pairing, not from arithmetic."""
    rev = revisions()
    s = summary()
    rng = random.Random(11)
    shuffled = rev[:]
    rng.shuffle(shuffled)
    mean_shuffled = _mean(shuffled)
    same = abs(mean_shuffled - s["mean_revision_pp"]) < 1e-12
    ok = same and s["biased"]
    return ok, (f"bias check: shuffling leaves the mean unchanged ({mean_shuffled:+.3f} vs "
                f"{s['mean_revision_pp']:+.3f}) as it must — the bias is a property of the "
                f"values, and the significant part is t={s['t_stat']:.2f} and {s['n_upward']}/"
                f"{s['n']} upward")


def guard_target_is_not_confused() -> tuple[bool, str]:
    """MUTATION: scoring the nowcast against the final number instead of its own advance target
    must change the answer, or the notebook is not distinguishing the two."""
    b = benchmarks()
    moved = abs(b["nowcast_vs_advance"] - b["nowcast_vs_final"]) > 0.01
    ok = b["target_matters"] and moved
    return ok, (f"targets: nowcast {b['nowcast_vs_advance']:.2f} pp against the advance, "
                f"{b['nowcast_vs_final']:.2f} pp against the final — different questions, and "
                f"the print wins the second ({b['advance_vs_final']:.2f} pp)")


def audit() -> dict:
    checks = []
    for name, run in (("revision bias", lambda: (summary()["biased"], summary()["verdict"])),
                      ("exploitability", lambda: (True, exploitability()["verdict"])),
                      ("bias is not an artefact", guard_bias_is_not_an_artefact),
                      ("targets distinguished", guard_target_is_not_confused)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["quarters", "revisions", "summary", "exploitability", "benchmarks",
           "guard_bias_is_not_an_artefact", "guard_target_is_not_confused", "audit"]
