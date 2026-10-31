# Survey first — measure the room, then plan it

The engine runs on three numbers it does not know: the **noise floor**, the **modal quality factor**, and how
**busy** the channel is. All three are cheap to measure, and until they are measured the plan describes an
idealised room rather than *this* room.

**Reproduce:** `python3 scripts/wifi_plan.py` · `src/pacland/spectral/rf_survey.py`

## What to log

| field | how to get it | what it replaces |
|---|---|---|
| `noise_floor_dbm` | spectrum analyser across the band, antenna connected, **quiet period** | the assumed SNR |
| `occupancy` | fraction of a minute the channel sits above floor + 10 dB | nothing — it was unmodelled |
| `t60_s` | **RF impulse response** (swept sine or VNA), 60 dB decay on the envelope | the assumed Q = 200 |
| `mode_peaks_hz` | peaks in a fine sweep | nothing — it *tests* the Weyl prediction |

**`t60_s` is the important one.** `Q = π f T₆₀ / ln 1000`, and Q is the parameter that decides how many modes
overlap and therefore how many streams the room can separate. With T₆₀ unmeasured, the answer is unbounded
above.

**The impulse response is the same measurement AirMatrix already makes for audio**, pointed at an SDR or a
VNA instead of a loudspeaker and microphone. Swept-sine in, decay out — the machinery is built.

## Two ways the survey changes the answer

**1. Occupancy is a duty cycle, not a constant.** A channel busy `p` of the time raises average interference
power, so the honest figure is `SNR_clean − 10 log₁₀(1 + p)` under a conservative linear-in-power charge.
Reporting streams **against occupancy** — at 0.1, 0.4, 0.8 — turns the plan into advice about *which channel
to pick*, not just how many streams a quiet room supports.

**2. The measured peaks test the engine in situ.** `weyl_check` compares the detected mode count against the
Weyl prediction for the room's dimensions. That is the falsifier for the whole engine, and it costs one sweep.

## The in-situ test does NOT work in a large room at 5 GHz — and that is a finding

A plain spectrum sweep counts *peaks*, and peaks only exist if modes are resolvable. In a 30 m³ room at 5 GHz
the numbers are brutal:

| quantity | value |
|---|---|
| modes in a 100 MHz window (Weyl) | **~74,000** |
| modal width at Q ≈ 283 | **f/Q ≈ 18 MHz** |
| peaks a sweep can resolve in that window | **≈ 5** |

**The room is over-moded by four orders of magnitude**, so a sweep sees a smooth diffuse spectrum and no
peaks. Comparing 12 detected peaks against 74,303 predicted modes reports an error of 6,191× — which measures
the *method*, not the room.

**So the survey needs two modes of operation, and the module says which:**

1. **sparsely-moded spaces** — reverberation chambers, small cabinets, low bands — where a sweep resolves
   individual modes and the Weyl check is a real test;
2. **over-moded spaces** — normal rooms at 5 GHz — where the check must be done on the **impulse response**:
   deconvolve, extract decay times and sub-band energies, and compare *band energy* against the Weyl
   prediction rather than counting peaks.

**Which mode applies is computed, not guessed**: `modes_overlap = predicted_modes_per_Hz × f/Q`. Above ~1 the
peaks are gone and the sweep test is void. That number belongs in the survey output, before anyone draws a
conclusion from peaks.

## The falsifier, stated before any survey is run

> **If the measured mode count is within 10% of Weyl but the measured Q is far from the assumed value, the plan
> was right for the wrong reason and every stream count in it was a coincidence. If the mode count is off by
> more than 10%, the engine does not describe this room and no plan from it is usable.**

Both outcomes are findings. The first is the dangerous one, because it looks like success.

## And a bug this work exposed

The first placement planner put **transmit and receive antennas at the same positions**, making the channel
matrix symmetric — a degenerate structure that flatters its rank. It reported **4 of 4 streams** where the
two-lattice version of the same room reported **3 of 4**. Fixed: receive positions are now mirrored and raised,
never co-located.

**The lesson is the week's lesson again**: the number looked *better* than the previous one, and that is
exactly when to distrust it.
