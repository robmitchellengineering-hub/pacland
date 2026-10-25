# SOP — figuring a complex system out

A worked method, written down after applying it to macro-finance for nine merged slices
([the roster](economics-model-roster.md)). It is the generalisation, not the case study:
the case study is the evidence that it runs.

The rule this document exists to enforce: **the goal is answers.** Elegance, analogy and
inherited form are not the goal, and none of them may narrow the method.

---

## 0. Borrow the machine, not the result

Physics supplied the *machine*: **constraint → proof → guard → deficit → out-of-sample →
falsifier → published tier.** Take the machine.

Do **not** inherit its answers as requirements. The landscape has a single invariant —
the D3 tadpole — because it has a duality group (Sp(2n) × SL(2,ℤ)) and a finite-generation
theorem (Weyl's FFT), so the invariant ring is `C[N]`, one generator, and "nothing else is
exact" is *proved*. A field without a group cannot have that, and insisting on it produces
a fake theorem.

**If the system needs eleven constraints to be accurate, it gets eleven.** The question is
never "which is the one"; it is **"how many are independent?"**

## 1. Classify every constraint, and source it

Three kinds, and they are not interchangeable:

| kind | meaning | force |
|---|---|---|
| **identity** | true by construction (double-entry, `S+E+I+R=N`, charge balance) | consistency only — it can never fail, so it can never select |
| **model** | true of the solution (Fisher, the Taylor principle, the Phillips slope) | delimits admissible solutions |
| **domain** | where the model is defined at all (zero net inflation, non-negative prices) | refuses out-of-domain use |

A constraint with no statement and no source is a claim wearing a label.
`guard_every_constraint_sourced` refuses it.

## 2. Measure the count — never assert it

Two numbers, and neither is "how many we wrote down":

1. **Independent rank** = rank of the constraint Jacobian, at a **generic** point.
   Rank is a property of the set, not of one point; at the solution, squared residuals
   have zero gradient and `max()`-form residuals sit on a kink, so both look dependent
   when they are not. Nudge every field off the solution first.
2. **Slack ordering** — which constraints actually bind. A constraint the data never
   approaches is decoration; it should be demoted or deleted, not counted.

**Prove the detector.** A duplicate (`2·(i − r* − π)` beside `i − r* − π`) must lift the
count by one and leave the rank unchanged. A rank test that has never caught a duplicate
has not been shown to work.

## 3. Derive the reference point; do not hand-tune it

Build the state the system actually produces — the model's own steady state joined to a
closed set of accounts — and demand every constraint hold there. If one doesn't, a
constraint and a model have drifted apart, and the *guard* is what tells you (it caught two
on first use, in the commit that introduced it).

## 4. Find the field's oracle, and a free validation target

- **Exact and closed-form beats installed and approximate.** A closed-form oracle (T⁶
  periods; the accounting identities) can be validated at zero tolerance and never
  silently changes version.
- **Adapters behind a protocol** for the real tools (CYTools, JAXVacua, cymetric), each
  raising a *named* gap when absent — never a silent fallback.
- **Free known-answer targets**: mirror symmetry in the landscape (h¹¹↔h²¹, χ→−χ); the
  paper's own reported numbers in an empirical field. Validation that costs nothing is
  validation you will actually run.

## 5. Verify against the source, not against memory

Fetch the paper. Re-derive, from the published parameters, at least three quantities the
authors state in prose (they reported ≈3% real, ≈6% nominal, ≈3% inflation; the derivation
returned 3.02 / 6.14 / 3.12). A transcription error breaks one, so the record is checked
rather than trusted.

**If a claim of yours is disproved by the source, retract it in the same commit** — in the
doc, in the test, in the board row. An uncorrected claim is worse than a missing one.

## 6. Build the falsifier before the result

Every guard needs a **seeded fault it goes red on**: a passive policy rule, a non-CRS
technology, a level-scale error table, a target leaked into a forecast's input. A guard
that cannot be shown to fire is decoration with a green light.

For a stability condition, run the analytic arm against a numeric one and require them to
agree (the Taylor boundary matched the eigen-search to 3·10⁻¹⁵ across calibrations). Two
implementations of the same algebra are one check; two *independent* ones are a proof.

## 7. The null is the unit; the result is part of the tier

No out-of-sample number means anything without "no change". And a model that **took** the
test and **lost** must not be trusted more than one that never took it:

> every slot earned **and** `loses_to_null` ⇒ still `weak`.

That rule cost us a clean row and was worth it. A checklist rewards effort; a board must
reward evidence.

## 8. Real-time, not revised

A backtest on revised data is not a forecast — the revision carries information the
forecaster did not have. Get vintages (they are often free and keyless). Then:

- **check units**: an old vintage may sit on a different *base* (rebasing, not revision).
  Compare growth within a vintage, never levels across vintages — our first run reported a
  50% "error" that was a rebasing, and the guard now refuses level-scale tables;
- **never let the target into the input**;
- **report the sample size** (26 forecasts from 9 vintages is a direction, not a verdict).

## 9. State the scope inside the artifact

The artifact — code, doc, PR, board row — carries its own boundary:

- `16 of 20 conditions proved, 4 are specifications, 0 unresolved`;
- `calibrated, not estimated`;
- `not SW: a three-equation subsystem at SW's published parameters`.

A reader should never have to ask what a number *is*. Where the boundary is a missing
capability, name it (`estimation is a project, not a slice`) instead of hiding it in prose.

## 10. Refuse the overclaim mechanically

Every claim carries evidence, and evidence that is a file must exist. Three refusals,
each with a seeded fault in the tests:

1. a claimed slot with no evidence;
2. a claimed slot whose evidence file does not exist;
3. an `out_of_sample` claim that names no real-time vintage source.

A model carrying any of them is scored **broken** regardless of everything else it passes.

## 11. Write the next step into the repo, not the transcript

Chat does not survive the session; the repo does. When a method stops at a boundary, the
boundary and its next step go into the doc — plus, where possible, a **registered
prediction** that says what the next run will find, so the work resumes with a test rather
than an opinion.

---

## The test, in one line

> **Count constraints by rank, not by list; prove the detector with a duplicate; source
> every constraint; derive the reference point; fetch the source; seed a fault under every
> guard; put the null in every table and the outcome in every tier; name the scope in the
> artifact; and refuse the overclaim mechanically.**

## Worked example — the nine slices this came from

| slice | what it demonstrated |
|---|---|
| the bar + roster | a fixed 9-slot bar, and an audit that refuses unsupported claims |
| NK 3-equation | 8/8 sympy proofs; a guard for a domain the field uses outside of |
| SW record | source fetched, re-derived, and our own claim retracted |
| vintages | keyless real-time access; the rebasing trap and its guard |
| SW inventory | 16 proved, 4 specifications, 0 unresolved — scope inside the artifact |
| NK out-of-sample | the null won, and the tier says so |
| inventory closed | a taxonomy that fits the evidence instead of the analogy |
| three-way | SW's own parameters did not rescue the forecast |
| constraint set | 11 constraints, 8 independent, measured by rank |

Full record: [economics-model-roster.md](economics-model-roster.md). Evidence:
`scripts/validate_economics_nk3.py` · `validate_economics_sw.py` ·
`validate_sw_structure.py` · `economics_realtime_forecast.py` · `economics_nk3_oos.py` ·
`economics_three_way.py` · `economics_constraint_set.py`.
