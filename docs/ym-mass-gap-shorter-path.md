# Yang-Mills mass gap — the shorter path (3-way research fan-out, 2026-11)

Synthesis of three parallel literature probes. Replaces the "M3 = reconstruct Balaban's multiscale RG"
step in `ym-mass-gap-plan.md` with a shorter, tractable route.

## The three probes, one line each

1. **Confinement / area law** — NOT a shortcut. No proven "area law ⇒ mass gap" (the converse is false:
   the Higgs phase has a gap + perimeter law). G₂ gauge theory confines without center symmetry
   (Holland–Pepe–Wiese 2003), so center ⇔ confinement is clean only at finite T, not for the area law.
   Equal difficulty, parallel paths.
2. **Monotonicity / comparison** — dead end. The string tension is monotone *non-increasing* in β (Ginibre
   2nd inequality), so the strong-coupling gap is an *upper* bound, never a lower bound at weak coupling.
   The 2D `g²C₂` is dimensionally incompatible with d≥3. The one lever: Tomboulis–Yaffe/Kanazawa
   "boundary/vortex-insensitivity ⇒ string tension" criterion + the *proven* volume-monotonicity direction.
3. **Shortest approaches** — the winner is the **lattice Langevin + Bakry–Émery (stochastic quantization)
   route**: Shen–Zhu–Zhu, CMP 400:805 (2023) [arXiv:2204.12737] proves a strictly positive mass gap for
   SU(N)/SO(N) lattice YM in any d>1 **at strong coupling**; Nissim [arXiv:2510.22788] + Cao–Nissim–Sheffield
   [arXiv:2509.04688] extend to U(N) / the 't Hooft (large-N) regime + the area law.

## The better attack

**Swap** the "M3 = Balaban multiscale RG" step for:

- **M3′ — formalize the SZZ spectral gap.** The mass gap = the spectral gap of the lattice Langevin
  generator (a Poincaré/log-Sobolev inequality via the Bakry–Émery Γ₂-calculus). Finite-dimensional,
  Lie-theoretic calculus (Ricci lower bound of the bi-invariant SU(N) metric + the Bochner formula +
  spectral-gap ⇒ exponential clustering) — exactly what a proof assistant handles well.
- **Bridges (already proven, formalizable):** Durhuus–Fröhlich 1980 (mass gap ⇒ area law) +
  Chatterjee 2021 (confinement ⇔ center symmetry, "exponential correlation decay ⇒ confinement").

## The honest boundary (the real open step)

The Bakry–Émery curvature `Ric − β·Hess(action)` turns **negative at large β** — the *same ceiling* as the
Dobrushin bound (α=1). **No known approach crosses it; a weak-coupling d≥3 lower bound does not exist in any
literature.** The open endgame, stated precisely:

> **Can a β-dependent spectral-gap bound with the correct `e^{−cβ}` (asymptotic-freedom) scaling be proven
> past the curvature ceiling, and if not, what exactly fails?**

That is the Clay problem reduced to one precise statement — the hypothesis engine's target.

## Sources (verified URLs)

- Shen–Zhu–Zhu 2023 (CMP 400): https://arxiv.org/abs/2204.12737
- Nissim 2025 (U(N) + large-N): https://arxiv.org/abs/2510.22788
- Cao–Nissim–Sheffield 2025 (mass gap ⇒ area law): https://arxiv.org/abs/2509.04688 ; https://arxiv.org/abs/2505.16585
- Durhuus–Fröhlich 1980 (mass gap ⇒ area law): CMP 75:103, https://inspirehep.net/api/literature/158755
- Chatterjee 2021 (confinement ⇔ center): https://arxiv.org/abs/2006.16229 ; survey https://arxiv.org/abs/1803.01950
- Tomboulis–Yaffe 1985: https://projecteuclid.org/euclid.cmp/1103942420 ; Kanazawa (SU(N)): https://arxiv.org/abs/0808.3442
- Holland–Pepe–Wiese 2003 (G₂ confinement, no center): https://www.sciencedirect.com/science/article/abs/pii/S0550321303005716
- Göpfert–Mack 1982 (3D U(1) all couplings, monopole mechanism): https://projecteuclid.org/euclid.cmp/1103920658

## Caveat

Web search surfaces many 2024–2026 non-peer-reviewed "solution" preprints (Zenodo etc.) claiming a
weak-coupling d=4 mass gap. ALL are unverified and excluded. The Clay problem remains officially open.
