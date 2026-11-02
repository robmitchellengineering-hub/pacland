"""The counting laws: detection probability, the detection limit, and how many species a budget resolves.

Every function here is a statement about a Poisson counting process with a contamination floor. No biology enters: λ is
"reads per species", ε is "the rate at which reads appear for something that is not there", and both are what a sequencing
run reports.
"""
from __future__ import annotations

import math


def detection_probability(mean_reads: float, reads_needed: int = 1) -> float:
    """P(at least `reads_needed` reads) when a species contributes `mean_reads` on average.

    Poisson by construction: reads are independent rare events, which is the one assumption the field agrees on. `reads_needed`
    defaults to 1 because a single read is the usual detection bar - and that is exactly why the contamination floor, not the
    read count, sets the limit.
    """
    if mean_reads <= 0:
        return 0.0
    if reads_needed <= 1:
        return 1.0 - math.exp(-mean_reads)
    # complement of the Poisson CDF, summed directly (small counts only)
    tail = sum(math.exp(-mean_reads) * mean_reads ** k / math.factorial(k) for k in range(reads_needed))
    return max(0.0, 1.0 - tail)


def contamination_floor(false_reads_per_sample: float, samples: int, confidence: float = 0.95) -> int:
    """How many reads a species must draw before it is more than the contamination.

    With `samples` samples each carrying a Poisson contamination mean, the background count is Poisson(samples * mean). A
    detection at `confidence` needs a read count above the background quantile - **the eDNA analogue of the 6 dB action
    floor**: below it, a detection is indistinguishable from what the process produces when nothing is there.
    """
    if samples <= 0:
        raise ValueError("samples must be positive")
    lam = max(false_reads_per_sample, 0.0) * samples
    if lam <= 0:
        return 1
    # smallest k with P(X <= k-1) <= confidence
    cdf, k = 0.0, 0
    term = math.exp(-lam)
    while True:
        cdf += term
        if cdf > confidence:
            return max(k, 1)
        k += 1
        term = math.exp(-lam) * lam ** k / math.factorial(k)


def detection_limit_reads(false_reads_per_sample: float, samples: int, confidence: float = 0.95) -> float:
    """The SPECIES' OWN mean read contribution needed to be detected at `confidence` above the contamination background.

    **The units are the trap, and it cost a test.** The contamination floor is a *total* read count; this returns the species'
    *contribution on top of the background*. At contamination 1.0 read/sample over 10 samples the background alone is 10 reads
    and the floor is 15, so a species needs only about 12 of its own - less than the floor, which looks wrong and is right.
    The operational reading is: *this many reads attributable to the species, over and above what the library produces anyway.*

    The requirement is that the expected count with the species present clears the background quantile at `confidence`, which
    makes the limit a property of **samples and contamination**, not of the species. That is the whole point: more samples
    lower the limit, and no amount of extra sequencing depth rescues a contaminated library.
    """
    floor = contamination_floor(false_reads_per_sample, samples, confidence)
    background = false_reads_per_sample * samples
    # invert Poisson: find mu with P(X >= floor | mu) = confidence
    lo, hi = 0.0, max(floor * 4.0, 10.0)
    for _ in range(200):
        mid = (lo + hi) / 2.0
        p = 1.0 - _poisson_cdf(floor - 1, mid + background)
        if p < confidence:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _poisson_cdf(k: int, mu: float) -> float:
    if k < 0:
        return 0.0
    term = math.exp(-mu)
    total = term
    for i in range(1, k + 1):
        term *= mu / i
        total += term
    return total


def distinguishable_species(read_budget: float, mean_reads_per_species: float, false_reads_per_sample: float = 0.0) -> int:
    """How many species a read budget can carry at a given detection reliability.

    The limit is not "reads divided by reads-per-species": species whose expected counts are within the Poisson noise of each
    other cannot be told apart, so the useful count is the number that clears the floor **and** stays separated by a stated
    margin. This returns how many fit, which is the eDNA version of a mode count.
    """
    if mean_reads_per_species <= 0:
        return 0
    floor = max(false_reads_per_sample * 10.0, 1.0)
    usable = read_budget / mean_reads_per_species
    separated = usable / (1.0 + floor / max(mean_reads_per_species, 1e-9))
    return max(int(separated), 0)


def sample_requirement(false_reads_per_sample: float, target_limit_reads: float, confidence: float = 0.95) -> int:
    """How many samples are needed to push the detection limit down to `target_limit_reads`.

    The inverse of [`detection_limit_reads`], and the operationally useful direction: an operator has a target ("I need to see a
    species contributing 20 reads") and this says what the sampling effort has to be.
    """
    if target_limit_reads <= 0:
        raise ValueError("the target limit must be positive")
    if false_reads_per_sample <= 0:
        return 1
    for n in range(1, 10001):
        if detection_limit_reads(false_reads_per_sample, n, confidence) <= target_limit_reads:
            return n
    return 10001
