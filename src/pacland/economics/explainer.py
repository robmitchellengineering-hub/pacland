"""Economics explainer content — generated from live data, not hand-written prose.

``content()`` pulls the real numbers from the economics modules (deficit, guard-suite),
so the PDF is always current when the numbers change.
"""
from __future__ import annotations

from .deficit import economics_deficit_report


def content() -> list[tuple[str, str]]:
    ret, pro = economics_deficit_report()
    return [
        ("title", "PACLAND · Economics"),
        ("subtitle", "The verification discipline applied to macroeconomics — a plain-English brief"),
        ("h", "The headlines — and what to do about each"),
        ("headline", f"A policy forecast is extrapolation, not verification ({pro.n_validation} of {pro.n_observables} targets measured) — treat any central-bank projection as a scenario, not a certified outcome."),
        ("headline", f"Only {ret.n_validation} of {ret.n_observables} backcast series are validated — spend on out-of-sample evaluation, not on more in-sample fit."),
        ("headline", "The field's own record: structural models fail to beat a random walk out of sample — rule out before you predict."),
        ("headline", "Trust by accounting, not by confidence band — a model that breaks a national-accounts identity is wrong by construction, no data needed."),
        ("h", "1 · What we are measuring"),
        ("p", "Macroeconomics is a search over a high-dimensional, non-stationary, ever-shifting economy with scarce ground truth: the future is never observed. The discipline asks how much of a forecasting or policy decision is verified, versus extrapolated."),
        ("h", "2 · The oracle and the Rule of Three"),
        ("b", "Oracle: accounting consistency — double-entry identities hold by construction. Income equals expenditure equals output; every financial asset is someone's liability. A 'model' that breaks an identity is not a model; consistency is an always-true answer."),
        ("b", "Rule of Three: three independent ledgers a model must all close — the circular flow (income ≡ expenditure ≡ output), the sectoral balances ((S−I)+(T−G)+(M−X)=0), and stock-flow consistency (Δstock = flow)."),
        ("h", "3 · The verification deficit"),
        ("b", f"{ret.n_validation} of {ret.n_observables} backcast series are measured + computable + validated — a certificate radius of {ret.radius:.0%}."),
        ("b", f"{pro.n_validation} of {pro.n_observables} forecast targets are validated — the projection central banks act on is extrapolation, not verification."),
        ("h", "4 · The accounting guard-suite"),
        ("b", "5 guards, each mutation-tested: circular flow, sectoral balances, stock-flow consistency, the budget constraint, non-negative prices."),
        ("p", "The field has run these identities for a century — national accounts, double-entry, Godley–Lavoie stock-flow consistency — as bookkeeping. The guard-suite wraps them as a pass/fail test a model must pass, with a seeded fault proving each guard fires."),
        ("h", "5 · Why it matters"),
        ("p", "Meese–Rogoff (1983) found structural exchange-rate models fail to beat a random walk out of sample, and Rossi's (2013) survey confirms it; DSGE models forecast no better than simple VARs (Gürkaynak et al.). 'Verified' macro forecasts are, in large part, extrapolation — and the discipline makes that a machine-checked verdict."),
        ("h", "6 · Reproduce"),
        ("p", "pacland economics · docs/economics-verification-deficit.md"),
    ]


__all__ = ["content"]
