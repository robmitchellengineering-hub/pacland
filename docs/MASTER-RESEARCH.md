# SEXTANT — Master Research Document

The single source of truth for the mass-gap program. It states the **one metric**, names the **exact
assumptions still doing the heavy lifting**, separates the **four competing tracks**, gives each an
**objective and a falsification criterion**, connects each into the **discovery engine**, and defines a
**measurable definition of progress**.

---

## 0. The one metric

> **How much closer are we to deriving a new, rigorous, volume-uniform lower bound for the physical
> Yang–Mills spectral gap?**

We do **not** measure progress by Lean-theorem count, commit count, or hypothesis count. The single
result that matters is a lower bound `m(β) ≥ c(β) > 0` that is **uniform in volume and coupling** and
survives the continuum limit, reaching `A·e^(−(12π²/11)β)`.

---

## 1. The heavy-lifting assumptions (what is still unproven)

Five assumptions remain, and each track bets on a *different* one. They are the things that, if proven,
carry the whole result; if any fails, its track fails.

| id | the assumption | what it buys |
|---|---|---|
| A1 | **volume-uniformity** — the bound holds uniformly as `V → ∞` | the thermodynamic limit |
| A2 | **β-uniformity** — the bound holds at every coupling, not just strong or weak | no ceiling / no gap breakdown |
| A3 | **continuum survival** — the lattice bound transfers as `a → 0` | the continuum theory |
| A4 | **spectral positivity** — `m > 0`, not merely "the operator is bounded" | the mass gap itself |
| A5 | **non-perturbativity** — the bound is not a truncated expansion | a genuine, not perturbative, statement |

A track "does the heavy lifting" precisely when it is the one that must deliver A1–A5. The referee
today checks A2 and A4 partially; **A1 and A3 are unchecked** — that is the missing uniformity.

---

## 2. The four competing tracks

Each track is a *competing research programme*. SEXTANT's job is to run all four and identify which one
produces the first genuinely new result.

### Track 1 — Gribov (gauge-orbit geometry)

- **Heavy-lifting assumption it must prove:** restricting to the first Gribov region (the horizon)
  removes the gauge flat directions *and* the horizon's geometry transfers to a positive spectral gap
  (A4, A5).
- **Objective:** a volume-uniform, non-perturbative lower bound on the spectral gap from the
  Gribov–Zwanziger horizon.
- **Falsification:** a gauge-orbit quotient that fails to remove the flat directions — a **residual
  Gribov copy** — or a horizon that does not yield `m > 0`.
- **In the repo:** the gauge-orbit quotient setup (`GaugeOrbit.lean`, the `sextant.py` falsifier
  "a quotient that fails to remove the gauge flat directions (a residual Gribov copy)").

### Track 2 — Coulomb (confinement + string tension)

- **Heavy-lifting assumption it must prove:** the Coulomb string tension σ(β) is bounded below,
  uniformly in β and volume, so `m = 3.2·√σ` gives the spectral gap (A1, A3, A4).
- **Objective:** a *proved* (not Monte-Carlo) lower bound on σ(β), uniform in β and volume, with a
  spectral estimate connecting it to the mass gap.
- **Falsification:** a Wilson loop that violates the area law, or σ(β) → 0 at weak coupling (the
  U(1) Coulomb phase is exactly this — it deconfines).
- **In the repo:** `lattice_ym_su2.py` (Creutz ratio), `lattice_ym_su3.py`,
  `mass_gap_falsifiers.py` (d5, bulk-transition, universality, large-N ratio, polyakov); the honest
  record already shows the *Abelian* Coulomb phase fails — only the non-Abelian survives.

### Track 3 — RG (multiscale Polchinski / functional RG)

- **Heavy-lifting assumption it must prove:** the curvature of the effective action's Hessian is
  **uniformly bounded along the flow** — the effective interactions stay controlled at every scale
  (A1, A3, A5).
- **Objective:** a uniform (scale-independent) bound on the RG flow's curvature that yields a
  scale-uniform mass-gap bound.
- **Falsification:** a flow (or truncation) where the curvature diverges — the effective couplings run
  away, so the bound does not survive the limit.
- **In the repo:** `energy/frg.py` (Carrier A rung 1), `energy/frg_poly.py` (rung 2), `energy/lattice.py`,
  `energy/referee.py` — the FRG solver + the honest "what the truncation reproduces and what it cannot."

### Track 4 — Curvature / functional inequalities (survive scaling)

- **Heavy-lifting assumption it must prove:** "negative curvature on a *measure-negligible* set +
  Lyapunov drift ⇒ positive spectral gap," **β-uniform** (A2, A4, A5).
- **Objective:** a weighted spectral / nonlinear functional inequality (Wang's criterion, a weighted
  Poincaré/log-Sobolev) that is β-uniform and reaches the asymptotic-freedom scale.
- **Falsification:** a full-lattice configuration where the curvature stays negative on a
  measure-non-negligible set.
- **In the repo:** the kernel-checked SU(2) Bakry-Émery ceiling (`curvature 1/4 + 2β·cosθ`,
  `Su2Curvature.lean`); Wang's criterion is named but not yet formalized (`hypotheses.py`).

---

## 3. The engine connection

Each track is a **hypothesis + a runnable falsifier** in the registry, not prose:

- the hypothesis is a candidate bound `c(β)` (or a candidate statement of A1–A5);
- `bound_search.check_bound` tests it against the referee (R1 positivity, R2 β-uniformity, R5 scale);
- **after** extending the referee, R3 (volume-uniformity) and R4 (continuum survival) are checked too;
- `registry.record_claim` records survive-or-fail, so a track that fails a falsification is a recorded
  dead direction, and a track that advances is a recorded result.

`lean_scrape.harvest_mathlib` feeds each track the proven lemmas it needs (contraction, martingale,
decay, spectral); `synthesis_bounds` combines them — but the upgrade in §5 must make synthesis search
*combinations of structures*, not just products of existing bounds.

---

## 4. The measurable definition of progress

Progress on a track is measured by **how many of A1–A5 its best candidate bound currently satisfies** —
and specifically whether it has cleared the two unchecked ones (A1 volume-uniformity, A3 continuum
survival).

```
track score = count of {A1..A5} satisfied by the track's best candidate bound
```

- A bound that is positive on the lattice but not volume-uniform: **2/5** (A2 + A4 only) — not yet the result.
- A bound that is positive, β-uniform, *and* volume-uniform: **3/5** — a genuine advance.
- A bound satisfying all five and reaching the scale: **the result**.

This number — not the theorem count, not the commit count — is the KPI. Every track reports its score,
and the first to reach 5/5 (or the closest to it) is the one SEXTANT identifies as producing the first
genuinely new result.

---

## 5. The transition

The machinery is built and merged. The next phase is to **run the four tracks as competing programmes**
and let the engine arbitrate. The honest gate stands: before confidence, the engine must pass a
**withheld, independent** problem where it induces a candidate and the falsifier verifies it.

The move is: **stop building; start deriving.** Pick the track whose heavy-lifting assumption is most
likely to be provable (Coulomb or RG are the two with the most machinery already behind them), derive
its A1/A3 assumptions, and let the referee tell us whether it clears the missing uniformity.
