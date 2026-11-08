# The BMV experiment — a spec for "finding it"

**The theoretical verdict is already settled (kernel-checked):** a classical gravitational coupling
is impossible (Gleason's linearity + no-cloning's no-signaling + LOCC's no-entanglement). The
experiment is the *confirmation*, and it tests the **kind** of the coupling (quantum vs classical),
not its **value** (the race model proves the verdict is independent of `G`'s strength).

## What to build

1. **Two masses** `m ≈ 10⁻¹⁴ kg` (nanoparticles, e.g. diamond with a nitrogen-vacancy centre or a
   silica nanosphere), each prepared in a **spatial superposition** of width `Δx ≈ 10 µm`.
2. **Separation** `d ≈ 100 µm` between their centres.
3. **Hold** the superposition for `t ≈ 1 s` under a gravitational interaction only.
4. **Measure** the two-qubit density matrix; the entangling phase is
   `φ = 2 G m² t Δx² / (ħ d³) ≈ 0.013 rad`  (exact, from SI constants).

## What "found it" looks like

- **Classical gravity** (LOCC): the channel cannot entangle (kernel-checked), so the final state is
  **separable** — the two masses never show entanglement, no matter how long `t`.
- **Quantum gravity**: the state acquires the phase `φ`, entangling the masses; concurrence
  `C ≈ |φ|` at small `φ`, rising with `t`.
- **Verdict:** any measured entanglement **confirms** the coupling is quantum; its absence at the
  predicted `φ` would **falsify** our no-go.

## The three dials to reach φ ~ 1 (and their costs)

| dial | reach | cost |
|---|---|---|
| hold time `t → 10³ s` | φ → 12.7 | seismic/acoustic isolation |
| mass `m → 10⁻¹² kg` | φ → 127 | delocalizing a microgram (hard) |
| distance `d → 10 µm` | φ → 0.13 | Casimir/electrostatic control |

The sweet spot is **long `t` at small `d`**, avoiding the microgram-mass wall.

## The decoherence race (already won, on paper)

The proper-time decoherence competes with the entangling phase, but the exact two-body model shows
**entanglement survives with a nonzero floor** — decoherence reduces but does not erase it, and the
verdict is **independent of `G`'s strength** (only `G·t` appears). So the experiment is *not*
doomed by decoherence; it needs isolation, not a new theory.

## The one-sentence ask

A lab with optomechanical nanoparticles: prepare two masses in superposition, hold them 100 µm
apart for seconds, and look for the 0.013-rad entangling phase — that single measurement is the
empirical end of the whole constraint-first QG chain.
