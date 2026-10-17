# L5 formalization — educability as verified knowledge transfer

This formalizes the meta-loop: how verified knowledge accumulates and transfers across
generations — and across *sources* — without redoing the search that produced it. It is
the PACLAND instantiation of Valiant's **educability** (2024).

Status: draft. Valiant's educability is a *concept/program*, not yet a theorem in the way
PAC learning and evolvability are; §2–§3 mark what is his and what is PACLAND's own
formalization.

---

## 1. The gap L4 leaves, and what educability adds

L4's population carries *implicit* memory — a distribution over vacua, subject to drift,
selection pressure, and loss. That memory is lossy: when a run ends, only the final
population survives, and nothing in it is *individually justified*.

Educability is the move from implicit population memory to **explicit, verified,
transferable knowledge**: a knowledge base `K_t` whose every entry carries a certificate.
That is what lets knowledge survive its producer and be reused by others.

## 2. Valiant's educability — and what it is not

Valiant's distinction (2024, *The Importance of Being Educable*):

- **Learning** — an agent acquires knowledge by its *own* interaction with the
  environment: its own examples, its own search, its own mistakes.
- **Educability** — an agent can *absorb knowledge created by others*: receive a
  hypothesis from an external source, **evaluate** whether it is consistent with the
  agent's own experience, and **assimilate** it — with far fewer resources than
  re-deriving it would take.

The computational core Valiant points to is exactly PAC-style *evaluation*: the ability
to test a hypothesis proposed by someone else against your own distribution and adopt it
if it passes. The emphasis is the **division of labor in knowledge creation** — one agent
does the expensive discovery; many agents do the cheap verification and adoption.

## 3. The PACLAND instantiation

Three objects define L5:

### 3.1 Knowledge unit

A verified partial result. Four kinds:

| Kind | Form | Certificate? |
|---|---|---|
| Verified candidate | vacuum `v` with error ≤ `b` | L3 certificate |
| Ruled-out region | subclass `V' ⊂ V` with error > ε on all of it | negative certificate |
| Constraint | an inequality/relation the map satisfies | verified against `D` |
| Surrogate model | fast evaluator of the map | **must** emit a certificate (non-goal of README) |

### 3.2 Evaluation primitive (assimilation test)

Given a *proposed* knowledge unit from any source, assimilate it iff both hold:

1. **It verifies** — its L3 certificate passes (with the two-level bound of
   `verification-formal.md`, Theorem 2).
2. **It is consistent** — it does not contradict any entry already in `K_t` beyond the
   union of their confidence budgets.

The evaluation primitive **is the L3 certificate**. This is the load-bearing fact:
educability does not need a new mechanism; it needs L3, applied to proposals instead of
to search output.

### 3.3 Assimilation rule

```
adopt(u)  ⇔  verify(u) ∧ consistent(u, K_t)
```

## 4. Why educability ≠ more search (the cheap-assimilation claim)

The cost of *producing* a verified hypothesis (L4 search) can be large — generations ×
certificate cost. The cost of *assimilating* it is **one L3 certificate** — polynomial in
`(1/ε, log 1/δ)`, and independent of what produced it.

**Claim (PACLAND's educability guarantee).** The marginal cost to the system of adopting
a *given* verified hypothesis is one certificate, regardless of the hypothesis's
provenance. This is what makes the division of labor real: the expensive search happens
once, the cheap verification-and-adoption happens arbitrarily many times.

This is the formal analogue of Valiant's "benefit from knowledge you did not derive."
Note the boundary honestly: this claim is about *assimilation cost*, not about the
*epistemic value* of what is assimilated — a cheaply-assimilated hypothesis can still be
wrong if its certificate is weak.

## 5. The meta-loop

```
K_0 = ∅
for each generation t:
    seeds   = draw from verified candidates in K_{t-1}          (not random)
    avoid   = constrain mutation away from ruled-out regions
    L4 runs = selection + mutation, certificate-only access
    emit    = certificates for best candidates + ruled-out regions
    K_t     = K_{t-1} ∪ { newly verified, consistent units }
external proposals (theorists, other theories, other runs) enter the same way:
    evaluate → assimilate → seed
```

Three consequences worth stating:

1. **Search composes with knowledge.** Each generation starts from verified ground
   rather than from scratch — the ecorithm upgrade over blind L4.
2. **External proposals are first-class.** A candidate vacuum proposed by a human for a
   reason (a symmetry, a known construction) does not require PACLAND to re-derive it;
   it requires one certificate. PACLAND is educable by the entire theoretical community,
   not only by its own search.
3. **The fallback is preserved.** This is the concrete mechanism behind
   `verification-formal.md` §6: if L4 dies (conjecture false), L5 survives as a
   *verifier-and-accumulator* of externally proposed hypotheses.

## 6. What is guaranteed, and what is not

| Guaranteed | Not guaranteed |
|---|---|
| Assimilated units have passed their own certificate | Assimilated units are *true* (they are (ε,δ)-close, per `open-questions.md`) |
| Assimilation cost is one certificate per unit | The knowledge base converges to a *complete* description |
| `K_t` is certificate-consistent at each step | `K_t` stays correct as certificates improve |

The "not guaranteed" column is not decoration; it is the failure mode of the next
section.

## 7. The failure mode: entrenchment, and the revision problem

Monotone assimilation has a real cost. Two ways it goes wrong:

1. **Entrenchment.** A wrong entry that passed a *weak* certificate (few samples, wide
   radius) now blocks *correct* knowledge that contradicts it — the consistency check
   (§3.2) rejects the newcomer.
2. **Stale verification.** A `K_t` entry certified at tolerance `ε₀` may fail a stronger
   certificate at `ε₁ < ε₀`. "Verified" is relative to a budget; budgets tighten.

So L5 needs **revision**, not just accumulation: periodically re-verify old entries
against the strongest current certificate, and retract or weaken those that fail. This
is belief revision, and it is the genuinely hard part — monotone accumulation is the easy
case, revision is where the system's honesty lives.

- Open: a revision policy with a cost model (how often to re-verify, which entries
  first), balancing the risk of entrenchment against the cost of re-certification.

## 8. Relation to the other layers

| Layer | Role in L5 |
|---|---|
| L1 | defines the space over which `K_t`'s units and regions are stated |
| L3 | **is** the evaluation primitive (§3.2); no new mechanism needed |
| L4 | a *producer* of knowledge units; also a *consumer* via seeding |
| L6 | untouched — `K_t` records *verified membership*, never *selection* |

The three Valiant ideas, now each with a layer, reuse each other:

- **L3 (PAC)** provides the evaluation primitive — the certificate.
- **L4 (evolvability)** consumes L3 as its statistical-query access to *search*.
- **L5 (educability)** consumes L3 as its evaluation primitive to *absorb* knowledge —
  including L4's output and the wider field's proposals.

## 9. Open items specific to L5

1. **Revision policy** (§7) — the belief-revision problem with a per-entry re-verification
   cost.
2. **Consistency semantics** — what "contradicts beyond confidence budgets" means
   precisely when two certificates have different `ε, δ`; a formal conflict measure.
3. **Provenance weighting** — should `K_t` weight a unit by *whose* certificate it is
   (an external source with unknown error model vs an internal run with a known `p_e`)?
   This is the trust problem, and it is not solved by a certificate alone.
4. **Negative-result units** — how to certify a *ruled-out region* efficiently without
   evaluating every vacuum in it; needs the same imperfect-oracle care as L3, applied
   to sets rather than points.

## 10. One-sentence summary

L5 is the layer that makes PACLAND **educable**: it verifies, accumulates, and reuses
knowledge — its own and the field's — at a marginal cost of one certificate per idea,
and its real research content is not the accumulation but the **revision**.
