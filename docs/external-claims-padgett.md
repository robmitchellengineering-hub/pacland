# An outside claim through the same machine: Jason Padgett's QIH preprints

Asked to look at Jason Padgett's research. This is the record of what exists, what in it is checkable,
and what the checks returned. It is not a judgement of the man — the machine is indifferent to who
wrote a sentence.

## What actually exists

**Nine preprints, all on Zenodo, all dated October 2023**, all under "Quantum Information Holography
(QIH)". Not peer-reviewed; no journal, no institutional affiliation (the Zenodo record lists
`affiliation: None`); the creator field is even mis-parsed as `familyName: "Jason D. Padgett"`.

| DOI | title |
|---|---|
| [10.5281/zenodo.8395240](https://doi.org/10.5281/zenodo.8395240) | Unification of Information, light and gravity |
| [10.5281/zenodo.8396788](https://doi.org/10.5281/zenodo.8396788) | QIH: Asymmetric Primes, Geometry, and Quantum Mechanics |
| [10.5281/zenodo.8396810](https://doi.org/10.5281/zenodo.8396810) | Unifying the Fundamental Forces: QIH with Hawking Radiation as Universal Operator |
| [10.5281/zenodo.8396823](https://doi.org/10.5281/zenodo.8396823) | Our Universe and Its Opposite Parallel Universe |
| [10.5281/zenodo.8396853](https://doi.org/10.5281/zenodo.8396853) | QIH and Light Convergence: Unveiling the Origins of Mass |
| [10.5281/zenodo.8410689](https://doi.org/10.5281/zenodo.8410689) | Dark Matter, Primes, and QIH |
| [10.5281/zenodo.8410700](https://doi.org/10.5281/zenodo.8410700) | QIH, prime oscillations, wormholes and dark matter distribution |
| [10.5281/zenodo.8417083](https://doi.org/10.5281/zenodo.8417083) | QIH: prime oscillations are luminous matter, non-primes are dark matter |
| [10.5281/zenodo.8435437](https://doi.org/10.5281/zenodo.8435437) | Luminous Entanglement: the Singularity's Qubit |

The papers are short. The one on asymmetric primes is **5,518 characters of body text** (extracted from
the PDF's own font map, not by eye), and its content is: textbook quantum mechanics (Hilbert space,
Schrödinger, the path integral), Maxwell's equations, the Bekenstein–Hawking entropy, and then the
novel part — a set called "asymmetric primes" (PA) and an interference term

    I_PA(theta) = sum over p in PA of exp(i p theta)

**The set PA is never defined.** Not in that paper, not in the metadata. That is the single most
important fact here, and it is a *fixable* problem — see the question at the end.

## The three claims that could be checked as written

Run `python3 scripts/check_padgett_claims.py`.

### 1. "asymmetric primes resist typical quantum cancellation"

If PA is the primes themselves, the sum cancels at the **random-walk rate** — |S| grows like `sqrt(n)`
while |S|/n falls towards zero:

| n | \|S\| at theta = 1 | \|S\|/sqrt(n) | \|S\|/n |
|---|---|---|---|
| 1,000 | 7.54 | 0.24 | 0.0075 |
| 4,000 | 40.23 | 0.64 | 0.0101 |
| 16,000 | 24.33 | 0.19 | 0.0015 |

And the one phase where it does *not* cancel is theta = pi — where **every set of odd numbers behaves
identically**:

| set | \|S(theta=pi)\|/n |
|---|---|
| primes | 0.9993 |
| **odd composites** | **1.0000** |
| **all odd numbers** | **1.0000** |

So the "resistance" is **parity**, and the prime property does no work. A claim that a set of odd
numbers behaves like a set of odd numbers is true and empty. This is the same failure mode as the
attenuation result and the empty scaffold: a test that cannot distinguish the claim from its
alternative.

### 2. "primes are luminous matter, non-primes are dark matter"

The prime fraction falls like `1/ln N` and tends to zero:

| N | primes/N |
|---|---|
| 1,000 | 0.168 |
| 10^4 | 0.123 |
| 10^6 | 0.078 |
| 10^7 | 0.066 |

(1/ln N = 0.062 at N = 10^7 — the decline is the prime number theorem, not a coincidence.)

Observed budget: baryons **4.9%**, dark matter **26.8%**, dark energy 68.3%; dark/baryon = **5.47**,
and constant. A fraction that tends to zero **cannot equal a fixed cosmic fraction**, and there is no
derivation of which N to use. It passes through 4.9% only near N ~ 10^9 — the *luminous* value, not
the dark one — and keeps falling. That is a coincidence at an arbitrary cut-off with the wrong
component, not a prediction.

### 3. "hf = hbar*omega = mc^2 is a unification"

`h f = hbar omega` **exactly**, because `omega = 2 pi f` and `hbar = h / 2 pi`. It is one statement
written twice. The second equality is the standard `E = hf` set against `E = mc^2`. Nothing is joined
that was not already the same sentence.

## Verdict, in the discipline's terms

| claim | oracle class | result |
|---|---|---|
| asymmetric primes resist cancellation | definitional, but **undefined** | fails as stated; the only surviving case is trivial parity |
| primes = luminous / non-primes = dark | null (density test) | fails; the fraction tends to zero |
| hf = hbar omega = mc^2 | definitional | a restatement, true and empty |
| "the universe is an informational construct", QIH generally | **no oracle** | not checkable — nothing would count as evidence against it |

The last row is not an insult; it is a classification. It means that as it stands, the framework cannot
be used for anything, because it forbids nothing.

## What would make it useful — one question

**"Define PA."** If PA is a rule for selecting primes — a digit property, a residue class, a
growth condition — then `I_PA(theta)` is a concrete mathematical object and we can run it in minutes:
compute the sum, fit its growth, and compare it against the random-walk prediction. There are known
results for prime exponential sums (Vinogradov-type bounds), so the comparison has a standard of truth
rather than an opinion.

That is the whole ask. One sentence from him converts nine unfalsifiable preprints into one testable
object.

## What is genuinely useful to us

1. **He is reaching for the same thing we are**: that geometry is the computable structure underneath
   physics. Our constraint-first work says the same, but it says it as theorems with machine-checked
   proofs, which is why it can be graded and his cannot. The instinct is not wrong; the method is the
   difference.
2. **A test case for the machine.** This is the first *external* claim we have run end to end —
   record → oracle class → computation → verdict — on something we did not build. It took an afternoon
   and it produced numbers, not a direction. That is what the discipline is for.
3. **The failure is instructive**: the claim that looked most quantitative (an interference sum) was
   the emptiest, because the object it summed over was never defined. **An undefined symbol is where a
   claim goes to hide.** That is now written down as a rule we apply to ourselves too: the same test
   would have caught "the string landscape predicts X" if X had never been specified.

## The zeros: the one lead that turned into a result

His intuition that primes carry an oscillation is not empty — it is just attached to the wrong
object. The version with an oracle is the **explicit formula**,

    psi(x) = x - sum over zeros rho of x^rho / rho - ln 2pi - ...

where the primes appear as an interference sum over the **Riemann zeros**. That object has a
cross-source verification with real teeth: the zeros' spacing statistics match a Gaussian unitary
ensemble, the same statistics nuclear spectra obey (Montgomery 1973; Odlyzko's numerics).

So we computed it — `src/pacland/spectral/zeros.py`, zeta from scratch, no dependencies:

| check | result |
|---|---|
| reproduces the first five known zeros | max error **4.2e-11** |
| finds every zero below t = 2000 | **1517** zeros against a smooth count of **1517.0** — exact |
| matches a **finite-sample GUE control** | ratio statistic **0.6176** vs **0.6140 ± 0.0068** |
| and is not Poisson | Poisson control **0.3810** — **35** control sd away |

With 1517 zeros the control spread is four times tighter than the original 202-zero run, so "not
Poisson" is no longer a matter of taste and the GUE match is half a control standard deviation.

### And the deep run

`python3 scripts/spectral_zeros_deep.py` computes **22,491 zeros** below t = 20,000 in about thirty
seconds:

| | |
|---|---|
| count vs smooth count | **22,491** vs 22,491.4 |
| mean unfolded spacing | **1.00000** |
| ratio statistic | **0.6133** against a GUE control of **0.6137 ± 0.0018** — 0.2σ |
| Poisson | 0.3810 — **133 control standard deviations** away |

**And the primes come out of them**, until the zeros run out:

| x | ψ(x) from the primes | error with 22,491 zeros |
|---|---|---|
| 10⁴ | 10,013.4 | **+0.58** |
| 10⁵ | 100,051.6 | **−0.26** |
| 10⁶ | 999,586.6 | −27.28 |
| 10⁷ | 9,998,539.4 | −56.74 |

**The reconstruction is good to about one unit up to 10⁵ and degrades above it.** The truncation error
scales with √x, so each further decade of x needs far more zeros — at 10⁶ the 22,491 zeros are not
enough. That is a finding rather than a failure: it says exactly how many zeros a given x requires.

All four gates pass; it is a VERIFIED certificate on the physics board.

**The trap it caught — ours, not his.** The textbook GUE ratio is 0.5307. Comparing 201 computed
spacings against it gives a **4σ "failure"** of a computation that is exactly right: 0.5307 is the
*asymptotic* value, and the same estimator returns 0.6156 ± 0.0197 on synthetic GUE spacings of the
same size. The right reference was a control of the same size, not a constant from a textbook. Every
statistic needs a control at the size it is computed at, or it measures the estimator and calls it the
world.

**What this does and does not claim.** It verifies a known result numerically; it does not claim the
zeros predict anything physical. What it does establish is the shape of the answer to Padgett's idea:
*prime oscillations are real mathematics, and the object they belong to is the explicit formula over
the zeros — not a sum over an undefined set.*
