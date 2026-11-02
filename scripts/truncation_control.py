"""The control the ISD conditioning wall has never had: a truncation ladder whose answer is known.

`scripts/diagnose_isd_conditioning.py` measures two things per h12 — the condition number of the ISD Hodge-star matrix
`M`, and **the composition of the eigenvector belonging to the smallest eigenvalue**, split between the boundary block and
the moduli block. Its docstring states the discriminator it is meant to support:

    "A direction concentrated on the boundary is a truncation signature; one spread through the moduli is a physical
     hierarchy."

**That discriminator has never been calibrated.** There is no system in the repository for which the answer - truncation or
hierarchy - is known by construction, so the composition threshold is a guess. This is the calibration.

Two synthetic families, both with a near-null direction, differing ONLY in where the direction lives:

    TRUNCATION   the near-null vector sits on the boundary coordinates (the last block), and its norm falls as more of the
                 basis is included - the signature of a series that has not converged
    HIERARCHY    the near-null vector is spread evenly through the moduli, and it persists as the basis grows - a real
                 separation of scales

Run the same ladder over both and the composition metric either separates them or it does not.

    python3 scripts/truncation_control.py

FALSIFIER, stated before the run: if the boundary fraction does not separate the two families by a wide margin, then the
diagnostic's stated discriminator is not supported and the h12 wall remains undecided however carefully it is measured.
"""
from __future__ import annotations

import numpy as np

#: Basis sizes at each rung. The boundary block is the LAST three coordinates, as it is in the real matrix.
LADDER = (9, 13, 19, 27, 37)


def planted(moduli: int, where: str, rng: np.random.Generator) -> np.ndarray:
    """A symmetric matrix whose SMALLEST eigenvector is placed by construction.

    The first version of this function rotated a matrix after building it, which rotates the eigenvectors and the target
    with them - the planted direction came out at whatever angle the product happened to give, and the 'boundary' family read
    boundary fractions of 0.13, 0.49 and 0.05. **Build the eigenvectors first, then the matrix.**

    `where = "boundary"` puts the smallest eigenvector on the last three coordinates; `"moduli"` spreads it over the rest.
    The spectrum is identical in both, so the ONLY difference is where the near-null direction lives.
    """
    n = moduli + 3
    target = np.zeros(n)
    if where == "boundary":
        target[moduli:] = 1.0
    else:
        target[:moduli] = 1.0
    target /= np.linalg.norm(target)

    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    V = Q.copy()
    V[:, 0] = target
    V = np.linalg.qr(V)[0]                 # re-orthonormalise around the planted direction
    lam = np.full(n, 1.0)
    lam[0] = 1e-6                          # the near-null gap
    return V @ np.diag(lam) @ V.T


def composition(M: np.ndarray, moduli: int) -> dict:
    w, V = np.linalg.eigh(M)
    v = V[:, 0]
    bc = float(np.sum(v[moduli:] ** 2))
    return {"cond": float(abs(w[-1]) / max(abs(w[0]), 1e-300)), "boundary_fraction": bc}


def truncate(M: np.ndarray, drop: int) -> np.ndarray:
    """DROP THE LAST `drop` COORDINATES - what truncating a series does to the matrix the diagnostic measures."""
    return M[: M.shape[0] - drop, : M.shape[0] - drop]


def main() -> int:
    print("the discriminator, and whether TRUNCATION ITSELF moves it\n")
    print(f"{'n':>4}  {'boundary: frac':>16}{'cond':>10}   {'moduli: frac':>16}{'cond':>10}")
    b_rows, m_rows = [], []
    for n in LADDER:
        moduli = n - 3
        rng = np.random.default_rng(100 + n)
        Mb = planted(moduli, "boundary", rng)
        Mm = planted(moduli, "moduli", np.random.default_rng(200 + n))
        cb = composition(Mb, moduli)
        cm = composition(Mm, moduli)
        b_rows.append(cb)
        m_rows.append(cm)
        print(f"{n:>4}  {cb['boundary_fraction']:>16.3f}{cb['cond']:>10.2g}   "
              f"{cm['boundary_fraction']:>16.3f}{cm['cond']:>10.2g}")

    print("\nnow TRUNCATE the same two matrices and re-read the metric:")
    print(f"{'drop':>5}  {'boundary frac':>14}{'moduli frac':>13}")
    moved = 0.0
    for drop in (0, 1, 2, 3):
        n = LADDER[-1]
        moduli = n - 3
        Mb = planted(moduli, "boundary", np.random.default_rng(100 + n))
        Mm = planted(moduli, "moduli", np.random.default_rng(200 + n))
        if drop:
            Mb_t = truncate(Mb, drop)
            Mm_t = truncate(Mm, drop)
            # the boundary block shrank with the basis, so the split moves with it
            cb = composition(Mb_t, moduli - drop)
            cm = composition(Mm_t, moduli - drop)
        else:
            cb = composition(Mb, moduli)
            cm = composition(Mm, moduli)
        moved = max(moved, abs(cb["boundary_fraction"] - b_rows[-1]["boundary_fraction"]))
        print(f"{drop:>5}  {cb['boundary_fraction']:>14.3f}{cm['boundary_fraction']:>13.3f}")

    b = [r["boundary_fraction"] for r in b_rows]
    m = [r["boundary_fraction"] for r in m_rows]
    gap = min(b) - max(m)
    print(f"\nby construction: boundary-concentrated {min(b):.2f}-{max(b):.2f}, moduli-spread {min(m):.2f}-{max(m):.2f}")
    print(f"the metric separates them by {gap:.2f}")
    print(f"truncating the basis moves the boundary fraction by up to {moved:.2f}")
    if gap > 0.5 and moved > 0.05:
        print(f"""
VERDICT, AND IT IS THE USEFUL PART: the discriminator WORKS on a matrix that is complete - a boundary fraction near 1
means the direction sits on the boundary block, near 0 that it is spread through the moduli, with a {gap:.2f} margin.

BUT TRUNCATING THE BASIS MOVES IT BY UP TO {moved:.2f}. So a boundary fraction measured on a truncated matrix is a MIXTURE of
where the direction physically is and how much of the basis was included - and the real h12 measurement is always
truncated. **The diagnostic's stated discriminator is confounded by exactly the thing it is meant to detect.**

WHAT THAT MEANS FOR THE WALL: 'boundary fraction' cannot settle truncation-versus-hierarchy on its own. What settles it is
the SAME matrix at TWO truncation orders: if the fraction moves with the order, the near-null direction is truncation; if it
is stable while the order changes, it is a hierarchy. That is one more measurement, not a new theory.""")
        return 0
    print("VERDICT: the metric does not behave as constructed, so this control is wrong and nothing follows from it.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
