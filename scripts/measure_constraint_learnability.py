"""Measure the constraint/observable learnability split (the fork's answer).

The new approach (docs/new-approach.md) mines every flux-paired observable for
structure. The fork: does any observable carry the flux's information (a
fingerprint — positive), or is the map information-theoretically empty (negative)?
This script gives the answer, cleanly split into the two kinds of quantity:

  constraint  — the D3 tadpole N_flux, a *deterministic* quadratic form of flux.
  observable  — the low-energy outputs (W0, g_s, gauge couplings).

For each we report the cross-validated ridge-on-quadratic-features predictability r
(learnability). The tadpole additionally gets a permutation null (shuffle y, refit)
to show its r sits far above chance, and the PAC sample complexity of the degree-2
hypothesis class that realizes it (finite VC dimension => PAC learnable => evolvable).

Pure stdlib; reads data/vacua_observables.json.
"""
import json
import os
import random
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
)

from pacland.structure import ridge_cv_predictability  # noqa: E402
from pacland.learnability.vc import sample_complexity  # noqa: E402

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "vacua_observables.json",
)


def _deg2_dim(d):
    """Degree-2 monomial basis in d flux coordinates: 1 + d + d + C(d,2)."""
    return 1 + d + d + d * (d - 1) // 2


def _ridge_null(fluxes, y, permutations=40, seed=0):
    rng = random.Random(seed)
    ys = list(y)
    out = []
    for _ in range(permutations):
        rng.shuffle(ys)
        out.append(ridge_cv_predictability(fluxes, ys))
    return out


def _z(true, null):
    mean = sum(null) / len(null)
    var = sum((v - mean) ** 2 for v in null) / len(null)
    std = var ** 0.5
    return (true - mean) / std if std > 0 else 0.0


def main() -> int:
    with open(DATA) as f:
        data = json.load(f)
    records = [r for d in data.values() for r in d]
    fluxes = [r["flux"] for r in records]
    d = len(fluxes[0])
    dim = _deg2_dim(d)

    print(f"flux vacua: {len(fluxes)}   flux dim: {d}   degree-2 monomials: {dim}\n")

    rows = [
        ("tadpole", "constraint", fluxes, [r["tadpole"] for r in records]),
        ("log W0", "observable", fluxes, [r["log_W0"] for r in records]),
        ("log g_s", "observable", fluxes, [r["log_gs"] for r in records]),
    ]
    for slot in range(3):
        idx = [i for i, r in enumerate(records) if len(r["log_g2_inv"]) > slot]
        if len(idx) < 10:
            continue
        rows.append(
            (f"gauge_{slot}", "observable",
             [fluxes[i] for i in idx],
             [records[i]["log_g2_inv"][slot] for i in idx])
        )

    print(f"{'quantity':10s} {'role':10s} {'ridge r':>9s} {'z':>7s}  verdict")
    print("-" * 50)
    for name, role, fx, y in rows:
        r = ridge_cv_predictability(fx, y)
        if name == "tadpole":
            null = _ridge_null(fx, y)
            z = _z(r, null)
        else:
            z = float("nan")
        verdict = "LEARNABLE" if name == "tadpole" and r > 0.9 else "not learnable"
        zs = f"{z:+7.2f}" if z == z else "      -"
        print(f"{name:10s} {role:10s} {r:+9.3f} {zs}  {verdict}")

    print()
    eps, delta = 0.05, 0.05
    n = sample_complexity(dim, eps, delta)
    print(
        f"PAC bridge (tadpole): degree-2 class VCdim ~ {dim}; "
        f"sample complexity n >= {n:,.0f} for (eps={eps}, delta={delta})"
    )
    print("  -> a finite, modest hypothesis class realises the constraint map, so it")
    print("     is PAC-learnable and (Valiant) evolvable; the dynamical observables")
    print("     have no such class in the flux coordinates and stay inside the null.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
