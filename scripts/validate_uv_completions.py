"""Validate the UV-completion catalog (Machine 3) against the literature collapse
counts from the falsifier-#2 adversarial pass.

Each completion's collapse count must match the known value, and the verified
deficit must be exactly 2 (gauge-coupling unification).

Sources: Georgi-Glashow PRL 32 (1974) 438; Buras-Ellis-Gaillard-Nanopoulos
Nucl.Phys.B135 (1978) 66; Fritzsch-Minkowski Ann.Phys. 93 (1975) 193; Pati-Salam
PRD 10 (1974) 275; Martin hep-ph/9709356.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.uv_completions import CATALOG, deficit

EXPECTED = {
    "Standard Model": 0,
    "Minimal SU(5)": 5,
    "Minimal SO(10)": 12,
    "Minimal E6": 12,
    "Minimal Pati-Salam": 12,
    "Minimal trinification SU(3)^3": 12,
    "Flipped SU(5)": 2,
    "Realistic multi-Higgs SO(10)/E6/PS": 2,
    "MSSM": 1,
    "SUSY SU(5)": 6,
    "SUSY minimal SO(10)": 13,
    "Warped RS / composite / Froggatt-Nielsen / texture zeros": 0,
}

NUMERICALLY_CORRECT = {
    "Standard Model": 0,
    "Minimal SU(5)": 2,
    "Minimal SO(10)": 2,
    "Minimal E6": 2,
    "Minimal Pati-Salam": 2,
    "Minimal trinification SU(3)^3": 2,
    "Flipped SU(5)": 2,
    "Realistic multi-Higgs SO(10)/E6/PS": 2,
    "MSSM": 0,
    "SUSY SU(5)": 2,
    "SUSY minimal SO(10)": 2,
    "Warped RS / composite / Froggatt-Nielsen / texture zeros": 0,
}


def main() -> int:
    failures = 0
    for c in CATALOG:
        exp = EXPECTED.get(c.name)
        expn = NUMERICALLY_CORRECT.get(c.name)
        if exp is None:
            print(f"[FAIL] unknown completion not in EXPECTED: {c.name}")
            failures += 1
            continue
        got = c.collapse_count()
        gotn = c.numerically_correct()
        status = "PASS" if (got == exp and gotn == expn) else "FAIL"
        if got != exp or gotn != expn:
            failures += 1
        print(f"[{status}] {c.name:52s} collapse={got:2d} (expect {exp:2d})  "
              f"numerically-correct={gotn} (expect {expn})")

    print()
    print(f"deficit: {deficit()}")
    if failures:
        print(f"RESULT: {failures} failure(s)")
        return 1
    print("RESULT: all collapse counts and the numerically-correct filter PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
