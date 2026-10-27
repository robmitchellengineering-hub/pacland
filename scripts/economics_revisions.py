#!/usr/bin/env python3
"""What the first GDP print is worth: biased, un-exploitable, and still the best guess.

    python3 scripts/economics_revisions.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.economics import revisions  # noqa: E402


def main() -> int:
    s = revisions.summary()
    e = revisions.exploitability()
    b = revisions.benchmarks()
    print("PACLAND · economics — the first GDP print, measured\n")
    print(f"revisions          n={s['n']}  mean {s['mean_revision_pp']:+.3f} pp  "
          f"sd {s['sd_pp']:.3f}  t={s['t_stat']:.2f}")
    print(f"direction          {s['n_upward']}/{s['n']} upward ({s['share_upward']:.0%}), "
          f"exact sign-test p = {s['sign_test_p']:.3f}")
    print(f"memory             AR(1) = {s['ar1']:.3f}  -> "
          f"{'has memory' if s['has_memory'] else 'no usable memory'}")
    print(f"\nexploitability     bias fitted on {e['train_n']} quarters = "
          f"{e['train_bias_pp']:+.3f} pp")
    print(f"                   out of sample: raw {e['mae_raw']:.3f} pp vs corrected "
          f"{e['mae_corrected']:.3f} pp  -> ratio {e['ratio']:.2f}x")
    print(f"\nbenchmarks (against the FINAL number, n={b['n']}):")
    print(f"                   zero-growth null {b['null_vs_final']:.2f} pp")
    print(f"                   official first print {b['advance_vs_final']:.2f} pp")
    print(f"                   Atlanta Fed nowcast {b['nowcast_vs_final']:.2f} pp")
    print(f"                   nowcast against ITS OWN target {b['nowcast_vs_advance']:.2f} pp")
    report = revisions.audit()
    print(f"\n{report['n_pass']}/{report['n']} checks pass, each with its seeded fault fired")
    print(f"VERDICT: {s['verdict']}.")
    print(f"         {e['verdict']}.")
    print(f"         {b['verdict']}.")
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
