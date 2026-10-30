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
            "`h12 = 5` sampler yield is **zero** at instanton degree 0, 1 **and** 2 "
            "(~360 valid candidates each, ~180 s; JOBS.md, 2026-10-29)",
            "#208 concluded the `h12 >= 5` wall is degree-1 truncation and that **degree 2 fixes it**",
        ],
        "clash": "one says degree 2 does not help; the other says it is the fix",
        "discriminator": ("recompute `cond(M)` — the quantity #208 measured — for the *same* `h12 = 5` "
                          "proposals at degree 1 and degree 2, and compare it with the observed yield. If the "
                          "diagnostic improves and the yield stays zero, #208 measured the wrong thing; if "
                          "both improve, the yield run had a different fault (budget or initialisation)."),
        "state": "open",
        "resolution": "",
        "cost": "one node job, ~15 min (pacland-rog, the cytools venv)",
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
            "the same F1 table shows `flux-uniform` and `primitive` agreeing exactly (0.2015 both)",
        ],
        "clash": "a 5x spread across measures, and two of those measures indistinguishable",
        "discriminator": "ask `measures.table()` which measures differ for the property, and check that the "
                        "ratio is max/min rather than a real-vs-null comparison",
        "state": "resolved",
        "resolution": ("the 5.05x is `max/min` across five defensible measures (`log-N` 0.3609 vs "
                       "`tadpole-uniform` 0.0714). `flux-uniform` and `primitive` coincide here because "
                       "primitivity and `|N| <= 1` are independent in the window — so an analysis that "
                       "compared *those two* would have reported 1.00 and called it robust. Both facts are "
                       "true; the tension was a temptation, and the robustness regression test pins it."),
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
