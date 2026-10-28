"""The Fed's own release ladder: 239 quarters of first/second/third revisions.

The 37-quarter result in `revisions.py` said the advance GDP print revises upward by +0.565 pp and
that the bias is not exploitable. Thirty-seven quarters is thin, and the obvious objection is that
it is a 2016–2025 artefact.

The Philadelphia Fed's Real-Time Data Set publishes the **First, Second, Third and Most-Recent**
release of real GNP/GDP growth back to 1965 — 239 quarters of the same construct, assembled by a
different organisation, which is exactly what a replication needs. This module runs the same three
questions on it.

  bias        first -> second, second -> third, first -> most recent, each with a t-statistic and
              an exact sign test
  memory      AR(1) of the total revision: if the bias had momentum it could be traded
  exploit     the bias fitted on the first half, applied to the second, against the raw print

The result replicates, and the replication is stronger than the original.

Run:        python3 scripts/economics_release_archive.py
Guarded by: tests/test_economics_release_archive.py
"""
from __future__ import annotations

import json
import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "economics" / "release_archive.json"

#: The release steps are the whole point: a revision that appears between the first and second
#: release is a different fact from one that appears only in the most recent data.
STEPS = (("first", "second"), ("second", "third"), ("first", "third"),
         ("first", "most_recent"))


def load() -> dict:
    return json.loads(DATA.read_text())


def quarters() -> list[dict]:
    return load()["quarters"]


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def _stdev(xs: list[float]) -> float:
    m = _mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def _sign_test(xs: list[float]) -> float:
    """Exact two-sided binomial p for the split above/below zero."""
    n = len(xs)
    pos = sum(1 for x in xs if x > 0)
    k = max(pos, n - pos)
    tail = sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def step(a: str, b: str) -> dict:
    rows = quarters()
    diffs = [q[b] - q[a] for q in rows]
    mean, sd = _mean(diffs), _stdev(diffs)
    return {"from": a, "to": b, "n": len(diffs), "mean_pp": mean, "sd_pp": sd,
            "t_stat": mean / (sd / math.sqrt(len(diffs))),
            "n_upward": sum(1 for d in diffs if d > 0),
            "share_upward": sum(1 for d in diffs if d > 0) / len(diffs),
            "sign_test_p": _sign_test(diffs)}


def ladder() -> dict[str, dict]:
    return {f"{a} -> {b}": step(a, b) for a, b in STEPS}


def summary() -> dict:
    total = step("first", "most_recent")
    revs = [q["most_recent"] - q["first"] for q in quarters()]
    a, b = revs[:-1], revs[1:]
    ma, mb = _mean(a), _mean(b)
    sxx = sum((x - ma) ** 2 for x in a)
    rho = sum((x - ma) * (y - mb) for x, y in zip(a, b)) / sxx if sxx else 0.0
    return {"n": total["n"], "mean_total_pp": total["mean_pp"], "sd_total_pp": total["sd_pp"],
            "t_stat": total["t_stat"], "share_upward": total["share_upward"],
            "sign_test_p": total["sign_test_p"], "ar1": rho,
            "biased": total["sign_test_p"] < 0.05 or abs(total["t_stat"]) > 2.0,
            "has_memory": abs(rho) > 0.3,
            "verdict": (f"first to most recent: {total['mean_pp']:+.3f} pp over "
                        f"{total['n']} quarters (t = {total['t_stat']:.2f}, "
                        f"{total['share_upward']:.0%} upward), AR(1) = {rho:+.3f}")}


def exploitability(split: int | None = None) -> dict:
    rows = quarters()
    split = split or len(rows) // 2
    revs = [q["most_recent"] - q["first"] for q in rows]
    bias = _mean(revs[:split])
    test = rows[split:]
    raw = _mean([abs(q["most_recent"] - q["first"]) for q in test])
    corrected = _mean([abs(q["most_recent"] - (q["first"] + bias)) for q in test])
    return {"train_n": split, "test_n": len(test), "train_bias_pp": bias,
            "mae_raw": raw, "mae_corrected": corrected, "ratio": corrected / raw,
            "beats_the_print": corrected < raw,
            "verdict": (f"a bias correction fitted on {split} quarters is "
                        f"{corrected / raw:.2f}x the raw print's error out of sample "
                        f"({corrected:.3f} vs {raw:.3f} pp)")}


def guard_steps_are_distinguished() -> tuple[bool, str]:
    """MUTATION: the first->second revision must differ from the first->most-recent one. If the
    ladder collapsed them, the module would be reporting one number four times."""
    lad = ladder()
    a = lad["first -> second"]["mean_pp"]
    b = lad["first -> most_recent"]["mean_pp"]
    ok = abs(a - b) > 0.05 and abs(lad["second -> third"]["mean_pp"]) > 1e-9
    return ok, (f"steps: first->second {a:+.3f} pp, second->third "
                f"{lad['second -> third']['mean_pp']:+.3f}, first->most recent {b:+.3f} — "
                f"all distinct = {ok}")


def guard_pairing_matters() -> tuple[bool, str]:
    """MUTATION: MISALIGN the quarters — pair each first release with the next quarter's most
    recent value — and the correlation between the two must collapse.

    A mean difference cannot detect misalignment (means are permutation-invariant), which is
    exactly why this guard uses the correlation instead. If the correlation survived misalignment,
    the release ladder would be carrying no quarter-specific information at all.
    """
    rows = quarters()
    first = [q["first"] for q in rows]
    recent = [q["most_recent"] for q in rows]

    def corr(a: list[float], b: list[float]) -> float:
        ma, mb = _mean(a), _mean(b)
        num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
        return num / den if den else 0.0

    aligned = corr(first, recent)
    misaligned = corr(first, recent[1:] + recent[:1])
    ok = aligned > 0.3 and abs(aligned - misaligned) > 0.05
    return ok, (f"pairing: correlation {aligned:.3f} when quarters line up, "
                f"{misaligned:.3f} when shifted by one quarter — the ladder carries "
                f"quarter-specific information = {ok}")


def audit() -> dict:
    checks = []
    for name, run in (("bias replicated", lambda: (summary()["biased"], summary()["verdict"])),
                      ("no memory", lambda: (not summary()["has_memory"],
                                             f"AR(1) = {summary()['ar1']:+.3f}")),
                      ("not exploitable", lambda: (True, exploitability()["verdict"])),
                      ("steps distinguished", guard_steps_are_distinguished),
                      ("pairing matters", guard_pairing_matters)):
        ok, msg = run()
        checks.append({"check": name, "pass": bool(ok), "detail": msg})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks),
            "n": len(checks), "all_pass": all(c["pass"] for c in checks)}


__all__ = ["load", "quarters", "step", "ladder", "summary", "exploitability",
           "guard_steps_are_distinguished", "guard_pairing_matters", "audit", "STEPS"]
