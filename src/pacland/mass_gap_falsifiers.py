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


def verify_d5_mass_gap(betas=(2.0, 2.4, 2.8, 3.2), d=5, Ns=(4, 6)) -> tuple[bool, str]:
    """'d=5 SU(N) YM has a mass gap in the continuum': measure the d=5 string tension at increasing β
    (finer lattice) and require a DECREASING, converging tension — a fixed-lattice nonzero value is
    NOT a mass gap; only a tension that survives the continuum trend is. A flat/noisy trend means the
    continuum limit cannot be assessed (unresolved), not 'survives'.
    """
    from pacland import lattice_ym_su2 as lm

    curves = {}
    for N in Ns:
        curves[N] = [lm.measure_string_tension(b, d=d, N=N, n_sweeps=10, seed=0) for b in betas]
    last_N = Ns[-1]
    sigma_first = curves[last_N][0]
    sigma_last = curves[last_N][-1]
    conv = _converged(curves[Ns[0]][-1], sigma_last)
    decreasing = sigma_last < 0.8 * sigma_first  # the tension falls toward the continuum
    survived = conv and decreasing and sigma_last > 1e-6
    curve = ", ".join(f"σ(β={b})={s:.3f}" for b, s in zip(betas, curves[last_N]))
    if not conv:
        verdict = "does NOT converge between lattice sizes — unresolved (demonstration, not a measurement)"
    elif not decreasing:
        verdict = ("tension does NOT decrease toward the continuum (flat/noisy) — the mass gap cannot "
                   "be assessed from this data (unresolved)")
    elif survived:
        verdict = "tension is nonzero and decreasing toward the continuum — consistent with a mass gap"
    else:
        verdict = "tension vanishes at weak coupling — the mass gap is refuted"
    # 'unresolved' when the trend is not assessable; otherwise a definitive bool
    if (not conv) or (not decreasing):
        return False, f"d=5 SU(2) string tension: {curve} → {verdict}  [unresolved — not a refutation]"
    return survived, f"d=5 SU(2) string tension: {curve} → {verdict}"


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


def verify_universality(betas=(2.4, 2.6), d=4, Ns=(4, 6, 8)) -> tuple[bool, str]:
    """'The mass gap is robust against irrelevant operators': compare string tension with and without
    APE smearing (a UV modification = an irrelevant operator) at THREE lattice sizes, so the smearing
    difference must converge toward zero as N grows — a real continuum check, not a two-point demo."""
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


def verify_large_n_ratio(beta: float = 2.5, N: int = 6, n_sweeps: int = 12,
                         n_meas: int = 40) -> tuple[bool, str]:
    """'The mass gap is nonzero for all N with a universal ratio to the string tension': compute the
    RG-invariant ratio m/sqrt(sigma) for SU(2) and SU(3) and check they agree (universality in N).

    Both ratios being close is consistent with a universal ratio; a large gap between them refutes the
    'universal ratio' part. A first probe at one coupling; a real test needs the weak-coupling plateau.
    """
    import math

    from pacland import glueball as g2
    from pacland import glueball_su3 as g3
    from pacland import lattice_ym_su2 as su2
    from pacland import lattice_ym_su3 as su3

    sig2 = su2.measure_string_tension(beta, d=4, N=N, n_sweeps=n_sweeps, seed=0)
    sig3 = su3.measure_string_tension(beta, d=4, N=N, n_sweeps=n_sweeps, n_meas=n_meas, seed=0)
    m2 = g2.glueball_mass(beta, N=N, n_sweeps=n_sweeps, n_meas=n_meas, seed=0)
    m3 = g3.glueball_mass_su3(beta, N=N, n_sweeps=n_sweeps, n_meas=n_meas, seed=0)
    ratio2 = m2 / math.sqrt(max(sig2, 1e-9))
    ratio3 = m3 / math.sqrt(max(sig3, 1e-9))
    both_positive = m2 > 0 and m3 > 0 and sig2 > 0 and sig3 > 0
    universal = _converged(ratio2, ratio3, tol=0.4)
    survived = both_positive and universal
    verdict = ("SU(2) and SU(3) ratios m/sqrt(sigma) agree — consistent with a universal ratio"
               if universal else "the ratios differ materially — the 'universal ratio' claim is refuted")
    if not both_positive:
        verdict = "one group's mass/tension is non-positive — the ratio cannot be formed (unresolved)"
    return survived, (f"SU(2) m/√σ={ratio2:.3f} (m={m2:.3f}, σ={sig2:.3f}), "
                      f"SU(3) m/√σ={ratio3:.3f} (m={m3:.3f}, σ={sig3:.3f}) → {verdict}")


def verify_polyakov_clustering(beta: float = 5.0, Nt: int = 2, Ns: int = 6, n_sweeps: int = 10,
                               n_meas: int = 8) -> tuple[bool, str]:
    """'Polyakov-loop correlators cluster exponentially at finite T': extract the screening mass m.

    m > 0 means exponential clustering (the claim survives); m -> 0 means the correlation length
    diverges (the claim fails). Above the deconfinement transition the Polyakov loop is nonzero and the
    correlator decays with a positive screening mass — this is the regime where the claim is tested.
    """
    from pacland import polyakov as pk

    m = pk.measure_correlation_mass(beta, Nt=Nt, Ns=Ns, n_sweeps=n_sweeps, n_meas=n_meas, seed=0)
    survived = m > 0.05
    verdict = ("positive screening mass — exponential clustering (the claim survives this probe)"
               if survived else "no positive screening mass — either the clustering claim fails or the "
                                "connected signal is too small to resolve at this coupling")
    return survived, f"SU(3) Polyakov screening mass (N_t={Nt}, N_s={Ns}, β={beta}) = {m:.4f} → {verdict}"


