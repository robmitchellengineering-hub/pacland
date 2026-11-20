"""Honest measurement: a DISTINCT judge (deepseek-reasoner) grades deepseek-chat's proposals."""
import json
import os

from pacland import benchmarks as b

print("=" * 70)
print(f"DISTINCT-JUDGE MEASUREMENT (generator={os.environ.get('SEXTANT_LLM_MODEL', '?')}, "
      f"judge={os.environ.get('SEXTANT_JUDGE_MODEL', '?')})")
print("=" * 70)
print(f"judge_is_distinct: {b.judge_is_distinct()}")
print()

print("Campaign A, paired seeds (3 repeats):")
rep = b.run_campaign_repeated(b.llm_generator, campaign="A", repeats=3)
print(json.dumps({k: rep[k] for k in ("recall_mean", "recall_stdev", "recalls")}, indent=2))
print()

print("Independent decontaminated baselines (distinct judge):")
ind = b.measure_independent(b.llm_generator, n_synthetic=10, seed=0)
for label, m in ind.items():
    print(f"  {label:12s} recall={m['recall']:.2f}  baseline={m['baseline_recall']:.2f}  "
          f"problems={m['problems']}")
