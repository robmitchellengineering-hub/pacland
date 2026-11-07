"""The theorem registry — the "yes/no catalog".

Each claim is data, not logic: a natural-language question, the asserted value, the oracle
class that checks it, the falsifier written *before* the run, the theorem that supplies the
verdict, and the verdict itself.

The 21 ids, oracle classes, falsifiers, remedies and verdicts mirror ``morph-verify``'s
``CATALOG`` one-to-one (the Rust registry the Conductor consumes), so the two cannot drift.

Verdict alphabet (PLAN-sextant-proof-engine.md):
  FORCED     the value is fixed by the theory (a theorem / a bound)
  FREE       the value is not fixed (a free parameter, an open column)
  IMPOSSIBLE the thing cannot be done (a no-go)
"""
from __future__ import annotations

from dataclasses import dataclass

FORCED = "FORCED"
FREE = "FREE"
IMPOSSIBLE = "IMPOSSIBLE"


@dataclass(frozen=True)
class Claim:
    id: str
    question: str
    value: str
    oracle_class: str
    falsifier: str
    remedy: str
    verdict: str
    keywords: tuple[str, ...] = ()


CLAIMS: tuple[Claim, ...] = (
    Claim(
        id="bell-classical",
        question="What is the classical (local hidden-variable) CHSH bound?",
        value="2",
        oracle_class="quantum-simulated (Phantom) + kernel-checked (Lean)",
        falsifier="a classical strategy exceeding 2",
        remedy="QM.CHSH (Bell)",
        verdict=FORCED,
        keywords=("bell", "classical chsh", "local hidden-variable"),
    ),
    Claim(
        id="chsh",
        question="What is the maximum CHSH violation a quantum strategy can reach?",
        value="2*sqrt(2) ≈ 2.8284271",
        oracle_class="quantum-simulated (Phantom) + kernel-checked (Lean)",
        falsifier="a state exceeding 2√2",
        remedy="QM.Tsirelson",
        verdict=FORCED,
        keywords=("chsh", "tsirelson"),
    ),
    Claim(
        id="no-cloning",
        question="Can an arbitrary unknown quantum state be cloned?",
        value="no",
        oracle_class="kernel-checked (Lean)",
        falsifier="a universal cloner",
        remedy="QM.NoCloning",
        verdict=IMPOSSIBLE,
        keywords=("clone", "cloning", "no-cloning"),
    ),
    Claim(
        id="no-broadcasting",
        question="Can an arbitrary mixed state be broadcast?",
        value="no",
        oracle_class="kernel-checked (Lean)",
        falsifier="a linear broadcasting map",
        remedy="QM.NoBroadcasting",
        verdict=IMPOSSIBLE,
        keywords=("broadcast",),
    ),
    Claim(
        id="locc-no-entanglement",
        question="Can a classical (LOCC) channel create entanglement?",
        value="no",
        oracle_class="kernel-checked (Lean)",
        falsifier="a classical channel entangling two systems",
        remedy="QM.Entanglement",
        verdict=IMPOSSIBLE,
        keywords=("locc", "create entanglement"),
    ),
    Claim(
        id="born-rule",
        question="Is the Born rule the unique non-contextual probability rule?",
        value="yes (Gleason)",
        oracle_class="kernel-checked (Lean)",
        falsifier="a second non-contextual probability rule",
        remedy="Gleason",
        verdict=FORCED,
        keywords=("born", "gleason", "probability rule"),
    ),
    Claim(
        id="pbr",
        question="Can distinct pure states share a ψ-epistemic ontic overlap?",
        value="no",
        oracle_class="kernel-checked (Lean)",
        falsifier="two distinct states with overlapping ontic support",
        remedy="QM.PBR",
        verdict=FORCED,
        keywords=("pbr", "ontic", "epistemic"),
    ),
    Claim(
        id="mermin",
        question="Does a non-contextual ±1 assignment to the Mermin square exist?",
        value="no",
        oracle_class="quantum-simulated (Phantom) + kernel-checked (Lean)",
        falsifier="a non-contextual ±1 assignment",
        remedy="QM.Mermin",
        verdict=IMPOSSIBLE,
        keywords=("mermin", "contextual"),
    ),
    Claim(
        id="clifford-polynomial",
        question="Are Clifford/stabilizer circuits classically simulable in polynomial time?",
        value="yes",
        oracle_class="quantum-simulated (Phantom/Stim) + kernel-checked (Lean)",
        falsifier="a T-gate circuit blowing past 2^n",
        remedy="QM.Stabilizer",
        verdict=FORCED,
        keywords=("clifford", "stabilizer", "simulable"),
    ),
    Claim(
        id="entanglement-area",
        question="Is entanglement across a cut bounded by the cut area?",
        value="yes (D^m)",
        oracle_class="quantum-simulated (Phantom/Quimb) + kernel-checked (Lean)",
        falsifier="entanglement exceeding D^m",
        remedy="QM.MERA",
        verdict=FORCED,
        keywords=("area", "mera", "entanglement entropy"),
    ),
    Claim(
        id="coupling-free",
        question="Is the gravitational coupling G derived?",
        value="no (free)",
        oracle_class="kernel-checked (Lean)",
        falsifier="a derivation of G from the forced halves",
        remedy="Gravity.QG.coupling_free",
        verdict=FREE,
        keywords=("coupling", "gravitational coupling"),
    ),
    Claim(
        id="gravity-quantum",
        question="Must the gravitational coupling be quantum, not classical?",
        value="yes",
        oracle_class="kernel-checked (Lean)",
        falsifier="a consistent classical (LOCC) coupling",
        remedy="QM.Entanglement + QM.NoCloning + Gleason",
        verdict=FORCED,
        keywords=("gravity quantum", "quantum gravity"),
    ),
    Claim(
        id="lovelock",
        question="Is the Einstein equation the unique divergence-free 2-tensor theory in 4D?",
        value="yes",
        oracle_class="kernel-checked (Lean)",
        falsifier="a second divergence-free gravity theory",
        remedy="Gravity.Lovelock",
        verdict=FORCED,
        keywords=("lovelock", "einstein", "unique gravity"),
    ),
    Claim(
        id="bianchi",
        question="Is the Einstein tensor divergence-free?",
        value="yes (∇·G = 0)",
        oracle_class="kernel-checked (Lean)",
        falsifier="a metric with ∇·G ≠ 0",
        remedy="Gravity.QG.einstein_divergence_free",
        verdict=FORCED,
        keywords=("bianchi", "divergence-free"),
    ),
    Claim(
        id="wdw",
        question="Do physical states satisfy the Wheeler–DeWitt equation Ĥ|ψ⟩ = 0?",
        value="yes",
        oracle_class="kernel-checked (Lean)",
        falsifier="a physical state not in ker Ĥ",
        remedy="Gravity.WheelerDeWitt",
        verdict=FORCED,
        keywords=("wheeler", "dewitt", "wdw"),
    ),
    Claim(
        id="dirac",
        question="Do the ADM constraints close under the Dirac algebra?",
        value="yes",
        oracle_class="kernel-checked (Lean)",
        falsifier="a constraint algebra that fails to close",
        remedy="Gravity.Dirac",
        verdict=FORCED,
        keywords=("dirac", "constraint algebra"),
    ),
    Claim(
        id="adm",
        question="Is QG's forced content the ADM constraint system {Ĥ = G·ππ − R, Ĥa = ∇·π}?",
        value="yes",
        oracle_class="kernel-checked (Lean)",
        falsifier="a third independent constraint",
        remedy="Gravity.ADMConstraints",
        verdict=FORCED,
        keywords=("adm",),
    ),
    Claim(
        id="hypercharge-uniqueness",
        question="Do the SM anomaly conditions fix the hypercharges uniquely?",
        value="yes, up to normalisation and u↔d swap",
        oracle_class="kernel-checked (Lean)",
        falsifier="a second anomaly-free hypercharge assignment",
        remedy="SM.Hypercharge",
        verdict=FORCED,
        keywords=("hypercharge",),
    ),
    Claim(
        id="anomaly-cancellation",
        question="Do the SM's five anomaly coefficients vanish?",
        value="yes",
        oracle_class="kernel-checked (Lean)",
        falsifier="a nonzero anomaly coefficient",
        remedy="SM.Anomaly",
        verdict=FORCED,
        keywords=("anomaly",),
    ),
    Claim(
        id="generation-free",
        question="Is the generation number N_gen fixed by anomaly cancellation?",
        value="no (free)",
        oracle_class="kernel-checked (Lean)",
        falsifier="an anomaly condition fixing N_gen",
        remedy="SM.Generation",
        verdict=FREE,
        keywords=("generation", "n_gen"),
    ),
    Claim(
        id="the-19",
        question="How many free parameters does the Standard Model have?",
        value="19 (the orbit-space dimension)",
        oracle_class="kernel-checked (Lean) + exact-symbolic",
        falsifier="a relation collapsing more than 2 of the 19 correctly",
        remedy="SM.ParameterCount",
        verdict=FREE,
        keywords=("free parameters", "parameter count", "the 19"),
    ),
)
