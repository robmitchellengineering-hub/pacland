#!/usr/bin/env python3
"""The tension register — pairs of established facts that cannot both be true as stated.

    python3 scripts/tensions.py           # write docs/tensions.md
    python3 scripts/tensions.py --check   # fail if stale (drift guard, runs in the suite)

A tension is more useful than a defect: it is a **question with a computable answer**. Each entry carries
the two facts, why they clash, the cheapest discriminating computation, and a state — open, or resolved with
the resolution written down. Nothing enters without both facts being established somewhere in the repo.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "tensions.md"

TENSIONS = [
    {
        "id": "T1",
        "facts": [
            "`h12 = 5` sampler yield was **zero** at instanton degree 0, 1 **and** 2 at 400 tries each",
            "#208 concluded the `h12 >= 5` wall is degree-1 truncation and that **degree 2 fixes it**",
        ],
        "clash": "one says degree 2 does not help; the other says it is the fix",
        "discriminator": ("spend a real budget with `try_budget.run_to_budget` (calls, not `n_target`) and "
                          "compare the two degrees"),
        "state": "resolved",
        "resolution": ("**both degrees work; the zero was a budget artefact.** Five calls each (~2,000 tries) "
                       "on pacland-rog: degree 1 → **2 points** `[0,1,0,0,1]` in 504 s, degree 2 → **2 points** "
                       "`[0,0,1,0,1]` in 521 s. Indistinguishable. So `h12 = 5` is **not** a degree wall: "
                       "degree 1 yields at the same rate, and the earlier zero was 400 tries being too few. "
                       "#208's \"degree 2 fixes it\" is refuted as a statement about yield — the real wall "
                       "is the **rate** (~0.008 points per valid candidate at `h12 = 5`, against 0.138 at "
                       "`h12 = 2`), which no degree change addresses. Job state was `suspect` with the "
                       "DEGREE lines and DONE present; the per-call counts are the datum."),
        "cost": "done — one node job, ~15 min",
    },
    {
        "id": "T2",
        "facts": [
            "the pooled SUSY fraction is **21.17%** (95% CI [20.15, 22.22], 5,962 primitive rows)",
            "the stratified rates are **27.9%** at `h12 = 2` and **1.2%** at `h12 = 4`",
        ],
        "clash": "a pooled 21% and a 1.2% stratum cannot both be *the* SUSY fraction",
        "discriminator": "the robustness engine — pool the strata with the stated weights and see whether the "
                        "pooled number is the weighted average",
        "state": "resolved",
        "resolution": ("no contradiction: 21.17% **is** the row-weighted average of the strata. The tension "
                       "was in the quoting, not the physics — so the fraction must be quoted stratified, with "
                       "its weighting (`python3 scripts/robustness.py`)."),
        "cost": "done",
    },
    {
        "id": "T3",
        "facts": [
            "F1 states the small-tadpole fraction is **0.071 or 0.361** depending on measure — **5.05x**",
            "Route A: the same flux-uniform fraction is **0.901 at `b3=2`, 0.744 at `b3=4`, 0.644 at `b3=6`**",
        ],
        "clash": "a 5x spread across measures, and a further 40% movement across window sizes",
        "discriminator": "ask `measures.table()` which measures differ, AND `scaling.py` how the value moves "
                        "with `b3` — two independent dependencies on one number",
        "state": "resolved",
        "resolution": ("the 5.05x is `max/min` across five defensible measures (`log-N` 0.3609 vs "
                       "`tadpole-uniform` 0.0714). **And it is a ratio at one window size**: the flux-uniform "
                       "fraction moves 0.901 → 0.644 as `b3` goes 2 → 6, so the ratio is not a landscape "
                       "invariant either. Both facts are true; the tension was a temptation, and the "
                       "robustness regression test plus the scaling study now pin both halves."),
        "cost": "done",
    },
    {
        "id": "T4",
        "facts": [
            "`is_minimum` disagrees with the stored eigenvalues on **12 of 1,263** SUSY rows",
            "11 of those 12 have `|lambda_min| < 1e-20` — the flag is rounding, not geometry",
        ],
        "clash": "a boolean column that disagrees with its own evidence",
        "discriminator": "recover the threshold: compare the flag against `min(eigenvalue) > t` at every `t`",
        "state": "resolved",
        "resolution": ("`is_minimum` is **exactly** `min(eigenvalue) > 1e-6` — 0 missing, 0 extra across 5,965 "
                       "rows. Every minima count now carries that threshold; the corpus's own numbers move "
                       "2x (4,111 at t=0 to 2,045 at t=1e-3) across the plausible range."),
        "cost": "done",
    },
    {
        "id": "T5",
        "facts": [
            "3 of 5,965 corpus rows are **non-primitive** (gcd 2), and no primitive parent appears anywhere",
            "the flux-scaling lemma says `(F,H)` and `d(F,H)` are the **same** vacuum",
        ],
        "clash": "a corpus of distinct vacua contains three that are copies, with the originals missing",
        "discriminator": "gcd every stored flux against `windows.primitive`, then look for the parents",
        "state": "resolved",
        "resolution": ("a **coverage** defect, not duplication: those three classes are represented only by a "
                       "copy, one of them SUSY. At 0.05% it cannot move any published fraction, and "
                       "`corpus_primitivity()` now refuses a corpus whose rate grows."),
        "cost": "done",
    },
]


def render(items) -> str:
    out = ["# Tensions — facts that cannot both be true as stated",
           "",
           "*Generated by `python3 scripts/tensions.py`. A tension is a question with a computable answer: "
           "each entry carries the two facts, why they clash, the cheapest discriminator, and a state.*",
           "",
           f"**{len(items)} entries: {sum(1 for i in items if i['state'] == 'open')} open, "
           f"{sum(1 for i in items if i['state'] != 'open')} resolved.**", ""]
    for t in items:
        out += [f"## {t['id']} — {t['clash']}", "", f"**State: {t['state'].upper()}**", "", "Facts:"]
        out += [f"- {f}" for f in t["facts"]]
        out += ["", f"**Clash.** {t['clash']}.", "",
                f"**Cheapest discriminator.** {t['discriminator']}", ""]
        if t["resolution"]:
            out += [f"**Resolution.** {t['resolution']}", ""]
        out += [f"*cost:* {t['cost']}", ""]
    return "\n".join(out)


def main() -> int:
    text = render(TENSIONS)
    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"MISSING: {OUT}")
            return 1
        if OUT.read_text() != text:
            print("STALE: docs/tensions.md does not match a fresh generation")
            return 1
        print("current")
        return 0
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(text.splitlines())} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
