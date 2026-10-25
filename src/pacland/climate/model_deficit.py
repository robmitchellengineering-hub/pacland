"""The per-model verification deficit — how many observables *this* model actually has.

The discipline-level deficit (`climate/deficit.py`) counts four historical observables for
climate as a field. That number hides the thing a reader needs: **which model** is validated
against **how many** real measurements. Here it is computed per model, with the three-way
test the rest of the repo uses — an observable counts only if it is

- **measured**: an independent observational target exists;
- **computable**: this model produces a value for it;
- **validated**: the model's value survives the test it exists for.

For a CMIP6 model the three observables with all three properties available are:

1. **ECS** — the assessed range exists (Zelinka et al. 2020, 2.5–4.0 K); the model's ECS is
   computable; validated if it falls inside.
2. **ERF2x** — assessed 3.3–4.1 W/m²; validated if inside.
3. **Conservation** — drift ledgers measured (Irving et al. 2021, 17 of 53 models);
   computable for those models; validated if **no** ledger leaks.

A model that fails a test does not get a smaller radius for it — it gets **one fewer
observable**, which is the whole point: the deficit is a property of the model's evidence,
not of its enthusiasm.
"""
from __future__ import annotations

from typing import NamedTuple

from ..deficit import DeficitObservable, deficit_report
from .cmip6_drift import verdict_table
from .sensitivity_crosscheck import load


class ModelDeficit(NamedTuple):
    model: str
    ecs_validated: bool
    erf2x_validated: bool
    conservation_validated: bool | None   # None = no drift data for this model
    m: int
    n_observables: int
    radius: float
    report: object


def _assessed() -> dict:
    return load()


def model_deficit(model: str, delta_e: float = 0.025) -> ModelDeficit:
    d = _assessed()
    rows = {r["model"]: r for r in verdict_table()}
    ecs = d["ecs_K"].get(model)
    erf = d["erf2x_Wm2"].get(model)
    lo, hi = d.get("likely_range_K", (2.5, 4.0))[:2]
    f_lo, f_hi = (3.3, 4.1)   # assessed ERF2x range used by the trust board
    ecs_ok = ecs is not None and lo <= ecs <= hi
    erf_ok = erf is not None and f_lo <= erf <= f_hi
    ledgers = rows.get(model, {}).get("n_failed_ledgers")
    cons_ok = None if ledgers is None else (ledgers == 0)

    obs = (
        DeficitObservable("ECS", True, ecs is not None, ecs_ok),
        DeficitObservable("ERF2x", True, erf is not None, erf_ok),
        DeficitObservable("conservation drift", True, ledgers is not None, bool(cons_ok)),
    )
    rep = deficit_report(obs, delta_e)
    return ModelDeficit(model=model, ecs_validated=ecs_ok, erf2x_validated=erf_ok,
                        conservation_validated=cons_ok, m=rep.n_validation,
                        n_observables=len(obs), radius=rep.radius, report=rep)


def board_rows(delta_e: float = 0.025) -> list[ModelDeficit]:
    from .model_roster import CLIMATE_ROSTER

    return [model_deficit(m.name.replace("CMIP6 ", ""), delta_e) for m in CLIMATE_ROSTER]


def summary(delta_e: float = 0.025) -> str:
    rows = board_rows(delta_e)
    lines = [
        "CLIMATE — the per-model verification deficit",
        "=" * 62,
        f"{'model':<18}{'ECS':>5}{'ERF2x':>7}{'drift':>7}   m   radius",
    ]
    for r in rows:
        mark = lambda v: "  —" if v is None else ("  +" if v else "  x")   # noqa: E731
        lines.append(
            f"{r.model:<18}{mark(r.ecs_validated):>5}{mark(r.erf2x_validated):>7}"
            f"{mark(r.conservation_validated):>7}   {r.m}   {r.radius:.2f}"
        )
    lines += [
        "",
        "+  validated   x  failed   —  no data",
        "",
        "A failed test costs an observable, not a fraction: the radius is set by how many",
        "independent measured things a model survives, so a model that leaks a ledger is",
        "verified against one fewer of them.",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
