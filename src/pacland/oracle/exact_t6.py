"""Exact T^6 = (T^2)^3 toroidal orbifold — the exactly-solvable IIB flux compactification.

Build #2 done properly: every observable is a **closed form**, so the oracle error
is identically zero and each observable is a free validated rung for the Mitchell
Deficit. This supersedes the toy ``exact_toric`` (whose tadpole was a placeholder).

Physics (the untwisted T^6 in the standard symplectic basis of H^3):

* ``b3 = 8``; the period vector is the tensor product of the three T^2 periods.
* the intersection form is ``Sigma = sigma (x) sigma (x) sigma`` with
  ``sigma = [[0,1],[-1,0]]`` the T^2 symplectic form.
* ``K = -log(-i Pi^dag Sigma Pi) = -log(8 Im t1 Im t2 Im t3)``.
* ``g_{i jbar} = delta_ij / (4 Im(t_i)^2)`` (diagonal for the square torus).
* ``N_flux = F^T Sigma H`` (the D3 tadpole — the same symplectic pairing we already
  validate on the CY sample, now in closed form).
* ``W = (F - tau0 H) . Pi`` (the Gukov-Vafa-Witten superpotential).
* ``g_s = 1/Im(tau0)``.

All quantities are real physics; none is illustrative. The module is pure numpy.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..error_model import ErrorModel, Kind


SIGMA_2 = np.array([[0.0, 1.0], [-1.0, 0.0]])  # T^2 symplectic form


def symplectic_form() -> np.ndarray:
    """The 8x8 intersection form ``Sigma = sigma (x) sigma (x) sigma``.

    In the tensor-product basis of H^3(T^6) this is the integral of ``alpha_A ^
    alpha_B`` over T^6. It is unimodular (determinant 1), which is the no-global-
    symmetry statement on the charge lattice.
    """
    return np.kron(np.kron(SIGMA_2, SIGMA_2), SIGMA_2)


def period_vector(tau1, tau2, tau3) -> np.ndarray:
    """The 8-dim holomorphic 3-form period ``(1, tau1) (x) (1, tau2) (x) (1, tau3)``."""
    one = 1.0 + 0.0j
    p = np.kron(np.array([one, complex(tau1)]),
                np.array([one, complex(tau2)]))
    return np.kron(p, np.array([one, complex(tau3)]))


def kahler_potential(tau1, tau2, tau3) -> float:
    """``K = -log(8 Im t1 Im t2 Im t3)`` = ``-log(i Pi^dag Sigma Pi)``.

    With the standard T^2 intersection form ``sigma = [[0,1],[-1,0]]`` one has
    ``Pi^dag Sigma Pi = -8i Im(t1)Im(t2)Im(t3)``, so ``i Pi^dag Sigma Pi`` is the
    positive quantity ``8 Im(t1)Im(t2)Im(t3)`` that enters the Kaehler potential.
    """
    pi = period_vector(tau1, tau2, tau3)
    sigma = symplectic_form()
    return float(-np.log(np.real(1j * (pi.conj() @ sigma @ pi))))


def kahler_metric(tau1, tau2, tau3) -> np.ndarray:
    """The 3x3 Kaehler metric ``g_{i jbar} = delta_ij / (4 Im(t_i)^2)``.

    Diagonal because the square torus has no off-diagonal complex structure.
    """
    ims = [complex(t).imag for t in (tau1, tau2, tau3)]
    return np.diag([1.0 / (4.0 * im * im) for im in ims])


def tadpole(F, H) -> int:
    """``N_flux = F^T Sigma H`` — the D3 tadpole (an integer, exactly)."""
    F = np.asarray(F, dtype=float)
    H = np.asarray(H, dtype=float)
    return int(round(float(F @ symplectic_form() @ H)))


def superpotential(F, H, tau0, tau1, tau2, tau3) -> complex:
    """``W = (F - tau0 H) . Pi`` — the Gukov-Vafa-Witten superpotential."""
    pi = period_vector(tau1, tau2, tau3)
    G = np.asarray(F, dtype=float) - complex(tau0) * np.asarray(H, dtype=float)
    return complex(G @ pi)


def gauge_coupling(tau0) -> float:
    """``g_s = 1/Im(tau0)`` — the string coupling (closed form)."""
    return float(1.0 / complex(tau0).imag)


def kk_mass(v) -> float:
    """Kaluza-Klein scale of a T^2 of volume ``v``: ``m_KK = 1/sqrt(v)``.

    In string units (alpha' = 1) the KK mode mass is the inverse radius, and the
    T^2 radius is sqrt(v).
    """
    return float(1.0 / np.sqrt(v))


def winding_mass(v) -> float:
    """Winding-mode scale of a T^2 of volume ``v``: ``m_w = sqrt(v)``."""
    return float(np.sqrt(v))


def tower_mass(v) -> float:
    """Lightest tower mass (KK or winding, whichever is lighter): ``min(1/sqrt(v), sqrt(v))``."""
    return min(kk_mass(v), winding_mass(v))


def geodesic_distance(v, v0) -> float:
    """Geodesic distance in the Kaehler-moduli direction from volume ``v0`` to ``v``.

    The Kaehler metric on the T^6 volume direction is ``ds = dv/(2v)``, so the
    geodesic distance is ``(1/2) log(v/v0)``.
    """
    return float(0.5 * np.log(v / v0))


@dataclass(frozen=True)
class T6Background:
    """A T^6 = (T^2)^3 flux compactification — the oracle's genotype.

    ``F``, ``H`` are the 8 integer RR / NSNS 3-form fluxes. ``tau0`` is the
    axio-dilaton, ``tau1..tau3`` the three T^2 complex structures.
    """

    F: tuple[int, ...]
    H: tuple[int, ...]
    tau0: complex = 1j
    tau1: complex = 1j
    tau2: complex = 1j
    tau3: complex = 1j

    def __post_init__(self):
        if len(self.F) != 8 or len(self.H) != 8:
            raise ValueError("T^6 flux has 8 RR and 8 NSNS components (b3 = 8)")


def exact_t6_oracle(background: T6Background) -> dict[str, float]:
    """Exact observables for a T^6 background — zero error by construction.

    Satisfies the ``Oracle`` protocol: maps a genotype to a dict of log-space
    observable values. Every entry is a closed form, so the oracle's systematic
    error is identically zero and its error model is trivially calibrated.
    """
    w = superpotential(background.F, background.H, background.tau0,
                       background.tau1, background.tau2, background.tau3)
    return {
        "log_W0": float(np.log(abs(w))),
        "log_gs": float(np.log(gauge_coupling(background.tau0))),
        "tadpole": float(tadpole(background.F, background.H)),
        "kahler_potential": kahler_potential(background.tau1,
                                             background.tau2, background.tau3),
    }


def zero_error_model(validated: bool = True) -> ErrorModel:
    """The exact T^6 oracle's error model: zero bias, zero scale, zero tail."""
    return ErrorModel(
        bias=0.0,
        scale=0.0,
        beta=0.0,
        delta_beta=0.0,
        kind=Kind.INTERVAL,
        validated=validated,
    )


__all__ = [
    "SIGMA_2",
    "symplectic_form",
    "period_vector",
    "kahler_potential",
    "kahler_metric",
    "tadpole",
    "superpotential",
    "gauge_coupling",
    "kk_mass",
    "winding_mass",
    "tower_mass",
    "geodesic_distance",
    "T6Background",
    "exact_t6_oracle",
    "zero_error_model",
]
