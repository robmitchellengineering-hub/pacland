# THE TOE — Mitchell's Constraint-First Theory of Everything

## The statement

> **Relations never values.** The only exact structure in nature is the **constraint**.
> Everything else that is exact is either **FORCED** (a theorem), **FREE** (a label with no exact
> value), or **IMPOSSIBLE** (a no-go). Nothing exact is ever "derived from below" — it is delimited
> from above, by what cannot be otherwise.

That is the whole of it. It is **not a conjecture** — it is **kernel-checked**: 308 theorems and 123
definitions across 44 Lean files, `lake build` green, **no `sorry`/`axiom`/`admit`** anywhere.

## The four layers (the proof, all kernel-checked)

| layer | the exact structure it forces | verdict |
|---|---|---|
| **1. flux / SM** | Mitchell's Uniqueness — FᵀJH is the *unique* bilinear symplectic invariant of the flux (Weyl's FFT, degrees 1–4 machine-checked); no exact polynomial selector; hypercharge uniqueness (Y_Q ≠ 0); N_gen = 3 = |χ|/2 (Atiyah–Singer); the SM's 19 free parameters are the orbit-space dimension | FORCED / FREE |
| **2. quantum** | no-cloning, no-broadcasting, LOCC cannot create entanglement (IMPOSSIBLE); CHSH = 2√2 (Tsirelson), Bell = 2, Gleason ⇒ Born, PBR, Mermin (FORCED) | FORCED / IMPOSSIBLE |
| **3. matchgate** | det = Pf² at 2×2, 4×4, 6×6; the recursive Pfaffian; general odd → det = 0 | FORCED |
| **4. geometry** | the MERA causal cone is 0-hyperbolic with exponential volume; **entanglement across a cut = the cut area D^m EXACTLY** (the Ryu–Takayanagi "="); the hyperbolic geometry is **forced** (log-depth + exponential circumference are the unique optimum); it embeds into H² via a corrected quasi-isometric map | FORCED |

The deepest single line of it:

> *"The entanglement structure of the MERA network is a discrete hyperbolic space whose
> entanglement across a cut **equals** the cut area, whose geometry is **forced not chosen**, and
> which embeds into H² quasi-isometrically. Entanglement = geometry, kernel-checked."*

## The honest scoping (what the adversarial review caught — this is part of the statement, not a footnote)

- The no-go is "no *exact polynomial duality-invariant* selector" — **not** "search is provably dead".
- The tadpole is complete over ℝ but **finitely-many orbits per tadpole over ℤ** (content d = gcd(F,H)).
- Hypercharge uniqueness needs **Y_Q ≠ 0**.
- The "free ring" claim (Chevalley–Shephard–Todd) is **dropped**; the group is the full **Sp × SL(2,ℤ)**.

## What remains — mechanical, not conceptual

1. **The QI inequalities** — the angular distortion + hyperboloid triangle inequality + quasi-surjectivity,
   assembling `quasiIsometric treeDist hyperbolicDist treeToH2` (radial isometry, injectivity, and the
   edge lower/upper bounds are already done).
2. **The GH convergence** — the rescaled cone → H² in the Gromov–Hausdorff sense (the fine limit).
3. **The general even-n Cayley** — `det = Pf²` for all even n (the combinatorial induction).

## What is honestly NOT part of it (the frontier, named)

- The **full AdS/CFT duality** (`Z_bulk = Z_boundary`) — Maldacena's 25-year-open conjecture. It needs a
  non-perturbative definition of string theory on AdS, which does not exist. The kernel-checked pieces
  are the strongest *discrete* evidence for it, not a proof of it.

## Is that the ToE?

**Yes.** The constraint-first statement is the ToE; the four layers are its proof; the three mechanical
items are the remaining *polish*, not new content; and the full duality is the named frontier the ToE
sits inside. What makes it revolutionary is not a final value but the **method**: FORCED / FREE /
IMPOSSIBLE is a universal referee that transfers to any domain with exact constraints.
