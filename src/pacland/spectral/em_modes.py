"""Electromagnetic cavity modes — the same engine as the room work, with c instead of sound speed.

The claim being tested is a unification, not an analogy: **the mode count, the degeneracy structure, the
level statistics and the identifiability of a confined space are the same calculation for acoustic and
electromagnetic fields.** Only the speed and the boundary physics differ.

If that holds, one engine answers "how much information can this space carry, and where do I put the
antenna" for a metal cabinet, a room, or an implant-sized phantom — before anyone runs a full-wave solver.

Everything here is validated against EXACT enumeration of a rectangular conducting cavity, whose modes are
known in closed form:

    f_mnp = (c/2) * sqrt((m/a)^2 + (n/b)^2 + (p/d)^2),   m,n,p integers, not all zero

with TE modes (p >= 1) and TM modes (m, n >= 1), so both polarisations are counted.
"""
from __future__ import annotations

import math

C_LIGHT = 299_792_458.0  # m/s


def cavity_modes(a: float, b: float, d: float, f_max: float,
                 c: float = C_LIGHT) -> list[tuple[float, str, tuple[int, int, int]]]:
    """Exact modes of a rectangular conducting cavity below `f_max`, with polarisation label."""
    out: list[tuple[float, str, tuple[int, int, int]]] = []
    m_max = int(math.ceil(2 * f_max * a / c)) + 1
    n_max = int(math.ceil(2 * f_max * b / c)) + 1
    p_max = int(math.ceil(2 * f_max * d / c)) + 1
    for m in range(0, m_max + 1):
        for n in range(0, n_max + 1):
            for p in range(0, p_max + 1):
                if m == n == p == 0:
                    continue
                f = (c / 2.0) * math.sqrt((m / a) ** 2 + (n / b) ** 2 + (p / d) ** 2)
                if f > f_max or f <= 0:
                    continue
                # TE: p >= 1 AND at least one transverse index non-zero. (0,0,p) is NOT a mode: with both
                # transverse indices zero every transverse field component vanishes identically. Counting it
                # was a real bug — found by the TE101 test asserting (0,1,1) was lowest and getting (0,0,1).
                if p >= 1 and (m >= 1 or n >= 1):
                    out.append((f, "TE", (m, n, p)))
                # TM: m >= 1 and n >= 1 (p may be zero: TM_mn0 is physical)
                if m >= 1 and n >= 1:
                    out.append((f, "TM", (m, n, p)))
    out.sort()
    return out


def exact_count(a: float, b: float, d: float, f_max: float, c: float = C_LIGHT) -> int:
    return len(cavity_modes(a, b, d, f_max, c))


def weyl_count(f: float, volume: float, surface: float, c: float = C_LIGHT,
               surface_coefficient: float = 2.0) -> float:
    """Weyl's law for the electromagnetic case: volume term plus a surface correction.

    `N(f) = (8 pi V / 3)(f/c)^3 - surface_coefficient * (pi A / 2)(f/c)^2`

    The volume coefficient is theory, not fit: two polarisations of a scalar field give
    `2 * (4 pi V / 3)(f/c)^3 = (8 pi V / 3)(f/c)^3`. The surface coefficient is left as a parameter
    because its value depends on the boundary condition, and this module **measures** it rather than
    asserting it — see `fit_surface_coefficient`.
    """
    k = f / c
    return (8.0 * math.pi * volume / 3.0) * k ** 3 - surface_coefficient * (math.pi * surface / 2.0) * k ** 2


def fit_surface_coefficient(a: float, b: float, d: float, f_max: float,
                            c: float = C_LIGHT) -> dict:
    """Least squares for the surface coefficient against EXACT counts, with the volume term fixed.

    The honest order of operations: the volume term comes from theory, the surface term is fitted to exact
    enumeration, and the residual is then reported as the accuracy of the resulting law.
    """
    volume, surface = a * b * d, 2.0 * (a * b + b * d + a * d)
    ks, ys = [], []
    for frac in (0.25, 0.4, 0.55, 0.7, 0.85, 1.0):
        f = f_max * frac
        n_exact = exact_count(a, b, d, f, c)
        k = f / c
        ys.append(n_exact - (8.0 * math.pi * volume / 3.0) * k ** 3)
        ks.append(-(math.pi * surface / 2.0) * k ** 2)
    denom = sum(x * x for x in ks)
    coef = sum(x * y for x, y in zip(ks, ys)) / denom if denom else 0.0
    return {"surface_coefficient": coef, "volume": volume, "surface": surface}


def degeneracy(a: float, b: float, d: float, f_max: float, c: float = C_LIGHT) -> dict:
    """How many exact modes share a frequency — the degeneracy a naive spacing statistic would double-count."""
    modes = cavity_modes(a, b, d, f_max, c)
    freqs = [round(f, 6) for f, _, _ in modes]
    return {"modes": len(modes), "distinct": len(set(freqs)),
            "degenerate": len(freqs) - len(set(freqs)),
            "fraction": 1 - len(set(freqs)) / max(len(freqs), 1)}


def usable_modes(a: float, b: float, d: float, f_lo: float, f_hi: float, probes: int,
                 noise_db: float, q_factor: float = 50.0, max_modes: int = 40,
                 c: float = C_LIGHT) -> dict:
    """Identifiability of the mode set: how many directions survive at a given noise floor.

    The first version of this returned ZERO usable modes at -60 dB for two and three probes, against 3-7 for
    the acoustic case. That was a bug in the model, not a difference in the physics:

      - it used arbitrary complex phases instead of the cavity's own field, so every probe saw an
        independent random vector and the Jacobian columns were nearly collinear in magnitude;
      - it fixed a 2% damping with no stated Q.

    Now it uses the real rectangular-cavity field, `sin(m pi x/a) sin(n pi y/b) sin(p pi z/d)`, and a stated
    quality factor. The question is unchanged: how many mode amplitudes can `probes` positions resolve at
    `noise_db`?
    """
    import itertools
    import numpy as np

    band = [(f, idx) for f, _, idx in cavity_modes(a, b, d, f_hi, c) if f >= f_lo]
    if not band:
        return {"modes_in_band": 0, "usable_10pct": 0, "usable_25pct": 0}
    # collapse exact degeneracies FIRST: two modes at the same frequency are one measurement direction
    seen, chosen = set(), []
    for f, idx in reversed(band):
        key = round(f, 6)
        if key in seen:
            continue
        seen.add(key)
        chosen.append((f, idx))
    chosen = list(reversed(chosen))[:max_modes]
    freqs = [f for f, _ in chosen]
    idxs = [idx for _, idx in chosen]

    # Probes must be spread in THREE dimensions. The first attempt put every probe on the mid-plane z = d/2,
    # where every even-p mode vanishes identically, so adding probes added no information about half the
    # modes and the usable count stayed flat at 12 for 1, 2, 3, 4 and 6 probes.
    lattice = [(a * (0.2 + 0.2 * i), b * (0.25 + 0.2 * j), d * (0.15 + 0.35 * k))
               for i, j, k in itertools.product(range(3), repeat=3)]
    seats = lattice[:probes]

    def shape(idx, x, y, z):
        m, n, p = idx
        return (math.sin(m * math.pi * x / a) * math.sin(n * math.pi * y / b)
                * math.sin(p * math.pi * z / d))

    noise = 10 ** (noise_db / 20.0)
    obs_freqs = [f for f in freqs]
    rows = []
    for (x, y, z) in seats:
        for f in obs_freqs:
            w, row = 2 * math.pi * f, []
            for f0, idx in chosen:
                w0 = 2 * math.pi * f0
                denom = complex(w0 * w0 - w * w, w0 * w / q_factor)
                row.append(shape(idx, x, y, z) / denom)
            rows.append(row)
    jac = np.asarray(rows, dtype=complex)
    # `noise_db` is defined RELATIVE to the strongest response, not in absolute units: the raw response of a
    # GHz mode is ~1e-18 and an absolute 1e-3 noise floor makes every direction unidentifiable. Scaling the
    # Jacobian so its largest entry is 1 makes the number mean "signal-to-noise of the strongest mode", which
    # is what a measurement actually quotes.
    peak = float(np.max(np.abs(jac))) or 1.0
    jac = jac / peak
    j = np.concatenate([jac.real, jac.imag], axis=0)
    f_mat = (j.T @ j) / (noise ** 2)
    eig = np.linalg.eigvalsh(f_mat)
    dir_sd = 1.0 / np.sqrt(np.maximum(eig, 1e-300))
    return {"modes_in_band": len(band), "distinct_in_band": len(seen), "cap": len(chosen),
            "probes": len(seats), "q_factor": q_factor,
            "median_dir_sd": float(np.median(dir_sd)),
            "usable_10pct": int((dir_sd < 0.10).sum()),
            "usable_25pct": int((dir_sd < 0.25).sum())}


def thermal_capacity(contrast: float, bandwidth: float, temperature: float = 300.0,
                     target_ber: float = 1e-3) -> dict:
    """The thermal-noise link ceiling for this space, from the eta^2 m = 2[Q^-1(eps)]^2 bound."""
    def q_inv(p: float) -> float:
        lo, hi = -10.0, 10.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if 0.5 * math.erfc(mid / math.sqrt(2)) > p:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    m = 2.0 * q_inv(target_ber) ** 2 / (contrast ** 2)
    k_b = 1.380649e-23
    return {"contrast": contrast, "samples_per_bit": m,
            "integration_s": m / bandwidth,
            "energy_per_bit_J": k_b * temperature * m / 1.0}


_BAND_CACHE: dict = {}


def _cached_band(a, b, d, f, max_modes, c):
    """The mode list for a band, computed once. Rebuilding it per placement made the search unusable."""
    key = (round(a, 6), round(b, 6), round(d, 6), round(f, 3), max_modes, c)
    if key in _BAND_CACHE:
        return _BAND_CACHE[key]
    lo, hi = f - 1.0e9, f + 1.0e9
    seen, chosen = set(), []
    for f0, _, idx in cavity_modes(a, b, d, hi, c):
        if f0 < lo:
            continue
        k = round(f0, 3)
        if k in seen:
            continue
        seen.add(k)
        chosen.append((f0, idx))
    chosen = chosen[:max_modes]
    _BAND_CACHE[key] = chosen
    return chosen


def channel_matrix(a: float, b: float, d: float, f: float,
                   tx: list[tuple[float, float, float]], rx: list[tuple[float, float, float]],
                   q_factor: float = 200.0, max_modes: int = 120, c: float = C_LIGHT):
    """The MIMO channel between placed antennas, from the room's own modes.

    This is the piece that makes the engine a planning tool rather than a table: given WHERE the antennas go,
    it returns the matrix whose singular values decide how many independent streams the link can carry.
    """
    import numpy as np

    chosen = _cached_band(a, b, d, f, max_modes, c)

    def shape(idx, x, y, z):
        m, n, p = idx
        return (math.sin(m * math.pi * x / a) * math.sin(n * math.pi * y / b)
                * math.sin(p * math.pi * z / d))

    h = np.zeros((len(rx), len(tx)), dtype=complex)
    for t, (xt, yt, zt) in enumerate(tx):
        for r, (xr, yr, zr) in enumerate(rx):
            acc = 0j
            for f0, idx in chosen:
                w0, w = 2 * math.pi * f0, 2 * math.pi * f
                acc += shape(idx, xt, yt, zt) * shape(idx, xr, yr, zr) / complex(
                    w0 * w0 - w * w, w0 * w / q_factor)
            h[r, t] = acc
    return h


def streams(h, snr_db: float) -> int:
    """How many singular values of the channel clear the noise floor at this SNR."""
    import numpy as np

    sv = np.linalg.svd(h, compute_uv=False)
    if len(sv) == 0 or sv[0] == 0:
        return 0
    snr = 10 ** (snr_db / 10.0)
    return int((((sv / sv[0]) ** 2) * snr > 1.0).sum())


# ---------------------------------------------------------------------------------------
# polarisation: the omitted term that makes a stream count a CEILING
# ---------------------------------------------------------------------------------------
def mode_field(idx: tuple[int, int, int], kind: str, x: float, y: float, z: float,
               a: float, b: float, d: float) -> tuple[float, float, float]:
    """The electric field VECTOR of a rectangular-cavity mode at a point (unnormalised).

    Standard rectangular-cavity fields (Pozar, *Microwave Engineering*, §6.4; Collin, *Field Theory of Guided
    Waves*), with the conducting-wall boundary conditions:

        TE_mnp:  Ex ~ (n/b) cos(m pi x/a) sin(n pi y/b) sin(p pi z/d)
                 Ey ~ -(m/a) sin(m pi x/a) cos(n pi y/b) sin(p pi z/d)
                 Ez = 0
        TM_mnp:  Ex ~ (m/a) cos(m pi x/a) sin(n pi y/b) sin(p pi z/d)
                 Ey ~ (n/b) sin(m pi x/a) cos(n pi y/b) sin(p pi z/d)
                 Ez ~ -( (m/a)^2 + (n/b)^2 ) sin(m pi x/a) sin(n pi y/b) cos(p pi z/d)

    Only the DIRECTION matters for a stream count: the singular-value ratios of the channel matrix are
    scale-invariant, so no normalisation is applied and none is needed.
    """
    import math as _m
    m, n, p = idx
    sx, cx = _m.sin(m * _m.pi * x / a), _m.cos(m * _m.pi * x / a)
    sy, cy = _m.sin(n * _m.pi * y / b), _m.cos(n * _m.pi * y / b)
    sz, cz = _m.sin(p * _m.pi * z / d), _m.cos(p * _m.pi * z / d)
    if kind == "TE":
        kx, ky = n / b, m / a
        return (kx * cx * sy * sz, -ky * sx * cy * sz, 0.0)
    kx, ky = m / a, n / b
    kz = -((m / a) ** 2 + (n / b) ** 2)
    return (kx * cx * sy * sz, ky * sx * cy * sz, kz * sx * sy * cz)


def channel_matrix_polarised(a: float, b: float, d: float, f: float,
                             tx: list[tuple[float, float, float]],
                             rx: list[tuple[float, float, float]],
                             tx_pol: list[tuple[float, float, float]],
                             rx_pol: list[tuple[float, float, float]],
                             q_factor: float = 200.0, max_modes: int = 120, c: float = C_LIGHT,
                             seed: int = 11):
    """The channel matrix with antenna polarisation projected onto the mode fields.

    The unpolarised model (`channel_matrix`) treats every antenna as sampling every mode perfectly. Real
    elements are polarised, so a mode whose electric field is perpendicular to an element contributes nothing
    to it - which removes degrees of freedom and is the leading reason a real 4x4 link carries 2-3 streams
    where the scalar model says 4.
    """
    import numpy as np

    # THE WINDOW WAS WRONG. The first version took the lowest `max_modes` modes between f-1 GHz and f+1 GHz -
    # an arbitrary window dominated by FAR-OFF-RESONANCE modes, whose fields oscillate rapidly and cancel to a
    # rank-deficient sum. That is why vertical polarisation returned zero at every height.
    #
    # Physically only modes within one resonance width contribute: |f0 - f| < f/Q. At 5.18 GHz with Q = 200 that
    # is a 26 MHz window holding ~19,000 modes, so they are SAMPLED (uniformly, with a stated count) rather than
    # enumerated - a stated approximation, not an arbitrary cut.
    import random as _random
    width = f / max(q_factor, 1.0)
    lo, hi = f - width, f + width
    pool = [(f0, kind, idx) for f0, kind, idx in cavity_modes(a, b, d, hi, c) if f0 >= lo]
    if not pool:                                   # tiny cavity: fall back to the nearest modes
        pool = list(cavity_modes(a, b, d, f + width, c))[-max_modes:]
    rng = _random.Random(seed)
    chosen = pool if len(pool) <= max_modes else rng.sample(pool, max_modes)
    chosen.sort()

    def proj(pos, pol, kind, idx):
        e = mode_field(idx, kind, pos[0], pos[1], pos[2], a, b, d)
        return pol[0] * e[0] + pol[1] * e[1] + pol[2] * e[2]

    h = np.zeros((len(rx), len(tx)), dtype=complex)
    for t, (pt, ut) in enumerate(zip(tx, tx_pol)):
        for r, (pr, ur) in enumerate(zip(rx, rx_pol)):
            acc = 0j
            for f0, kind, idx in chosen:
                w0, w = 2 * math.pi * f0, 2 * math.pi * f
                acc += proj(pt, ut, kind, idx) * proj(pr, ur, kind, idx) / complex(
                    w0 * w0 - w * w, w0 * w / q_factor)
            h[r, t] = acc
    return h
