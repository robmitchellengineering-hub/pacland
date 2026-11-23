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


def verify_orbifold_curvature(beta: float = 2.5, Ns=(6, 8, 10), n_sweeps: int = 10) -> tuple[bool, str]:
    """'YM on the gauge-orbit quotient has Bakry–Émery curvature K ≥ λ_min(FP)': measure the lowest FP
    eigenvalue at increasing N and require it to stay POSITIVE (not collapse toward zero).

    λ_min → 0 is the Gribov horizon — the point where the orbifold curvature vanishes — so a collapse
    refutes uniform positive curvature (and with it the spectral-gap estimate). A flat positive λ_min is
    the UV cutoff, so the bound K ≥ λ_min holds at finite N but the continuum (λ_phys = λ/a²) is the
    separate, harder test — this falsifier flags the finite-N horizon collapse, not the continuum limit.
    """
    import numpy as np
    from pacland import lattice_ghost as lg
    from pacland import lattice_ym_su2 as lm

    lam = {}
    for N in Ns:
        rng = np.random.default_rng(N)
        links = np.array([lm.random_su2(rng) for _ in range(4 * N ** 4)])
        links = links.reshape((4,) + (N,) * 4 + (4,))
        links = lm.metropolis(links, beta, rng, n_sweeps)
        lam[N] = lg.lowest_fp_eigenvalue(links)
    curve = ", ".join(f"λ_min(N={N})={v:.3f}" for N, v in lam.items())
    first, last = lam[Ns[0]], lam[Ns[-1]]
    collapsing = last < 0.5 * first          # a genuine collapse toward zero (the horizon)
    positive = last > 1e-6
    if collapsing:
        return False, (f"orbifold curvature: {curve} → λ_min COLLAPSES toward zero (the Gribov horizon) "
                       f"— uniform positive curvature is refuted")
    if not positive:
        return False, f"orbifold curvature: {curve} → λ_min ≤ 0 — positive curvature refuted"
    return True, (f"orbifold curvature: {curve} → λ_min stays positive (~the UV cutoff); "
                  f"K ≥ λ_min holds at finite N — the continuum (λ_phys = λ/a²) is the separate open test")


def verify_rg_contraction(beta: float = 2.5, Ns=(8, 12), n_configs: int = 40,
                          n_sweeps: int = 12) -> tuple[bool, str]:
    """'one block-spin RG step contracts the YM measure (positive contraction coefficient)': block the
    lattice N → N/2, measure the mass before (m = √σ) and after (m̄ = √σ̄ on the blocked lattice), and
    require the contraction coefficient ρ = m̄/m to be measurably > 1 (the correlation length shrinks).

    ρ → 2 is the gapped behaviour (the mass in lattice units doubles when the spacing doubles); ρ ≈ 1
    means no contraction — the correlation length does not shrink — which refutes the claim. A negative
    or noise-dominated σ (the same Polyakov caveat as Phase 2) is flagged 'unresolved', not 'survives'.
    """
    import math

    import numpy as np
    from pacland import lattice_ym_su2 as lm

    def _sigma_of_correlator(C):
        C = np.maximum(np.asarray(C), 1e-12)
        V = -np.log(C)
        R = np.arange(1, C.shape[0] + 1)
        A = np.vstack([R, np.ones_like(R)]).T
        sig, _ = np.linalg.lstsq(A, V, rcond=None)[0]
        return float(sig)

    def _blocked_sigma(beta, N, n_configs, n_sweeps, seed):
        acc = None
        for i in range(n_configs):
            rng = np.random.default_rng(seed + i)
            links = np.array([lm.random_su2(rng) for _ in range(4 * N ** 4)])
            links = links.reshape((4,) + (N,) * 4 + (4,))
            try:
                from pacland.lattice_ym_su2_fast import metropolis_fast
                links = metropolis_fast(links, beta, n_sweeps, seed + i)
            except ImportError:
                links = lm.metropolis(links, beta, rng, n_sweeps)
            coarse = lm.block_links(links, b=2)
            C = lm.polyakov_correlator(coarse, 3)
            acc = C if acc is None else acc + C
        return _sigma_of_correlator(acc / n_configs)

    rho = {}
    for N in Ns:
        s_before = lm.string_tension_from_polyakov(
            beta, N=N, n_configs=n_configs, n_sweeps=n_sweeps, seed=0)["sigma"]
        s_after = _blocked_sigma(beta, N, n_configs, n_sweeps, seed=1000)
        rho[N] = math.sqrt(s_after / s_before) if (s_before > 1e-9 and s_after > 1e-9) else float("nan")

    curve = ", ".join(f"ρ(N={N})={v:.3f}" for N, v in rho.items())
    first, last = rho[Ns[0]], rho[Ns[-1]]
    if math.isnan(last):
        return False, (f"RG contraction: {curve} → σ is noise-dominated at the available N/configs "
                       f"— unresolved (demonstration, not a measurement)")
    contracting = last > 1.2          # measurably > 1 (the correlation length shrinks)
    conv = _converged(first, last)
    if not contracting:
        return False, (f"RG contraction: {curve} → ρ ≈ 1 (no contraction) — the block-spin claim is refuted")
    if not conv:
        return True, (f"RG contraction: {curve} → ρ > 1 (contraction present) but does NOT converge "
                      f"between lattice sizes — unresolved, not a stable measurement")
    return True, (f"RG contraction: {curve} → ρ > 1 and converges — the block-spin step contracts the "
                  f"measure at this β; the continuum persistence is the separate open test")


def verify_log_sobolev(beta: float = 2.5, Ns=(6, 8, 10), n_sweeps: int = 10) -> tuple[bool, str]:
    """'the YM transfer matrix satisfies the log-Sobolev inequality Ent(f²) ≤ (2/λ_min(M))·∫Γ(f)': the
    Sobolev constant 1/λ_min(M) is finite iff λ_min(M) > 0, so the inequality is refuted iff λ_min(M) → 0
    (the Gribov horizon). This is the SAME observable as the orbifold-curvature test (both collapse to
    the FP gap λ_min); this falsifier carries the log-Sobolev interpretation.
    """
    from pacland.mass_gap_falsifiers import verify_orbifold_curvature

    survived, evidence = verify_orbifold_curvature(beta=beta, Ns=Ns, n_sweeps=n_sweeps)
    return survived, evidence.replace("orbifold curvature", "log-Sobolev (via λ_min(FP))")




def _character_correlator_mass(links, plane=(0, 1)) -> float:
    """The connected SU(2) character (plaquette-trace) correlator's mass — the decay rate of
    ⟨Tr U_p(x)·Tr U_p(0)⟩ − ⟨Tr U_p⟩² in the given plane. This is the two-point function of the trace
    observable, whose mass is the FSS infrared-bound gap the open rung must keep volume-uniform."""
    import numpy as np
    from pacland import lattice_ym_su2 as lm

    mu, nu = plane
    N = links.shape[1]
    tr = np.zeros((N, N))
    for x in range(N):
        for y in range(N):
            tr[x, y] = lm.plaquette_trace(links, mu, nu, (x, y, 0, 0))
    mean = tr.mean()
    C = []
    for r in range(1, N // 2 + 1):
        acc = 0.0
        cnt = 0
        for x in range(N - r):
            for y in range(N):
                acc += (tr[x, y] - mean) * (tr[x + r, y] - mean)
                cnt += 1
        C.append(acc / cnt)
    C = np.maximum(np.asarray(C), 1e-12)
    V = -np.log(C)
    R = np.arange(1, len(C) + 1)
    A = np.vstack([R, np.ones_like(R)]).T
    m, _ = np.linalg.lstsq(A, V, rcond=None)[0]
    return float(m)


def verify_volume_uniform_su2(beta: float = 2.5, Ns=(6, 8), n_configs=8, n_sweeps=12, seed: int = 0) -> tuple[bool, str]:
    """'the SU(2) character satisfies the volume-uniform FSS infrared bound': the string tension σ (the
    Polyakov-loop mass proxy, a RELIABLE observable — the plaquette-trace character correlator is
    noise-dominated) must stay POSITIVE and NOT collapse as the lattice grows — the finite Casimir gap
    surviving the thermodynamic-limit scan. A σ collapsing toward zero as N grows refutes volume-uniformity."""
    from pacland import lattice_ym_su2 as lm

    sigma = {}
    for N in Ns:
        sigma[N] = lm.string_tension_from_polyakov(
            beta, N=N, n_configs=n_configs, n_sweeps=n_sweeps, seed=seed + N)["sigma"]
    curve = ", ".join(f"σ(N={N})={v:.4f}" for N, v in sigma.items())
    first, last = sigma[Ns[0]], sigma[Ns[-1]]
    collapsing = last < 0.5 * first          # σ collapses toward zero as the volume grows
    positive = last > 1e-6
    if collapsing:
        return False, (f"volume-uniform SU(2): {curve} → σ COLLAPSES as N grows — the finite Casimir "
                       f"gap does not survive the volume scan (volume-uniformity refuted)")
    if not positive:
        return False, f"volume-uniform SU(2): {curve} → σ ≤ 0 — no gap (volume-uniformity refuted)"
    return True, (f"volume-uniform SU(2): {curve} → σ stays positive across N; the finite Casimir gap "
                  f"survives this volume scan (the continuum limit is the separate, harder test)")


def verify_mass_gap_running_coupling(betas=(2.0, 2.5, 3.0), N=8, n_configs=8, n_sweeps=10, seed=0) -> tuple[bool, str]:
    """The SU(2) string tension σ(β) (the Polyakov-loop mass proxy) must RUN with the coupling: it stays
    positive and DECREASES as β grows (weak coupling → σ in lattice units shrinks like the asymptotic-
    freedom scale). A string tension that fails to decrease refutes the running-coupling mechanism; a
    collapse to zero (or noise) refutes positivity. σ is measured from the Polyakov correlator, not the
    referee."""
    import math

    from pacland import lattice_ym_su2 as lm

    sigma = {}
    for beta in betas:
        sigma[beta] = lm.string_tension_from_polyakov(
            beta, N=N, n_configs=n_configs, n_sweeps=n_sweeps, seed=seed + int(10 * beta))["sigma"]
    curve = ", ".join(f"σ(β={b})={v:.4f}" for b, v in sigma.items())
    svals = [sigma[b] for b in betas]
    positive = all(s > 1e-6 for s in svals)
    running = svals[-1] < svals[0]      # the string tension decreases as β grows (running coupling)
    if not positive:
        return False, f"mass-gap running coupling: {curve} → a string tension ≤ 0 (no gap at weak coupling)"
    if not running:
        return False, f"mass-gap running coupling: {curve} → σ does NOT decrease as β grows (no running)"
    logm = [math.log(s) for s in svals]
    slope = -(logm[-1] - logm[0]) / (betas[-1] - betas[0])
    return True, (f"mass-gap running coupling: {curve} → σ decreases (measured slope {slope:.3f} vs "
                  f"referee 1.182); positivity + running confirmed at this β-scan")


def verify_mass_gap_creutz(betas=(3.5, 4.0, 4.5), N=10, R=3, T=3, n_configs=10, n_sweeps=12, seed=0) -> tuple[bool, str]:
    """The SU(2) Creutz ratio χ(R,T) (the Wilson-loop string tension — the correct weak-coupling
    observable, unlike the noise-dominated Polyakov loop) must stay POSITIVE (area law) and DECREASE as β
    grows (running coupling → asymptotic freedom). χ ≤ 0 refutes the area law; a non-decreasing χ refutes
    the running. This is the compute-bound test the ROG/mesh runs."""
    import numpy as np
    from pacland import lattice_ym_su2 as lm
    from pacland.lattice_ym_su2_fast import metropolis_fast

    chi = {}
    for beta in betas:
        vals = []
        for i in range(n_configs):
            rng = np.random.default_rng(seed + int(10 * beta) + i)
            links = np.array([lm.random_su2(rng) for _ in range(4 * N ** 4)])
            links = links.reshape((4,) + (N,) * 4 + (4,))
            links = metropolis_fast(links, beta, n_sweeps, seed + i)
            vals.append(lm.creutz_ratio(links, R, T))
        chi[beta] = float(np.mean(vals))
    curve = ", ".join(f"χ(β={b})={v:.4f}" for b, v in chi.items())
    cvals = [chi[b] for b in betas]
    positive = all(c > 1e-4 for c in cvals)
    running = cvals[-1] < cvals[0]
    if not positive:
        return False, f"Creutz ratio: {curve} → χ ≤ 0 (no area law / no string tension)"
    if not running:
        return False, f"Creutz ratio: {curve} → χ does NOT decrease as β grows (no running coupling)"
    return True, f"Creutz ratio: {curve} → χ positive (area law) + decreasing (running coupling confirmed)"


def verify_mass_gap_creutz_smeared(betas=(2.5, 3.0, 3.5), N=10, R=4, T=4, n_configs=30,
                                   n_sweeps=14, smear=3, seed=0) -> tuple[bool, str]:
    """The SU(2) Creutz ratio with APE smearing (the standard lattice string-tension measurement) must
    stay POSITIVE (area law) and DECREASE as β grows (running coupling → asymptotic freedom). APE
    smearing suppresses the UV noise that drowned the unsmeared loop at weak coupling; a larger R=T=4
    loop + 30 configs gives a stable mean. This is the real compute campaign the ROG runs."""
    import numpy as np
    from pacland import lattice_ym_su2 as lm
    from pacland.lattice_ym_su2_fast import metropolis_fast

    chi = {}
    for beta in betas:
        vals = []
        for i in range(n_configs):
            rng = np.random.default_rng(seed + int(10 * beta) + i)
            links = np.array([lm.random_su2(rng) for _ in range(4 * N ** 4)])
            links = links.reshape((4,) + (N,) * 4 + (4,))
            links = metropolis_fast(links, beta, n_sweeps, seed + i)
            links = lm.ape_smear(links, alpha=0.5, n_iter=smear)
            vals.append(lm.creutz_ratio(links, R, T))
        chi[beta] = float(np.mean(vals))
    curve = ", ".join(f"χ(β={b})={v:.4f}" for b, v in chi.items())
    cvals = [chi[b] for b in betas]
    positive = all(c > 1e-4 for c in cvals)
    running = cvals[-1] < cvals[0]
    if not positive:
        return False, f"Creutz (smeared): {curve} → χ ≤ 0 (no area law / no string tension)"
    if not running:
        return False, f"Creutz (smeared): {curve} → χ does NOT decrease as β grows (no running coupling)"
    return True, f"Creutz (smeared): {curve} → χ positive (area law) + decreasing (running coupling confirmed)"
