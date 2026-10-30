"""The dictionary engine — a map with an inverse, not an invariance check.

`docs/plan-dictionary-engine.md`, under D17. The estate can certify what is *not*; this is the first
instrument that certifies a **positive**: that two descriptions are the same object, by exhibiting the
translation.

An entry is five things, and a missing one makes it a slogan rather than a dictionary:

1. the two frames, named;
2. `T` in closed form;
3. `T⁻¹` in closed form;
4. `T ∘ T⁻¹ = id` **verified** with a stated bound;
5. at least one **named observable carried across and compared** — never assumed invariant;
6. the **failure boundary**: where the map stops closing, and why.

The first entry is **flux scaling**, `(F, H) → d(F, H)`. It is packaging of a lemma that is already
proven (`W → dW`, `DW → d·DW`, `N → d²N`, zero set invariant, 5/5 exact in
`scripts/validate_flux_scaling_lemma.py`), so it is the cheapest possible test of whether this engine is
real: if the packaging cannot be made to fail, the engine is decoration.

Run:        python3 scripts/dictionary.py
Guarded by: tests/test_dictionary.py
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..exactness import identities
from ..oracle import exact_t6 as T


@dataclass
class Carry:
    """One named observable, carried across the map and compared."""
    name: str
    law: str                 # what the map says it becomes, in words
    value_a: float
    value_b: float
    residual: float          # |actual - predicted by the law|, relative
    passes: bool


@dataclass
class Entry:
    """A certified translation between two descriptions."""
    name: str
    frame_a: str
    frame_b: str
    identity_residual: float          # max |T⁻¹(T(x)) − x| / |x|
    carries: list = field(default_factory=list)
    boundary: str = ""
    t_note: str = ""
    tinv_note: str = ""

    @property
    def passes(self) -> bool:
        return self.identity_residual < 1e-12 and all(c.passes for c in self.carries)


def _flux_pair(seed: int = 7) -> tuple[np.ndarray, np.ndarray]:
    """A flux pair on the T^6 lattice — integral, as the theory requires."""
    rng = np.random.default_rng(seed)
    return rng.integers(-3, 4, 8).astype(float), rng.integers(-3, 4, 8).astype(float)


def flux_scaling(d: int = 2, seed: int = 7) -> Entry:
    """`(F, H) → d(F, H)` — the first dictionary entry.

    `T` multiplies the flux pair, `T⁻¹` divides it. The observables that must carry across are the two the
    lemma names: the superpotential (`W → dW`) and the tadpole (`N → d²N`). Both are **computed**, at a
    point in moduli space, not asserted.
    """
    if d < 1:
        raise ValueError("the scaling content must be a positive integer")
    F, H = _flux_pair(seed)
    taus = (1j, 1.3j, 0.9j, 1.7j)

    # identity: T^-1 o T = id on the lattice
    t = lambda f: d * f                                   # noqa: E731
    tinv = lambda f: f / d                                # noqa: E731
    identity_residual = float(max(np.max(np.abs(tinv(t(F)) - F)) if F.any() else 0.0,
                                  np.max(np.abs(tinv(t(H)) - H)) if H.any() else 0.0))

    # observable 1: W -> d W, computed through the period vector at a point
    w = T.superpotential(F, H, *taus)
    wd = T.superpotential(t(F), t(H), *taus)
    w_res = abs(wd - d * w) / max(abs(w), 1e-300)

    # observable 2: N -> d^2 N, computed from the symplectic pairing
    n = identities.tadpole(list(F) + list(H))
    nd = identities.tadpole(list(t(F)) + list(t(H)))
    n_res = abs(nd - d * d * n) / max(abs(n), 1)

    carries = [
        Carry("superpotential W", f"W -> {d}·W", float(abs(w)), float(abs(wd)), float(w_res),
              bool(w_res < 1e-10)),
        Carry("D3 tadpole N = F^T J H", f"N -> {d}²·N", float(n), float(nd), float(n_res),
              bool(n_res < 1e-12)),
    ]
    return Entry(
        name=f"flux scaling, d = {d}",
        frame_a="the flux lattice, content d",
        frame_b="the same vacuum rescaled by d",
        identity_residual=identity_residual,
        carries=carries,
        boundary=("d must be a **positive integer** for the map to be a map of the flux lattice: for real "
                  "d the scaling of W and N still holds, but the image is not on the lattice, and every "
                  "downstream statement about integer fluxes (quantisation, the tadpole bound N <= L) "
                  "stops applying. Exact at a shared critical point; it is NOT a statement that rescaling "
                  "produces a second distinct vacuum — the zero set is invariant, which is the whole point "
                  "of the lemma."),
        t_note=f"T: (F, H) -> {d}(F, H)",
        tinv_note=f"T⁻¹: (F, H) -> (F, H)/{d}",
    )


# ---------------------------------------------------------------------------------------
# entry 2: the mirror map, z-chart <-> conifold chart
# ---------------------------------------------------------------------------------------
def mirror_map(z_sample=(0.55, 0.65, 0.7, 0.75), dps: int = 50) -> Entry:
    """The mirror map between the two charts of the same family: `z` (large complex structure) and
    `u` (conifold).

    `T` is the coordinate change `u = 1 - z/z_c`, `T-inverse` is `z = z_c(1 - u)` — exact, and its
    identity residual is rounding. What makes this an *entry* rather than a coordinate substitution is
    the carried observable: a period whose value in the conifold chart must equal the value obtained by
    translating its representation in the `z` chart. That residual is the connection's own
    (`src/pacland/periods/connection.py`), computed here rather than quoted.

    **Boundary, stated:** only **three of the four** conifold branches have a certified translation. The
    exponent-0 branch needs the double resonance cancelled and has resisted a numeric probe
    (docs/plan-facts.md F2 M2e), so the map is certified on the span of the three and the fourth is
    *open*, not assumed. Both charts are also limited by their radii: the `z` series converges for
    `|z| < z_c`, the `u` series for `|u| < 1`.
    """
    import mpmath as mp

    from . import connection, conifold_recursion, quintic

    mp.mp.dps = dps
    zc = quintic.Z_CONIFOLD

    t = lambda z: 1 - mp.mpf(z) / zc              # noqa: E731  z -> u
    tinv = lambda u: zc * (1 - mp.mpf(u))         # noqa: E731  u -> z
    identity = max(abs(tinv(t(z)) - mp.mpf(z)) / mp.mpf(z) for z in z_sample)

    # the carried observable: the exponent-2 conifold branch, in both charts
    conn = connection.connect(n_max=160, dps=dps)
    carries = []
    for row in conn["rows"]:
        if not row["in_verdict"]:
            continue
        carries.append(Carry(name=f"period (exponent-2 branch) at z = {row['z']} z_c",
                             law="same value in both charts",
                             value_a=float(row["series"]), value_b=float(row["predicted"]),
                             residual=float(row["relative"]),
                             passes=bool(row["relative"] < 1e-10)))
    worst = max((c.residual for c in carries), default=float("inf"))

    return Entry(
        name="the mirror map, z-chart <-> conifold chart",
        frame_a="large complex structure, z = 1/(5 psi)^5",
        frame_b="conifold, u = 1 - z/z_c",
        identity_residual=float(identity),
        carries=carries,
        boundary=("**three of four branches**: the exponent-0 branch has no certified translation (double "
                  "resonance, F2 M2e), so the map is certified on the span of the other three and the "
                  "fourth is open. Radii: the z series converges for |z| < z_c, the u series for |u| < 1; "
                  "nothing is claimed outside them. The carried-observable residual at z = 0.75 z_c is "
                  f"{worst:.1e}, which is the truncation of the conifold series, not of the map."),
        t_note="T: z -> u = 1 - z/z_c",
        tinv_note="T⁻¹: u -> z = z_c(1 - u)",
    )


def report(d: int = 2, seed: int = 7) -> dict:
    e = flux_scaling(d, seed)
    return {"entry": e, "passes": e.passes}


__all__ = ["Carry", "Entry", "flux_scaling", "report"]
