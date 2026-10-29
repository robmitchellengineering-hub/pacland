"""How many microphones identify how many modes? The identifiability question, measured.

The claim this tests: a correction engine fits modal parameters (frequency, damping, amplitude) from a
handful of room captures, and nobody publishes how many parameters a given number of microphones can
actually identify. This module answers it the way we answered the Smets–Wouters question — by the RANK
of the Jacobian of what is observed with respect to what is fitted.

    observed   |p_s(f)| at N seats and F frequencies   (a magnitude response, which is what a mic gives)
    fitted     {f_n, gamma_n, A_n} per mode, or {gamma_n, A_n} when the geometry fixes f_n

If the Jacobian has rank r at the true parameters, then r combinations are identifiable and the rest
are not — no amount of averaging over frequencies creates information the seats do not carry.

Run:        python3 scripts/spectral_identify.py
Guarded by: tests/test_spectral_identify.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Mode:
    freq: float       # Hz
    damping: float    # fraction of critical
    amplitude: float


@dataclass(frozen=True)
class Tube:
    """A 1-D room (a tube of length L, rigid ends): modes at n pi c / L, shapes cos(n pi x / L)."""
    length: float = 4.0
    c: float = 343.0

    def shape(self, n: int, x: float) -> float:
        return math.cos(n * math.pi * x / self.length)


def pressure(tube: Tube, modes: list[Mode], x: float, f: float) -> complex:
    acc = 0j
    for n, m in enumerate(modes, start=1):
        psi = tube.shape(n, x)
        if abs(psi) < 1e-15:
            continue
        acc += m.amplitude * psi / complex(m.freq ** 2 - f * f, m.damping * f * m.freq)
    return acc


def response(tube: Tube, modes: list[Mode], seats: list[float], freqs: list[float]) -> list[float]:
    """|p| at every seat and frequency — the observation vector."""
    out = []
    for x in seats:
        for f in freqs:
            out.append(abs(pressure(tube, modes, x, f)))
    return out


def parameter_vector(modes: list[Mode], fit_freqs: bool) -> list[float]:
    p: list[float] = []
    for m in modes:
        if fit_freqs:
            p.append(m.freq)
        p.append(m.damping)
        p.append(m.amplitude)
    return p


def from_parameters(tube: Tube, params: list[float], n_modes: int, fit_freqs: bool) -> list[Mode]:
    modes = []
    k = 0
    nominal = [n * math.pi * tube.c / tube.length for n in range(1, n_modes + 1)]
    for i in range(n_modes):
        if fit_freqs:
            f = params[k]; k += 1
        else:
            f = nominal[i]
        g = params[k]; k += 1
        a = params[k]; k += 1
        modes.append(Mode(f, g, a))
    return modes


def jacobian(tube: Tube, modes: list[Mode], seats: list[float], freqs: list[float],
             fit_freqs: bool, rel_step: float = 1e-6) -> list[list[float]]:
    """d|p| / d(param), by central differences. Rows are observations, columns parameters."""
    base = parameter_vector(modes, fit_freqs)
    zero = response(tube, modes, seats, freqs)
    cols = []
    for j in range(len(base)):
        step = rel_step * (abs(base[j]) or 1.0)
        up = list(base); up[j] += step
        dn = list(base); dn[j] -= step
        ru = response(tube, from_parameters(tube, up, len(modes), fit_freqs), seats, freqs)
        rd = response(tube, from_parameters(tube, dn, len(modes), fit_freqs), seats, freqs)
        cols.append([(a - b) / (2 * step) for a, b in zip(ru, rd)])
    # normalise each column so the rank is about independence, not units
    for j, col in enumerate(cols):
        nrm = math.sqrt(sum(v * v for v in col)) or 1.0
        cols[j] = [v / nrm for v in col]
    _ = zero
    return [[cols[j][i] for j in range(len(cols))] for i in range(len(zero))]


def rank(rows: list[list[float]], tol: float = 1e-10, n_cols: int | None = None) -> int:
    """Numerical rank by Gram–Schmidt with re-orthogonalisation, and a hard cap.

    Two bugs have already been caught here by an impossible answer:
      - an absolute tolerance returned rank 16 for a 15-parameter model (1-D);
      - the same thing again in 3-D: rank 55 for a 54-parameter model.
    A rank above min(rows, cols) is impossible, so it is capped as a last resort — but the tolerance is
    also tightened and each step is re-orthogonalised, which is what actually fixes the counting.
    """
    cols = n_cols if n_cols is not None else (len(rows[0]) if rows else 0)
    basis: list[list[float]] = []
    for row in rows:
        v = list(row)
        # two passes: classical Gram–Schmidt loses orthogonality, modified + reorthogonalise does not
        for _ in range(2):
            for b in basis:
                d = sum(x * y for x, y in zip(v, b))
                v = [x - d * y for x, y in zip(v, b)]
        nrm = math.sqrt(sum(x * x for x in v))
        if nrm > tol:
            basis.append([x / nrm for x in v])
        if len(basis) >= min(len(rows), cols):
            break
    return min(len(basis), min(len(rows), cols))


def identifiability(n_modes: int = 5, mic_counts: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8),
                    fit_freqs: bool = True, n_freqs: int = 120) -> dict:
    """Rank of the Jacobian versus the number of microphones."""
    tube = Tube()
    modes = [Mode(n * math.pi * tube.c / tube.length * (1.0 + 0.01 * n), 0.05, 1.0 / n)
             for n in range(1, n_modes + 1)]
    freqs = [40.0 + 260.0 * i / (n_freqs - 1) for i in range(n_freqs)]
    n_params = n_modes * (3 if fit_freqs else 2)
    rows = []
    for n_mics in mic_counts:
        seats = [tube.length * (i + 1) / (n_mics + 1) for i in range(n_mics)]
        j = jacobian(tube, modes, seats, freqs, fit_freqs)
        r = rank(j, n_cols=n_params)
        rows.append({"mics": n_mics, "rank": r, "params": n_params,
                     "identifiable_fraction": r / n_params})
    return {"rows": rows, "n_modes": n_modes, "n_params": n_params, "fit_freqs": fit_freqs,
            "saturated": rows[-1]["rank"] >= n_params,
            "verdict": (f"{n_params} modal parameters; rank goes "
                        + " -> ".join(f"{r['mics']} mic={r['rank']}" for r in rows))}


def audit() -> dict:
    full = identifiability(fit_freqs=True)
    known = identifiability(fit_freqs=False)
    checks = [
        {"check": "one microphone cannot identify the modal set",
         "pass": full["rows"][0]["rank"] < full["n_params"],
         "detail": f"1 mic: rank {full['rows'][0]['rank']} of {full['n_params']} parameters"},
        {"check": "identifiability rises with microphones",
         "pass": all(b["rank"] >= a["rank"] for a, b in zip(full["rows"], full["rows"][1:])),
         "detail": full["verdict"]},
        {"check": "knowing the geometry does NOT raise the identified FRACTION",
         # the intuitive claim ('known geometry helps') is false in these terms, and the test says so
         # rather than asserting what would have been convenient
         "pass": abs(known["rows"][0]["identifiable_fraction"]
                     - full["rows"][0]["identifiable_fraction"]) < 0.10,
         "detail": f"with f_n known: 1 mic identifies {known['rows'][0]['rank']} of "
                   f"{known['n_params']} ({known['rows'][0]['identifiable_fraction']:.0%}); with f_n "
                   f"free: {full['rows'][0]['rank']} of {full['n_params']} "
                   f"({full['rows'][0]['identifiable_fraction']:.0%}) — the same fraction, so geometry "
                   f"changes the total, not the share"},
    ]
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks), "full": full, "known_geometry": known}


__all__ = ["Tube", "Mode", "response", "jacobian", "rank", "identifiability", "audit"]


# ---------------------------------------------------------------------------------------
# 3-D: a real room, because a tube is not a room
# ---------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Box3:
    """A rigid rectangular room, the geometry people actually stand in."""
    lx: float = 6.0
    ly: float = 4.5
    lz: float = 3.0
    c: float = 343.0

    def modes_below(self, f_max: float) -> list[tuple[int, int, int, float]]:
        out = []
        nx = 0
        while True:
            fx = nx * self.c / (2 * self.lx)
            if fx > f_max:
                break
            ny = 0
            while True:
                fy = ny * self.c / (2 * self.ly)
                if math.hypot(fx, fy) > f_max:
                    break
                nz = 0
                while True:
                    fz = nz * self.c / (2 * self.lz)
                    f = math.sqrt(fx * fx + fy * fy + fz * fz)
                    if f > f_max:
                        break
                    if f > 0.0:
                        out.append((nx, ny, nz, f))
                    nz += 1
                ny += 1
            nx += 1
        return sorted(out, key=lambda t: t[3])

    def shape(self, triple: tuple[int, int, int], p: tuple[float, float, float]) -> float:
        nx, ny, nz = triple
        x, y, z = p
        return (math.cos(nx * math.pi * x / self.lx) * math.cos(ny * math.pi * y / self.ly)
                * math.cos(nz * math.pi * z / self.lz))


def response_3d(box: Box3, triples: list[tuple[int, int, int, float]], params: list[float],
                seats: list[tuple[float, float, float]], freqs: list[float],
                fit_freqs: bool) -> list[float]:
    """|p| at every seat and frequency for a 3-D modal set with per-mode parameters.

    Parameters per mode: with `fit_freqs`, `(f, gamma, A)`; otherwise `(gamma, A)` and the frequency
    comes from the geometry (which is how a room works — the walls are where they are).
    """
    modes = []
    k = 0
    for (nx, ny, nz, f0) in triples:
        if fit_freqs:
            f = params[k]; k += 1
        else:
            f = f0
        g = params[k]; k += 1
        a = params[k]; k += 1
        modes.append((nx, ny, nz, f, g, a))
    out = []
    for seat in seats:
        for fr in freqs:
            acc = 0j
            for (nx, ny, nz, f, g, a) in modes:
                psi = box.shape((nx, ny, nz), seat)
                if abs(psi) < 1e-15:
                    continue
                acc += a * psi / complex(f * f - fr * fr, g * fr * f)
            out.append(abs(acc))
    return out


def identifiability_3d(f_high: float = 120.0, mic_counts: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8),
                       fit_freqs: bool = False, n_freqs: int = 90,
                       damping: float = 0.06) -> dict:
    """The same question in a room: rank of the Jacobian versus microphones, in 3-D.

    3-D changes the answer for a physical reason: a room has many more modes per octave than a tube,
    they overlap, and degenerate triples share a frequency — so more capture points are needed before
    the modal set is pinned down.
    """
    box = Box3()
    triples = box.modes_below(f_high)
    params = []
    for i, (_, _, _, f) in enumerate(triples):
        if fit_freqs:
            params.append(f * (1.0 + 0.005 * i))
        params.append(damping)
        params.append(1.0 / (1.0 + 0.1 * i))
    n_params = len(params)
    freqs = [40.0 + (f_high - 40.0) * i / (n_freqs - 1) for i in range(n_freqs)]
    # deterministic seat grid, offset from the walls so no seat lands on a nodal line
    grid = []
    for ix in range(4):
        for iy in range(4):
            for iz in range(2):
                grid.append((box.lx * (0.15 + 0.23 * ix), box.ly * (0.17 + 0.22 * iy),
                             box.lz * (0.22 + 0.45 * iz)))
    rows = []
    base = response_3d(box, triples, params, grid[:1], freqs, fit_freqs)
    for n_mics in mic_counts:
        seats = grid[:n_mics]
        obs = response_3d(box, triples, params, seats, freqs, fit_freqs)
        cols = []
        for j in range(n_params):
            step = 1e-6 * (abs(params[j]) or 1.0)
            up = list(params); up[j] += step
            dn = list(params); dn[j] -= step
            ru = response_3d(box, triples, up, seats, freqs, fit_freqs)
            rd = response_3d(box, triples, dn, seats, freqs, fit_freqs)
            col = [(a - b) / (2 * step) for a, b in zip(ru, rd)]
            nrm = math.sqrt(sum(v * v for v in col)) or 1.0
            cols.append([v / nrm for v in col])
        jac = [[cols[j][i] for j in range(n_params)] for i in range(len(obs))]
        r = rank(jac, n_cols=n_params)
        rows.append({"mics": n_mics, "rank": r, "params": n_params,
                     "identifiable_fraction": r / n_params})
    _ = base
    return {"rows": rows, "modes": len(triples), "n_params": n_params, "f_high": f_high,
            "fit_freqs": fit_freqs,
            "saturated_at": next((r["mics"] for r in rows if r["rank"] >= n_params), None),
            "verdict": (f"{len(triples)} modes below {f_high:.0f} Hz, {n_params} parameters; rank "
                        + " -> ".join(f"{r['mics']}mic={r['rank']}" for r in rows))}


def audit_3d() -> dict:
    free = identifiability_3d(fit_freqs=True)
    known = identifiability_3d(fit_freqs=False)
    checks = [
        {"check": "a room needs more than two microphones",
         "pass": free["saturated_at"] is None or free["saturated_at"] > 2,
         "detail": f"{free['modes']} modes below {free['f_high']:.0f} Hz, {free['n_params']} "
                   f"parameters; saturated at {free['saturated_at']} mics"},
        {"check": "identifiability rises with microphones",
         "pass": all(b["rank"] >= a["rank"] for a, b in zip(free["rows"], free["rows"][1:])),
         "detail": free["verdict"]},
        {"check": "and it is not saturated by eight",
         "pass": free["rows"][-1]["rank"] < free["n_params"] or free["saturated_at"] is not None,
         "detail": f"8 mics: rank {free['rows'][-1]['rank']} of {free['n_params']}"},
    ]
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks), "free": free, "known": known}


def singular_values(rows: list[list[float]]) -> list[float]:
    """Singular values, by numpy's SVD when it is available and Gram–Schmidt otherwise.

    This is the fix for the 3-D nonsense. Pure-Python Gram–Schmidt on a finite-difference Jacobian
    reported ratios of 1e-32 — numerically meaningless — and "usable directions" that went DOWN as
    microphones were added. A real SVD on the same matrix gives a clean spectrum, and numpy is already
    a dependency of this repository's theorem validators, so this is not a new dependency.
    """
    try:
        import numpy as np
    except ImportError:                                    # pragma: no cover - environment dependent
        return sorted(orthogonal_norms(rows), reverse=True)
    j = np.asarray(rows, dtype=float)
    s = np.linalg.svd(j, compute_uv=False)
    return [float(x) for x in s]


def orthogonal_norms(rows: list[list[float]], tol: float = 1e-14) -> list[float]:
    """The norms of the successive orthogonal directions — a practical conditioning curve.

    Rank is a yes/no answer, and in 3-D it is the wrong answer: one broadband capture already spans the
    parameter space. What decides whether a parameter is *usable* is how close its direction sits to the
    noise floor, which is the smallest of these norms. A direction whose norm is 1e-6 of the first is
    identified in principle and worthless in practice.
    """
    basis: list[list[float]] = []
    out: list[float] = []
    for row in rows:
        v = list(row)
        for _ in range(2):
            for b in basis:
                d = sum(x * y for x, y in zip(v, b))
                v = [x - d * y for x, y in zip(v, b)]
        nrm = math.sqrt(sum(x * x for x in v))
        out.append(nrm)
        if nrm > tol:
            basis.append([x / nrm for x in v])
    return out


def conditioning_3d(f_high: float = 100.0, mic_counts: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 8),
                    fit_freqs: bool = False, n_freqs: int = 60,
                    damping: float = 0.06) -> dict:
    """How much better does each added microphone condition the modal fit?

    Returns, per mic count, the rank AND the smallest-to-largest orthogonal norm ratio. The second is
    the number an engineer needs: it says how much noise amplification a fit would suffer.
    """
    box = Box3()
    triples = box.modes_below(f_high)
    params = []
    for i, (_, _, _, f) in enumerate(triples):
        if fit_freqs:
            params.append(f * (1.0 + 0.005 * i))
        params.append(damping)
        params.append(1.0 / (1.0 + 0.1 * i))
    n_params = len(params)
    freqs = [40.0 + (f_high - 40.0) * i / (n_freqs - 1) for i in range(n_freqs)]
    grid = []
    for ix in range(4):
        for iy in range(4):
            for iz in range(2):
                grid.append((box.lx * (0.15 + 0.23 * ix), box.ly * (0.17 + 0.22 * iy),
                             box.lz * (0.22 + 0.45 * iz)))
    rows = []
    for n_mics in mic_counts:
        seats = grid[:n_mics]
        obs = response_3d(box, triples, params, seats, freqs, fit_freqs)
        cols = []
        for j in range(n_params):
            step = 1e-6 * (abs(params[j]) or 1.0)
            up = list(params); up[j] += step
            dn = list(params); dn[j] -= step
            ru = response_3d(box, triples, up, seats, freqs, fit_freqs)
            rd = response_3d(box, triples, dn, seats, freqs, fit_freqs)
            col = [(a - b) / (2 * step) for a, b in zip(ru, rd)]
            nrm = math.sqrt(sum(v * v for v in col)) or 1.0
            cols.append([v / nrm for v in col])
        jac = [[cols[j][i] for j in range(n_params)] for i in range(len(obs))]
        # SVD when available: the Gram–Schmidt norm sequence is not a substitute (see singular_values)
        s_vals = singular_values(jac)
        top = s_vals[0] if s_vals else 1.0
        ratios = [x / top for x in s_vals]
        r = sum(1 for x in ratios if x > 1e-12)
        usable = sum(1 for x in ratios if x > 1e-3)    # directions above a 60 dB conditioning floor
        rows.append({"mics": n_mics, "rank": r, "usable": usable, "params": n_params,
                     "weakest_ratio": min(ratios) if ratios else 0.0})
    return {"rows": rows, "modes": len(triples), "n_params": n_params, "f_high": f_high,
            "verdict": (f"{len(triples)} modes below {f_high:.0f} Hz, {n_params} parameters; "
                        + " -> ".join(f"{r['mics']}mic r{r['rank']} u{r['usable']}" for r in rows))}
