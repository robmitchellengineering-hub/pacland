# The channel plan as an action, for AirMatrix's router automation

**`python3 scripts/channel_plan.py --json`** → `rf-channel-action@1`

AirMatrix has router control. That means this analysis does not end in a recommendation — **it ends in a transaction**,
and a transaction needs more than a channel number.

## What the automation receives

```json
{
  "format": "rf-channel-action@1",
  "observations": {"scans": 16, "networks": 33, "fading_floor_db": 16.0, "minimum_actionable_drop_db": 6.0},
  "actions": [
    {
      "band": "2.4 GHz",
      "from_channel": 11,
      "to_channel": 1,
      "current_interference_dbm": -50.1,
      "expected_interference_dbm": -74.1,
      "expected_drop_db": 24.0,
      "own_level_dbm": -33,
      "confidence": "high",
      "verify": {
        "method": "rescan the same spots after the change",
        "pass_if": "interference on ch 1 stays below -56.1 dBm",
        "fail_if": "interference rises above -56.1 dBm, or the link rate drops"
      },
      "rollback": {"to_channel": 11}
    }
  ],
  "refused": []
}
```

| field | why the automation needs it |
|---|---|
| **`from_channel`** | the change is only meaningful as a transition from a known state |
| **`expected_drop_db`** | a number to check afterwards, not a vibe |
| **`verify.pass_if` / `fail_if`** | the automation can decide, without a human, whether the change worked |
| **`rollback.to_channel`** | a bad outcome is one call away, and the previous channel is recorded |
| **`confidence`** | `high` at ≥12 dB, `medium` at ≥6 dB, **and nothing below 6 dB** |
| **`refused`** | the recommendations the tool declined to make, with the reason |

## The rule that matters most for automation

**The tool refuses to emit an action inside the fading it measured.** 16 dB at a fixed spot is the noise floor of this
instrument, so **a 3 dB "improvement" is not a signal — and an automation that acts on it will hunt between channels
all night.**

**`minimum_actionable_drop_db: 6.0` is in the envelope, not buried in code**, so the automation can see the threshold
it was given and a reviewer can disagree with it in one place.

## The loop this completes

```
survey  →  analysis  →  ACTION  →  apply (AirMatrix)  →  verify (rescan)  →  keep or roll back
```

**Every step now has a machine-readable artefact except the apply**, which is AirMatrix's to own. **The verify step is
the same scan capability the phone already has** — so the automation can close its own loop without new hardware.

## What it does not do yet

- **The verify step is specified, not wired.** The envelope says what to measure and what counts as failure; nothing
  calls it automatically yet.
- **Occupancy changes.** These are 16 snapshots taken while walking. An automation that re-plans twice a day, keeps its
  own history, and only acts when the margin **persists across two scans** would be far more robust than this.
- **No channel-width decision.** 20 MHz is assumed; 40/80 MHz changes the overlap and is a real lever that this analysis
  does not yet model.
