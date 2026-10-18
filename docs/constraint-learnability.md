# The constraint/observable split — the structure miner's answer

The first build of the new approach (`docs/new-approach.md` §"The first build") was
a non-linear structure miner whose fork was: *either* some observable carries the
flux's information (a fingerprint — positive), *or* the map is
information-theoretically empty (negative). This is the answer, measured on 107 real
SUSY flux vacua across two h¹²=2 models (`data/vacua_observables.json`).

## The measurement

For each flux-paired quantity, cross-validated ridge regression on the degree-2
monomial basis of the 12 flux coordinates (91 features) — the strongest joint test
the miner has (per-coordinate mutual information is blind to quadratic structure):

| quantity | role | ridge r (CV) | perm. z | verdict |
|---|---|---|---|---|
| tadpole N_flux | **constraint** | **+0.991** | **+9.09** | **LEARNABLE** |
| log W₀ | observable | +0.099 | — | not learnable |
| log g_s | observable | +0.210 | — | not learnable |
| gauge coupling 0 | observable | −0.155 | — | not learnable |
| gauge coupling 1 | observable | −0.126 | — | not learnable |
| gauge coupling 2 | observable | +0.166 | — | not learnable |

The permutation z-score is on the tadpole only (it is the claim that needs
significance); the dynamical observables sit at |r| < 0.22, indistinguishable from
the shuffle null, so no permutation test is needed to call them unlearnable.

## What this means

1. **The only learnable structure in the flux coordinates is the constraint.**
   The D3 tadpole N_flux is a *deterministic* quadratic form of the flux integers,
   and the miner recovers it essentially exactly (r = 0.991) — far above chance
   (z = +9.09).

2. **Every dynamical observable is information-theoretically empty in flux.**
   W₀ (the known case), g_s, *and the three gauge couplings* all fail to be
   predictable from flux. This closes the "maybe gauge couplings carry structure"
   hope that `new-approach.md` Q1 left open: in the flux coordinates they do not.

3. **The constraint map is PAC-learnable, hence evolvable.** The tadpole lives in
   the degree-2 class (VC dimension ~ 91), so by Valiant's theorem it is learnable
   and evolvable with sample complexity n ≥ ~10⁵ — finite and modest next to the
   10⁵⁰⁰ landscape. The dynamical map has no such finite class in flux.

## The honest reading (not overclaimed)

The tadpole's learnability is partly *by construction*: N_flux is *defined* as a
bilinear form of flux, so "a quadratic model recovers it" is expected. What is not
tautological is the **split**:

> **The information in the flux flows into the *constraints*, not into the
> low-energy observables.** The one learnable quantity is the one that rules vacua
> out (the tadpole bound); the quantities that would *select* a vacuum (W₀, g_s,
> gauge couplings) are statistically uniform in the flux that produced them.

This is the empirical foundation of "constraint-first": search is dead not merely
for W₀ but for the whole observable sector; the only thing the landscape lets you
*learn* is what it *forbids*.

## Q2 closes the loop: the constraints *compose*

The second pillar (verified constraint elimination) composes the same way. On the
same 107 vacua, the two phenomenological constraints combine to eliminate
**99.1%** of the landscape, against an independence-product benchmark of 98.2%:

| constraint | eliminates |
|---|---|
| weak coupling (g_s < 1) | 72.9% |
| small \|W₀\| < 1 | 93.5% |
| **intersection** | **99.1%** |
| certified interval (δ=0.05) | [87.2%, 100.0%] |

The interaction (joint − independent) is **+0.8%** — and it is **not significant**.
A permutation test over the 2×2 survival table gives **z = +0.74**, i.e. the
departure from independence is a *single vacuum*: under independence you expect
1.90 vacua to survive both constraints, and exactly **1** does. The constraints are
consistent with **perfect independence**, so the elimination compounds
multiplicatively and the composition adds no hidden overlap penalty.

`src/pacland/constraints.py::joint_elimination` computes the joint fraction, the
independence benchmark, the signed interaction, its permutation z-score and verdict
(`independent` / `redundant` / `complementary`), and a Hoeffding interval on the
joint fraction. Run it with `pacland constrain data/vacua_observables.json`.

The loop is now closed end-to-end: **Q1** says the learnable structure is the
constraint (tadpole r=0.99, observables random); **Q2** says the constraints are
independent and compose to eliminate ~99% with a certificate. Constraint-first is
no longer a preference — it is the only learnable structure *and* the only thing
that narrows the landscape.

## Limits (named)

- Scoped to the IIB flux corner, 107 vacua, two h¹²=2 models, 12 flux coordinates.
- "Gauge couplings not learnable" means *from flux*; they are functions of the
  Kähler moduli and may be learnable from those coordinates instead — an open test,
  not a closed one.
- The ridge r is a *linear-in-quadratic-features* test; it bounds what is
  learnable by a degree-2 model, which is exactly the tadpole's own class.

## Where this lives

- `scripts/measure_constraint_learnability.py` — the measurement.
- `src/pacland/structure.py` — `ridge_cv_predictability` (the joint learnability test).
- `src/pacland/learnability/vc.py` — `sample_complexity` (the PAC bridge).
- `src/pacland/constraints.py` — `joint_elimination` (the Q2 composition).
- `docs/new-approach.md` — the fork this resolves.
