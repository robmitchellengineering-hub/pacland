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

__all__ = ["STANDARD_OBSERVABLES"]
