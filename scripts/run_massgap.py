"""One full frontier pass of the automated machine on the Yang-Mills mass gap."""
import json

from pacland import benchmarks as b
from pacland import runner

print("=" * 72)
print("MASS-GAP FRONTIER — run_autonomous (DeepSeek), budget=8")
print("=" * 72)
print()

out = runner.run_autonomous(b.FRONTIER, rounds=1, budget=8)
r = out["rounds"][0]
print(f"run_id: {out['run_id']}")
print(f"survivors: {len(r['survivors'])}   falsified: {len(r['proposals'])}   open: {len(r['open'])}")
print()

for s in r["survivors"]:
    print(f"[SURVIVED] {s['statement'][:100]}")
    print(f"    proof: {json.dumps(s.get('proof', {}))[:120]}")
    print()

for p in r["proposals"]:
    print(f"[FALSIFIED] {p['statement'][:100]}")
    print(f"    evidence: {p.get('evidence', '')[:120]}")
    print()

for o in r["open"]:
    print(f"[OPEN] {o['statement'][:100]}")
    print(f"    evidence: {o.get('evidence', '')[:100]}")
    synth = o.get("synthesized_test", {})
    print(f"    synthesized_test ran: {synth.get('ran')}  "
          f"candidate_verdict: {o.get('candidate_verdict', 'none')}")
    if not synth.get("ran"):
        print(f"    build reason: {synth.get('reason', '')[:100]}")
    challenges = o.get("challenges", {})
    decisive = {k: v for k, v in challenges.items() if v in ("FAIL", "NOT_APPLICABLE")}
    print(f"    challenges (decisive): {json.dumps(decisive)}")
    print()
