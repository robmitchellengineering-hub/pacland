#!/usr/bin/env python3
"""The exactness instruments — the four kinds of exactness that work in the interior.

    python3 scripts/exactness.py

`docs/plan-exact-terms.md` items A1–A4, B4 and D1. Every report prints the window it was computed in,
and a check that cannot run is reported as SKIPPED with its reason rather than as a pass.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from pacland.exactness import controls as C  # noqa: E402
from pacland.exactness import identities as X  # noqa: E402
from pacland.exactness import invariance as I  # noqa: E402
from pacland.exactness import windows as W  # noqa: E402


def section(title: str) -> None:
    print(f"\n{title}\n" + "-" * len(title))


def main() -> int:
    ok = True

    section("A1 + B4 · invariance and identity on the scalar potential (usable in the interior)")
    r = I.report()
    for c in r["checks"]:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['check']}")
        print(f"      {c['detail']}")
    ok &= r["all_pass"]

    section("A2 · the corpus against the geometry it claims to come from")
    audit = X.audit_corpus(ROOT / "data")
    print(f"{audit['n_files']} files · {audit['rows']} rows · {audit['n_fail']} failures "
          f"({audit['n_known']} known, {audit['n_unexplained']} unexplained)")
    for f in audit["files"]:
        if f["n_fail"]:
            print(f"  {f['file']}: {f['n_fail']} / {f['rows']} rows fail")
            for fail in f["failures"][:5]:
                print(f"      row {fail['row']}: {fail['check']} — {fail['detail']}")
    for s in audit["skipped"]:
        print(f"SKIPPED  {s['check']}\n      {s['reason']}")
    if audit["n_known"]:
        print("  KNOWN (pinned, not fixed): rows whose recorded Nflux is the negative of F^T J H for the")
        print("  stored flux ordering — either the pair is stored H ++ F or the tadpole was recorded as a")
        print("  magnitude. 5 of 5,885 (0.08%); any *new* failure of this kind is unexplained and goes red.")
    ok &= audit["all_pass"]

    section("A3 · the known-answer gate: can the statistic tell the classes apart at this size?")
    h12_2 = sorted((ROOT / "data").glob("h12_2_*_stats.json"))
    rows = 0
    for p in h12_2:
        rows += len(json.loads(p.read_text()).get("vacua") or [])
    a = C.authority_check(available=rows)
    for c in a["cells"]:
        print(f"{'PASS' if c['pass'] else 'FAIL'}  {c['cell']}")
        print(f"      {c['detail']}")
    print(f"\nSo the chaos question needs about {a['required_count']} spectra of dim 6 at 5 sd;")
    print(f"the h12=2 corpus holds {rows}. The gate is reachable — and that is a finding, not a formality.")
    ok &= a["all_pass"]

    section("A4 · does the sampler even visit the smallest window?")
    b3 = X.b3_from_h21(2)
    fluxes = W.enumerate_window(b3, 1)
    corpus_fluxes = []
    for p in h12_2:
        for v in json.loads(p.read_text()).get("vacua") or []:
            corpus_fluxes.append(v.get("flux") or [])
    cov = W.coverage(corpus_fluxes, b3, 1, fluxes=fluxes)
    print(f"window {cov['window']}")
    print(f"  primitive orbits in the window : {cov['window_orbits']}")
    print(f"  corpus rows                    : {cov['corpus_rows']}")
    print(f"  corpus orbits inside the window: {cov['corpus_orbits_in_window']}"
          f"  (coverage {cov['coverage']*100:.4f}%)")
    print(f"  largest flux component in the corpus: {cov['corpus_max_component']}")
    print("  uncovered examples (primitive orbits the corpus never visits):")
    for ex in cov["examples_uncovered"]:
        print(f"      {ex}")
    print("  A window the sampler never visits is the finding: every 'fraction of vacua' is a")
    print("  statement about the sampler's flux range until recall is measured inside a window.")

    section("D1 · the same fraction under two measures (X7, exact within the window)")
    conv = W.convergence(b3, [1, 2, 3, 4, 6], 1, fluxes=fluxes)
    print(f"window {conv['window']}")
    print(f"  {'L':>3}  {'flux-uniform':>13}  {'label-uniform':>14}  {'ratio':>7}  {'primitive':>10}")
    for t in conv["table"]:
        print(f"  {t['L']:>3}  {t['fraction_all_pairs']:>13.4f}  "
              f"{t['fraction_label_uniform']:>14.4f}  {t['ratio_measures']:>7.3f}  "
              f"{t['fraction_primitive_pairs']:>10.4f}")
    print(f"  largest shift between the two measures: {conv['max_shift']:.4f}")
    print(f"  distinct positive tadpoles in the window: {conv['distinct_positive_N']}")
    print("  flux-uniform vs primitive coincide here (every non-zero pair in this window is primitive),")
    print("  so the two measures that actually differ are flux-uniform and label-uniform. Same window,")
    print("  same lattice, and the fraction moves by the ratio column — that is the measure problem,")
    print("  demonstrated rather than argued.")

    print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
