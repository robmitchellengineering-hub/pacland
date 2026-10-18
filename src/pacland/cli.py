"""PACLAND command-line interface.

The user-facing surface of the verification discipline. Subcommands:

    pacland limits                 print the boundary map (the cartography)
    pacland certify "<question>"   certify which sense of "uncomputable" applies
    pacland mine <data.json>       mine structure in flux-vacua data
    pacland constrain <data.json>  measure constraint elimination

``mine`` and ``constrain`` accept a JSON file in the repository's data format:
either ``{model: {"flux": [...], "log_W0": [...], "log_gs": [...]}}`` or the richer
per-vacuum list format.
"""
from __future__ import annotations

import argparse
import json
import math
import sys


def _load_flat(data_path: str):
    """Load flux-vacua data and flatten to (fluxes, log_W0, log_gs)."""
    with open(data_path) as f:
        data = json.load(f)
    fluxes, logW, loggs = [], [], []
    for d in data.values():
        if isinstance(d, dict) and "flux" in d:  # {model: {flux, log_W0, log_gs}}
            fluxes.extend(d["flux"])
            logW.extend(d["log_W0"])
            loggs.extend(d["log_gs"])
        elif isinstance(d, list):  # {model: [ {flux, log_W0, log_gs, ...} ]}
            for v in d:
                if "flux" in v:
                    fluxes.append(v["flux"])
                    logW.append(v["log_W0"])
                    loggs.append(v["log_gs"])
    return fluxes, logW, loggs


def _cmd_mine(args) -> None:
    from .structure import classify_observable, cv_predictability, ridge_cv_predictability

    fluxes, logW, loggs = _load_flat(args.data)
    dim = len(fluxes[0])
    flux_cols = [[f[i] for f in fluxes] for i in range(dim)]
    print(f"flux vacua: {len(fluxes)}  flux dim: {dim}")
    for name, y in [("log_W0", logW), ("log_gs", loggs)]:
        r = classify_observable(flux_cols, y)
        knn = cv_predictability(fluxes, y)
        ridge = ridge_cv_predictability(fluxes, y)
        print(
            f"{name:8s} -> {r['verdict']:10s} (MI {r['max_mi']:.3f}, z {r['max_z']:.2f})"
            f"  |  KNN r {knn:+.3f}  |  ridge(quad) r {ridge:+.3f}"
        )


def _cmd_constrain(args) -> None:
    from .constraints import elimination_certificate

    _, logW, loggs = _load_flat(args.data)
    vacua = [{"log_W0": w, "log_gs": g} for w, g in zip(logW, loggs)]
    for name, keep in [
        ("weak coupling (gs < 1)", lambda v: v["log_gs"] < 0.0),
        ("small W0 (|W0| < 1)", lambda v: v["log_W0"] < 0.0),
    ]:
        c = elimination_certificate(vacua, keep)
        print(f"{name:26s} eliminates {c['eliminated'] * 100:5.1f}%")

    # log-uniform check
    from .constraints import elimination_curve, linearity_r2

    w0sq = [math.exp(2 * w) for w in logW]
    lo, hi = min(w0sq), max(w0sq)
    ts = [lo + (hi - lo) * i / 20 for i in range(21)]
    r2 = linearity_r2(ts, elimination_curve(w0sq, ts))
    print(f"{'|W0|^2 uniformity':26s} CDF linearity R^2 = {r2:.3f} (1.0 = uniform)")


def _cmd_limits(_args) -> None:
    from .limits import boundary_map

    for b in boundary_map():
        print(f"[{b.limit.value}] {b.question}")
        print(f"    move: {b.positive}")
        print()


def _cmd_certify(args) -> None:
    from .limits import certify

    b = certify(args.question)
    if b is None:
        print("uncertified — no boundary matches that question.")
        return
    print(f"[{b.limit.value}] {b.question}")
    print(f"    justification: {b.justification}")
    print(f"    positive: {b.positive}")


def _cmd_verify(args) -> None:
    """Run a candidate through the physics guards (Vault) + reality guards."""
    from .guards import guard_hodge_numbers, guard_integer_flux, guard_tadpole
    from .reality_guards import STANDARD_REALITY_GUARDS, falsify_all, ruled_out

    with open(args.candidate) as f:
        cand = json.load(f)

    flux = cand.get("flux", [])
    predictions = cand.get("predictions", {})
    bound = cand.get("tadpole_bound", 100)

    physics = [
        ("integer_flux", guard_integer_flux(flux)),
        ("tadpole", guard_tadpole(flux, bound)),
    ]
    if "h11" in cand and "h21" in cand:
        physics.append(("hodge_numbers", guard_hodge_numbers(cand["h11"], cand["h21"])))

    print("Vault — physics guards:")
    for name, (ok, msg) in physics:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {msg}")
    admitted = all(ok for _, (ok, _) in physics)
    print(f"  -> {'ADMITTED' if admitted else 'REFUSED'} "
          f"({'certificate may be minted' if admitted else 'no certificate'})")

    verdicts = falsify_all(STANDARD_REALITY_GUARDS, predictions)
    ro = ruled_out(verdicts)
    pz = [g.name for g in STANDARD_REALITY_GUARDS if verdicts[g.name].in_prediction_zone]
    print("Reality — falsification vs the Standard Model:")
    print(f"  ruled out by: {ro if ro else 'none'}")
    print(f"  prediction zone (not computable): {pz if pz else 'none'}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(
        prog="pacland",
        description="A verification discipline for the string landscape.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("mine", help="mine structure in flux-vacua data")
    m.add_argument("data", help="JSON file of flux-vacua data")
    m.set_defaults(func=_cmd_mine)

    c = sub.add_parser("constrain", help="measure constraint elimination")
    c.add_argument("data", help="JSON file of flux-vacua data")
    c.set_defaults(func=_cmd_constrain)

    v = sub.add_parser("verify", help="run a candidate through guards + falsification")
    v.add_argument("candidate", help="JSON: {flux, predictions, tadpole_bound?, h11?, h21?}")
    v.set_defaults(func=_cmd_verify)

    l = sub.add_parser("limits", help="print the boundary map")
    l.set_defaults(func=_cmd_limits)

    cf = sub.add_parser("certify", help="certify a question's boundary")
    cf.add_argument("question", help="a question string")
    cf.set_defaults(func=_cmd_certify)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
