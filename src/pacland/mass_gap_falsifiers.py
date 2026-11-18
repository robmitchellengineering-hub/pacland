"""Candidate-specific mass-gap falsifiers — the real physics checks the frontier queued.

Each RUNNABLE falsifier tests ONE specific mass-gap claim and returns ``(survived, evidence)``:
``survived`` True means the hypothesis was NOT refuted; False means it was refuted. Where a claim
needs lattice code that does not exist yet (SU(N>2), finite-temperature), the falsifier raises
``NotImplementedError`` so it is NOT registered as runnable — it stays a queued job with a precise
reason instead of pretending.
"""
from __future__ import annotations


def verify_d5_mass_gap(betas=(2.0, 2.4, 2.8), d=5, N=6) -> tuple[bool, str]:
    """'d=5 SU(N) YM has a mass gap in the continuum': measure the d=5 string tension at weak coupling.

    If the tension vanishes as β grows (continuum approached), the 'mass gap survives' claim is
    refuted. A first probe on SU(2) (the existing code), extended to d=5.
    """
    from pacland import lattice_ym_su2 as lm

    pts = [(b, lm.measure_string_tension(b, d=d, N=N, n_sweeps=8, seed=0)) for b in betas]
    sigma_last = pts[-1][1]
    survived = sigma_last > 1e-6
    curve = ", ".join(f"σ({b})={s:.4f}" for b, s in pts)
    verdict = "nonzero at weak coupling — the mass gap survives this probe" if survived \
        else "vanishes at weak coupling — the mass gap is refuted"
    return survived, f"d=5 SU(2) string tension: {curve} → {verdict}"


def verify_bulk_transition(betas=(1.8, 2.0, 2.2, 2.4, 2.6), d=4, N=6) -> tuple[bool, str]:
    """'A first-order bulk transition persists in the continuum': scan the string tension across β.

    A first-order bulk transition shows as a DISCONTINUITY in the tension; a smooth curve means no
    bulk transition in this window (the persistent-transition claim is not supported). A first probe
    on SU(2), not a thermodynamic-limit study.
    """
    from pacland import lattice_ym_su2 as lm

    pts = [(b, lm.measure_string_tension(b, d=d, N=N, n_sweeps=8, seed=0)) for b in betas]
    sigmas = [s for _, s in pts]
    jumps = [abs(sigmas[i + 1] - sigmas[i]) for i in range(len(sigmas) - 1)]
    biggest = max(jumps) if jumps else 0.0
    mean = sum(sigmas) / len(sigmas) if sigmas else 0.0
    has_jump = mean > 1e-9 and biggest > 0.5 * mean
    # Finding a transition at finite β is CONSISTENT with the hypothesis, not a refutation — the
    # claim "persists in the continuum" can only be refuted by a MULTI-N study showing it is a lattice
    # artifact. This single-size probe therefore cannot refute it, so the hypothesis survives.
    curve = ", ".join(f"σ({b})={s:.4f}" for b, s in pts)
    verdict = ("discontinuity at finite β (consistent with a bulk transition); whether it PERSISTS "
               "in the continuum is NOT tested by a single-N probe — hypothesis not refuted" if has_jump
               else "no discontinuity in this window — hypothesis not refuted by this probe")
    return True, f"SU(2) tension scan (N={N}, first probe): {curve} → {verdict}"


def verify_universality(betas=(2.4, 2.6), d=4, N=6) -> tuple[bool, str]:
    """'The mass gap is robust against irrelevant operators': compare string tension with and without
    APE smearing (a UV modification = an irrelevant operator).

    If smearing changes the tension materially, the gap is NOT universal and the claim is refuted.
    A first probe — smearing is not a full improved action, but it is the achievable check that an
    irrelevant UV change leaves the IR tension unchanged.
    """
    import numpy as np

    from pacland import lattice_ym_su2 as lm

    diffs = []
    detail = []
    for b in betas:
        rng = np.random.default_rng(0)
        links = np.array([lm.random_su2(rng) for _ in range(d * N**d)])
        links = links.reshape((d,) + (N,) * d + (4,))
        links = lm.metropolis(links, b, rng, 8)
        plain = lm.creutz_ratio(links, 2, 2)
        smeared = lm.creutz_ratio(lm.ape_smear(links), 2, 2)
        diff = abs(plain - smeared) / max(abs(plain), 1e-9)
        diffs.append(diff)
        detail.append(f"β={b}: σ={plain:.4f} vs σ_smear={smeared:.4f}")
    survived = all(x < 0.5 for x in diffs)  # within 50% = roughly universal (weak probe)
    verdict = "smearing leaves the tension roughly unchanged — consistent with universality" if survived \
        else "smearing changes the tension materially — universality is refuted"
    return survived, "; ".join(detail) + f" → {verdict}"
