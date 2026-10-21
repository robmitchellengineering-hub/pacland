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
import os
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


def _load_records(data_path: str):
    """Flatten to per-vacuum dicts (the full record, incl. gauge + tadpole)."""
    with open(data_path) as f:
        data = json.load(f)
    records = []
    for d in data.values():
        if isinstance(d, list):
            records.extend(v for v in d if isinstance(v, dict) and "flux" in v)
    return records


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
    from .constraints import elimination_certificate, joint_elimination

    _, logW, loggs = _load_flat(args.data)
    vacua = [{"log_W0": w, "log_gs": g} for w, g in zip(logW, loggs)]
    named = [
        ("weak coupling (gs < 1)", lambda v: v["log_gs"] < 0.0),
        ("small W0 (|W0| < 1)", lambda v: v["log_W0"] < 0.0),
    ]
    for name, keep in named:
        c = elimination_certificate(vacua, keep)
        print(f"{name:26s} eliminates {c['eliminated'] * 100:5.1f}%")

    j = joint_elimination(vacua, named)
    print()
    print(f"{'INTERSECTION (both constraints)':26s} eliminates {j['joint'] * 100:5.1f}%")
    print(f"{'  independent-product benchmark':26s} {j['independent'] * 100:5.1f}%")
    print(f"{'  interaction (joint - indep)':26s} {j['interaction'] * 100:+.1f}%")
    print(
        f"{'  independence test':26s} z = {j['interaction_z']:+.2f} -> "
        f"{j['interaction_verdict']}  ({j['n_survive_all']} vacua survive both)"
    )
    c = j["certificate"]
    print(
        f"{'  certified interval':26s} [{c['lower'] * 100:.1f}%, {c['upper'] * 100:.1f}%]"
        f"  (delta={c['delta']})"
    )

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


def _cmd_deficit(args) -> None:
    """Compute the Mitchell Verification Deficit: m = validated oracle outputs."""
    from .deficit import DeficitObservable, deficit_report
    from .observables import STANDARD_OBSERVABLES, TOPOLOGY_OBSERVABLES, FLUX_OBSERVABLES, SM_OBSERVABLES

    obs = list(STANDARD_OBSERVABLES)
    if args.observables:
        with open(args.observables) as f:
            obs = [DeficitObservable(**o) for o in json.load(f)]

    r = deficit_report(obs, delta_e=args.delta)
    print("Mitchell Verification Deficit — SM physics sector")
    print(f"  observables: {r.n_observables}")
    print(f"  measured:    {r.n_measured}   (target c* known)")
    print(f"  computable:  {r.n_computable}   (oracle can evaluate)")
    print(f"  VALIDATED:   {r.n_validation}   (calibrated error model)  <- m")
    print(f"  prediction zone (computable, not measured): {r.n_prediction_zone}")
    print(f"  unverifiable (measured, not computable):   {r.n_unverifiable}")
    radius = "INFINITE (vacuous)" if r.vacuous else f"{r.radius:.4f}"
    print(f"  certificate radius sqrt(ln(1/delta_e)/2m): {radius}")
    print(f"  verdict: {'deficit TOTAL — no error-bounded certificate exists' if r.vacuous else 'bounded'}")

    # The validated oracle (CYTools topology) — the deficit-closing mechanism.
    t = deficit_report(list(TOPOLOGY_OBSERVABLES), delta_e=args.delta)
    print("\nMitchell Verification Deficit — topology sector (CYTools, quintic)")
    print(f"  observables: {t.n_observables}  measured: {t.n_measured}  "
          f"computable: {t.n_computable}  VALIDATED: {t.n_validation}  <- m")
    print(f"  certificate radius: {t.radius:.4f}  verdict: {'bounded' if not t.vacuous else 'vacuous'}")

    # The flux-vacua oracle (JAXVacua) — first validated rung: the tadpole.
    f = deficit_report(list(FLUX_OBSERVABLES), delta_e=args.delta)
    print("\nMitchell Verification Deficit — flux sector (JAXVacua)")
    print(f"  observables: {f.n_observables}  measured: {f.n_measured}  "
          f"computable: {f.n_computable}  VALIDATED: {f.n_validation}  <- m")
    print(f"  certificate radius: {f.radius:.4f}  verdict: {'bounded' if not f.vacuous else 'vacuous'}")

    # The Standard-Model sector (sympy, exact) — the m=0 frontier, now climbed.
    s = deficit_report(list(SM_OBSERVABLES), delta_e=args.delta)
    print("\nMitchell Verification Deficit — Standard-Model sector (sympy, exact)")
    print(f"  observables: {s.n_observables}  measured: {s.n_measured}  "
          f"computable: {s.n_computable}  VALIDATED: {s.n_validation}  <- m")
    print(f"  certificate radius: {s.radius:.4f}  verdict: {'bounded' if not s.vacuous else 'vacuous'}")

    total = t.n_validation + f.n_validation + s.n_validation
    print(f"\n  -> total validated oracle outputs m = {total} "
          f"(topology {t.n_validation} + flux {f.n_validation} + SM {s.n_validation}).")
    print("     SM rungs: anomaly cancellation (5/5), hypercharge uniqueness (4/4),")
    print("     N_gen=3 (index |chi|/2), and the 19 = orbit-space dimension — the SM's exact")
    print("     structure (constraints + labels + parameters), all validated against the measured SM.")


def _cmd_viable(args) -> None:
    """The viability polytope: the constraint-first answer, computed."""
    from .viability import elimination_compression, viable_polytope

    _, logW, loggs = _load_flat(args.data)
    xmin, xmax = min(loggs), max(loggs)
    ymin, ymax = min(logW), max(logW)
    # pad the box a touch so the polytope edges don't sit exactly on the sample
    pad = 0.05 * max(xmax - xmin, ymax - ymin, 1e-6)
    box = (xmin - pad, xmax + pad, ymin - pad, ymax + pad)

    half_planes = [
        (1.0, 0.0, 0.0, "weak coupling  gs < 1  (log gs < 0)"),
        (0.0, 1.0, 0.0, "small W0  |W0| < 1  (log W0 < 0)"),
        (1.0, 1.0, math.log(0.1), "combined  gs * |W0| < 0.1  (illustrative)"),
    ]
    v = viable_polytope(half_planes, box)
    print("Viability polytope — the constraint-first answer")
    print(f"  box (sampled range): log gs [{xmin:.2f}, {xmax:.2f}], log W0 [{ymin:.2f}, {ymax:.2f}]")
    print(f"  viable fraction of box: {v['area_fraction'] * 100:.2f}%")
    print(f"  active constraints ({len(v['active_constraints'])}/{v['n_constraints']}):")
    for name in v["active_constraints"]:
        print(f"    - {name}")
    print(f"  vertices ({len(v['vertices'])}):")
    for x, y in v["vertices"]:
        print(f"    ({x:+.3f}, {y:+.3f})")

    c = elimination_compression([1.0 - v["area_fraction"]])
    print()
    print("  The answer is not a point; it is this polygon. Each verified constraint")
    print("  is one half-space; their intersection IS the viable compactification class.")
    print(f"  ({c['n_constraints']} constraints -> survivor fraction "
          f"{c['survivor'] * 100:.2f}%)")


def _cmd_solve(args) -> None:
    """The constraint-first solver: real constraints -> the certified viable class."""
    from .solve import solve

    records = _load_records(args.data)
    r = solve(records)
    print("Constraint-first solve — the certified viable class")
    print(f"  vacua: {r['n']}")
    for p in r["per"]:
        print(f"    {p['name']:32s} eliminates {p['eliminated'] * 100:5.1f}%")
    print(f"  INTERSECTION eliminates {r['joint'] * 100:.1f}%  "
          f"(interaction {r['interaction'] * 100:+.1f}%, z {r['interaction_z']:+.2f} -> "
          f"{r['interaction_verdict']})")
    c = r["certificate"]
    print(f"  certified interval [{c['lower'] * 100:.1f}%, {c['upper'] * 100:.1f}%] "
          f"(delta={c['delta']})")
    print(f"  -> {r['n_survive']} of {r['n']} vacua survive all constraints")
    print()
    print("  narrowing (survivor-range / full-range; lower = more pinned):")
    for o, f in r["narrowing"].items():
        label = "n/a (<2 survivors)" if f is None else f"{f * 100:5.1f}%"
        print(f"    {o:10s} {label}")
    print()
    print("  The viable class is a REGION, not a point: the sample holds only")
    print("  one survivor, so per-observable narrowing is unmeasurable here. The")
    print("  observables that would pinch the region — the mass spectrum, gauge")
    print("  couplings to threshold — are the SAME ones that are uncomputable")
    print("  (m=0 in the Mitchell Verification Deficit). Closing the deficit IS")
    print("  finishing the solve.")


def _cmd_climb(args) -> None:
    """Run the autonomous deficit climber on the mesh and print the report."""
    from .climb import run_climb

    corpus = args.corpus or "data/cy_corpus.json"
    climber = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "scripts", "climb_deficit.py",
    )
    r = run_climb(climber, corpus)
    if "error" in r:
        print("climb failed:", r.get("error"))
        return
    print("Deficit climb report — CYTools on studio-linux")
    for mf in r.get("manifolds", []):
        mark = "PASS" if mf.get("passed") else "FAIL"
        print(f"  {mf['name']}: {mark}")
        for obs, c in mf.get("checks", {}).items():
            tag = "ok" if c.get("passed") else "MISMATCH"
            print(f"    {obs:6s} got={c['got']} expected={c['expected']} {tag}")
    print(f"  m = {r.get('m')}  (validated: {', '.join(r.get('validated_observables', []))})")
    print(f"  n = {r.get('n_points')} validation points")
    print(f"  certificate radius sqrt(ln(1/delta)/2m) = {r.get('radius'):.4f}")
    print(f"  all passed: {r.get('all_passed')}")


def _cmd_disciplines(_args) -> None:
    """List the discipline sections — each its own thing within PACLAND."""
    from .disciplines import DISCIPLINES

    for d in DISCIPLINES:
        print(f"[{d.slug:10s}] {d.name} — {d.status}")
        print(f"    {d.blurb}")
        print(f"    docs: {d.docs}   code: {d.package or 'not built yet'}")
        print()


def _cmd_climate(args) -> None:
    """Climate discipline: the verification deficit (playbook item #1)."""
    from .climate.deficit import summary

    print(summary(delta_e=args.delta))


def _cmd_drugs(args) -> None:
    """Drug discovery discipline: the verification deficit (playbook item #2)."""
    from .drugs.deficit import summary

    print(summary(delta_e=args.delta))


def _cmd_trust(_args) -> None:
    """The trust board — every discipline, one ranked output."""
    from .trust import board, summary

    s = summary()
    marks = {"broken": "RED", "weak": "AMBER", "clean": "GREEN"}
    print("Trust board — every discipline, one ranked output")
    print(f"  artifacts: {s['n_artifacts']}  broken: {s['n_broken']}  "
          f"weak: {s['n_weak']}  clean: {s['n_clean']}")
    print()
    for e in board():
        print(f"[{marks[e.tier]:5s}] [{e.discipline:9s}] {e.artifact}")
        print(f"         {e.detail}")
        print(f"         src: {e.evidence}")


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

    vb = sub.add_parser("viable", help="compute the viability polytope (the constraint-first answer)")
    vb.add_argument("data", help="JSON file of flux-vacua data")
    vb.set_defaults(func=_cmd_viable)

    s = sub.add_parser("solve", help="apply the real constraint set -> certified viable class")
    s.add_argument("data", help="JSON file of flux-vacua data")
    s.set_defaults(func=_cmd_solve)

    cl = sub.add_parser("climb", help="run the autonomous deficit climber on the mesh")
    cl.add_argument("corpus", nargs="?", help="corpus JSON (default data/cy_corpus.json)")
    cl.set_defaults(func=_cmd_climb)

    v = sub.add_parser("verify", help="run a candidate through guards + falsification")
    v.add_argument("candidate", help="JSON: {flux, predictions, tadpole_bound?, h11?, h21?}")
    v.set_defaults(func=_cmd_verify)

    d = sub.add_parser("deficit", help="compute the Mitchell Verification Deficit")
    d.add_argument("--observables", help="optional JSON: [ {name, measured, computable, validated}, ... ]")
    d.add_argument("--delta", type=float, default=0.025, help="confidence budget delta_e")
    d.set_defaults(func=_cmd_deficit)

    l = sub.add_parser("limits", help="print the boundary map")
    l.set_defaults(func=_cmd_limits)

    cf = sub.add_parser("certify", help="certify a question's boundary")
    cf.add_argument("question", help="a question string")
    cf.set_defaults(func=_cmd_certify)

    di = sub.add_parser("disciplines", help="list the discipline sections")
    di.set_defaults(func=_cmd_disciplines)

    cm = sub.add_parser("climate", help="climate discipline: the verification deficit")
    cm.add_argument("--delta", type=float, default=0.025, help="confidence budget delta_e")
    cm.set_defaults(func=_cmd_climate)

    dm = sub.add_parser("drugs", help="drug discovery discipline: the verification deficit")
    dm.add_argument("--delta", type=float, default=0.025, help="confidence budget delta_e")
    dm.set_defaults(func=_cmd_drugs)

    t = sub.add_parser("trust", help="the trust board — ranked artifacts across disciplines")
    t.set_defaults(func=_cmd_trust)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
