# PACLAND v2 — plan

**Objective:** use *our* Valiant Verification engineering discipline (guards + mutation
testing + hazard library + asymmetric reviewer + the (ε,δ) certificate) to attack unified
string theory — not import a theorist's framework (that was v1), but point our working,
battle-tested verification machine at the field's known-unverified computations.

Status: **executed (2026-10-18)** — the staged portfolio (6 → 1 → 2) is built and validated on
real physics. See the execution record at the bottom.

---

## 0. Honesty up front — what "solve" can and cannot mean

- **Literal unification** (derive the correct vacuum, the measure that selects it, and get
  experimental confirmation): **P ≈ 0** for any software, any near-term timeframe. It is a
  physics discovery, not an engineering task. Stated once so the project never fools itself
  (same honesty rule pacland v1 already carried).
- **What IS achievable:** a real, citable, defensible advance — and a genuinely novel
  tool/framework — that moves the *verification half* of the problem from "vibe" to
  "quantified." **"Success" below = producing that within ~6–12 months of focused work.**
- The verification/selection split (v1's core insight) remains correct: our system attacks
  **verification**; the measure/selection problem stays a separate, open physics hole.

## 1. The one finding that unlocks the whole thing

Gap analysis (three parallel research threads, 2026-10-18) found:

1. **Our exact discipline does not exist in the field.** Guard-based / assertion-based
   verification of physics software (CYTools, cymetric, cohomCalg, JAXVacua) **does not
   exist as a category** — all four ship conventional unit tests, no guards, no certification.
   PAC/Valiant-style certification of physical theory choice is **empty**. Mutation/fault-injection
   exists only adjacent (simulation-engine fuzzing), never on string/QFT code.
2. **The field is converging on verification from three sides:**
   - Michael Douglas (the landscape's leading statistician) is now **formalizing QFT in Lean 4**
     ([arXiv:2603.15770](https://arxiv.org/abs/2603.15770), Mar 2026) — explicitly "AI-assisted
     formalization may influence the future of theoretical physics."
   - **PhysProver** ([arXiv:2601.15737](https://arxiv.org/abs/2601.15737), Jan 2026) is the first
     LLM theorem-prover trained for physics (PhysLean + RLVR).
   - "**How to falsify string theory at a collider**" ([arXiv:2412.13192](https://arxiv.org/abs/2412.13192),
     PRR 7, 023184, 2025) formalizes falsification targets — the seed of a "guard suite" for the theory.
3. **The field's real bottleneck is unverified computation.** The de Sitter/KKLT debate, the
   measure problem, and the ~10^500 count are all *disputed* — literally disputes about whether
   a proof is valid — with no consensus (briefing: `hep-th/0004134`, `1806.08362`,
   `hep-th/0301240`, `2406.13751`). DESI's evolving-dark-energy signal (2.5–3.9σ) has revived
   the quintessence/swampland question.

**The move:** our system's value is precisely in the regime where *ground truth is absent* —
we guard against **known failure modes** (symmetries, invariants, bounds, known-wrong traps),
not against "the wrong answer." That is the one thing the field has no tool for.

## 2. The approaches, rated

"P(success)" = probability of a real, citable, defensible advance within ~6–12 months.
(All approaches have P ≈ 0 for *literal* unification; that is not the bar.)

| # | Approach | P(success) | Time to first artifact | One-line thesis |
|---|---|---|---|---|
| 6 | **Verification Deficit Report** — quantify how unverifiable string theory is | **45%** | 4–6 wks | Turn "string theory is untestable" into a number with error bars, computed by a guarded pipeline |
| 1 | **Verification Vault** — certified computational substrate (guards over CYTools/JAXVacua/cymetric) | **40%** | 2–3 mo | The first verified string-theory computation pipeline: every observable gets a mutation-tested guard + (ε,δ) error model |
| 2 | **Reality Guards** — the 19 measured parameters as a falsification guard-suite | **35%** | 3–4 mo | Don't verify a vacuum matches us; falsify any candidate that fails a reality-guard; map ruled-out vs still-possible |
| 4 | **Certified Landscape Search** — evolvability with certificate-as-fitness, mutation-tested | **25%** | 4–6 mo (needs #1) | Guarded search over flux vacua; answer "is the map learnable?" either way |
| 3 | **Falsify the Swampland** — mutation-test the conjectures themselves | **22%** | 3–6 mo | Seed counterexamples against de Sitter/distance conjectures; find where they over-claim |
| 5 | **Formalized Landscape** — Lean machine-check of a disputed theorem (e.g. KKLT/dS) | **15%** | 6–12+ mo | Settle a live 20-year dispute by machine-checking the proof; moonshot |

### Pros / cons per approach

**6. Verification Deficit Report** — *highest P(success), fastest.*
- Pros: doesn't require the hard physics to *work*, only to *measure honestly* what is
  computable vs measurable; ships the (ε,δ) certificate as a real artifact; directly
  continues v1's strongest contribution; defensible-by-construction.
- Cons: it is a *characterization/negative* result, not "progress toward unification";
  can read as "we gave up and wrote an essay" if not framed right.

**1. Verification Vault** — *the substrate everything else needs.*
- Pros: builds on tools already verified working (CYTools 1.4.12 + JAXVacua on studio-linux);
  the gap is real and empty; produces the first certified string-theory computation pipeline;
  every other approach consumes it.
- Cons: "infrastructure," not a physics result; GPL-3.0 entanglement with CYTools; the
  systematic errors (α′ corrections, uplift ambiguity) are hard to even *bound*, let alone
  certify; writing correct physics guards needs real domain expertise.

**2. Reality Guards** — *highest physics leverage per effort.*
- Pros: builds on a real 2025 line (falsify-at-collider); guards are well-defined (SM
  parameters + error bars); "falsify" is more achievable than "verify"; mutation-testing
  transfers cleanly; honest endpoint (a rigorous map of the ruled-out).
- Cons: falsification ≠ unification (must be said); many key observables (Λ, Yukawas) are
  "not computable" for realistic vacua → many guards stay in the prediction zone; risk of
  reading as "string theory is dead" without landing that claim.

**4. Certified Landscape Search** — *uses the evolvability/educability layers.*
- Pros: mutation-testing the fitness evaluator is exactly what stops a search from silently
  wandering 10^500 noise; either a navigation tool OR a rigorous negative result (both citable).
- Cons: needs #1's oracle first; heavy compute (CY metric per candidate); can't select
  (measure untouched); real risk the answer is "not learnable" (honest but demoralizing).

**3. Falsify the Swampland** — *outside-the-box, adversarial.*
- Pros: no one is *attacking* the swampland program, only extending it; mutation-testing
  (our signature move) maps perfectly ("does the conjecture's guard fire on a seeded
  counterexample?"); cheap to start (known tension cases exist).
- Cons: needs deep swampland expertise; high risk of "counterexample already known/refuted";
  lower ceiling than settling dS directly.

**5. Formalized Landscape** — *moonshot, highest upside.*
- Pros: settles a live 20-year dispute (is KKLT dS valid?) with a machine-checked proof;
  sits exactly on the hot Douglas/PhysProver line; our mutation discipline = "find the gap
  in the proof"; a partial result that *exposes* a gap is still citable.
- Cons: enormous lift (CY geometry + SUSY + flux compactification are not formalized anywhere;
  only free QFT exists so far); we are not Lean/string-theory experts; highest risk of months
  with nothing; Douglas's group is ahead — we'd be following, not leading.

## 3. Recommendation — a staged portfolio, not a single bet

1. **Start with #6** (fast, honest, ships the certificate, establishes the novel framing and
   the "verification deficit" number as *our* contribution).
2. **Then #1** (the substrate; every computation-backed approach needs it).
3. **Then #2** (highest physics leverage per effort; the falsification machine).
4. **Keep #5 as the watched moonshot** — track Douglas/PhysProver; join if a tractable target
   (one disputed theorem) crystallizes.
5. **#4 only after #1 exists; #3 opportunistically** if a swampland counterexample shows up.

Net: this is "verify first, falsify second, formalize last" — and it converts "solve unified
string theory" into a sequence of checkable, shippable claims, which is the whole point of
the verification discipline applied to itself.

## 4. What we keep from pacland v1 (the useful bits)

- `certificate.py` (two-level bound), `error_model.py` (calibration), `measure.py` (finite-D),
  `selection.py` (typicality/KS) — port to the new system, don't rewrite.
- The two-level certificate and the finite-set collapse (sampling vanishes; oracle-validation
  term dominates) — the mathematical spine.
- The honest-deficit framing (~19 measurable points → tens-of-% radius) and the "validated vs
  extrapolated / no certificate no claim" rule.
- `docs/tooling.md` (CYTools/JAXVacua/cymetric/cohomCalg/KS census + the ML-for-landscape map)
  and `docs/toolchain.md` (Linux install path, verified).
- The verified Linux path: CYTools 1.4.12 + JAXVacua on studio-linux via the harness mesh.

## 5. Open decisions (for Rob)

- Commit to the staged portfolio (6 → 1 → 2, moonshot 5), or pick one approach outright?
- Scope of "success" for the first milestone: a citable preprint? a shipped tool? a number?
- Resources: run on the harness mesh (studio-linux for CYTools/JAXVacua), or keep it Mac-only first?

---

## 6. Execution record (2026-10-18)

| Stage | Result |
|---|---|
| **1 — #6 Deficit Report** | ✅ `docs/verification-deficit.md` + `deficit.py` + `observables.py` + mutation tests. Honest finding: **deficit is total** (real `m`=0, radius ∞, not the ~31% v1 claimed). |
| **2 — #1 Verification Vault** | ✅ `guards.py` + `vault.py` + calibration + certificate. **Real validations:** CYTools quintic → `h11=1, h21=101` passed on studio-linux; 163 real JAXVacua flux vectors → `integer_flux` passed, `sl2z` clean. |
| **3 — #2 Reality Guards** | ✅ `reality_guards.py` — falsification suite over the 10 measured observables + tests. |
| **Moonshot #5** | 🔭 **tracking, not building**: Douglas et al. QFT-in-Lean ([arXiv:2603.15770](https://arxiv.org/abs/2603.15770)); PhysProver ([arXiv:2601.15737](https://arxiv.org/abs/2601.15737)). Revisit if one disputed theorem becomes a tractable machine-check target. |

70/70 tests pass. All code is pure-stdlib except the optional oracle adapters (lazy imports).

**Toolchain (studio-linux):** CYTools 1.4.12 + JAXVacua 0.1.2 at `/home/rob/cytools-venv`.
Route `mac → win-2 (100.86.50.6) → studio-linux (192.168.28.128)`; the win-2 hop needs
`-i C:\Users\robmi\.ssh\mesh-vm`, and PowerShell 5.1 there rejects `&&` (use `;`).
