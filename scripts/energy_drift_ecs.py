#!/usr/bin/env python3
"""Climate: does conservation drift transfer into ECS, and at what coefficient?

    python3 scripts/energy_drift_ecs.py [--ecs PATH]

Claim (docs/energy-conjectures.md): a model's conservation residual eps in piControl transfers linearly to
its ECS — |dECS|/|eps| ~ 0.76 K per W/m2, the AR6 ratio (3.0 K / 3.93 W/m2) — so a one-line correction to
abrupt-4xCO2 ECS suffices.

**Two different quantities are in play, and this script keeps them apart:**

1. the **ECS-per-forcing coefficient** — dECS/dERF2x across models — computable from the Zelinka table
   (53 models with both ECS and ERF2x, `data/climate/cmip6_ecs_models.json`), computed here;
2. the **drift-to-ECS transfer** — dECS/deps — which needs a per-model abrupt-4xCO2 regression with and
   without the drift correction. That data is not in this repository, so what is reported is a rank
   correlation and it is **not** dressed up as the transfer.

Falsifier (registered): slope > 1.3 or < 0.7, or the ratio outside [0.4, 1.2] K per W/m2.
"""
import argparse
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DRIFT = ROOT / "data" / "climate" / "cmip6_drift.json"
ECS = ROOT / "data" / "climate" / "cmip6_ecs_models.json"
AREA_M2 = 5.1e14
SECONDS_PER_YEAR = 3.15e7
#: The coefficient the claim predicts, K per W/m2 (AR6: 3.0 K assessed / 3.93 W/m2 F2x).
CLAIMED = 0.76


def net_toa_wm2(row: dict) -> float:
    """The model's net top-of-atmosphere imbalance in W/m2 from its J/yr ledger."""
    return row["netTOA_J_per_yr"] / (AREA_M2 * SECONDS_PER_YEAR)


def ols_slope(xs: list, ys: list) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / sxx


def r_squared(xs: list, ys: list, slope: float) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    ss_tot = sum((y - my) ** 2 for y in ys)
    intercept = my - slope * mx
    ss_res = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys))
    return 1 - ss_res / ss_tot if ss_tot else float("nan")


def bootstrap_ci(xs: list, ys: list, draws: int = 2000, seed: int = 20261103):
    rng = random.Random(seed)
    n = len(xs)
    slopes = []
    for _ in range(draws):
        idx = [rng.randrange(n) for _ in range(n)]
        bx = [xs[i] for i in idx]
        by = [ys[i] for i in idx]
        if len(set(bx)) > 1:
            slopes.append(ols_slope(bx, by))
    slopes.sort()
    return slopes[int(0.025 * len(slopes))], slopes[int(0.975 * len(slopes))]


def spearman(xs: list, ys: list) -> float:
    def ranks(values):
        order = sorted(range(len(values)), key=lambda i: values[i])
        out = [0.0] * len(values)
        for rank, i in enumerate(order):
            out[i] = float(rank + 1)
        return out

    rx, ry = ranks(xs), ranks(ys)
    n = len(rx)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Drift -> ECS transfer (partly computable).")
    ap.add_argument("--ecs", default=str(ECS))
    args = ap.parse_args(argv[1:])

    ecs_path = pathlib.Path(args.ecs)
    if not ecs_path.is_file():
        print(f"REFUSED: no ECS table at {ecs_path}")
        return 2
    table = json.loads(ecs_path.read_text())
    models = table.get("models", [])
    if len(models) < 10:
        print(f"REFUSED: {len(models)} models is too few to fit a slope")
        return 2

    xs = [m["erf2x_wm2"] for m in models]
    ys = [m["ecs_K"] for m in models]
    slope = ols_slope(xs, ys)
    lo, hi = bootstrap_ci(xs, ys)
    r2 = r_squared(xs, ys, slope)

    print(f"1) ECS per unit forcing, {len(models)} CMIP6 models (Zelinka et al. 2020)\n")
    print(f"   slope  dECS/dERF2x : {slope:.3f} K per W/m2   95% CI [{lo:.3f}, {hi:.3f}]   R2 {r2:.2f}")
    print(f"   the claim says     : {CLAIMED:.2f} K per W/m2")
    inside = lo <= CLAIMED <= hi
    print("   verdict            : " + ("CONSISTENT — the claimed value is inside the CI"
                                        if inside else "CONTRADICTED — the claimed value is outside the CI"))

    if not DRIFT.is_file():
        print("\n2) drift join: REFUSED — no drift ledger")
        return 0
    drift = json.loads(DRIFT.read_text()).get("models", [])
    by_model = {m["model"]: m["ecs_K"] for m in models}
    joined = [(r["model"], net_toa_wm2(r), by_model[r["model"]]) for r in drift if r["model"] in by_model]
    print(f"\n2) drift join: {len(joined)} of {len(drift)} models have both a drift residual and an ECS\n")
    print(f"   {'model':24} {'netTOA W/m2':>12} {'ECS K':>7}")
    for name, eps, ecs in sorted(joined, key=lambda r: abs(r[1]), reverse=True)[:8]:
        print(f"   {name[:24]:24} {eps:>+12.3f} {ecs:>7.2f}")
    if len(joined) >= 8:
        rho = spearman([r[1] for r in joined], [r[2] for r in joined])
        print(f"\n   rank correlation (eps vs ECS): rho = {rho:+.2f} on {len(joined)} models")
    print()
    print("   NOT claimed: this correlation is not the transfer. dECS/deps needs a per-model")
    print("   abrupt-4xCO2 regression with and without correction; that data is not here, so")
    print("   the drift-to-ECS claim stays registered, not computed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
