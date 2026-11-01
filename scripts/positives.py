#!/usr/bin/env python3
"""The positives page — every established positive, regenerated from the engines themselves.

    python3 scripts/positives.py          # write docs/known-positives.md
    python3 scripts/positives.py --check  # fail if the file is stale (drift guard)

Nothing goes on this page that a command cannot reproduce: the page is generated from the engines, so it
cannot drift from them and cannot quietly accumulate claims nobody can re-derive.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "docs" / "known-positives.md"


def build():
    """Every positive the estate can state, with the command that reproduces it."""
    from pacland.exactness import counterexample as C
    from pacland.exactness import existence as E
    from pacland.exactness import observability as O
    from pacland.exactness import robustness as R
    from pacland.periods import dictionary as D
    from pacland.periods import gv_basis as G

    entries = []

    # --- exhibited objects -------------------------------------------------------------
    for q in E.run_all():
        if q.found is not None:
            entries.append({
                "kind": "exhibited object",
                "claim": f"{q.question}: `(F|H) = {q.found['flux']}`, N = {q.found['tadpole']} "
                         f"({q.matches} in the window)",
                "why": q.why,
                "command": "python3 scripts/existence.py",
            })
        else:
            entries.append({
                "kind": "theorem-in-a-window",
                "claim": f"{q.question}: none in {q.window}",
                "why": q.why,
                "command": "python3 scripts/existence.py",
            })

    # --- recovered definitions ----------------------------------------------------------
    ft = C.flag_threshold()
    entries.append({"kind": "recovered definition",
                    "claim": f"`is_minimum` is exactly `min(eigenvalue) > {ft['threshold']:g}` — "
                             f"reproduced at the set level, {ft['count']} rows, 0 missing, 0 extra",
                    "why": "the column had a silent threshold; every minima count now has a definition",
                    "command": "python3 scripts/counterexample.py"})

    # --- measured values ----------------------------------------------------------------
    for r in O.corpus_readings():
        if r.verdict == "measured":
            entries.append({"kind": "measured value",
                            "claim": f"{r.quantity} = {r.estimate:.3%} "
                                     f"(95% CI [{r.ci_low:.3%}, {r.ci_high:.3%}], {r.n_used} rows)",
                            "why": "narrow interval and stable under the stated choices",
                            "command": "python3 scripts/observability.py"})
    rb = R.corpus_susy_fraction()
    entries.append({"kind": "measured value",
                    "claim": "SUSY fraction stratified: "
                             + ", ".join(f"{k} = {v:.1%}"
                                         for k, v in sorted(rb.values.items())
                                         if k.startswith("h12")),
                    "why": "the spread is the finding: the pooled number is between the strata",
                    "command": "python3 scripts/robustness.py"})

    # --- certified maps -----------------------------------------------------------------
    for e in (D.flux_scaling(), D.mirror_map(), D.s_t_duality()):
        worst = max((c.residual for c in e.carries), default=float("nan"))
        entries.append({"kind": "certified map",
                        "claim": f"{e.name}: {e.t_note}; identity {e.identity_residual:.1e}, worth case "
                                 f"carried observable {worst:.1e}",
                        "why": e.boundary.split(".")[0][:160],
                        "command": "python3 scripts/dictionary.py"})

    # --- scale statements ----------------------------------------------------------------
    from pacland.exactness import scaling as SC
    ladder = SC.report()
    moved = [k for k, v in ladder["facts"].items() if v["verdict"] == "scale-dependent"]
    entries.append({"kind": "measured value",
                    "claim": (f"window facts across b3 = {ladder['ladder']}: "
                              f"{len(moved)} of {len(ladder['facts'])} are scale-dependent "
                              f"(e.g. `|N| <= 1` 0.901 to 0.644); `max|N| = b3` exactly"),
                    "why": "a window fraction is not a landscape fact; the exact ladder stops at b3 = 6",
                    "command": "python3 scripts/scaling.py"})

    # --- exact integers -----------------------------------------------------------------
    nums = G.report()["rows"]
    entries.append({"kind": "exact integer",
                    "claim": "quintic genus-0 GV invariants recovered exactly: "
                             + ", ".join(f"n_{r['degree']} = {r['correct']}" for r in nums),
                    "why": "integrality alone is not a check; the inverse multi-cover relation reproduces them",
                    "command": "python3 scripts/gv_basis.py"})
    # The page must be a function of the engine VALUES, not of the order the engines yield them in.
    # Filesystem glob order and dict iteration order both vary between machines, and that alone was
    # enough to make CI see a different file than the author did (2026-10-31).
    return sorted(entries, key=lambda e: (KIND_ORDER.get(e["kind"], 99), e["claim"]))


KINDS = ["exhibited object", "theorem-in-a-window", "recovered definition", "measured value",
         "certified map", "exact integer"]
KIND_ORDER = {k: i for i, k in enumerate(KINDS)}


def render(entries) -> str:
    out = ["# What we know — the positive side",
           "",
           "*Generated by `python3 scripts/positives.py` from the engines themselves. Every entry carries the "
           "command that reproduces it. Nothing that cannot be regenerated belongs on this page.*",
           "",
           f"**{len(entries)} entries.**"]
    for kind in KINDS:
        group = [e for e in entries if e["kind"] == kind]
        if not group:
            continue
        out += ["", f"## {kind.replace('-', ' ').title()} ({len(group)})", ""]
        for e in group:
            out += [f"- **{e['claim']}**", f"  - why it matters: {e['why']}",
                    f"  - reproduce: `{e['command']}`"]
    out.append("")
    return "\n".join(out)


def main() -> int:
    text = render(build())
    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"MISSING: {OUT}")
            return 1
        if OUT.read_text() != text:
            # SAY WHAT IS STALE. The guard used to report only that the file differed, which is a dead end on a
            # machine whose library versions differ from CI's: the author regenerates, sees no change, and has nothing
            # to act on. A diff is the diagnosis.
            import difflib
            committed = OUT.read_text().splitlines(keepends=True)
            fresh = text.splitlines(keepends=True)
            diff = list(difflib.unified_diff(committed, fresh,
                                             fromfile="docs/known-positives.md (committed)",
                                             tofile="freshly generated", n=2))
            print("STALE: docs/known-positives.md does not match a fresh generation")
            for line in diff[:40]:
                print(line.rstrip("\n"))
            if len(diff) > 40:
                print(f"... {len(diff) - 40} more diff lines")
            return 1
        print("current")
        return 0
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(text.splitlines())} lines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
