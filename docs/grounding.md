# The grounding — how the method knows it is measuring the right things

This is the shared foundation for **every** discipline the verification spine is
applied to. It answers the one question that never goes away: *how do you know you
are picking the right things to verify?* The answer has three parts, and every
discipline must satisfy all three.

## 1. Constraints pick themselves — verify what is forbidden, not what is predicted

A **necessary condition** is self-justifying: it has a yes/no answer that does not
depend on opinion. Each discipline's guards *are* its necessary conditions.

| discipline | its necessary conditions (what must hold) |
|---|---|
| **landscape** | the tadpole `N = FᵀJH` is the unique symplectic invariant; flux quantization; anomaly cancellation |
| **climate** | energy + mass conservation; the energy / water / carbon budgets close |
| **drugs** | net charge, valence, synthesizability — the molecule's forbidden states |
| **ai (Valiant Verification)** | a gate passes by name; a guard fires under its seeded mutation; the ledger names a RULE + GUARD |

An artifact that violates one of these is wrong *before any other question is asked*.
The method therefore measures the things that cannot be argued with, not the things
that look interesting.

## 2. The deficit is a conservative lower bound — measured + computable + validated

An observable counts toward `m` only if it is **simultaneously** measured, computable,
and validated — three independent ticks, all required. So `m` is a *lower bound*: even
under the most generous selection of observables, only `m` earn all three. The
certificate radius `1/√m` is therefore a **ceiling on verifiability** — a different
choice of observables can only shrink `m`, never grow it. The set is stated and
revisable: hand over a better observable and, if it earns all three ticks, `m` rises
and the certificate tightens. The method welcomes a better choice; it never claims the
current one is complete.

## 3. Three safeguards against fooling ourselves

- **Rule of Three** — no claim from one test; three independent methods must agree
  (and the disagreement cases are the ones that got retracted, e.g. the W₀ over-reach).
- **Known-answer oracles** — validate the *instrument* against an always-true answer
  (mirror symmetry, the exact tadpole, valency/charge sanity) before trusting it on
  unknown data.
- **Falsification over verification, mutation-tested** — every guard must be able to
  fire. It ships with a seeded fault proving it goes red; a guard that never fires is a
  broken guard, not a passing one. The test *opposes* the artifact rather than
  confirming the choice.

## Why this is honest

The specific choice of observables in each discipline is a **stated judgment, not a
proof**. But the structure is built so a wrong judgment can only make the result
*weaker* (smaller `m`, looser certificate), never falsely stronger. That asymmetry is
the whole point: the method is a **lower bound on certainty**, and a lower bound is
the only claim you can make without a leap of faith.
