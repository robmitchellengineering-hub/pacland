"""The canonical observable set and its honest status — approach #6 data.

The ten dimensionless observables of ``docs/observable-measure.md`` §3, classified
for the deficit report by three independent questions:

  measured   — an independent experimental target c* exists?
  computable — can the flux-vacua oracle evaluate O(x), even approximately?
  validated  — is the oracle's error model calibrated against c* here?

Status as of 2026-10-18: all ten are *measured* (targets exist); the seven
"easy/medium" ones are *computable*; the three "hard/hardest" (m_u/m_d, m_H/m_Z,
Lambda) are not; and NONE are *validated*, because the flux-vacua oracle (L2,
build #3) is not implemented. Hence the real validation count ``m`` is 0 and the
deficit is total — the input to ``deficit.deficit_report``.
"""
from __future__ import annotations

from .deficit import DeficitObservable

# name,              measured, computable, validated   (oracle difficulty)
STANDARD_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("alpha_s_MZ",      True, True,  False),  # easy
    DeficitObservable("alpha_em_MZ",     True, True,  False),  # easy
    DeficitObservable("m_t_over_m_Z",    True, True,  False),  # easy
    DeficitObservable("sin2_theta_W",    True, True,  False),  # easy
    DeficitObservable("m_b_over_m_t",    True, True,  False),  # medium
    DeficitObservable("m_mu_over_m_tau", True, True,  False),  # medium
    DeficitObservable("theta_C",         True, True,  False),  # medium
    DeficitObservable("m_u_over_m_d",    True, False, False),  # hard — no oracle value
    DeficitObservable("m_H_over_m_Z",    True, False, False),  # hard — no oracle value
    DeficitObservable("Lambda_MPl4",     True, False, False),  # hardest — not computable
)

# The validated oracle outputs: CYTools topology, grown by climbing the rung.
#
# Verified 2026-10-18 on studio-linux (CYTools 1.4.12, quintic):
#   h11 = 1, h21 = 101, chi = -200, c2 = [-250, 50, 50, 50, 50, 50],
#   kappa = 5  (Kähler-basis triple intersection, intersection_numbers(in_basis=True)).
#
# Only the *independent* invariants count toward m: h11, h21, c2, kappa (m=4).
# chi is NOT counted — chi = 2(h11 - h21) is *derived*, a consistency check (the
# oracle is internally coherent), not a new independent validation point. The
# toric-basis intersection numbers ([-625, -25, 5, 125]) are basis-dependent;
# only the Kähler-basis kappa=5 is the physical triple intersection. Honest count:
# m=4.
TOPOLOGY_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("h11 (quintic)", True, True, True),
    DeficitObservable("h21 (quintic)", True, True, True),
    DeficitObservable("c2 (quintic)", True, True, True),
    DeficitObservable("kappa (quintic)", True, True, True),
)

# The flux-vacua oracle (JAXVacua) sector. The D3 tadpole N_flux is EXACTLY the
# symplectic pairing F^T J H — recovered at machine precision (r=1.0, residual
# ~1e-14) from data/vacua_observables.json, with J = [0 I; -I 0] the standard
# symplectic form (scripts/validate_tadpole.py). That is the first validated rung
# of the flux sector (m=1); W0, g_s, gauge couplings and the mass spectrum remain
# unvalidated — and the mass spectrum is uncomputable (the documented boundary).
FLUX_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("N_flux (tadpole)", True, True, True),
    DeficitObservable("log W0", True, True, False),
    DeficitObservable("log g_s", True, True, False),
    DeficitObservable("gauge coupling", True, True, False),
    DeficitObservable("mass spectrum", True, False, False),
)

# The Standard-Model sector — constraint-first, one sector up. The SM's *exact*
# structure (the Complete Exact Structure theorem's "constraints + labels +
# parameters") is computed EXACTLY by sympy (zero tolerance) and validated against
# the measured SM. Four independent exact facts, each a real deficit rung:
#   anomaly cancellation     5/5  — the five gauge/gravitational anomalies vanish
#   hypercharge uniqueness   4/4  — the anomaly conditions uniquely fix hypercharge
#   generation number        1    — N_gen = 3 = a topological index (|chi|/2)
#   free-parameter count     1    — 19 = orbit-space dimension of the flavor group
# These are the m=0 frontier the flux theorem named: the SM sector's exact content,
# now climbed. (The 19 free parameters remain unVALIDATED as *predictions* — their
# measured values are the c*; what is validated here is the exact structure that
# classifies them, not a vacuum that produces them.)
SM_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("SM anomaly cancellation (5/5)", True, True, True),
    DeficitObservable("SM hypercharge uniqueness (4/4)", True, True, True),
    DeficitObservable("SM generation number N_gen=3", True, True, True),
    DeficitObservable("SM free-parameter count = 19", True, True, True),
)

__all__ = ["STANDARD_OBSERVABLES", "TOPOLOGY_OBSERVABLES", "FLUX_OBSERVABLES", "SM_OBSERVABLES"]
