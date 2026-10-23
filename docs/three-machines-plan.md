# The Three Machines — dissolving the remaining "can'ts"

Build order: **3 → 1 → 2**. Each machine turns a "can't" (a verification wall) into a
computable/falsifiable positive. Status tiered: **built** / **in progress** / **spec**.

---

## Machine 3 — the Completion-Enumerator + Deficit (close the SM extension)

- **Dissolves:** "can't prove no UV completion derives the 19 correctly" (a universal negative).
- **Precise question:** replace the negative with an exhaustive, falsifiable positive — catalog
  every known UV completion, compute the exact relations each imposes on the 19, and report the
  verified deficit.
- **Phases:** (1) catalog + symbolic collapse-count checker; (2) the numerically-correct filter;
  (3) the deficit report ("of N completions, none derives the values; exactly 2 survive").
- **Falsifiable output:** a running counter — any new numerically-correct 4th relation falsifies it.
- **Known collapse counts** (from the falsifier-#2 adversarial pass): SM 0 · minimal SU(5) 5 ·
  minimal SO(10)/E₆/PS/trinification 12 · flipped SU(5) 2 · realistic multi-Higgs GUTs 2 ·
  MSSM +1 · SUSY SU(5) 6 · SUSY SO(10) 13 · heterotic/F-theory 2–5 · warped/composite/FN 0.
- **Runs:** Mac (Python, no jaxvacua needed).
- **Status:** **in progress** — catalog module + validator being built.

## Machine 1 — the Uplift-Control Solver (settle the dS question)

- **Dissolves:** "the community can't compute the 10D backreaction, so the uplift stays contested."
- **Precise question:** does a corner of `(g_s, M, K)` exist where the anti-D3/KPV uplift is
  *controlled* — small α′² corrections, large NS5 polarization radius, satisfiable tadpole, small
  uplift?
- **Key insight:** the probe KPV potential `V(ψ; g_s, M)` is **analytic**; the "control problem" is
  a symbolic potential + a curvature estimate, not a full 10D PDE.
- **Phases:** (1) analytic KPV potential + numerical parameter scan (tests HSV `g_s M ≳ 20`);
  (2) the α′² curvature-control boundary `α′²R² < 1`; (3, optional) the backreacted radial ODEs.
- **Falsifiable output:** "the controlled corner is empty" or "a controlled corner exists at
  `(g_s, M, K) = …`".
- **Runs:** pacland-rog (scipy) — the KPV potential is a known function; Phase 1 is a scan.
- **Status:** **spec**.

## Machine 2 — the Auto-Formalization Engine (machine-check the FFT)

- **Dissolves:** "can't Lean the full Weyl FFT by hand — it's research-grade."
- **Precise question:** machine-check, in Lean, that the invariant ring is `ℂ[N]` at *every* degree.
- **Key insight:** the sympy proof already verifies it degree-by-degree (5 degrees); the engine
  upgrades degree-by-degree to general-degree, via LLM + compiler iteration.
- **Phases:** (1) Lean the degree-3 slice (no cubic invariant) and degree-4 slice (only `N²`);
  (2) the general-degree FFT (double commutant / Schur–Weyl); (3) a reusable LLM-proposes →
  Lean-checks → LLM-fixes loop.
- **Falsifiable output:** a `lake build`-green Lean proof of degrees 1–4, then the general FFT.
- **Runs:** Mac (`~/.elan/bin/lake`).
- **Status:** **spec**.

## Order and routing

1. Machine 3 (catalog + checker) — Mac, Python. **First.**
2. Machine 1 (KPV scan) — pacland-rog, scipy. **Second.**
3. Machine 2 (Lean degree-3/4) — Mac, Lean. **Third.**
