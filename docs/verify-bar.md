# The verification bar — one machine, any discipline

Extracted from the macro-finance work (`docs/economics-model-roster.md`) because what
transfers between fields is the **machine**, not the answer. `src/pacland/bar.py` holds it;
each discipline supplies rows.

## The nine slots

| slot | what a model must show |
|---|---|
| `exact_structure` | an inventory of **constraints + labels**, proven not asserted |
| `deficit` | `m` computed two-tier — backcast and forecast — with its radius |
| `rule_of_three` | three independent checks, distinct failure modes, agreeing |
| `guard_suite` | what the model **forbids**, each guard red on a seeded fault |
| `out_of_sample` | measured against a **real-time vintage**, benchmarked |
| `benchmark` | the no-change null it must beat |
| `trust_entry` | a per-model tier with named evidence, on the board |
| `falsifiable_prediction` | a registered claim that could die |
| `reproduce` | one command, green |

A model's **kind** decides which it owes: `control`, `oracle`, `forecast`, `statistical`.

## Three refusals, each mechanical

1. a claimed slot with **no evidence**;
2. a claimed slot whose evidence is a **repo path that does not exist**;
3. an `out_of_sample` claim naming **no real-time vintage source** — a current-vintage
   backtest is not an out-of-sample test.

Plus the tier rule: **every slot earned and `loses_to_null` is still `weak`.** Taking the
test is not passing it.

## Two instantiations

**Macro-finance** — 6 rows, 4 clean (`economics/model_roster.py`).

**Climate** — 3 CMIP6 rows on the same bar (`climate/model_roster.py`), now with a **null**.

`climate/baseline.py` builds it: the observed trend continued (the analogue of persistence
for a warming series), plus a one-box ECS/ERF2x emulator per model, all scored on a
**real-time hindcast** — fit only on data as of each start year, CO2 extrapolated from that
date, target observed later:

| method | MAE (deg C) | vs trend null |
|---|---|---|
| persistence (strict no-change) | 0.270 | 3/7 |
| **trend (the null)** | **0.165** | — |
| emulator: GISS-E2-1-G | 0.183 | 3/7 |
| emulator: MPI-ESM1-2-HR | 0.178 | 2/7 |
| emulator: UKESM1-0-LL | 0.192 | 2/7 |

> **The trend null wins.** The emulators beat persistence and lose to the observed trend
> continued. The same shape as macro-finance: the null is the frontier, and structure has to
> earn its way past it.

The emulators are **not** the CMIP6 runs — they are one-box energy balances at each model's
published ECS and ERF2x. That is stated in the module, the report and the doc, because the
difference is the whole claim.

### The per-model deficit (`climate/model_deficit.py`)

The discipline-level deficit hid the thing a reader needs — *which* model is validated
against *how many* measurements:

| model | ECS | ERF2x | conservation | m | radius |
|---|---|---|---|---|---|
| GISS-E2-1-G | + | + | + | **3** | **0.78** |
| MPI-ESM1-2-HR | + | + | ✗ | 2 | 0.96 |
| UKESM1-0-LL | ✗ | + | ✗ | 1 | 1.36 |

**A failed test costs an observable, not a fraction.** The radius is set by how many
independent measured things a model survives, so MPI-ESM1-2-HR — which passes sensitivity
and forcing but leaks a ledger — is verified against one fewer of them. That is the
difference between a score and a certificate.

Climate now owes only `exact_structure` and `falsifiable_prediction` per model: an invariant
inventory proved rather than measured, and a registered claim.

The bar also reproduces the trust board's own distinction without being told it: GISS-E2-1-G
claims the conservation Rule of Three, MPI-ESM1-2-HR **cannot** (it leaks a ledger), and
UKESM1-0-LL claims only the two things true of it.

## What the transfer establishes, and what it does not

**Establishes:** the machine is discipline-agnostic — it ran on climate with no change, and
the *shape* of the missing verification is the same (a null, a real-time test, a per-model
deficit).

**Does not establish:** that climate's gaps are as deep as macro-finance's. Climate has real
invariants and a measurable oracle; macro-finance has definitional identities and a
non-identified parameter set. The bar names the gap; it does not rank the fields.
