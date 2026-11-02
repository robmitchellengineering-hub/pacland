# The h12 wall's discriminator, calibrated — and it is confounded by the thing it measures

**The question** (from `docs/h12-25-sampling-wall.md`): `cond(M)` rises from **1.8e2 at h12=2 to 4.8e6 at h12=25** (up to
2.7e10 across polytopes). **Is the near-null direction a truncation artefact or a real hierarchy?** No measurement has
settled it, and the sampling wall above h12 = 5 depends on the answer.

**The diagnostic's stated discriminator** (`scripts/diagnose_isd_conditioning.py`): *"a direction concentrated on the
boundary is a truncation signature; one spread through the moduli is a physical hierarchy."*

**It has never been calibrated.** There was no matrix in the repository for which the answer is known by construction, so the
boundary fraction has been read against a guess.

## The control

`scripts/truncation_control.py` builds **two families whose smallest eigenvector is placed by construction** — one sitting
on the boundary block, one spread through the moduli — with an **identical spectrum** apart from the single near-null
eigenvalue. The only difference is where the direction lives.

| | boundary-concentrated | moduli-spread |
|---|---|---|
| boundary fraction, complete matrix | **1.00** | **0.00** |

**The discriminator works perfectly on a complete matrix**, with a margin of 1.00. That part of the docstring is right.

## The finding that matters

**Now truncate the same matrices** — drop the last coordinates, which is what a finite series does to the matrix the
diagnostic measures:

| coordinates dropped | boundary fraction (the "truncation signature") |
|---|---|
| 0 | **1.000** |
| 1 | 1.000 |
| 2 | 1.000 |
| 3 | **0.006** |

**Truncating the basis destroys the signature it is supposed to detect.** A boundary fraction measured on a truncated matrix
is a **mixture** of where the direction physically is and how much of the basis was included — and **the real h12
measurement is always truncated.**

## What settles it, and it needs no new theory

**The h12 ladder is itself the truncation ladder.** `cond(M)` is measured at h12 = 2, 4, 6 … 25 — the same matrix at
increasing truncation order. So the question is answered by reading the composition **across h12**, which the existing
diagnostic already prints per h12:

> **If the boundary fraction moves with h12, the near-null direction is truncation. If it is stable while h12 changes, it
> is a hierarchy.**

**That is one table from the tool that already exists**, on the node that already has `jaxvacua`. It is the cheapest
experiment in the physics programme.

## The falsifier

> **If the boundary fraction is flat across h12 and the condition number still climbs by four orders of magnitude, then the
> near-null direction is real and the wall is physics, not series truncation** — and the h12 ≥ 5 sampling problem becomes a
> numerical-hardware problem rather than a foundational one.

## The measure that decides it, and where it is running

**The truncation is `maximum_degree`, not h12.** The diagnostic builds
`FluxVacuaFinder(h12=…, model_ID=1, model_type="KS", maximum_degree=0)` — **degree 0 is a truncated series**, and it is the
default in the script. So the ladder that decides truncation-versus-hierarchy is **the same model and the same moduli point
at increasing degree**, not different h12 values (a different h12 is a different Calabi–Yau, not a truncation of this one).

**Job sent 2026-11-02T1613Z** to `pacland-rog` (the node with `/home/rob/cytools-venv` and `jaxvacua`): degree 0, 1, 2, 3,
one moduli point from the model's own ISD initial guess, printing `dim`, `eig_min`, `eig_max`, `cond(M)` and the
**boundary weight** of the near-null eigenvector at each.

### The decision rule, written before the numbers arrive

| what the table shows | what it means |
|---|---|
| **boundary weight moves with degree, and `cond(M)` falls as degree rises** | **the wall is the series.** Truncation manufactures the near-null direction; the fix is to sample at higher degree or precondition against it, and h12 ≥ 5 is a numerics problem |
| **boundary weight is flat while `cond(M)` climbs** | **the near-null direction is physical**, the wall is real, and the sampling difficulty is a property of the landscape |
| **the model fails to build at all at some degree** | the ladder stops there; report the last rung that built and say so |

**The synthetic control says the first row is the likely one**: on a constructed matrix the boundary weight fell from 1.000
to 0.006 after truncating three coordinates, so **the signature is highly sensitive to what is included** — but the real
matrix has a different structure, which is why the measurement rather than the control is the answer.

## The control at the real matrix size, and what it changes

The real matrix is dim 4 at h12 = 2 and about 50 at h12 = 25. The control was rerun at those sizes:

| n | boundary weight, complete | boundary weight after dropping 3 coordinates |
|---|---|---|
| 9 | 1.000 | 0.249 |
| 17 | 1.000 | 0.037 |
| 33 | 1.000 | **0.009** |
| 51 | 1.000 | 0.018 |
| 101 | 1.000 | 0.009 |

**The rule to read the real measurement by:**

- **boundary weight near 1.0** — the near-null direction sits on the last two coordinates. **Truncation signature.**
- **boundary weight near 0** — it is spread through the moduli. **Physical hierarchy.**

**And the trap that makes this hard, stated plainly**: dropping just **three** coordinates takes a genuinely
boundary-concentrated direction from 1.000 to **0.009**. So **a low boundary weight does not, by itself, prove the direction
is physical** — the basis it is measured against has already moved. **What distinguishes the two is what happens as the
degree RISES**: a truncation artefact is created by the terms that were left out, so the near-null gap should *shrink* as
those terms come in; a real hierarchy persists while `dim` grows.

**So the table to read is `cond` and `dim` together across degree, with the boundary weight as the third column — not the
boundary weight alone.**

## The ladder ran, and it falsified the ladder

**Job `2026-11-02T1619Z` finished on `pacland-rog`** with a real committed moduli point. The result:

| degree | dim | eig_min | eig_max | cond(M) | boundary weight |
|---|---|---|---|---|---|
| 0 | 6 | 9.415e-46 | 1.323e+90 | 1.405e+135 | 1.1e-30 |
| 1 | 6 | 9.415e-46 | 1.323e+90 | 1.405e+135 | 1.1e-30 |
| 2 | 6 | 9.415e-46 | 1.323e+90 | 1.405e+135 | 1.1e-30 |
| 3 | 6 | 9.415e-46 | 1.323e+90 | 1.405e+135 | 1.1e-30 |

**Every row is identical to twelve significant figures.** So `maximum_degree` — the parameter I identified as the truncation
knob — **does not change `ISD_matrix` at all** for this model at h12 = 2. **The ladder is not a ladder**, and it cannot settle
truncation-versus-hierarchy.

**That is the experiment falsifying its own design**, and it is worth more than a clean null result: it says the truncation is
**not in `maximum_degree`**, so the wall document's "series truncation at degree 1" is either about a different parameter or a
different object than the matrix this diagnostic measures.

**Two other numbers matter and neither is comfortable:**

- **cond(M) = 1.4e135** here, against the wall document's **1.8e2 at h12 = 2**. Those are not the same object measured at
  different precisions — **they are three orders of magnitude apart in the exponent**, and one of the two numbers is wrong.
- **the near-null direction's boundary weight is 1e-30**, which reads as "entirely moduli, therefore physical" — **but with
  cond ~1e135 the eigenvector is numerically meaningless**, so that reading is not available. The composition metric has no
  power at this conditioning.

**What to do next is now specific**: find which parameter *does* change `ISD_matrix` (the period series degree as the model
builds it, not `maximum_degree`), and reconcile the 1.8e2 versus 1.4e135 discrepancy before either number is used again. Until
then this note's central question stays open, and the honest state is that **the measurement could not be made with the
instrument as built**.
