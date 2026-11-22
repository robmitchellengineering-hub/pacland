# SEXTANT — Research Plan (ordered actions)

The master document (`MASTER-RESEARCH.md`) is the *why* and *what*. This is the *how*, in order. Each
action is a concrete build with a test and a PR; nothing is prose-only.

## The one metric (repeated so it is not lost)

**Closeness to a new, rigorous, volume-uniform lower bound for the physical Yang–Mills spectral gap.**
Tracked as each track's score = how many of A1–A5 its best candidate bound satisfies.

---

## Actions, in order

1. **Encode the tracks as code.** `research_program.py`: the four tracks (Gribov, Coulomb, RG,
   Curvature), the A1–A5 assumptions, each track's objective + falsification, and the `track_score` +
   `leaderboard` functions. *This is the "competing programmes" structure.*

2. **Extend the referee for the missing uniformity.** `bound_search.check_bound` gains R3
   (volume-uniformity) and R4 (continuum survival) checks, so a bound that is only finite-volume or
   only lattice is honestly refused. *This is the machine-checkable "A1 + A3" that the metric needs.*

3. **Upgrade synthesis beyond products.** `synthesis_bounds` currently combines bound *shapes* by
   product; upgrade it to combine *structures* (confinement × spectral, RP × weighted-inequality) so it
   searches the space that actually covers A1–A5.

4. **Wire each track into the engine.** Add each track as a hypothesis + runnable falsifier in
   `hypotheses.py` / `mass_gap_falsifiers.py`, so the engine *works* them (propose → falsify → record),
   not just lists them. The Coulomb track (Task C) and the RG track (Task A) have the most machinery
   already behind them.

5. **The withheld-problem validation gate.** A genuinely-independent problem (answer withheld from the
   engine) where the engine induces a candidate and the falsifier verifies it, and a re-run reproduces
   it. No discovery is credited until it passes.

6. **Run the race.** Start all four tracks; report each track's score after every round; the first to
   clear A1 + A3 (volume + continuum) is the leader, and the first to 5/5 is the result.

---

## The honest gate (never dropped)

Before placing confidence in the engine, it must pass a withheld, independent problem. "Infrastructure
is increasingly sophisticated" is not evidence of blind discovery — only a passed withheld problem is.
