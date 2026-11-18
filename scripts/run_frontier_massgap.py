"""One frontier run: the mass gap (Campaign C). The LLM proposes, SEXTANT falsifies, report survivors."""
from pacland import runner

PROBLEM = ("does non-Abelian lattice Yang-Mills have a mass gap (exponential clustering) in the "
           "continuum limit at weak coupling in d >= 4")


def main() -> None:
    print("=" * 72)
    print("MASS-GAP FRONTIER RUN (Campaign C)")
    print("=" * 72)
    print()

    s = runner.LlmSearch()
    cands = s.generate(PROBLEM, 8)
    print(f"LLM PROPOSALS: {len(cands)} hypotheses, each run through SEXTANT falsifiers\n")
    survived = 0
    for c in cands:
        ran, ok, evidence = runner._falsify(c)
        if ran and ok:
            verdict = "SURVIVED"
            survived += 1
        elif ran:
            verdict = "FALSIFIED"
        else:
            verdict = "OPEN (no runnable falsifier)"
        pad = " " * 28
        print(f"[{verdict:27s}] {c.statement[:100]}")
        print(f"{pad} falsifier: {c.falsifier[:110]}")
        print(f"{pad} evidence:  {evidence[:140]}")
        print()
    print(f"LLM SURVIVORS: {survived}/{len(cands)} hypotheses survived falsification\n")

    eng = runner.DiscoveryEngine()
    r = eng.lifecycle(PROBLEM, budget=6)
    print("FULL ENGINE SCORE (all strategies):")
    per = sorted(r["score"]["per_strategy"].items(), key=lambda kv: -kv[1]["discoveries_per_effort"])
    for strat, m in per:
        print(f"  {strat:22s} discoveries={m['discoveries']} effort={m['effort']:.1f} "
              f"d/e={m['discoveries_per_effort']:.3f}")
    g = r["score"]["global"]
    print(f"  {'global':22s} discoveries={g['discoveries']} effort={g['effort']:.1f}")


if __name__ == "__main__":
    main()
