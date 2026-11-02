# Is our question well-posed? A reply to Woit's charge, in his terms

Peter Woit's criticism of the string programme includes one sentence that applies to us and is not aimed at string
theory at all:

> **"it's not like there's some kind of well-defined thing you can write down… that's not the kind of problem it is
> at all"** — *Not Even Wrong* interview, 01:06:35

That is a denial that **enumeration** is a well-posed route to an answer. This page answers it not with a defence of
string theory but with a **criterion** and an audit of our own record against it.

## The criterion

**A question is well-posed when it terminates in a theorem or an exact count. It is not well-posed when it
terminates only in a sampling with a budget.**

The distinction is not rhetorical — it is what separates two kinds of number in our own repository, and the split
was visible before Woit was read. A sampling can be improved but never concluded; a theorem or an exact count
**cannot be revised by a bigger run**, and that is precisely the property a well-posed answer must have.

## What we claim is well-posed

| result | kind | where |
|---|---|---|
| `max |N| = b3` | **theorem** (|N| ≤ 2n = b3, attained) | `exactness/tadpole_bound.py` |
| conifold coefficients `37/30`, `2309/1800` | **exact rationals** | `periods/conifold_recursion.py` |
| ζ zeros to 6.4e-13 | **exact count against a known spectrum** | `spectral/zeros.py` |
| content law `A = 8.554` (intervals agree to 0.6%) | **exact count, closed form** | `exactness/b3_scaling.py` |
| gauge quotient: 1 orbit removed in 531,441 | **exact count** | `exactness/landscape_count.py` |

Each of these terminates. None of them can be overturned by running longer.

## What we do NOT claim is well-posed — and hereby demote

| claim | why it fails the criterion |
|---|---|
| the "accessibility minimum" near `b3 = 12` | a **sampling with a budget** (`n_batch`, `max_batches`); five candidate explanations eliminated, the sixth still open |
| the `5.05×` measure-dependence | **measure-dependent by construction** — it reports the spread of conventions, not a fact about nature |
| the `b3 = 6` yield `0.1325`/try | an **artefact of the `n_target = 20` cap**, not a rate |
| the "two-instrument regime change" near `b3 = 10` | half of it is a sampler observable; only the corpus half (`N/b3` collapse breaking at `b3 = 10`) stands |

**These are demoted, not withdrawn.** They are recorded, with their windows, as observations about our instruments.

## The measured number we claim to reproduce

Woit's own accepted bar **[01:05:56]** is: *"all those numbers… it will show you how to calculate them."* He does
**not** require uniqueness — a point worth stating because most defences of string theory assume he does.

We claim: **the first nontrivial zeros of the Riemann zeta function to 6.4e-13**, computed from Euler–Maclaurin and
Riemann–Siegel in `spectral/zeros.py`, agree with the literature values. That is a measured number, reproduced by
our own code, and it is the standard Woit says he would accept.

## What this implies for the guiding goal

Unifying string theory is retained as the **direction**, not as a claim about a unique theory. What changes is the
**admission test** for anything we publish: it must terminate in a theorem or an exact count, or it must be labelled
an instrument observation. A programme that cannot state which of its numbers are of which kind is doing exactly what
Woit accuses the string community of — and that accusation would then be correct.

## What would change our mind

If a question we currently class as **empirical** can be shown to terminate — e.g. if the accessibility series turns
out to be a closed form in `b3` rather than a budget effect — then it belongs in the first table. Conversely, if one
of the "theorems" turns out to depend on a window choice, it moves to the second. The audit is a live classification,
not a laurel.
