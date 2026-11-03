# Energy conjectures — registered, with their falsifiers

Five claims, each stated so it can be wrong, each with the observation that would kill it. Two are
computed here (arithmetic on published constants); three are **registered but not yet run**, and their
scripts say so rather than printing a number they have not earned.

The rule this file exists to enforce: **no conjecture is published before its falsifier is registered.**
The registry entry is what stops a claim being quietly softened after the data arrives.

| id | claim in one line | status |
|---|---|---|
| `lithium-mass-ceiling` | lithium mass balance, not cost, caps deployment near **3.2 TWh/yr** | computed (PASS-1) |
| `li-s-electrolyte-ceiling` | Li–S specific energy is set by the electrolyte/sulfur ratio — **680 Wh/kg at r = 3** | computed (PASS-1) |
| `fusion-confinement-exponent` | the 0.93 current exponent is between-machine; within-machine it is **0.55 ± 0.12** | registered |
| `climate-drift-ecs-transfer` | drift → ECS transfer is linear, **0.76 K per W/m²** | registered |
| `verification-joule-floor` | verification has a **µJ floor** (1–3 µJ/check) and a crossover at 10⁴–10⁶ ops | registered |

A *registered* claim has a falsifier and a script and no evidence yet. It is deliberately not "PASS-1":
PASS-1 means one run happened, and for these three it has not.

---

## 1 · `lithium-mass-ceiling` — computed

**Claim.** An LFP cell carries **0.41 kg LCE per kWh**, so at the 2024 world supply of **1.3 Mt LCE** the
deployment ceiling is **3.2 TWh/yr**; a 6 TWh/yr year needs ~2.5 Mt LCE.

**Derivation**, all published constants:
`1.75 kg LFP/kWh × (6.94/157.76) = 0.077 kg Li/kWh`; `× 5.32 kg LCE per kg Li = 0.41 kg LCE/kWh`;
`1.3 × 10⁹ kg / 0.41 kg/kWh = 3.17 × 10⁹ kWh`.

**Falsifier.** More than 5 TWh/yr of Li-ion produced from less than 1.5 Mt LCE primary supply, with no
more than a 2× lithium price rise.

**Reproduce:** `python3 scripts/energy_lithium_ceiling.py`

## 2 · `li-s-electrolyte-ceiling` — computed

**Claim.** A Li–S cell's specific energy is **set by the electrolyte/sulfur ratio**, not by cathode
chemistry: `E(q, r) = 2.15 q / [q(1.007 + 0.718 r) + 9.7]` Wh/kg, so `r = 3 µL/mg` caps a cell at
**680 Wh/kg** however good the cathode is.

**Falsifier.** Any full cell (≥ 1 Ah, ≥ 50 cycles, total mass) measured above **680 Wh/kg** at
`r ≥ 3 µL/mg`.

**Reproduce:** `python3 scripts/energy_li_s_ceiling.py`

**Note on what this is not:** the constants are a materials budget (foil thickness, separator, 6 %
packaging excluded), not a measured bill of materials. A 10 % error in the budget moves the cap by ~7 %.

## 3 · `fusion-confinement-exponent` — registered, not run

**Claim.** In the ITPA H-mode database the `I_p` exponent of IPB98(y,2) (**0.93**) is carried by
cross-machine collinearity with `B_T`, `R` and `n`. With per-machine offsets the **within-machine
exponent is 0.55 ± 0.12** (and the `B_T` exponent rises from 0.15 to ~0.40), which predicts
**τ_E = 0.85 ± 0.08 × IPB98** at ITER's point — so the 15 MA baseline needs `H98 ≈ 1.15`, not 1.0.

**Falsifier.** A within-machine exponent ≥ 0.85 (95 % CI), or SPARC's first H-mode τ_E within ±10 % of
the IPB98 line at 8.7 MA / 12.2 T.

**Why it is not computed here:** it needs the ITPA global H-mode database, which is not in this repository.
`scripts/energy_fusion_exponent.py` refuses without it and says how to supply it.

## 4 · `climate-drift-ecs-transfer` — registered, partly prepared

**Claim.** A model's conservation residual `ε` in piControl transfers **linearly** to its ECS:
slope of `log|ΔECS|` on `log|ε|` is 1.0 ± 0.2, with `|ΔECS|/|ε| ≈ 0.76 K per W/m²`
(AR6: 3.0 K / 3.93 W/m²), so a one-line correction to abrupt-4xCO2 ECS suffices.

**Falsifier.** Slope > 1.3 or < 0.7, or the ratio outside [0.4, 1.2] — which would mean drift
*amplifies* into ECS and every AR6-era number needs re-derivation.

**What exists here:** `data/climate/cmip6_drift.json` holds the three conservation ledgers for **19
models** (Irving et al. 2021). What is missing is the per-model ECS column (Zelinka et al. 2020); the
script joins them if the file is supplied and refuses otherwise.

## 5 · `verification-joule-floor` — registered, not run

**Claim.** Verification has an energy floor of **1–3 µJ per check** (process overhead, not the hash) and
a crossover at **10⁴–10⁶ operations per item**: above it, checking a witness beats re-executing the work;
below it, it loses.

**Falsifier.** A measured floor outside 0.3–10 µJ, or a crossover outside 10³–10⁷ operations per item.

**Why it is not computed here:** it is a measurement, not an arithmetic query. It needs one machine
(batched SHA-256d at 10⁶ scale) and belongs in a job, not in a documentation change.

---

## What this page deliberately does not contain

The value of the cosmological constant (no falsifier exists), ANEC/QNEC (already theorems — nothing to
fund), and any statement of the form "X matters". If a claim cannot be written as an exponent, a bound, or
an exact count, it is not admitted here.
