# Prior art and tooling — what to build on

Existing public work that shortens the path. Each entry maps to a PACLAND layer
(`docs/architecture.md`) and says whether it is *directly integrable* (a library
with a pip install) or *background* (methodology / results to cite and learn from,
not code to import). URLs are the ones verified in research on 2026-10-18.

---

## Directly integrable software (the oracle stack, L1 + L2)

### CYTools — Calabi-Yau topology, cohomology, flux vacua
- **Repo:** https://github.com/LiamMcAllisterGroup/cytools
- **Paper:** [CYTools: A Software Package for Analyzing Calabi-Yau Manifolds](https://arxiv.org/abs/2211.03823)
- **What it does:** builds a polytope → triangulation pipeline; computes Hodge
  numbers `h^{1,1}`, `h^{2,1}`, triple intersection numbers, line-bundle
  cohomology, and searches for flux vacua.
- **Maps to:** L1 encoding (topology data) and L2 stages 2–4 (cohomology, flux
  enumeration). This is the single highest-value integration — it provides the
  *discrete* half of the genotype almost for free.
- **License:** GPL-3.0 (copyleft). Fine for *generating data*; imposes GPL
  obligations only if PACLAND itself is distributed *linked against* CYTools.
- **Adapter:** `src/pacland/oracle/adapters.py::CyToolsAdapter`

### cymetric — neural Calabi-Yau metrics
- **Repo:** https://github.com/kitft/cymetric
- **Paper:** Larfors et al., *Learning the Size and Shape of Calabi-Yau Manifolds*
- **What it does:** trains a neural network ansatz for the Ricci-flat metric on a
  CY, via the Donaldson / Monge-Ampère loss.
- **Maps to:** L2 stage 1 (the metric solve) — the hardest *computable* stage.
- **Adapter:** `src/pacland/oracle/adapters.py::CymetricAdapter`

### cohomCalg — line-bundle cohomology
- **Paper:** Blumenhagen, Jurke, Rahn, Roschy, *Cohomology of Line Bundles: A
  Computational Algorithm* (2010), arXiv:1003.5217
- **What it does:** exact computation of line-bundle cohomology on toric
  varieties — the standard tool for the massless spectrum.
- **Maps to:** L2 stage 5 (spectrum / EFT extraction).

### Kreuzer–Skarke database — the CY census
- **Paper:** Kreuzer & Skarke, *Complete classification of reflexive polyhedra in
  four dimensions*, Adv. Theor. Math. Phys. 4 (2000), arXiv:hep-th/0002240
- **What it does:** the list of 473,800,776 reflexive 4d polyhedra — the raw input
  space for L1 encoding.
- **Maps to:** L1 topology sourcing.

---

## Methodology and results (background — cite, don't import)

### Surveys
- Ruehle, *Data science applications to string theory*, Phys. Rep. 839 (2020) —
  [CERN record](https://cds.cern.ch/record/2709400). The canonical map of ML-for-
  strings; the best single place to see what has and has not been tried.

### ML for the landscape (the closest prior work to PACLAND's oracle)
- He, Krefl, Seong, *Machine-learning the string landscape*, Phys. Lett. B 774
  (2017) — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0370269317308365). Early neural surrogates over flux vacua. **Note the gap:**
  these are black-box surrogates with *no error model*, which is exactly what
  PACLAND's non-goal (no certificate, no claim) rules out.
- Ruehle, *Evolving neural networks with genetic algorithms to study the String
  Landscape*, [arXiv:1706.07024](https://arxiv.org/abs/1706.07024). Genetic search
  over the landscape — the closest thing to L4 (evolvability), but again without a
  verification guarantee.
- Douglas, *The statistics of string/M theory vacua*, JHEP 2003 — the statistical
  framing the landscape's `10^500` comes from.

### Neural metric line (the computational core of L2 stage 1)
- He, *Deep learning the geometry of Calabi-Yau manifolds* (2017) — started the
  neural-metric approach that cymetric implements.
- *Calabi-Yau metrics through Grassmannian learning and Donaldson's algorithm*,
  [arXiv:2410.11284](https://arxiv.org/abs/2410.11284) (Contemp. Math. 835, 2026) —
  current state of the art.

### Learning theory (already cited in ROADMAP, restated for the map)
- Valiant, *A Theory of the Learnable* (1984); *Evolvability* (2009); *Probably
  Approximately Correct* (2013); *The Importance of Being Educable* (2024).
- Feldman, *Evolvability from learning algorithms* (STOC 2008) and the complete
  characterization of statistical-query learning — the theorem that makes L4's
  gate (`evolvable ⇒ learnable`) precise.

---

## The integration gap this research surfaced

Every ML-for-the-landscape result above produces a **black-box surrogate**: a
function that predicts an observable from a compactification with no stated
uncertainty. None emit the one object PACLAND's certificate depends on — a
**calibrated per-observable error model** (`docs/oracle.md` §4).

That is not a coincidence to regret; it is the opening. The public tools
(CYTools, cymetric, cohomCalg) supply the *compute*, and PACLAND supplies the
*guarantee layer* on top of them: wrap them behind the `Oracle` protocol, attach
error models, calibrate against exact/measured points, and emit certificates. The
pieces exist; no one has wired them into a verification framework.

## What to integrate next (in order of leverage)

1. **CYTools adapter, made real** — install `cytools`, confirm the API in
   `CyToolsAdapter`, and generate the discrete half of the genotype for real CYs.
2. **cohomCalg adapter** — add the spectrum computation to L2 stage 5.
3. **cymetric adapter, made real** — wire the metric solve; this is the
   hard-compute step and the main source of the systematic error the framework
   must calibrate.
4. **The exact-background benchmark** — use `exact_toric_oracle` (build #2 seed)
   to validate the certificate loop before any approximate oracle is trusted.
