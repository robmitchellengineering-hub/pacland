"""Companion theorem explainers for the Yang–Mills mass-gap tower.

Each theorem is explained in plain English — what it *says*, what it *means*, and
why it *matters* — so a mathematician who did not watch the proof happen can read
it back and see what the machine actually did. ``content()`` returns the
``(kind, text)`` tuples the shared ``explainer.render`` turns into the A4 PDF.

This is the theorem-level companion to ``docs/METHODOLOGY-DISCOVERIES.md`` (the
discovery-level catalog).
"""
from __future__ import annotations


def content() -> list[tuple[str, str]]:
    return [
        ("title", "The mass gap — companion theorem explainers"),
        ("subtitle", "Each theorem the tower proves, in plain English: what it says, what it means, why it matters."),

        ("h", "The spine — one chain of implications"),
        ("p", "The whole reduction is a single chain. Each step below is one theorem; reading them in order is reading the proof as a story, not a list."),

        ("h", "1 · Clustering <-> spectral gap  (MassGapDiamond.lean, proved)"),
        ("p", "What it says: exponential decay of the two-point function is exactly the statement that the transfer operator's second eigenvalue is strictly below its first."),
        ("p", "What it means: the mass gap is not a separate thing to hunt for — it *is* the spectral gap m = −log(λ₁/λ₀). 'Is there a gap' becomes 'where is this eigenvalue'."),
        ("b", "Why it matters: it is the universal container. Every later estimate is a bound on this one eigenvalue, so all routes are forced to talk about the same number."),

        ("h", "2 · The chessboard estimate (proved)"),
        ("p", "What it says: reflection positivity turns the two-point function into a norm, so the correlation is bounded by a sum over lattice domains with a geometric weight."),
        ("p", "What it means: positivity is not a soft condition — it gives a concrete, computable upper bound on correlations."),
        ("b", "Why it matters: it is the bridge from 'the measure is reflection-positive' to 'the correlation decays', the step that makes positivity pay."),

        ("h", "3 · Contraction rate = the gap (proved)"),
        ("p", "What it says: the transfer operator's iteration contracts at the rate e^(−m), where m is the gap; the contraction rate and the gap are the same number."),
        ("p", "What it means: one computation — the contraction rate — gives both 'it converges' and 'how fast', which is the gap."),
        ("b", "Why it matters: it lets the block-spin / decimation argument speak the language of spectral gaps, the common currency of the whole tower."),

        ("h", "4 · Strict contraction => positive gap (proved)"),
        ("p", "What it says: if the transfer operator is a strict contraction on the orthogonal complement of the top state, the gap is strictly positive."),
        ("p", "What it means: a finite-volume gap is not asserted — it follows from a contraction that can be checked."),
        ("b", "Why it matters: this is the *finite-volume* gap, the result that then has to survive the volume limit (the open rung below)."),

        ("h", "5 · The animal→uniform-cluster bridge (AnimalsBound.lean, in proof)"),
        ("p", "What it says: the number of connected clusters of size n is bounded by |V|·(2n)·(Δ+1)^(2(n−1)), and this size-class summability is what closes the single-cluster expansion into a volume-uniform cluster bound."),
        ("p", "What it means: counting connected subgraphs reduces to counting rooted spanning trees (each has an Euler tour of length 2(n−1), each step ≤ Δ choices). The combinatorics is the walks count."),
        ("b", "Why it matters: it is the current frontier — the step that turns a single-cluster expansion into the uniform bound that carries the gap."),

        ("h", "6 · The heat-kernel determinant scale (HeatKernel.lean, proved)"),
        ("p", "What it says: the weak-coupling exponent c in m ≥ A·e^(−cβ) is derived from the beta function — det P = e^(−Tr log P), a₂ ∝ b₀, Tr log P = c·β."),
        ("p", "What it means: c is not fitted to data; it is a consequence of the one-loop determinant. A fitted c is a free lunch; a derived c is a theorem."),
        ("b", "Why it matters: it converts 'the running coupling' from a heuristic into the exponent the bound actually needs, kernel-checked."),

        ("h", "7 · Trace is the fundamental character (GaussianRigidity.lean, proved)"),
        ("p", "What it says: on the torus g = diag(e^(iθ), e^(−iθ)), Tr g = 2·cos θ = sin(2θ)/sin θ — the SU(2) trace *is* the spin-1/2 character."),
        ("p", "What it means: the trace observable decomposes per-character (Peter–Weyl), so a bound on the trace reduces to the per-character case."),
        ("b", "Why it matters: it is the first rigidity lemma for Gaussian domination — the observable has a canonical character decomposition, so the comparison is well-defined."),

        ("h", "8 · Gauge-invariance rigidity → the covariant Laplacian (STATED, the open rung)"),
        ("p", "What it says: the Gaussian covariance of a gauge theory is forced by gauge invariance to be the covariant kinetic operator K = −∇·D (the transverse condition p^μ K_{μν} = 0)."),
        ("p", "What it means: 'the covariance is Gaussian' collapses to 'the covariance is −∇·D' — there is essentially one quadratic form compatible with gauge invariance."),
        ("b", "Why it matters: THIS is the single open rung. Proving the physical YM measure has this covariance is what turns Gaussian domination into the volume-uniform gap."),
        ("headline", "Status: theorems 1–7 are kernel-checked (no sorry). Theorem 8 is the open obligation — the one statement the whole reduction now waits on."),
    ]
