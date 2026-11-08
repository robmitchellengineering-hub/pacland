#!/usr/bin/env python3
"""SEXTANT guard — the theorem registry is well-formed and the CHSH control is exact.

A guard that cannot fail is not a guard: this one runs on the catalog and fails if any claim
is missing a field, has a bad verdict, or if the CHSH control drifts off 2√2."""
import sys, math
sys.path.insert(0, "src")
from pacland import sextant

required = {"claim", "theorem", "falsifier", "oracle", "verdict", "why"}
problems = []
for name, e in sextant.CATALOG.items():
    missing = required - set(e)
    if missing:
        problems.append(f"{name}: missing {sorted(missing)}")
    if e["verdict"] not in {"FORCED", "FREE", "IMPOSSIBLE"}:
        problems.append(f"{name}: bad verdict {e['verdict']!r}")

# known-truth control: the Phantom-computed CHSH value must be exactly 2√2
from pacland import phantom
expected = 2 * math.sqrt(2)
got = phantom.chsh_value()
if abs(got - expected) > 1e-6:
    problems.append(f"chsh: Phantom computed {got}, drifted from 2√2 ({expected})")

# known-truth control: the classical CHSH wall must be exactly 2
if abs(phantom.bell_classical() - 2.0) > 1e-9:
    problems.append(f"bell-classical: Phantom computed {phantom.bell_classical()}, drifted from 2")

# every live oracle must run without error (a live oracle that throws is a silent break)
for name, e in sextant.CATALOG.items():
    if "simulate" in e:
        try:
            e["simulate"]()
        except Exception as exc:
            problems.append(f"{name}: simulate raised {type(exc).__name__}: {exc}")

# every falsifier must run, and every claim must SURVIVE it (a fired falsifier refutes the claim)
for name in sextant.CATALOG:
    if name in phantom.FALSIFIERS:
        try:
            ok, _ = phantom.FALSIFIERS[name]()
            if not ok:
                problems.append(f"{name}: falsifier FIRED — claim refuted")
        except Exception as exc:
            problems.append(f"{name}: falsifier raised {type(exc).__name__}: {exc}")

# the hardware referee must be able to refuse, certify and stay silent — its falsifiers
from pacland import sextant_referee
_expected_referee = {
    "cheating": sextant_referee.REFUSED,
    "quantum": sextant_referee.CERTIFIED,
    "classical": sextant_referee.UNKNOWN,
    "empty": sextant_referee.UNKNOWN,
}
for _name, _expected in _expected_referee.items():
    _got = sextant_referee.referee(sextant_referee.probe_devices()[_name])["verdict"]
    if _got != _expected:
        problems.append(f"referee/{_name}: expected {_expected}, got {_got}")

# Phantom self-test: the referee certifies the simulator's own optimal-strategy device
if sextant_referee.referee({"circuits": {"chsh": {
        "expectations": phantom.chsh_expectations(), "shots": 10**6}}})["verdict"] != sextant_referee.CERTIFIED:
    problems.append("referee/phantom: the referee did not certify Phantom's own quantum device")

if problems:
    print("\n".join(problems))
    sys.exit(1)
print(f"sextant catalog OK: {len(sextant.CATALOG)} claims, CHSH control exact (2√2), classical wall exact (2), all live oracles run, referee falsifiers hold")
