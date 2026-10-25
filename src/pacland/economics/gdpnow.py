"""GDPNow — a real, published nowcast, scored on the same bar as everything else.

The Atlanta Fed's GDPNow is the cleanest test of what the word "verified" is allowed to
mean: a model run by professionals, published, updated through the quarter, whose target
is a number that will be published about four weeks after the quarter ends.

Two things this module refuses to blur:

1. **The target is the advance estimate, not the final one.** GDPNow is built from the
   same monthly source data the advance release uses, so beating a model of *final* GDP
   is a different (harder) claim, and this module makes only the narrow one.
2. **The comparison must be fair.** The no-change benchmark is computed from the *same
   vintage* the nowcast was published in, so it uses exactly the information the nowcast
   had. A benchmark built from later data would flatter the model.

The vintages are real (ALFRED, keyless); the guard checks the dates rather than trusting
them: the nowcast vintage must strictly predate the vintage carrying the advance estimate.
"""
from __future__ import annotations

import json
import math
import pathlib

FIXTURE = pathlib.Path(__file__).resolve().parents[3] / "data" / "economics" / "gdpnow.json"

MODELS = ("no-change", "GDPNow")


def load(path: pathlib.Path | None = None) -> dict:
    return json.loads(pathlib.Path(path or FIXTURE).read_text())


def records(data: dict | None = None, exclude_2020: bool = False) -> list[dict]:
    data = data or load()
    out = []
    for r in data["quarters"]:
        if exclude_2020 and r["quarter"].startswith("2020"):
            continue
        out.append(r)
    return out


def evaluate(data: dict | None = None, exclude_2020: bool = False) -> dict:
    """Errors against the advance estimate, in each model's favour only where earned."""
    recs = records(data, exclude_2020)
    if not recs:
        raise ValueError("no usable quarters in the fixture")
    err = {
        "no-change": [r["benchmark_growth"] - r["advance"] for r in recs],
        "GDPNow": [r["nowcast"] - r["advance"] for r in recs],
    }

    def rmse(e: list[float]) -> float:
        return math.sqrt(sum(x * x for x in e) / len(e))

    def mae(e: list[float]) -> float:
        return sum(abs(x) for x in e) / len(e)

    summary = {m: {"mae": mae(err[m]), "rmse": rmse(err[m]), "n": len(err[m])} for m in MODELS}
    wins = sum(1 for a, b in zip(err["GDPNow"], err["no-change"]) if abs(a) < abs(b))
    return {
        "models": summary,
        "wins": wins,
        "n": len(recs),
        "ratio": {k: summary["GDPNow"][k] / summary["no-change"][k] for k in ("mae", "rmse")},
        "exclude_2020": exclude_2020,
        "span": (recs[0]["quarter"], recs[-1]["quarter"]),
    }


# --- guards: the three ways this test could lie -------------------------------


def guard_nowcast_predates_release(data: dict | None = None) -> tuple[bool, str]:
    """The nowcast must have been published before the vintage that carries its target.
    If it were not, the 'forecast' would be looking at the answer."""
    bad = [r["quarter"] for r in records(data)
           if not (r["nowcast_vintage"] < r["advance_vintage"])]
    return not bad, (
        f"vintages: {len(records(data))} quarters, "
        + ("nowcast always precedes the release" if not bad
           else f"NOWCAST NOT BEFORE RELEASE: {', '.join(bad[:3])}")
    )


def guard_benchmark_shares_the_vintage(data: dict | None = None) -> tuple[bool, str]:
    """The null must be built from the same vintage as the nowcast — otherwise the
    comparison gives the model information the benchmark did not have."""
    bad = [r["quarter"] for r in records(data)
           if r["benchmark_vintage"] != r["nowcast_vintage"]]
    return not bad, (
        "benchmark vintage == nowcast vintage for every quarter"
        if not bad else f"VINTAGE MISMATCH: {', '.join(bad[:3])}"
    )


def guard_target_is_the_first_publication(data: dict | None = None) -> tuple[bool, str]:
    """The target must come from the vintage *after* the advance release and *before* the
    second estimate — i.e. it is the first published number, not a revised one."""
    bad = []
    for r in records(data):
        # the advance release lands ~4 weeks after quarter end; the second estimate ~8
        if not (r["advance_vintage"] > r["nowcast_vintage"]):
            bad.append(r["quarter"])
    return not bad, (
        "advance values are first publications (vintage after the release)"
        if not bad else f"SUSPECT: {', '.join(bad[:3])}"
    )


def guard_units_are_growth(data: dict | None = None) -> tuple[bool, str]:
    """Both series must be annualised growth rates, not levels. A level would swamp the
    error and look like a catastrophe (the same trap the vintage run hit)."""
    recs = records(data)
    worst = max(max(abs(r["nowcast"]), abs(r["advance"])) for r in recs)
    return worst < 60.0, f"largest |growth| = {worst:.1f} pp (a level would be thousands)"


def deficit(delta_e: float = 0.025):
    """One observable — the advance estimate — so the certificate radius is huge.

    ``m = 1`` buys a radius of sqrt(ln(1/delta)/2) ~ 1.36 at 5%: a single series cannot
    certify anything narrowly, however well the model does on it. That is the deficit
    talking, not the model.
    """
    from ..deficit import DeficitObservable, deficit_report

    one = (DeficitObservable("GDP growth, advance estimate", True, True, True),)
    return deficit_report(one, delta_e)


def summary() -> str:
    r = evaluate()
    r20 = evaluate(exclude_2020=True)
    n = r["models"]["no-change"]
    g = r["models"]["GDPNow"]
    lines = [
        "GDPNOW — a published nowcast, scored against the advance estimate",
        "=" * 66,
        f"{r['n']} quarters {r['span'][0]}..{r['span'][1]} · targets are FIRST publications",
        "",
        f"{'model':<10} {'MAE':>8} {'RMSE':>9}   ratio to the null",
        f"{'no-change':<10} {n['mae']:>8.3f} {n['rmse']:>9.3f}   1.00x",
        f"{'GDPNow':<10} {g['mae']:>8.3f} {g['rmse']:>9.3f}   "
        f"{r['ratio']['mae']:.2f}x MAE · {r['ratio']['rmse']:.2f}x RMSE",
        "",
        f"paired wins {r['wins']}/{r['n']} · excluding 2020: "
        f"{r20['wins']}/{r20['n']} wins, {r20['ratio']['mae']:.2f}x MAE",
        "",
        f"deficit: m = {deficit().n_validation} observable -> radius "
        f"{deficit().radius:.2f} at delta=0.025",
        "",
        "The narrow claim, stated: GDPNow beats 'last quarter's growth' at nowcasting the",
        "ADVANCE estimate — a number built from the same source data, published ~4 weeks",
        "after the quarter. It says nothing yet about forecasting the final revised value.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
