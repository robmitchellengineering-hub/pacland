# Partner appeals — the open problems, framed as collaborations

The program has a machine-checked core and a short list of things it **cannot yet
compute**. Each of those is a sharp, falsifiable problem a partner with the right
expertise can advance — and each carries a named, citable result.

## Why the open items are worth a partner's time

- The core is already machine-checked: five theorems, sympy symbolic (zero
  tolerance) **and** Lean 4 (kernel-checked, no axioms), measured on real flux vacua
  (`docs/constraint-first-theorem.md`, `pacland-proof/`).
- Every item below is **checkable in days**, not taken on faith — a partner verifies
  or refutes it, and either answer is a publishable result.
- Each is a co-authorship / named-contribution opportunity on a concrete statement.

## The "can't compute yet" list

### 1. The ℤ₂ torsion — the last step to unifying string theory

**The hook.** The D3 tadpole and the SM anomaly cancellation are the *same kind of
object* over the rationals — both are a K-theory class whose cohomology shadow is a
topological index that must vanish (the tadpole's is the **Euler** index, the
anomaly's is the **Dirac** index; both are "an index vanishes"). The last step —
proving it at **full** strength — is the ℤ₂ torsion, and it needs KO-theory.

**What's blocked.** Computing the Freed–Witten ℤ₂ (flux side) and Witten's global ℤ₂
(anomaly side) and checking they correspond. This is twisted-K / KO-theory, beyond
the current sympy/Lean toolchain.

**The ask.** A string theorist or mathematician in K-theory / KO-theory to verify (or
refute) the torsion correspondence. Deliverable: the "same object at full strength"
theorem — or its sharp refutation. Either is publishable.

### 2. The landscape frontier — where isolated vacua end (h12 ≥ 5)

**The hook.** Measured, not guessed: isolated SUSY vacua exist and are samplable up
to **4** moduli, and the regime collapses at **5**. Explaining *why* — the flat-tower
/ distance-conjecture structure — is open and computable.

**What's blocked.** The ISD sampler's matrix becomes ill-conditioned at h12 ≥ 5 (a
nearly-flat moduli direction — the measured mechanism is in
`docs/h12-25-sampling-wall.md`). Needs a regularised sampler (algorithm), or, for the
full 272-moduli case, a GPU.

**The ask.** A computational physicist / ML person to build the flat-direction-
regularised sampler, or a partner with GPU hours to run h12 = 272. Deliverable: the
first sample of the high-h12 landscape, and the distance-conjecture boundary made
quantitative.

### 3. The "19 floor" — can a UV completion reduce the SM parameters?

**The hook.** Proved: the SM's 19 free couplings are the orbit-space dimension of the
flavor group — a real, not reducible, floor (`docs/sm-floor-notes.md`). The open half
is the *conjectured* generalisation: no UV completion reduces them.

**What's blocked.** The Jacobian-rank test of whether the 19 can be generated from
fewer than ~14 UV parameters. This is the next research fan-out.

**The ask.** A GUT / string-phenomenology partner to attack the rank question.
Deliverable: either "the 19 floor survives every known UV completion" or a specific
reduction — both publishable.

### 4. Machine-checking the last theorem (Lean, general-n)

**The hook.** The theorem tower is kernel-checked in Lean except one: transitivity for
**general n** (the orbit-tangent rank argument; n=1 is done).

**The ask.** A Lean formaliser (or a PhysLib contributor) to finish it. Deliverable:
the entire tower machine-checked, no axioms.

### 5. The five-pillars named next steps (four open theorem-computations)

From `docs/five-pillars.md`, each is a concrete, citable item already queued:

- **Morse/ADD quantification** — bound the unsigned vacuum count by the Betti numbers
  of the tadpole-truncated moduli space.
- **K-theory reformulation** — write the tadpole as `[total charge] = 0` in twisted
  `K_H(X)` (Freed–Witten), and identify the ℤ₂ torsion charges a cohomology-only
  tadpole misses.
- **Symplectic-quotient identification** — match the flux superpotential/tadpole to an
  explicit moment map (Marsden–Weinstein).
- **Molien–Weyl cert** — confirm the SU(3)⁵ Molien integral's pole order at t=1 is
  exactly 19 (Hilbert–Serre).

Each is a named theorem waiting to be certified; the machinery (sympy, the invariant
ring, the K-theory scaffolding) is already in the repo.

### 6. arXiv endorsement — the gate to the community (not a compute item)

The five named researchers and the personalised email templates are in
`docs/outreach-emails.md` and `docs/publication-plan.md`. This is the "who can check
it" step, and it is the prerequisite for everything above being *seen*.

---

**The through-line:** every item is a **wall we have hit and classified** (not a
vague "we can't do it") — a partner is asked to *use* a specific wall, with the exact
obstruction named, and the deliverable is a citable theorem or its refutation.
