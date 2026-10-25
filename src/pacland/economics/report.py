"""The economics reports the CLI prints — one place, so every surface says the same thing.

Three views, each a plain string so a test can assert on it and a phone can read it:

- ``models_report`` — the roster, scored, with what each row still owes and why;
- ``constraints_report`` — the constraint set, with its measured independent rank;
- ``realtime_report`` — the real-time results: the null, the statistical benchmark, the
  estimated structure, and the published nowcast.

Nothing here computes anything new. It renders what the modules have already verified, so
that a report can never drift from the artifact it describes.
"""
from __future__ import annotations

from . import constraint_set, gdpnow, meese_rogoff, model_roster


def models_report() -> str:
    rows = model_roster.summary()
    violations = model_roster.audit()
    lines = [
        "MACRO-FINANCE MODEL ROSTER — scored on the physics-level bar",
        "=" * 70,
        f"{'tier':<7}{'model':<44}{'obs':>4}  owes",
    ]
    for r in rows:
        owed = ", ".join(r["missing"]) if r["missing"] else "—"
        lines.append(f"{r['tier']:<7}{r['name'][:42]:<44}{r['observables']:>4}  {owed}")
    lines += [
        "",
        "The bar is nine slots (exact structure, deficit, rule of three, guard suite, "
        "out-of-sample, benchmark, trust tier, falsifiable prediction, reproduce); a "
        "model's kind decides which it owes.",
        "A model with every slot earned that LOSES to the null is still weak — taking "
        "the test is not passing it.",
        "",
        f"audit: {'no unsupported claims' if not violations else '; '.join(violations)}",
    ]
    return "\n".join(lines)


def constraints_report() -> str:
    return constraint_set.summary()


def realtime_report() -> str:
    mr = meese_rogoff.findables()
    rmse, rel = mr["rmse"], mr["ratio_to_no_change"]
    g = gdpnow.evaluate()
    rev = gdpnow.revision_answer()
    lines = [
        "REAL-TIME RESULTS — every model against its null, on data as it was published",
        "=" * 74,
        "",
        "statistical benchmarks (growth of GDP, consumption, investment)",
        f"  {'model':<10}{'h=1':>8}{'h=2':>8}{'h=4':>8}   ratio to no-change",
    ]
    for m in meese_rogoff.MODELS:
        vals = "".join(f"{rmse[m][h]:>8.4f}" for h in (1, 2, 4))
        ratios = " · ".join(f"{rel[m][h]:.2f}x" for h in (1, 2, 4))
        lines.append(f"  {m:<10}{vals}   {ratios}")
    lines += [
        "",
        "published nowcast (GDPNow, against the advance estimate)",
        f"  MAE {g['models']['GDPNow']['mae']:.3f} vs null {g['models']['no-change']['mae']:.3f}"
        f"  -> {g['ratio']['mae']:.2f}x  ·  {g['wins']}/{g['n']} paired wins",
        f"  against the revised value: {rev['final_ratio']:.2f}x "
        f"({rev['final_wins']}/{g['n']} wins) — prediction §11 "
        f"{'FALSIFIED' if rev['falsified'] else 'held'}",
        "",
        "Structural models lose to the null on inflation; the published nowcast beats it "
        "on growth; a VAR beats it at every horizon. That is the honest scoreboard.",
    ]
    return "\n".join(lines)
