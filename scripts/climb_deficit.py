"""The autonomous deficit climber — run the oracle over a corpus and hone m.

Self-contained and self-asserting (mesh discipline: a job asserts its own result).
Run on studio-linux with the CYTools venv:

    /home/rob/cytools-venv/bin/python scripts/climb_deficit.py data/cy_corpus.json

Reads a corpus of Calabi-Yau manifolds with known exact topological invariants,
computes each via CYTools, validates against the known answer, and accumulates the
Mitchell Verification Deficit count ``m`` (the number of *independent* observables
the oracle is validated on) plus ``n`` (total validation points). It prints a JSON
climb report and exits 0 iff every known value matches.

The "honing in" is two-directional: each new *observable* grows m and shrinks the
certificate radius sqrt(ln(1/delta)/2m); each new *manifold* grows n and tightens
the empirical error model of the oracle. Both are reported.
"""
import json
import math
import sys


def hoefding(m, delta):
    """The Mitchell Deficit radius: sqrt(ln(1/delta) / (2m))."""
    if m <= 0:
        return float("inf")
    return math.sqrt(math.log(1.0 / delta) / (2.0 * m))


def compute_quintic(cy):
    """CYTools -> (h11, h21, chi, c2) for a CY object."""
    h11 = int(cy.h11())
    h21 = int(cy.h21())
    chi = int(cy.chi())
    c2 = [int(x) for x in cy.second_chern_class()]
    return h11, h21, chi, c2


def main(argv) -> int:
    path = argv[1] if len(argv) > 1 else "data/cy_corpus.json"
    with open(path) as f:
        corpus = json.load(f)
    delta = corpus.get("delta", 0.025)

    try:
        from cytools import Polytope
    except ImportError as exc:
        print(json.dumps({"error": "cytools not importable: " + str(exc)}))
        return 1

    manifolds = corpus.get("manifolds", [])
    report = {"delta": delta, "manifolds": [], "errors": []}
    distinct = {}   # observable name -> all values matched so far
    n_points = 0

    for m in manifolds:
        name = m["name"]
        polytope = m["polytope"]
        known = m.get("known", {})
        counted = m.get("counted", list(known.keys()))
        cy = Polytope(polytope).triangulate().get_cy()
        got = {
            "h11": int(cy.h11()),
            "h21": int(cy.h21()),
            "chi": int(cy.chi()),
            "c2": [int(x) for x in cy.second_chern_class()],
        }
        checks = {}
        ok = True
        for obs in known:
            if obs not in got:
                continue
            matches = got[obs] == known[obs]
            checks[obs] = {"got": got[obs], "expected": known[obs], "passed": matches}
            if not matches:
                ok = False
                report["errors"].append({"manifold": name, "observable": obs,
                                          "got": got[obs], "expected": known[obs]})
            if obs in counted and matches:
                distinct.setdefault(obs, True)
                n_points += 1
        report["manifolds"].append({"name": name, "checks": checks, "passed": ok})

    report["m"] = len(distinct)
    report["n_points"] = n_points
    report["radius"] = hoefding(report["m"], delta)
    report["validated_observables"] = sorted(distinct.keys())
    report["all_passed"] = not report["errors"]
    print(json.dumps(report, default=str))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
