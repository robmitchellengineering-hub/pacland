#!/usr/bin/env python3
"""Run the entire PACLAND theorem tower and report one green/red verdict.

The four theorem proofs (plus the exact T^6 oracle) are the symbolic backbone of the
constraint-first program.  This runs each as a subprocess and asserts every one
exits 0, so the whole tower can be reproduced with a single command.

Tower:
  1. Mitchell's Uniqueness Theorem   (6/6 symbolic)
  2. Constraint-First Theorem        (5/5 degrees, FFT)
  3. Mitchell's Completeness Theorem (6 exact + 2 numeric)
  4. Full-duality completion         (5/5, Sp(b3) x SL(2,Z))
  5. T^6 exact oracle, symbolic      (8/8)
  6. T^6 exact oracle, numerical     (21/21)
"""

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

TOWER = [
    ("Mitchell's Uniqueness Theorem", "validate_mitchell_uniqueness.py", "6/6 symbolic"),
    ("Constraint-First Theorem", "validate_constraint_first.py", "5/5 degrees, FFT"),
    ("Mitchell's Completeness Theorem", "validate_mitchell_completeness.py", "6 exact + 2 numeric"),
    ("Full-duality completion", "validate_full_duality.py", "5/5, Sp x SL(2,Z)"),
    ("T^6 exact oracle (symbolic)", "validate_t6_sympy.py", "8/8"),
    ("T^6 exact oracle (numerical)", "validate_t6.py", "21/21"),
]


def main():
    failures = []
    for name, script, grade in TOWER:
        path = os.path.join(HERE, script)
        r = subprocess.run([sys.executable, path], capture_output=True, text=True)
        status = "PASS" if r.returncode == 0 else "FAIL"
        print(f"[{status}] {name}  ({grade})")
        if r.returncode != 0:
            failures.append(name)
            print("    " + (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "no stderr"))

    print(f"\n{'=' * 68}")
    if failures:
        print(f"{len(failures)}/{len(TOWER)} theorems FAILED: {', '.join(failures)}")
        sys.exit(1)
    print(f"All {len(TOWER)} theorems PASS — the constraint-first tower is green.")
    sys.exit(0)


if __name__ == "__main__":
    main()
