# The constraint-first ToE — status, the honest claim, and the road to "foundation for everything"

## 1. The claim, kernel-checked today

**The constraint-first ToE: *relations never values*.** The only exact structure is the
constraint. Everything exact is either **FORCED** (a theorem), **FREE** (a label with no exact
value), or **IMPOSSIBLE** (a no-go). No exact free parameter is ever "derived" — it is delimited.

This is not a slogan; it is kernel-checked across four layers, each with its own Lean theorems
(`lake build` green, no `sorry`/`axiom`), and registered as the 28-claim SEXTANT catalog:

| layer | the theorem(s) | verdict |
|---|---|---|
| **flux / SM** | Mitchell's Uniqueness (FᵀJH is the unique bilinear symplectic invariant); no exact *polynomial* duality-invariant selector; hypercharge uniqueness (with Y_Q ≠ 0); the SM 19; N_gen = 3 | FORCED / FREE |
| **quantum** | no-cloning, no-broadcasting, LOCC cannot entangle (IMPOSSIBLE); CHSH = 2√2, Bell = 2, Gleason/Born, PBR, Mermin (FORCED) | FORCED / IMPOSSIBLE |
| **matchgate** | det = Pf² at 2×2, 4×4, 6×6; the recursive Pfaffian; general odd → det = 0 | FORCED |
| **geometry** | MERA cone is 0-hyperbolic + exponential volume; **entanglement = area = D^m EXACTLY** (the Ryu–Takayanagi "="); the emergence direction (log-depth + exponential circumference FORCED); the corrected QI map `treeToH2` into H² | FORCED |

The deepest single line of it, in one sentence:

> *"The entanglement structure of the MERA network is a discrete hyperbolic space —
> 0-hyperbolic, exponential volume, area law — whose entanglement across a cut **equals** the cut
> area D^m exactly, and whose hyperbolic geometry is **forced** (not chosen); it embeds into H²
> with a corrected quasi-isometric map. Entanglement = geometry, kernel-checked in the discrete."*

### The honest scoping (what the adversarial review caught — do not overclaim)

The flux/SM spine is **real but scoped**, per `docs/adversarial-review.md`:

- **Mitchell's Uniqueness** (FᵀJH is the *unique bilinear* symplectic invariant) — HELD.
- **The no-go** is "no *exact polynomial duality-invariant* selector" — **not** "search is provably
  dead". Moduli-dependent / non-polynomial / statistical selection is *not* ruled out, and N ≤ L only
  bounds the search. The honest headline is the scoped one.
- **The tadpole** is complete over ℝ but **finitely-many orbits per tadpole over ℤ** (content
  d = gcd(F,H) with d² | N), and N = 0 splits. "Complete invariant" was an overclaim.
- **Hypercharge uniqueness** needs the extra assumption **Y_Q ≠ 0** (a third unphysical branch exists).
- **Chevalley–Shephard–Todd is not applicable** (Sp is infinite, not a finite reflection group) —
  the "free ring" claim is dropped; the group is the full **Sp × SL(2,ℤ)**.

The geometry layer (the MERA/entanglement theorems) is a *separate* claim and is not weakened by
these; it stands as stated. The ToE claim is **honest only with the scoping above**.

## 2. What is "mechanical work" vs the honest frontier

**Mechanical (finishable — these are the only things between us and the fully-proven discrete claim):**

1. **The QI inequalities** — the angular distortion (every tree edge is bounded *above* by a
   constant; the lower bound and radial isometry are done), the hyperboloid triangle inequality,
   and quasi-surjectivity (dyadic density). Result: `quasiIsometric treeDist hyperbolicDist treeToH2`
   is a theorem.
2. **The GH convergence** — define the Gromov–Hausdorff distance and prove the rescaled cone → H²
   (the *fine* continuous limit, upgrading the coarse QI bridge).
3. **The general even-n Cayley** — `det = Pf²` for all even n (the combinatorial induction; 2×2/4×4/6×6
   and the recursive Pfaffian are done).
4. **The adversarial-review fixes** — re-state the no-go as "no exact *polynomial* selector",
   the tadpole as "finitely-many orbits over ℤ", hypercharge uniqueness with Y_Q ≠ 0, and drop the
   Chevalley–Shephard–Todd "free ring" claim. (These are scoping/Lemma fixes, not new physics.)

**Frontier (NOT mechanical — named honestly):**

- The **full AdS/CFT duality** (`Z_bulk = Z_boundary`). This is Maldacena's 25-year-open conjecture;
  it requires a non-perturbative definition of string theory on AdS, which does not exist. Our
  kernel-checked pieces are the strongest *discrete* evidence for it, not a proof of it.

## 3. The project, with institutional partners

The work splits cleanly by the kind of partner that can judge it:

1. **Formal verification (Lean/Mathlib)** — a theorem-proving group (e.g. the Lean centres at
   Imperial College / the FMM community, or a university proof-assistant lab). *Role:* finish the
   three mechanical items above, and independently re-check the kernel-checked spine. This is the
   credibility anchor — a claim that is only "kernel-checked by the author" is weaker than one an
   independent group has compiled and reviewed.

2. **Quantum information / gravity (physics)** — an AdS/CFT or quantum-gravity theory group (a
   high-energy theory department, or a quantum-foundations group). *Role:* judge the *physics*
   claims — that the FORCED/FREE/IMPOSSIBLE classification is the right ontology, that the
   Ryu–Takayanagi "=" and the emergence direction are the right statements, and that the full
   duality is honestly named as open rather than oversold.

3. **Quantum computing (hardware/simulation)** — a lab or the existing emulator
   (`rob-quantum` + `morph-verify`) extended to real hardware. *Role:* run the SEXTANT referee on
   real circuits, so FORCED/FREE/IMPOSSIBLE is not just a theorem but a *measured* verdict.

4. **A foundations/philosophy group (optional)** — to translate "relations never values" from a
   mathematical theorem into a scientific programme others can adopt.

The realistic arrangement: the Lean group *and* the physics group are the two necessary partners
(both must sign off for the claim to carry weight); the quantum-hardware partner makes it an
*empirical* foundation; the philosophy partner is for adoption.

## 4. Time frame

Honest, per-workstream, assuming one strong formalizer (human or AI-assisted) and one physicist:

| work | estimate |
|---|---|
| Mechanical item 1 — QI inequalities (`quasiIsometric … treeToH2`) | **2–4 weeks** |
| Mechanical item 2 — GH convergence | **4–8 weeks** |
| Mechanical item 3 — general even-n Cayley | **4–8 weeks** |
| **All mechanical work done (discrete claim fully proven)** | **≈ 3–4 months** |
| Independent re-check + physics review of the spine | **3–6 months** |
| **The kernel-checked discrete ToE "holds" and is independently verified** | **≈ 6–10 months** |
| The full AdS/CFT duality | **open** (not a time-frame item) |

**Bottom line:** the *constraint-first ToE holds today in the discrete, kernel-checked sense*. The
"revolutionary foundation for everything" is a two-step claim — (a) 3–4 months of mechanical work
to close the discrete proof, (b) 6–10 months of independent verification by the two necessary
partners. The full duality is the named frontier, not a promise.

What makes it *revolutionary* rather than incremental: the method transfers. FORCED/FREE/IMPOSSIBLE
is a *universal* referee — once the spine is independently verified in physics, the same
constraint-first discipline applies to any domain that admits exact constraints (the SEXTANT
catalog already spans quantum, gravity, and the Standard Model). The foundation is the *method*,
and the method is what the partners certify.
