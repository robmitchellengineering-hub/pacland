"""Catalog of known ultraviolet completions of the Standard Model, with the exact
relations each imposes on the 19 parameters and the resulting collapse count.

Machine 3, Phase 1: replaces the unprovable negative "no UV completion derives the
19 correctly" with an exhaustive, falsifiable catalog plus a verified deficit.

The 19 = 6 quark masses + 3 CKM angles + 1 CP phase + 3 charged-lepton masses
        + 3 gauge couplings + 2 Higgs parameters + theta_QCD.

Collapse arithmetic (from the adversarial pass, cross-checked against the
literature):
  * gauge unification: 3 gauge couplings -> 1, a collapse of 2;
  * down-lepton unification (Y_e = Y_d^T): a 3x3 MATRIX identity, i.e. three
    eigenvalue relations m_e=m_d, m_mu=m_s, m_tau=m_b, a collapse of 3;
  * full Yukawa unification (Y_u = Y_d = Y_e): 9 masses -> 3, a collapse of 6,
    plus V_CKM = 1, a collapse of 4 (3 angles + 1 phase);
  * MSSM Higgs quartic lambda = (g^2 + g'^2)/8 is not free: a collapse of 1.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Completion:
    name: str
    gauge_unified: bool          # one gauge group (collapses 3 -> 1, i.e. -2)
    down_lepton_unified: bool    # Y_e = Y_d^T (three mass relations)
    full_yukawa_unified: bool    # Y_u = Y_d = Y_e (six mass relations + CKM = 1)
    susy: bool                   # MSSM Higgs quartic not free (one relation)
    note: str = ""

    def collapse_count(self) -> int:
        """The number of the 19 that this completion collapses via exact,
        derivable relations (whether or not those relations are numerically correct)."""
        c = 0
        if self.gauge_unified:
            c += 2                       # 3 gauge couplings -> 1
        if self.full_yukawa_unified:
            c += 6 + 4                   # 9 masses -> 3 (6) and V_CKM = 1 (4)
        elif self.down_lepton_unified:
            c += 3                       # three eigenvalue relations
        if self.susy:
            c += 1                       # Higgs quartic tied to the gauge couplings
        return c

    def numerically_correct(self) -> int:
        """How many of the collapsed relations survive data to experimental
        precision. Only gauge-coupling unification does; the Yukawa relations are
        wrong by O(10-30%) and V_CKM = 1 is badly wrong; the MSSM quartic is
        excluded by m_h > M_Z."""
        return 2 if self.gauge_unified else 0


CATALOG: list[Completion] = [
    Completion("Standard Model", False, False, False, False),
    Completion("Minimal SU(5)", True, True, False, False),
    Completion("Minimal SO(10)", True, False, True, False),
    Completion("Minimal E6", True, False, True, False),
    Completion("Minimal Pati-Salam", True, False, True, False),
    Completion("Minimal trinification SU(3)^3", True, False, True, False),
    Completion("Flipped SU(5)", True, False, False, False,
               note="Y_e = Y_d^T is broken by the flipped embedding"),
    Completion("Realistic multi-Higgs SO(10)/E6/PS", True, False, False, False,
               note="flavor relations destroyed by the extra Higgs"),
    Completion("MSSM", False, False, False, True),
    Completion("SUSY SU(5)", True, True, False, True),
    Completion("SUSY minimal SO(10)", True, False, True, True),
    Completion("Warped RS / composite / Froggatt-Nielsen / texture zeros",
               False, False, False, False,
               note="re-parametrizations or ansaetze, no exact relation"),
]


def deficit() -> str:
    """The verified deficit: the maximum number of the 19 that any known
    completion derives *numerically correctly*."""
    best = max(c.numerically_correct() for c in CATALOG)
    n = len(CATALOG)
    return (
        f"of {n} catalogued completions, none derives more than {best} of the 19 "
        f"correctly; that survivor is gauge-coupling unification."
    )
