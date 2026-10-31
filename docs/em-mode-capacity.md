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
| metal cabinet (0.5 m cube) | | 1,027 | 81 | −0.107% |
| small room (3 × 4 × 2.5 m) | | **251,718** | 56,427 | **−0.004%** |
| implant phantom (10 × 10 × 20 cm) | | 11 | 5 | −0.745% |

The volume coefficient is theory — two polarisations of a scalar field give `(8πV/3)(f/c)³` exactly. The
surface coefficient is **measured against exact enumeration** (0.009–0.104 depending on the space), never
asserted.

**So the unification holds where it is testable and cheap: mode counting is the same computation.**
`c` in, room out; `c` in, cavity out.

## What the same table says that a solver does not

**77.6% of the modes in a 3 × 4 × 2.5 m space are exact degeneracies**, and **92.1%** in a cube. That is the
identical structural fact the acoustic work found (38 of 104 box modes below 200 Hz), and it has the same
consequence: **a spacing statistic computed on raw modes is measuring the symmetry of the box, not the
physics.** Any tool that reports "mode density" without collapsing degeneracies is reporting an artefact.

### A real bug found by a test, kept because it changes the numbers

The first enumeration counted `(0,0,p)` as a TE mode. **With both transverse indices zero every transverse
field component vanishes identically — it is not a mode.** The TE101 test asserted that `(0,1,1)` was the
lowest mode and got `(0,0,1)` back, which is how it was caught.

Corrected counts: cabinet **1,037 → 1,027**, room **251,768 → 251,718**, phantom **15 → 11**. The Weyl
agreement moved from *small-N* to a stated **−0.004%** on the room and **−0.745%** on the phantom, and the
degeneracy fractions rose slightly because the spurious modes were singletons.

**The test earned its keep on its first run** — and the fix changed three numbers on the page, which is why
they are quoted with the correction rather than silently updated.

## Identifiability, rebuilt — and it says something the acoustic case could not

The first version returned **zero usable directions at −60 dB**. Three separate bugs, each found by looking
at the number rather than believing it:

1. **arbitrary complex phases** instead of the cavity's own field — replaced with the real
   `sin(mπx/a) sin(nπy/b) sin(pπz/d)`;
2. **no stated Q** — now `Q = 50` explicitly, and the noise floor is defined **relative to the strongest
   response**, not in absolute units (a GHz response is ~1e-18; an absolute 1e-3 floor makes everything
   unidentifiable);
3. **every probe on the mid-plane `z = d/2`**, where *every even-p mode vanishes identically* — so adding
   probes added no information about half the modes, and the usable count sat flat at 12 for 1, 2, 3, 4 and
   6 probes. Probes are now spread in three dimensions.

**The result, 0.5 m cube, 0.5–3 GHz, 40 modes after collapse, Q = 50, −60 dB:**

| probes | usable @10% | median direction sd |
|---|---|---|
| 1 | **17** / 40 | 1.9e5 |
| 2 | 17 | 1.0e5 |
| 3 | 17 | 1.0e5 |
| 4 | **19** | 8.9e4 |
| 6 | 19 | 1.4e5 |
| 9 | 19 | 1.1e5 |

**And this is a finding, not a defect:** in a **high-Q** cavity a single probe with a wide spectrum already
resolves most modes, because the resonances are separated in *frequency*. Probes buy little beyond the
fourth. **The acoustic case was different because room modes are heavily damped and overlapping in frequency,
so only *space* separates them.** The same engine, a different answer, for a reason that is physical.

**So the unification holds for the counting and for the *method*, and the answer to "how many sensors" is
not transferable — which is exactly what the transfer note claimed.** The discipline transfers; the numbers
do not.

## Still not a result

**The ratio statistic** (0.8044 at the cabinet, outside the GUE control's range of 0.6136; 0.3573 at the room,
near Poisson) is still degenerate-dominated and is **not quoted as a finding**. Collapse-then-unfold is
implemented; what is missing is enough *distinct* modes in a band for the statistic to mean anything — 81 in
the cabinet, which is too few for a spacing distribution.

**Falsifier for the next attempt:** if a band with hundreds of distinct modes still gives a ratio outside
[0.38, 0.62], the estimator or the collapse is wrong; if it lands near Poisson, then a rectangular cavity is
integrable, which is the *expected* answer and would make the electrodynamic case a clean control for the
room case.

## What this is, and what it is not

It is **a design table computed analytically** — mode count, degeneracy fraction, and (once fixed) the
identifiability count and the thermal-noise ceiling from `η²m = 2[Q⁻¹(ε)]²`.

It is **not** a full-wave solution and does not compete with one. It answers a different question: not
*"what is the field at this point"* but **"how many independent things can this space carry, and at what
noise floor do they stop being usable"** — the question a small wireless device actually faces.
