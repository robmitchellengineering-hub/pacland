"""One live end-to-end measurement: independent decontaminated baselines + a frontier pass."""
from pacland import benchmarks as b
from pacland import runner

print("=" * 70)
print("LIVE MEASUREMENT — independent decontaminated baselines")
print("=" * 70)
print()
print("measure_independent (synthetic + disguised + post-cutoff, judged):")
ind = b.measure_independent(b.llm_generator, n_synthetic=10, seed=0)
for label, m in ind.items():
    print(f"  {label:12s} recall={m['recall']:.2f}  baseline={m['baseline_recall']:.2f}  "
          f"problems={m['problems']}")

print()
print("=" * 70)
print("LIVE FRONTIER PASS — run_autonomous on the mass gap (budget=3)")
print("=" * 70)
print()
out = runner.run_autonomous(b.FRONTIER, rounds=1, budget=3)
r = out["rounds"][0]
print(f"run_id: {out['run_id']}")
print(f"survivors: {len(r['survivors'])}  falsified: {len(r['proposals'])}  open: {len(r['open'])}")
for s in r["survivors"]:
    print(f"  [SURVIVED] {s['statement'][:80]}")
    print(f"    challenges: {s.get('challenges', {})}")
for o in r["open"]:
    print(f"  [OPEN] {o['statement'][:80]}")
    print(f"    candidate_verdict: {o.get('candidate_verdict', 'none')}")
    print(f"    synthesized_test: {o.get('synthesized_test', {}).get('reason', o.get('synthesized_test', {}).get('note', ''))[:80]}")
