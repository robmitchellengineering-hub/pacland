"""Candidate-specific mass-gap falsifiers — the real physics checks the frontier queued.

Each RUNNABLE falsifier tests ONE specific mass-gap claim and returns ``(survived, evidence)``:
``survived`` True means the hypothesis was NOT refuted; False means it was refuted. Every falsifier
runs at TWO lattice sizes and reports whether its signal CONVERGES with N — a non-converging number is
honestly flagged as a demonstration, not a measurement. Where a claim needs lattice code that does not
exist yet (SU(N>2), finite-temperature), the falsifier is NOT registered as runnable — it stays a
queued job with a precise reason instead of pretending.
"""
from __future__ import annotations


def _converged(a: float, b: float, tol: float = 0.3) -> bool:
    """True when ``a`` and ``b`` agree within ``tol`` (relative), i.e. the signal stabilises with N."""
    scale = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / scale < tol


def verify_d5_mass_gap(betas=(2.0, 2.4, 2.8), d=5, Ns=(4, 6)) -> tuple[bool, str]:
    """'d=5 SU(N) YM has a mass gap in the continuum': measure the d=5 string tension at weak coupling
    at two lattice sizes, and check whether the weak-coupling value converges."""
    from pacland import lattice_ym_su2 as lm

    per_n = []
    for N in Ns:
        pts = [(b, lm.measure_string_tension(b, d=d, N=N, n_sweeps=10, seed=0)) for b in betas]
        per_n.append((N, pts[-1][1]))
    last = per_n[-1][1]
    conv = _converged(per_n[0][1], per_n[-1][1])
    survived = last > 1e-6 and conv  # a mass gap survives only if the weak-coupling tension is
    # nonzero AND stable across lattice sizes
    curve = ", ".join(f"N={N}: σ(β={betas[-1]})={s:.4f}" for N, s in per_n)
    if not conv:
        verdict = "does NOT converge between lattice sizes — a demonstration, not a measurement"
    elif survived:
        verdict = "nonzero and converging at weak coupling — the mass gap survives this probe"
    else:
        verdict = "vanishing at weak coupling — the mass gap is refuted"
    return survived, f"d=5 SU(2) string tension at weak coupling: {curve} → {verdict}"


def verify_bulk_transition(betas=(1.8, 2.0, 2.2, 2.4, 2.6), d=4, Ns=(4, 6)) -> tuple[bool, str]:
    """'A first-order bulk transition persists in the continuum': scan the string tension across β at
    two lattice sizes and check whether a discontinuity PERSISTS (moves) with N."""
    from pacland import lattice_ym_su2 as lm

    per_n = {}
    for N in Ns:
        pts = [(b, lm.measure_string_tension(b, d=d, N=N, n_sweeps=10, seed=0)) for b in betas]
        sigmas = [s for _, s in pts]
        jumps = [abs(sigmas[i + 1] - sigmas[i]) for i in range(len(sigmas) - 1)]
        biggest = max(jumps) if jumps else 0.0
        mean = sum(sigmas) / len(sigmas) if sigmas else 0.0
        per_n[N] = biggest / max(mean, 1e-9)
    # a bulk transition that PERSISTS keeps its jump size across N; a lattice artifact shrinks as N
    # grows (moves to the continuum limit). Two sizes is the minimum to see the direction.
    jump_ratio_small, jump_ratio_big = per_n[Ns[0]], per_n[Ns[1]]
    shrinking = jump_ratio_big < 0.7 * jump_ratio_small  # jump shrinking => artifact
    conv = _converged(jump_ratio_small, jump_ratio_big)
    # the hypothesis (transition persists) is REFUTED if the jump shrinks toward the continuum;
    # it survives if the jump is stable/growing (not an artifact).
    survived = not shrinking
    detail = ", ".join(f"N={N}: max-jump/mean={r:.3f}" for N, r in per_n.items())
    if not conv:
        verdict = "jump size does not converge between lattice sizes — a demonstration, not a measurement"
    elif shrinking:
        verdict = "the discontinuity SHRINKS with N — it is a lattice artifact, so the persistent-transition claim is refuted"
    else:
        verdict = "the discontinuity persists (not shrinking) — the persistent-transition claim survives this probe"
    return survived, f"SU(2) tension scan: {detail} → {verdict}"


def verify_universality(betas=(2.4, 2.6), d=4, Ns=(4, 6)) -> tuple[bool, str]:
    """'The mass gap is robust against irrelevant operators': compare string tension with and without
    APE smearing (a UV modification = an irrelevant operator) at two lattice sizes."""
    import numpy as np

    from pacland import lattice_ym_su2 as lm

    per_n = {}
    for N in Ns:
        diffs = []
        for b in betas:
            rng = np.random.default_rng(0)
            links = np.array([lm.random_su2(rng) for _ in range(d * N**d)])
            links = links.reshape((d,) + (N,) * d + (4,))
            links = lm.metropolis(links, b, rng, 10)
            plain = lm.creutz_ratio(links, 2, 2)
            smeared = lm.creutz_ratio(lm.ape_smear(links), 2, 2)
            diffs.append(abs(plain - smeared) / max(abs(plain), 1e-9))
        per_n[N] = sum(diffs) / len(diffs)
    mean_diff = per_n[Ns[-1]]
    conv = _converged(per_n[Ns[0]], per_n[Ns[-1]])
    survived = conv and mean_diff < 0.5
    detail = ", ".join(f"N={N}: mean|Δσ|/σ={r:.3f}" for N, r in per_n.items())
    if not conv:
        verdict = "smearing ratio does not converge — a demonstration, not a measurement"
    elif survived:
        verdict = "smearing leaves the tension roughly unchanged — consistent with universality"
    else:
        verdict = "smearing changes the tension materially — universality is refuted"
    return survived, f"SU(2) smear-vs-plain: {detail} → {verdict}"
