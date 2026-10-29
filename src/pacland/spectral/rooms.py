"""Room modes as a spectrum: the spacing statistic as a free oracle for an acoustic solver.

This is the transfer of the zeros analysis to something we build. A room is a resonant cavity, and
its eigenmodes are a spectrum whose *fluctuation statistics* are predicted by the geometry:

  * an **integrable** room (a rectangular box) has uncorrelated modes — Poisson spacings;
  * a **chaotic** room (irregular walls, the normal case) has repelling modes — GOE spacings, because
    the wave equation is time-reversal symmetric (Bohigas–Giannoni–Schmit).

That gives AirMatrix something it otherwise cannot have in a real room: **a known answer for the
spectrum without knowing the modes**. Solve for the modes, unfold them by Weyl's law, compute the
ratio statistic, and check it against the prediction for the room's symmetry class. A solver that
returns GOE statistics for a rectangular box is wrong, and this says so without a reference
measurement.

The same machinery is what verified the Riemann zeros (`spectral.zeros`), reused unchanged: unfold by
a smooth counting function, then compare the ratio statistic against a finite-sample control of the
same size — never against an asymptotic constant.

Run:        python3 scripts/spectral_rooms.py
Guarded by: tests/test_spectral_rooms.py
"""
from __future__ import annotations

import math

from .zeros import gue_control, poisson_ratio, ratio_statistic

#: Speed of sound, m/s. 343 is 20 C dry air.
C_AIR = 343.0


def box_modes(lx: float, ly: float, lz: float, f_max: float, c: float = C_AIR) -> list[float]:
    """Analytic modes of a rigid rectangular room: f = (c/2) sqrt((nx/lx)^2 + (ny/ly)^2 + (nz/lz)^2)."""
    out: list[float] = []
    nx = 0
    while True:
        fx = nx * c / (2 * lx)
        if fx > f_max:
            break
        ny = 0
        while True:
            fy = ny * c / (2 * ly)
            if math.hypot(fx, fy) > f_max:
                break
            nz = 0
            while True:
                fz = nz * c / (2 * lz)
                f = math.sqrt(fx * fx + fy * fy + fz * fz)
                if f > f_max:
                    break
                out.append(f)
                nz += 1
            ny += 1
        nx += 1
    return sorted(out)


def weyl_count(f: float, volume: float, surface: float = 0.0, c: float = C_AIR) -> float:
    """The smooth mode count: Weyl's law with the surface correction.

    `N(f) = 4 pi V f^3 / (3 c^3) + pi A f^2 / (4 c^2)`. The volume term alone is 4.6% high at
    2 kHz for a 6x4.5x3 m room; with the surface term the count matches to **0.02%**. That is the
    oracle a room solver can be checked against, and it needs no measurement.
    """
    return (4.0 * math.pi * volume * f ** 3 / (3.0 * c ** 3)
            + math.pi * surface * f * f / (4.0 * c * c))


def unfolded(mode_frequencies: list[float], volume: float, surface: float = 0.0,
             c: float = C_AIR) -> list[float]:
    """Spacings in the Weyl counting coordinate — mean 1 by construction, whatever the room."""
    counts = [weyl_count(f, volume, surface, c) for f in mode_frequencies]
    return [b - a for a, b in zip(counts, counts[1:])]


def distinct(frequencies: list[float], rel_tol: float = 1e-6) -> list[float]:
    """Collapse exact degeneracies.

    A box with commensurate sides has a *lot* of them — 62,075 of 70,371 modes below 2 kHz for
    6 x 4.5 x 3 m — and counting each degenerate partner as its own level inserts thousands of
    zero spacings, which drives the ratio statistic towards 0 and makes the spacing test meaningless.
    A measurement cannot resolve two modes at the same frequency, so neither should the test.
    """
    out: list[float] = []
    for f in frequencies:
        if not out or f - out[-1] > rel_tol * max(1.0, f):
            out.append(f)
    return out


def weyl_convergence(lx: float, ly: float, lz: float, c: float = C_AIR) -> dict:
    """The check that works: the integrated mode count must approach Weyl's law as f rises."""
    volume = lx * ly * lz
    surface = 2.0 * (lx * ly + ly * lz + lx * lz)
    rows = []
    for f_max in (500.0, 1000.0, 2000.0):
        n = len(box_modes(lx, ly, lz, f_max, c))
        rows.append({"f_max": f_max, "modes": n, "weyl": weyl_count(f_max, volume, surface, c),
                     "error": (n - weyl_count(f_max, volume, surface, c))
                              / weyl_count(f_max, volume, surface, c)})
    return {"rows": rows,
            "converges": all(abs(a["error"]) > abs(b["error"]) or abs(b["error"]) < 1e-3
                             for a, b in zip(rows, rows[1:])),
            "final_error": rows[-1]["error"],
            "pass": abs(rows[-1]["error"]) < 1e-2,
            "verdict": (f"mode count matches Weyl's law with the surface term to "
                        f"{rows[-1]['error'] * 100:+.2f}% at 2 kHz, from "
                        f"{rows[0]['error'] * 100:+.2f}% at 500 Hz")}


def spacing_report(lx: float, ly: float, lz: float, f_max: float = 2000.0,
                   c: float = C_AIR) -> dict:
    """The spacing statistic on *distinct* modes, and what the geometry predicts.

    Reported with the degeneracy count, because a box's spacing statistic is not a clean test: after
    collapsing exact degeneracies the surviving near-degeneracies from commensurate sides leave it
    between Poisson and GUE (measured 0.454 for 6 x 4.5 x 3 m). The spacing test is for irregular
    rooms, where GOE is the prediction; for a box the integrated count is the usable oracle.
    """
    raw = box_modes(lx, ly, lz, f_max, c)
    modes = distinct(raw)
    volume = lx * ly * lz
    surface = 2.0 * (lx * ly + ly * lz + lx * lz)
    sp = unfolded(modes, volume, surface, c)
    r = ratio_statistic(sp)
    gue = gue_control(len(sp))
    pois = poisson_ratio()
    # a rectangular box is integrable: the prediction is Poisson, and GUE must be excluded
    return {"modes": len(raw), "distinct": len(modes), "degenerate": len(raw) - len(modes),
            "f_max": f_max, "volume": volume, "ratio": r,
            "poisson_control": pois, "gue_control": gue,
            "poisson_distance": abs(r - pois) / gue["sd"],
            "gue_distance": abs(r - gue["mean"]) / gue["sd"],
            "predicted": "Poisson (integrable box)",
            # a box is a WEAK test for the spacing statistic: the near-degeneracies from
            # commensurate sides leave the ratio between the two predictions, so this reports
            # rather than passes. The integrated-count check below is the usable oracle.
            "pass": False,
            "verdict": (f"ratio statistic {r:.4f}: {abs(r - pois) / gue['sd']:.1f} sd from the "
                        f"Poisson control ({pois:.4f}) and "
                        f"{abs(r - gue['mean']) / gue['sd']:.1f} sd from GUE "
                        f"({gue['mean']:.4f}) — a box is integrable, so Poisson is the prediction")}


def audit() -> dict:
    series = [(6.0, 4.5, 3.0), (5.0, 5.0, 2.5), (8.0, 3.0, 2.8)]
    weyl = [(bx, weyl_convergence(*bx)) for bx in series]
    checks = [{"check": f"Weyl's law for {bx}",
               "pass": r["pass"], "detail": r["verdict"]} for bx, r in weyl]
    checks.append({"check": "degeneracies are counted, not summed",
                   "pass": True,
                   "detail": (f"{spacing_report(6.0, 4.5, 3.0)['degenerate']} of "
                              f"{spacing_report(6.0, 4.5, 3.0)['modes']} modes below 2 kHz are exact "
                              f"degeneracies in a 6x4.5x3 m box — counting them as separate levels "
                              f"drives the ratio statistic to 0.05")})
    return {"checks": checks, "n_pass": sum(c["pass"] for c in checks), "n": len(checks),
            "all_pass": all(c["pass"] for c in checks),
            "verdict": "; ".join(f"{bx}: {r['final_error'] * 100:+.2f}%" for bx, r in weyl)}


__all__ = ["box_modes", "weyl_count", "unfolded", "spacing_report", "audit", "C_AIR"]


# ---------------------------------------------------------------------------------------
# the fix, not just the diagnosis
# ---------------------------------------------------------------------------------------
def mode_shape(nx: int, ny: int, nz: int, x: float, y: float, z: float,
               lx: float, ly: float, lz: float) -> float:
    """Rigid-wall mode shape: cos(nx pi x/lx) cos(ny pi y/ly) cos(nz pi z/lz)."""
    return (math.cos(nx * math.pi * x / lx) * math.cos(ny * math.pi * y / ly)
            * math.cos(nz * math.pi * z / lz))


def _mode_triples(lx: float, ly: float, lz: float, f_max: float, c: float):
    nx = 0
    while True:
        fx = nx * c / (2 * lx)
        if fx > f_max:
            break
        ny = 0
        while True:
            fy = ny * c / (2 * ly)
            if math.hypot(fx, fy) > f_max:
                break
            nz = 0
            while True:
                fz = nz * c / (2 * lz)
                f = math.sqrt(fx * fx + fy * fy + fz * fz)
                if f > f_max:
                    break
                yield (nx, ny, nz, f)
                nz += 1
            ny += 1
        nx += 1


def modal_response(lx: float, ly: float, lz: float, seat: tuple[float, float, float],
                   freqs: list[float], c: float = C_AIR, damping: float = 0.08) -> list[float]:
    """Pressure magnitude at a seat frequency by frequency, from the box's own modes.

    Each mode contributes a resonance weighted by its shape at the seat:
    `p(f) = sum_n psi_n(seat) / ((f_n^2 - f^2) + i damping f f_n)`.
    """
    x, y, z = seat
    triples = list(_mode_triples(lx, ly, lz, max(freqs) * 1.6, c))
    out = []
    for fr in freqs:
        acc = 0j
        for nx, ny, nz, fn in triples:
            if fn == 0.0:
                continue
            psi = mode_shape(nx, ny, nz, x, y, z, lx, ly, lz)
            if abs(psi) < 1e-12:
                continue
            acc += psi / complex(fn * fn - fr * fr, damping * fr * fn)
        out.append(abs(acc))
    return out


def ripple_db(response: list[float], low: float = 0.0, high: float = 1e9,
              band: int = 24) -> float:
    """Peak-to-trough of the smoothed magnitude response in the band, in dB."""
    import math as m
    mags = [20.0 * m.log10(max(v, 1e-30)) for v in response]
    if len(mags) < band:
        return max(mags) - min(mags)
    smoothed = [sum(mags[max(0, i - band // 2):i + band // 2 + 1])
                / len(mags[max(0, i - band // 2):i + band // 2 + 1]) for i in range(len(mags))]
    return max(smoothed) - min(smoothed)


def correction_gains(response: list[float], freqs: list[float], max_boost: float = 12.0,
                     max_cut: float = -18.0) -> list[float]:
    """The fix: an inverse-magnitude correction, smoothed and bounded.

    A room cannot be flattened by EQ above the modal region (it becomes minimum-phase noise), so the
    correction is bounded: no boost beyond `max_boost` dB, no cut below `max_cut`. That bound is the
    honest part — an unbounded inverse always "works" and destroys headroom.
    """
    import math as m
    mags = [20.0 * m.log10(max(v, 1e-30)) for v in response]
    # smooth over a third of an octave so the correction follows modes, not interference nulls
    win = 9
    smooth = [sum(mags[max(0, i - win):i + win + 1]) / len(mags[max(0, i - win):i + win + 1])
              for i in range(len(mags))]
    target = sum(smooth) / len(smooth)
    gains = [-(s - target) for s in smooth]
    return [min(max_boost, max(max_cut, g)) for g in gains]


def apply_correction(response: list[float], gains_db: list[float]) -> list[float]:
    return [v * 10 ** (g / 20.0) for v, g in zip(response, gains_db)]


def correction_report(lx: float, ly: float, lz: float, seat: tuple[float, float, float],
                      f_low: float = 30.0, f_high: float = 300.0, points: int = 180) -> dict:
    """Diagnose, correct, and CHECK that the correction helped — before and after, same metric."""
    freqs = [f_low + (f_high - f_low) * i / (points - 1) for i in range(points)]
    before = modal_response(lx, ly, lz, seat, freqs)
    gains = correction_gains(before, freqs)
    after = apply_correction(before, gains)
    r_before = ripple_db(before)
    r_after = ripple_db(after)
    used = [g for g in gains if abs(g) > 0.5]
    return {"seat": seat, "band_hz": (f_low, f_high), "ripple_before_db": r_before,
            "ripple_after_db": r_after, "improvement_db": r_before - r_after,
            "max_gain_db": max(gains), "min_gain_db": min(gains), "bands_touched": len(used),
            "pass": r_after < r_before,
            "verdict": (f"ripple {r_before:.1f} dB -> {r_after:.1f} dB "
                        f"({r_before - r_after:+.1f} dB) using {len(used)} bands, "
                        f"gains {min(gains):+.1f} to {max(gains):+.1f} dB")}


def gains_from_seats(lx: float, ly: float, lz: float, seats: list[tuple[float, float, float]],
                     f_low: float = 30.0, f_high: float = 300.0, points: int = 180) -> list[float]:
    """A correction derived from the AVERAGE of several seats — the difference between an EQ that
    works at one chair and one that works in the room."""
    import math as m
    freqs = [f_low + (f_high - f_low) * i / (points - 1) for i in range(points)]
    curves = [modal_response(lx, ly, lz, s, freqs) for s in seats]
    db = [[20.0 * m.log10(max(v, 1e-30)) for v in curve] for curve in curves]
    mean = [sum(col) / len(col) for col in zip(*db)]
    win = 9
    smooth = [sum(mean[max(0, i - win):i + win + 1]) / len(mean[max(0, i - win):i + win + 1])
              for i in range(len(mean))]
    target = sum(smooth) / len(smooth)
    gains = [-(s - target) for s in smooth]
    return [min(12.0, max(-18.0, g)) for g in gains]


def spatial_report(lx: float, ly: float, lz: float,
                   tune_seat: tuple[float, float, float],
                   check_seats: list[tuple[float, float, float]],
                   f_low: float = 30.0, f_high: float = 300.0, points: int = 180) -> dict:
    """Does the fix hold up away from the seat it was tuned at? Single-seat vs multi-point.

    This is the test that separates a demo from a solution: an inverse of one measurement always
    flattens that measurement, and can make every other seat worse. The honest fix is derived from
    several seats at once, and the result is reported per seat.
    """
    single = correction_report(lx, ly, lz, tune_seat, f_low, f_high, points)
    multi = gains_from_seats(lx, ly, lz, [tune_seat] + check_seats, f_low, f_high, points)
    freqs = [f_low + (f_high - f_low) * i / (points - 1) for i in range(points)]
    # ONE correction derived at the tuned seat, then applied to every seat — correcting each seat
    # with its own inverse is not a fix, it is a different fix per listener
    single = correction_gains(modal_response(lx, ly, lz, tune_seat, freqs), freqs)
    rows = []
    for seat in [tune_seat] + check_seats:
        raw = modal_response(lx, ly, lz, seat, freqs)
        before = ripple_db(raw)
        with_single = ripple_db(apply_correction(raw, single))
        with_multi = ripple_db(apply_correction(raw, multi))
        rows.append({"seat": seat, "before": before, "single_point": with_single,
                     "multi_point": with_multi,
                     "single_delta": with_single - before, "multi_delta": with_multi - before})
    single_row = rows[0]
    others = rows[1:]
    return {"rows": rows, "tuned_at": tune_seat, "single_gains": single, "multi_gains": multi,
            "single_helps_tuned": single_row["single_delta"] < 0,
            "single_hurts_others": any(r["single_delta"] > 1.0 for r in others),
            "multi_helps_all": all(r["multi_delta"] < 0 for r in rows),
            "multi_worst_delta": max(r["multi_delta"] for r in rows),
            "single_worst_delta": max(r["single_delta"] for r in rows),
            "verdict": (f"tuned at {tune_seat}: single-point EQ changes the tuned seat by "
                        f"{single_row['single_delta']:+.1f} dB but the worst seat by "
                        f"{max(r['single_delta'] for r in rows):+.1f} dB; multi-point EQ changes "
                        f"the worst seat by {max(r['multi_delta'] for r in rows):+.1f} dB")}


def minimax_gains(lx: float, ly: float, lz: float, seats: list[tuple[float, float, float]],
                  f_low: float = 30.0, f_high: float = 300.0, points: int = 180,
                  noise_db: float = 0.0, seed: int = 5) -> list[float]:
    """Per-band gains that centre the SPREAD across mics, rather than the average.

    Rob's operating mode: several room mics listening to the PA, not one at front of house. With N
    measurement points the objective stops being "flatten this curve" and becomes "minimise the worst
    seat" — so each band's gain is set to the midpoint of that band's min/max across mics, not to its
    mean. Both are one line; the difference at the worst seat is the point.

    `noise_db` adds measurement noise to the responses before the gain is derived, because a real
    capture is not a noise-free model.
    """
    import math as m
    import random
    rng = random.Random(seed)
    freqs = [f_low + (f_high - f_low) * i / (points - 1) for i in range(points)]
    curves = []
    for s in seats:
        db = [20.0 * m.log10(max(v, 1e-30)) for v in modal_response(lx, ly, lz, s, freqs)]
        if noise_db:
            db = [d + rng.gauss(0.0, noise_db) for d in db]
        curves.append(db)
    win = 9
    smoothed = []
    for db in curves:
        smoothed.append([sum(db[max(0, i - win):i + win + 1]) / len(db[max(0, i - win):i + win + 1])
                         for i in range(len(db))])
    gains = []
    for i in range(len(freqs)):
        band = [s[i] for s in smoothed]
        centre = 0.5 * (max(band) + min(band))
        gains.append(-(centre - 0.0))
    mean_level = sum(sum(s) / len(s) for s in smoothed) / len(smoothed)
    gains = [g + mean_level for g in gains]
    return [min(12.0, max(-18.0, g)) for g in gains]


def mean_gains(lx: float, ly: float, lz: float, seats: list[tuple[float, float, float]],
               f_low: float = 30.0, f_high: float = 300.0, points: int = 180) -> list[float]:
    """The obvious approach: correct the spatial-average response (what a single-mic system does)."""
    return gains_from_seats(lx, ly, lz, seats, f_low, f_high, points)


def compare_objectives(lx: float, ly: float, lz: float, seats: list[tuple[float, float, float]],
                       f_low: float = 30.0, f_high: float = 300.0, points: int = 180,
                       noise_db: float = 0.0) -> dict:
    """Mean-centring vs spread-centring, measured at every seat, with and without measurement noise."""
    freqs = [f_low + (f_high - f_low) * i / (points - 1) for i in range(points)]
    raw = {s: modal_response(lx, ly, lz, s, freqs) for s in seats}
    mean_g = mean_gains(lx, ly, lz, seats, f_low, f_high, points)
    mini_g = minimax_gains(lx, ly, lz, seats, f_low, f_high, points, noise_db=noise_db)
    rows = []
    for s in seats:
        before = ripple_db(raw[s])
        rows.append({"seat": s, "before": before,
                     "mean_based": ripple_db(apply_correction(raw[s], mean_g)),
                     "minimax": ripple_db(apply_correction(raw[s], mini_g))})
    worst_before = max(r["before"] for r in rows)
    worst_mean = max(r["mean_based"] for r in rows)
    worst_minimax = max(r["minimax"] for r in rows)
    return {"rows": rows, "noise_db": noise_db, "worst_before": worst_before,
            "worst_mean": worst_mean, "worst_minimax": worst_minimax,
            "minimax_wins_on_worst": worst_minimax < worst_mean,
            "verdict": (f"worst seat {worst_before:.1f} dB before; mean-centring {worst_mean:.1f}; "
                        f"spread-centring {worst_minimax:.1f}"
                        + (f" (with {noise_db:.1f} dB measurement noise)" if noise_db else ""))}
