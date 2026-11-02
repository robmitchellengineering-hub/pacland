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
