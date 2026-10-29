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


def rank(rows: list[list[float]], tol: float = 1e-6) -> int:
    """Numerical rank by Gram–Schmidt, with a RELATIVE tolerance.

    The absolute tolerance I used first returned rank 16 for a 15-parameter model — the finite-difference
    noise in the normalised columns was being counted as independent directions. A rank that exceeds the
    number of parameters is impossible and is the signature of exactly that bug.
    """
    largest = max((math.sqrt(sum(x * x for x in row)) for row in rows), default=0.0) or 1.0
    cut = tol * largest
    basis: list[list[float]] = []
    for row in rows:
        v = list(row)
        for b in basis:
            d = sum(x * y for x, y in zip(v, b))
            v = [x - d * y for x, y in zip(v, b)]
        nrm = math.sqrt(sum(x * x for x in v))
        if nrm > cut:
            basis.append([x / nrm for x in v])
    return len(basis)


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
        r = rank(j)
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
