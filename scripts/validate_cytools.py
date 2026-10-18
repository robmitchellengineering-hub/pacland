"""Run CYTools on a Linux node and check the quintic through the Hodge guard.

Self-contained and self-asserting (mesh discipline: a job asserts its own
result). Run with the cytools venv python on studio-linux:

    /home/rob/cytools-venv/bin/python scripts/validate_cytools.py

Exits 0 iff the quintic threefold returns h11=1, h21=101 — the known-answer
guard ``pacland.guards.guard_hodge_numbers``. Prints one JSON line for the record.
"""
import json
import sys


def main() -> int:
    try:
        from cytools import Polytope
    except ImportError as exc:
        print(json.dumps({"guard": "hodge_numbers", "passed": False, "error": str(exc)}))
        return 1

    # quintic threefold: the standard reflexive polytope, h11=1, h21=101
    p = Polytope([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [-1, -1, -1, -1]])
    cy = p.triangulate().get_cy()
    h11, h21 = cy.h11(), cy.h21()
    passed = (h11, h21) == (1, 101)
    result = {
        "guard": "hodge_numbers",
        "h11": h11,
        "h21": h21,
        "expected": [1, 101],
        "passed": passed,
    }
    print(json.dumps(result))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
