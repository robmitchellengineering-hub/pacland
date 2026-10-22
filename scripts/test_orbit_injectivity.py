"""Test 2 of the unification claim (C3, injectivity) — do distinct orbits share physics?

**The claim under test.** C3 says the low-energy data of a vacuum *are coordinates on the
orbit space*, which requires the map to be **locally injective**: two duality-inequivalent
vacua must not carry identical low-energy data. C1–C2 already say what the orbits are (fixed
by `(N, d)` over ℤ), so "inequivalent" here means *different flux vector*, and "identical
physics" means the same VEVs and the same physical observables.

**The measurement.** Group the committed corpus by moduli (the VEVs — the low-energy fields
themselves) within a stated tolerance, at fixed model. Where more than one **different flux**
sits at the same moduli, ask whether their observables (`g_s`, `V`, the Hessian spectrum,
`|DW|`) also coincide.

- Observables **differ** ⇒ the data distinguish the vacua ⇒ injectivity survives this test.
- Observables **coincide** ⇒ two inequivalent vacua are physically indistinguishable ⇒ C3's
  injectivity half is **false at degree 0**, and no dictionary can be written from these
  observables — only a many-to-one map.

**What this cannot see, stated up front.** The corpus stores no `W₀`, and `W₀` is the
observable that would most sharply separate two vacua at the same moduli. So a "coincide"
verdict here is a *strong* result (all available observables agree) while a "differ" verdict is
*weaker* than the full test: it shows these observables separate them, not that all do. That
asymmetry is reported, not hidden.

**Tolerance honesty.** "Same moduli" is only ever approximate. The tolerance is a parameter,
the number of groups it produces is printed, and the test is run at two tolerances so the
verdict is not an artefact of one arbitrary cut.

Run on any node (no jaxvacua needed):
    python3 scripts/test_orbit_injectivity.py
"""
import glob
import json
import statistics as st


def load():
    rows = []
    for fn in sorted(glob.glob("data/h12_*_stats.json")):
        doc = json.load(open(fn))
        for r in doc.get("vacua", []):
            if not r.get("flux") or not r.get("moduli"):
                continue
            r["_model"] = f"{fn.split('/')[-1]}:{doc.get('model_ID')}"
            rows.append(r)
    return rows


def flat_moduli(r):
    return [c for z in r["moduli"] for c in z]


def close(a, b, tol):
    return all(abs(x - y) <= tol * max(1.0, abs(x), abs(y)) for x, y in zip(a, b))


def observables(r):
    """The physical data stored per row, independent of the flux vector itself."""
    gs = 1.0 / abs(r["tau"][1]) if abs(r["tau"][1]) > 0 else float("inf")
    ev = r.get("eigenvalues") or []
    return {
        "g_s": gs,
        "V": r.get("V"),
        "|DW|": r.get("|DW|"),
        "eig0": (ev[0] if ev else None),
        "eig_top": (ev[-1] if ev else None),
    }


def same_observables(o1, o2, rel):
    for k in ("g_s", "V", "|DW|", "eig0", "eig_top"):
        a, b = o1[k], o2[k]
        if a is None or b is None:
            continue
        if a == b:
            continue
        if abs(a - b) > rel * max(abs(a), abs(b), 1e-300):
            return False
    return True


def run(rows, tol, rel):
    groups = []
    used = [False] * len(rows)
    for i, r in enumerate(rows):
        if used[i]:
            continue
        fi = flat_moduli(r)
        g = [i]
        for j in range(i + 1, len(rows)):
            if used[j] or rows[j]["_model"] != r["_model"]:
                continue
            if len(flat_moduli(rows[j])) != len(fi):
                continue
            if close(flat_moduli(rows[j]), fi, tol):
                g.append(j)
        if len(g) > 1:
            used = [u or (k in g) for k, u in enumerate(used)]
            groups.append(g)

    pairs = 0
    degenerate = 0
    examples = []
    for g in groups:
        for a in range(len(g)):
            for b in range(a + 1, len(g)):
                ra, rb = rows[g[a]], rows[g[b]]
                if [round(x) for x in ra["flux"]] == [round(x) for x in rb["flux"]]:
                    continue  # same flux = same vacuum, not a test
                pairs += 1
                oa, ob = observables(ra), observables(rb)
                if same_observables(oa, ob, rel):
                    degenerate += 1
                    if len(examples) < 3:
                        examples.append({
                            "same_moduli_TO": tol,
                            "rows": [ra["_model"], rb["_model"]],
                            "g_s": [oa["g_s"], ob["g_s"]],
                            "V": [oa["V"], ob["V"]],
                        })
    return {"tol": tol, "groups": len(groups), "flux_pairs": pairs,
            "degenerate_pairs": degenerate, "examples": examples}


def main():
    rows = load()
    print("=" * 84)
    print("Test 2 — injectivity: can two different fluxes at the same moduli be distinguished?")
    print("=" * 84)
    print(f"vacua loaded: {len(rows)}")
    if not rows:
        print("CANNOT-CHECK no corpus")
        return 2

    results = [run(rows, 1e-6, 1e-6), run(rows, 1e-3, 1e-3)]
    for res in results:
        print(f"\ntolerance {res['tol']:g}:  moduli-groups with >1 flux = {res['groups']}, "
              f"distinct-flux pairs = {res['flux_pairs']}, "
              f"observably identical = {res['degenerate_pairs']}")
        for ex in res["examples"]:
            print(f"  DEGENERATE {ex}")

    strict = results[0]
    if strict["flux_pairs"] == 0:
        verdict = "NO-TEST"
        print("\nverdict: NO-TEST — no two different fluxes share moduli within tolerance.")
        print("  This is not evidence for injectivity; it means the corpus never produced the")
        print("  situation the test needs. Reported as such, never as a pass.")
    elif strict["degenerate_pairs"] == 0:
        verdict = "INJECTIVE-ON-THESE"
        print(f"\nverdict: injective on these observables — {strict['flux_pairs']} pairs, "
              f"0 indistinguishable.")
        print("  NOTE: W0 is not in the corpus, so this is weaker than the full C3 test.")
    else:
        verdict = "DEGENERATE"
        print(f"\nverdict: DEGENERATE — {strict['degenerate_pairs']}/{strict['flux_pairs']} "
              f"pairs are indistinguishable on every stored observable.")
        print("  C3's injectivity half fails on this sample. A strong result: all available")
        print("  observables agree, not just one.")
    print(f"\n===VERDICT=== {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
