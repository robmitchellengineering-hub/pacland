# The electromagnetic twin — one engine, two fields

**Claim under test:** the mode count, the degeneracy structure, the level statistics and the identifiability
of a confined space are **the same calculation** for acoustic and electromagnetic fields. Only the speed and
the boundary physics differ. If that holds, one engine answers *"how much information can this space carry,
and where do I put the antenna"* for a metal cabinet, a room or an implant — before anyone runs a full-wave
solver.

**Reproduce:** `python3 scripts/em_capacity.py` · `src/pacland/spectral/em_modes.py`

## What holds: the mode count, to 0.001%

Exact rectangular conducting-cavity modes (TE with `p ≥ 1`, TM with `m,n ≥ 1`, both polarisations) against
Weyl's law with a **fitted** surface coefficient:

| space | to 3 GHz | exact modes | distinct | Weyl error |
|---|---|---|---|---|
| metal cabinet (0.5 m cube) | | 1,037 | 85 | small-N |
| small room (3 × 4 × 2.5 m) | | **251,768** | 56,454 | **−0.001%** |
| implant phantom (10 × 10 × 20 cm) | | 15 | 8 | **+1.02%** |

The volume coefficient is theory — two polarisations of a scalar field give `(8πV/3)(f/c)³` exactly. The
surface coefficient is **measured against exact enumeration** (0.009–0.104 depending on the space), never
asserted.

**So the unification holds where it is testable and cheap: mode counting is the same computation.**
`c` in, room out; `c` in, cavity out.

## What the same table says that a solver does not

**77.6% of the modes in a 3 × 4 × 2.5 m space are exact degeneracies**, and **91.8%** in a cube. That is the
identical structural fact the acoustic work found (38 of 104 box modes below 200 Hz), and it has the same
consequence: **a spacing statistic computed on raw modes is measuring the symmetry of the box, not the
physics.** Any tool that reports "mode density" without collapsing degeneracies is reporting an artefact.

## What does not yet hold, stated plainly

**Two failures, both mine, both recorded rather than reported as physics:**

1. **Identifiability returns 0 usable modes at −60 dB for 2 and 3 probes.** The acoustic run gives 3–7 at
   three mics, so a zero here is a **bug**, not a finding — my Jacobian uses arbitrary complex phases and a
   fixed 2% modal damping, and the Fisher matrix comes out effectively singular. It needs the same treatment
   the acoustic version got: a physical mode shape (the actual `sin` products, not phases), and a damping
   model with a stated Q.
2. **The ratio statistic is not yet meaningful**: 0.8044 at the cabinet (above the GUE control of 0.6136, so
   outside the model's range) and 0.3573 at the small room (near Poisson, 0.381) — both dominated by the
   degeneracy problem above. Until the collapse is done the way the acoustic work does it (collapse first,
   *then* unfold), these numbers are not results.

**Falsifier for the next attempt:** if collapsing degeneracies and using true mode shapes still gives zero
usable directions at −60 dB with three probes, then the electromagnetic case genuinely differs from the
acoustic one, and the unification claim is wrong for the information part while surviving for the counting
part.

## What this is, and what it is not

It is **a design table computed analytically** — mode count, degeneracy fraction, and (once fixed) the
identifiability count and the thermal-noise ceiling from `η²m = 2[Q⁻¹(ε)]²`.

It is **not** a full-wave solution and does not compete with one. It answers a different question: not
*"what is the field at this point"* but **"how many independent things can this space carry, and at what
noise floor do they stop being usable"** — the question a small wireless device actually faces.
