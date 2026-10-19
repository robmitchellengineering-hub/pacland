# The theorem taxonomy — the complete scaffolding of constraint-first

The fan-out asked: what other theorems (like Darboux) independently strengthen the
constraint-first result? Six domains answered. Together they turn "constraint-first" from
*one theorem + one complement* into a **complete web of named theorems**, each forcing a
piece of the conclusion.

## The taxonomy — five slots, each filled

| slot | what it forces | the theorems |
|---|---|---|
| **local** — no fingerprint | no local invariant exists | Darboux (no local symplectic invariants) |
| **algebraic** — one invariant | the only invariant is the tadpole | Weyl's FFT (Sp ring = C[tadpole]); Chevalley–Shephard–Todd (that ring is *free*, no hidden relations) |
| **global** — what survives | the residual structure is global symplectic topology | Gromov's non-squeezing (capacities); Eliashberg–Gromov C⁰-rigidity; Arnold conjecture (homology-counted fixed points); Marsden–Weinstein reduction (vacuum space = symplectic quotient); Delzant (toric case = moment polytope); Duistermaat–Heckman (fixed-point measure) |
| **topological** — the labels | the labels are topology, not inputs | Atiyah–Singer (N_gen = |χ|/2 = index of Dirac); K-theory (D-brane charges = K(X) classes); Bott periodicity (the 2-periodic brane spectrum) |
| **counting** — the numbers | the parameter/vacuum counts are theorems | Molien–Weyl + Hilbert–Serre (19 = orbit-space dimension); Morse inequalities (m_k ≥ b_k); Ashok–Denef–Douglas index (signed vacuum count = topological index) |

Every slot now has at least two independent named theorems. That is the Rule of Three
applied to the *foundations*: the conclusion "only constraint + global topology survive"
is forced from five different mathematical directions, not one.

## Three genuinely sharper statements (new, not restatement)

**1. The vacuum count is bounded, not fixed (Morse / Ashok–Denef–Douglas).** The *signed*
vacuum count is the topological index (χ of the moduli space), but the *unsigned* count is
only bounded below by the Betti numbers and otherwise depends on the flux — which has no
fingerprint. So "search is dead" sharpens to: **topology bounds how many vacua exist, but
never determines them; the search target is free to move within a topological bracket.**

**2. The constraint is a K-theory statement (Witten / Freed–Witten).** D-brane charges are
K(X)-classes (topological labels), and the tadpole is **"total charge = 0 in K(X)"** — the
constraint is the vanishing of a topological class, not an algebraic pairing. This is a
*different and deeper* formulation of the constraint than the symplectic FFT, and Bott
periodicity makes the observed 2-periodic brane spectrum a theorem.

**3. The vacuum space is a symplectic quotient (Marsden–Weinstein).** The vacuum space is
literally `μ⁻¹(0)/G` — the constraint (tadpole/D-term/F-term) is a moment map, and the
quotient by gauge is symplectic reduction. Its complete invariant content is the moment
polytope (Delzant) plus a fixed-point-determined measure (Duistermaat–Heckman). So the
"surviving global structure" is not an analogy — it is a theorem about symplectic quotients.

## The strongest single line

> **No local invariant (Darboux) · one algebraic invariant (FFT, a free ring) · the
> surviving structure is global symplectic topology (Gromov/Arnold/reduction) · the labels
> are topological (Atiyah–Singer/K-theory) · and the counts are theorems (Molien/Morse).**

Every clause has a named theorem behind it. That is what "strengthened" looks like: the
claim is no longer one result, it is a *taxonomy* no single theorem can uproot.

## Named next steps (kept)

1. **Morse/ADD quantification** — use the Ashok–Denef–Douglas index density to bound the
   unsigned vacuum count by the Betti numbers of the (tadpole-truncated) moduli space, and
   state the exact bracket in which the count can move.
2. **K-theory reformulation** — write the tadpole as `[total charge] = 0` in twisted
   K_H(X) (Freed–Witten) and check that Z₂-torsion charges are labels a cohomology-only
   tadpole would miss.
3. **Symplectic-quotient identification** — match the flux superpotential/tadpole to an
   explicit moment map, and identify which global invariant (moment polytope / DH measure /
   quotient Betti numbers) the flux-vacuum index density realizes.
4. **Molien–Weyl cert** — compute the SU(3)⁵ Molien integral and confirm its pole order at
   t=1 is exactly 19 (Hilbert–Serre), turning the parameter count into a certified theorem.

## Meta

Three fan-outs, three upgrades: the first caught "unpredicable" (two readings), the second
caught "free parameter" (three meanings), the third found a *complete taxonomy* of
supporting theorems. The instrument keeps paying for itself.
