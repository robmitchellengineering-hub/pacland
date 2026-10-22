"""Drug-discovery explainer content — generated from live data, not hand-written prose.

``content()`` pulls the real numbers from the drug modules (deficit, guard-suite),
so the PDF is always current when the numbers change.
"""
from __future__ import annotations

from .deficit import drug_deficit_report


def content() -> list[tuple[str, str]]:
    ret, pro = drug_deficit_report()
    return [
        ("title", "PACLAND · Drug discovery"),
        ("subtitle", "The verification discipline applied to computational drug discovery — a plain-English brief"),
        ("h", "The headlines — and what to do about each"),
        ("headline", f"A novel molecule is extrapolation, not verification ({pro.n_validation} of {pro.n_observables} endpoints measured) — assay it before you bet, don't trust the in-silico score."),
        ("headline", f"Only {ret.n_validation} of {ret.n_observables} benchmark endpoints are validated — spend on assay data, not on more ML."),
        ("headline", "The field's own census: 52% of 'verified' hits fail REOS, 18% are PAINS — rule out before you rank."),
        ("headline", "Trust by verdict, not by confidence score — pLDDT is not calibrated."),
        ("h", "1 · What we are measuring"),
        ("p", "Drug discovery is a search over chemical space (~10⁶⁰ molecules) with scarce ground truth: an assay exists only for the molecules you have already tested. The discipline asks how much of a screening decision is verified, versus predicted."),
        ("h", "2 · The oracle and the Rule of Three"),
        ("b", "Oracle: chemical validity — a molecule must be valency/charge/tautomer-consistent (RDKit sanitisation). A 'molecule' with a pentavalent carbon is not a molecule; validity is an always-true answer."),
        ("b", "Rule of Three: three independent checks a candidate must all pass — validity, drug-likeness (Lipinski / PAINS / REOS), and synthesizability (RAScore)."),
        ("h", "3 · The verification deficit"),
        ("b", f"{ret.n_validation} of {ret.n_observables} benchmark endpoints are measured + computable + validated — a certificate radius of {ret.radius:.0%}."),
        ("b", f"{pro.n_validation} of {pro.n_observables} endpoints for a novel molecule are validated — the hit you would synthesize is extrapolation, not verification."),
        ("h", "4 · The constraint guard-suite"),
        ("b", "4 guards, each mutation-tested: net charge, valence bounds, Lipinski (rule of five), synthesizability."),
        ("p", "The field has run these 'forbidden-state' filters for 25 years — PAINS, REOS, Lipinski, RDKit sanitization — as boolean heuristics. The guard-suite wraps them as a pass/fail test a model must pass, with a seeded fault proving each guard fires."),
        ("h", "5 · Why it matters"),
        ("p", "The field's own 2013 census (Zhu et al.) found 52% of reported virtual-screening hits fail REOS and 18% are PAINS artifacts, and AlphaFold's confidence score (pLDDT) is not calibrated. 'Verified' hits are, in large part, artifacts — and the discipline makes that a machine-checked verdict."),
        ("h", "6 · Reproduce"),
        ("p", "pacland drugs · docs/drugs-verification-deficit.md"),
    ]


__all__ = ["content"]
