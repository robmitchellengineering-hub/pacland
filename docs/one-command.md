# One command, one room, everything — `rf_plan.py`

```
python3 scripts/rf_plan.py --room 3,4,2.5 --band 5.18 --antennas 4 --snr 20
python3 scripts/rf_plan.py --room 3,4,2.5 --band 5.18 --antennas 4 --iw-link link.txt
python3 scripts/rf_plan.py --room 3,2.5,2.2 --band 0.3 --chamber
```

**One entry point.** The chamber analysis was a second script for one round; it is now a flag on the same command,
because a customer has one room and should not have to know which of our tools to open.

## What it prints, and the status of each line

| section | status |
|---|---|
| 1 mode structure | **PASS-2** — Weyl to 0.004%, degeneracy counted |
| 2 streams | **PASS-2** — 3–4 of 4 at 20 dB, across Q = 100…400 and three heights |
| 3 placement levers | **PASS-2** — receiver height is worth up to one stream |
| 4 chamber question | **closed form PASS-2, rule comparison PASS-1** — no chamber has been measured |
| 5 thermal ceiling | **PASS-2** — derived *and* simulated (and the constant was corrected from 2 to 4) |

And a closing block naming **what would falsify it**, with the measurement that settles it.

**Every section carries its mark because the marks are now enforced** by `tests/test_claims_registry.py` against
`docs/claims.json` — a claim cannot be promoted without two independent evidence lines.

## The two defects this consolidation caught

1. **Section 4 claimed PASS-2 for two different things.** The closed-form LUF is PASS-2; the claim that the
   rule of thumb is optimistic is **PASS-1**, because no chamber has been measured. One line, two statuses, and the
   line was printing the stronger one. **Now it names both.**
2. **A test asserted `PASS-1` appeared anywhere in the output.** When the thermal bound was promoted to PASS-2, the
   test failed — not because the output was wrong, but because the test was pinned to a *value* instead of to the
   *rule*. **It now checks that every numbered section carries a mark**, which is the property that matters.

## `--json`: the plan as data

A plan that only prints prose cannot be put in a report, a ticket or a test fixture. `--json` emits the same
figures with the same statuses:

```json
{
  "format": "rf-plan@1",
  "modes":    {"exact": 1296344, "weyl": 1295100, "weyl_error": -0.00096, "degenerate_fraction": 0.84, "status": "PASS-2"},
  "streams":  {"ceiling": 4, "across_heights": [3, 4], "status": "PASS-2"},
  "chamber":  {"luf_rule_hz": 1.12e8, "luf_density_hz": 1.93e8, "ratio": 1.71,
               "status": "closed form PASS-2, rule comparison PASS-1"},
  "thermal":  {"samples_per_bit": 3820, "status": "PASS-2"},
  "falsifier": {"exceeds_ceiling_above": 4, "falling_short_below": 3}
}
```

**Every block carries its own `status`**, so a consumer cannot pick a number out of the JSON and quote it as
settled — the status travels with it. That is the registry rule applied to a data format: **a status belongs to a
claim, not to a document.**

With `--iw-link`, the JSON carries the measured link and a **`discriminating`** flag:

```json
"measured": {"ssid": "Telstra3696", "band": "2.4 GHz", "nss": 2, "mcs": 15, "discriminating": false}
```

**`false` is the honest answer for a 2 × 2 link**: a ceiling of 2 cannot be beaten by an observation of 2, so this
row cannot falsify anything. A consumer that ignores the flag will read "consistent" as "confirmed", which is the
exact error the flag exists to prevent.

## The rule this file keeps

**A status belongs to a claim, not to a section of a report.** Where a section mixes a verified computation with an
unverified comparison, it must say which is which — because the reader will average them otherwise.
