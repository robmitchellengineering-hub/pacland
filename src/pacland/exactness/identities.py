"""X5 + X1 — the corpus against the geometry it claims to come from.

The 14 `data/h12_*_stats.json` files hold 5,885 vacua. Nothing in the repository has ever checked that a
recorded row is *internally* consistent with the flux pairing it reports, so this battery does exactly
that, per row, and prints failures rather than a verdict:

| check | why it must hold |
|---|---|
| `flux` is `F ++ H`, each of `b3` integral components | the flux is a pair of integral cohomology vectors |
| `b3 = 2 h21 + 2` and the spectrum has `b3` levels | the moduli count is `2(h21+1)`, and the recorded Hessian lives on that space |
| `N = F^T J H` equals the recorded `Nflux` | the tadpole is the symplectic pairing, not a label |
| `d = gcd(flux)` and `d^2 | N` | over Z the orbits are labelled by `(N, d)` with `d^2 | N` (Completeness) |

The pairing convention was **discovered, not assumed**: on the first row of `h12_2_m1_stats.json`
(`flux = [3,-1,-4,0,-2,11, 0,-2,-1,0,0,0]`, `Nflux = 7`) the naive `sum F_i H_i` gives `-25`, and
`F^T J H` with `J = [[0,I],[-I,0]]` gives `7`. Any other convention fails the same row.

**Deliberately reported as SKIPPED, never as a pass:** the topological charge relation `N <= chi/24`
needs `h11` for each sampled model, and no file on disk carries it — the model IDs are JAXVacua's, and
their topology lives on the node with CYTools. A check that cannot run is unknown, not green.

Run:        python3 scripts/exactness.py
Guarded by: tests/test_exactness_identities.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


#: Rows where the recorded `Nflux` is the **negative** of `F^T J H` for the stored flux ordering.
#: 5 of 5,885. Either those rows store `H ++ F` instead of `F ++ H`, or the tadpole was recorded as a
#: magnitude. Recorded, not corrected: the data files are measurement records, and rewriting them would
#: erase the evidence that the sampler's writer has a per-row convention bug on ~0.1% of rows.
KNOWN_SIGN_FLIPS: dict[str, tuple[int, ...]] = {
    "h12_2_m3_stats.json": (324,),
    "h12_4_m2_stats.json": (1, 42, 84, 119),
}


def b3_from_h21(h21: int) -> int:
    """`b3 = 2 h21 + 2` for a Calabi-Yau threefold."""
    return 2 * int(h21) + 2


def symplectic_form(n: int) -> np.ndarray:
    """`J = [[0, I], [-I, 0]]` on `2n = b3` dimensions — the intersection form in a symplectic basis."""
    j = np.zeros((2 * n, 2 * n), dtype=int)
    j[:n, n:] = np.eye(n, dtype=int)
    j[n:, :n] = -np.eye(n, dtype=int)
    return j


def split_flux(flux) -> tuple[np.ndarray, np.ndarray]:
    """The corpus stores `F ++ H`, each of length `b3`."""
    v = np.asarray(flux, dtype=float)
    if v.size % 2:
        raise ValueError(f"flux has {v.size} components, which is not 2*b3")
    half = v.size // 2
    return v[:half], v[half:]


def tadpole(flux) -> int:
    """`N = F^T J H` — the D3 tadpole, computed from the recorded flux alone."""
    f, h = split_flux(flux)
    n = f.size // 2                      # b3 = 2n
    return int(round(float(f @ symplectic_form(n) @ h)))


def gcd_int(values) -> int:
    g = 0
    for v in values:
        g = math.gcd(g, int(round(float(v))))
    return abs(g)


def audit_row(row: dict, h21: int, index: int) -> list[dict]:
    """Every check for one vacuum row. Returns a list of failures (empty means clean)."""
    failures: list[dict] = []
    b3 = b3_from_h21(h21)
    flux = row.get("flux") or []
    if len(flux) != 2 * b3:
        failures.append({"row": index, "check": "flux length",
                         "detail": f"{len(flux)} components, expected 2*b3 = {2 * b3}"})
        return failures
    v = np.asarray(flux, dtype=float)
    off = float(np.max(np.abs(v - np.round(v))))
    if off > 1e-9:
        failures.append({"row": index, "check": "flux is integral", "detail": f"off-grid by {off:.2e}"})
    n = tadpole(flux)
    recorded = row.get("Nflux")
    if recorded is None:
        failures.append({"row": index, "check": "Nflux recorded", "detail": "missing"})
    elif int(round(float(recorded))) != n:
        failures.append({"row": index, "check": "tadpole = F^T J H",
                         "detail": f"recorded {recorded} vs computed {n}",
                         "recorded": int(round(float(recorded))), "computed": n})
    d = gcd_int(v)
    if d == 0:
        failures.append({"row": index, "check": "gcd(flux) > 0", "detail": "all-zero flux"})
    elif recorded is not None and int(round(float(recorded))) % (d * d) != 0:
        failures.append({"row": index, "check": "d^2 divides N", "detail": f"d={d}, N={recorded}"})
    levels = row.get("eigenvalues") or []
    if len(levels) != b3:
        failures.append({"row": index, "check": "spectrum dimension",
                         "detail": f"{len(levels)} levels, expected b3 = {b3}"})
    return failures


def audit_file(path: str | Path) -> dict:
    """Audit one `h12_*_stats.json`."""
    path = Path(path)
    doc = json.loads(path.read_text())
    h21 = int(doc.get("h21") or doc.get("h12") or 0)
    vacua = doc.get("vacua") or []
    failures: list[dict] = []
    for i, row in enumerate(vacua):
        failures.extend(audit_row(row, h21, i))
    known = set(KNOWN_SIGN_FLIPS.get(path.name, ()))
    for f in failures:
        f["known"] = bool(
            f["check"] == "tadpole = F^T J H"
            and f["row"] in known
            and f.get("computed") == -f.get("recorded", 0)
        )
    return {"file": path.name, "h21": h21, "b3": b3_from_h21(h21), "rows": len(vacua),
            "failures": failures, "n_fail": len(failures),
            "n_known": sum(1 for f in failures if f["known"]),
            "n_unexplained": sum(1 for f in failures if not f["known"])}


def audit_corpus(data_dir: str | Path = "data") -> dict:
    """Audit every sampled-vacua file in the data directory."""
    files = sorted(Path(data_dir).glob("h12_*_stats.json"))
    reports = [audit_file(p) for p in files]
    skipped = [{
        "check": "N <= chi/24 (tadpole cancellation against the geometry)",
        "status": "skipped",
        "reason": "h11 is not recorded for the sampled models; their topology lives with CYTools on "
                  "the node. Unknown, not green.",
    }]
    rows = sum(r["rows"] for r in reports)
    n_fail = sum(r["n_fail"] for r in reports)
    n_known = sum(r["n_known"] for r in reports)
    n_unexplained = sum(r["n_unexplained"] for r in reports)
    return {"files": reports, "n_files": len(reports), "rows": rows, "n_fail": n_fail,
            "n_known": n_known, "n_unexplained": n_unexplained, "skipped": skipped,
            "all_pass": n_unexplained == 0}


__all__ = ["KNOWN_SIGN_FLIPS", "b3_from_h21", "symplectic_form", "split_flux", "tadpole", "gcd_int", "audit_row",
           "audit_file", "audit_corpus"]
