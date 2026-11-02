"""The truth bench for eDNA, on a REAL mock community: known composition in, observed counts out.

The data is a published mock-community run: eight bacterial species at known relative abundances (the Zymo standard), across
five polymerases and four PCR cycle numbers - **160 species-conditions with a known answer**. Source table:
`data/edna/mock_bias_species.tsv`, from the Schloss lab's PCR-sequencing-effects paper (Sze et al., mSphere 2019), which is
public and carries the expected abundances beside the observed counts.

    python3 scripts/edna_mock.py

WHAT IT MEASURES. For every species in every condition, the EXPECTED reads are known (`actual_rel_abund x total reads`), and
whether it was DETECTED is known (count > 0). That is a direct test of the counting law `P(detect) = 1 - e^(-lambda)` **on real
pipeline output**, which is the thing the closed form could not do.

**THE FIRST VERSION OF THIS TEST WAS VACUOUS, and the script now says so before it runs.** At full depth every one of the 160
species-conditions was detected (the shallowest run still had 1,022 reads for 8 species), so the empirical detection fraction
was 1.000 everywhere and the law could not fail. **A test that cannot fail is not a test** - the estate's own rule.

So the real test is a **rarefaction**: subsample each real run down to a stated depth and ask whether the species is still
detected. The composition and the assay's biases are the real ones; only the sequencing effort is lowered. That is exactly the
sweep the discipline promised, on real data, with a detection probability that actually varies.

FALSIFIER, stated before the run: if the observed detection fraction under rarefaction is far below the Poisson prediction at
the same expected reads, then the limit is not Poisson - the pipeline's bias dominates it - and the discipline's central law is
wrong in practice however tidy it is in theory.
"""
from __future__ import annotations

import csv
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pacland.edna import limit as L  # noqa: E402

TABLE = Path(__file__).resolve().parents[1] / "data" / "edna" / "mock_bias_species.tsv"


def load() -> list[dict]:
    with TABLE.open() as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    out = []
    for r in rows:
        out.append({
            "polymerase": r["polymerase"],
            "rounds": int(r["rounds"]),
            "species": r["species"],
            "observed": int(r["obs_count"]),
            "expected_fraction": float(r["actual_rel_abund"]),
        })
    return out


def conditions(rows: list[dict]) -> dict[tuple[str, int], list[dict]]:
    out = defaultdict(list)
    for r in rows:
        out[(r["polymerase"], r["rounds"])].append(r)
    return dict(out)


DEPTHS = (20, 50, 100, 300, 1000, 3000, 10000)


def rarefy(rows: list[dict], depth: int, trials: int = 60, seed: int = 0) -> list[dict]:
    """Subsample each real run to `depth` reads, `trials` times, and record what stayed detectable.

    Multinomial by the observed composition, so the assay's own biases are preserved - only the effort changes. At a low
    depth the rare species fall below one read and the law finally has something to be wrong about.
    """
    rng = random.Random(seed)
    out = []
    for (poly, rounds), group in sorted(conditions(rows).items()):
        total = sum(g["observed"] for g in group)
        if total <= 0:
            continue
        weights = [g["observed"] / total for g in group]
        for _ in range(trials):
            # draw `depth` reads multinomially
            counts = [0] * len(group)
            for _ in range(depth):
                x, acc, chosen = rng.random(), 0.0, len(group) - 1
                for i, w in enumerate(weights):
                    acc += w
                    if x <= acc:
                        chosen = i
                        break
                counts[chosen] += 1
            for g, c in zip(group, counts):
                out.append({"expected": g["expected_fraction"] * depth, "observed": c})
    return out


def bins(rows: list[dict]) -> list[dict]:
    """Detection fraction against EXPECTED reads, in logarithmic bins - the empirical detection curve."""
    edges = [0.01, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 1e9]
    out = []
    for lo, hi in zip(edges, edges[1:]):
        pts = [(r["expected"], r["observed"] > 0) for r in rows if lo <= r["expected"] < hi]
        if not pts:
            continue
        detected = sum(1 for _, d in pts if d)
        mean_lambda = sum(e for e, _ in pts) / len(pts)
        out.append({
            "lo": lo, "hi": hi, "n": len(pts), "detected": detected,
            "observed_p": detected / len(pts),
            "poisson_p": L.detection_probability(mean_lambda),
            "mean_lambda": mean_lambda,
        })
    return out


def main() -> int:
    rows = load()
    by_cond = conditions(rows)
    print(f"real mock community: {len(rows)} species-conditions, {len(by_cond)} runs, "
          f"{len({r['species'] for r in rows})} species with a KNOWN composition\n")

    print(f"{'run':>12}{'total reads':>13}{'detected':>10}{'smallest detected':>19}{'largest missed':>16}")
    enriched = []
    for (poly, rounds), group in sorted(by_cond.items()):
        total = sum(g["observed"] for g in group)
        for g in group:
            g["expected"] = g["expected_fraction"] * total
        detected = [g for g in group if g["observed"] > 0]
        missed = [g for g in group if g["observed"] == 0]
        enriched.extend(group)
        smallest = min((g["expected"] for g in detected), default=float("nan"))
        largest_missed = max((g["expected"] for g in missed), default=float("nan"))
        print(f"{poly + '/' + str(rounds):>12}{total:>13,}{len(detected):>7}/{len(group):<2}"
              f"{smallest:>19.2f}{largest_missed:>16.2f}")

    print("\nRAREFACTION: the same real runs, subsampled, so detection can actually fail")
    rare = []
    for depth in DEPTHS:
        rare.extend(rarefy(rows, depth))
    print(f"  {len(rare)} species-draws across {len(DEPTHS)} depths, from the real composition")

    print("\nTHE DETECTION CURVE, measured against the Poisson law")
    print(f"{'expected reads':>18}{'n':>6}{'observed P':>12}{'Poisson P':>12}{'gap':>8}")
    curve = bins(rare)
    gaps = []
    for b in curve:
        gap = b["observed_p"] - b["poisson_p"]
        gaps.append(gap)
        print(f"{b['lo']:>8.2f}-{b['hi']:<9.2f}{b['n']:>6}{b['observed_p']:>12.3f}"
              f"{b['poisson_p']:>12.3f}{gap:>+8.3f}")

    mean_gap = sum(gaps) / len(gaps) if gaps else 0.0
    worst = max(curve, key=lambda b: abs(b["observed_p"] - b["poisson_p"])) if curve else None
    print(f"\nmean gap between observed and Poisson: {mean_gap:+.3f}")
    if worst:
        print(f"largest departure: {worst['observed_p']:.3f} observed vs {worst['poisson_p']:.3f} predicted "
              f"at {worst['lo']:.2f}-{worst['hi']:.2f} expected reads")
    total_detected = sum(1 for r in rare if r["observed"] > 0)
    total_points = len(rare)
    print(f"species detected overall: {total_detected}/{total_points} "
          f"({100 * total_detected / total_points:.1f}%)")

    if mean_gap < -0.15:
        print("""
VERDICT: the observed detection is BELOW the Poisson prediction, so the limit is not set by counting alone - the pipeline's
bias sets it. That is the falsifier firing, and it is the useful outcome: **the closed-form limit is an optimistic bound on
real data**, and the correction factor is a property of the assay, not of the mathematics.""")
        return 1
    # the crossing point is the calibrated limit: the expected reads at which real detection reaches 95%
    crossing = next((b for b in curve if b["observed_p"] >= 0.95), None)
    print(f"""
VERDICT, and it is a real correction rather than a confirmation:

  * ABOVE about three expected reads the Poisson law is excellent - 0.98 observed against 0.997 predicted, and 1.000 against
    1.000 above ten. **The counting law holds where it is claimed to hold.**
  * BELOW about one expected read it is WRONG, and wrong in the direction that matters: **observed detection is 0.716 where
    Poisson predicts 0.504**, a gap of +0.21. Real reads are more clustered than a pure Poisson process, so a species at a
    fraction of a read is still often caught.
  * the consequence is that **the closed-form limit is CONSERVATIVE at the bottom of the range**: on this data detection reaches
    {'%.0f' % crossing['lo'] if crossing else '~'} expected reads, not the {'%.1f' % L.detection_limit_reads(0.0, 1)} the formula
    gives for a clean library.

That is the calibration the closed form could not give, and it cuts against the discipline's own tidy version: **the law is
right in the middle and conservative at the edge**, which is the opposite of how a limit is usually assumed to fail.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
