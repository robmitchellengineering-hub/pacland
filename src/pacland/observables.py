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
# First rung (verified earlier, docs/toolchain.md): h11=1, h21=101. Second rung
# (verified 2026-10-18 on studio-linux, CYTools 1.4.12, quintic):
#   h11 = 1, h21 = 101, chi = -200, c2 = [-250, 50, 50, 50, 50, 50].
#
# Only the *independent* invariants count toward m: h11, h21, and the second Chern
# class c2 (m=3). chi is NOT counted as a rung — chi = 2(h11 - h21) is *derived*
# from h11/h21, so it is a consistency check (the oracle is internally coherent),
# not a new independent validation point. The triple intersection number is
# basis-dependent in CYTools' toric basis ([-625, -25, 5, 125]); its Kähler-basis
# value kappa=5 needs a basis projection, so it is also NOT counted. The honest
# count is m=3, not 5.
TOPOLOGY_OBSERVABLES: tuple[DeficitObservable, ...] = (
    DeficitObservable("h11 (quintic)", True, True, True),
    DeficitObservable("h21 (quintic)", True, True, True),
    DeficitObservable("c2 (quintic)", True, True, True),
)

__all__ = ["STANDARD_OBSERVABLES", "TOPOLOGY_OBSERVABLES"]
