# What Pacland is

**The thesis.** Pacland is a reusable methodology for distinguishing what a machine, model, or
scientific claim actually *knows* from what it merely *asserts*.

Most claims cannot be checked. The failure mode is the same everywhere — a physics paper, a
financial model, an AI answer: confidence that does not track correctness. An overconfident wrong
answer ships because nothing measured the gap between "asserts" and "knows."

**The implementation (built, not aspirational):**

| the principle | the machinery |
|---|---|
| a claim is a theorem plus a falsifier | SEXTANT: FORCED / FREE / IMPOSSIBLE |
| a result is unknown until it ran | rule 67 — absent green is not green |
| the answer carries proof it is correct | the certificate + a re-runnable falsifier; a wrong answer is refused |
| confidence must track correctness | calibration: ECE, proper scoring, PAC-Bayes |
| where it cannot be proved, say how much you believe | the belief layer: Bayes, expected information gain, de Finetti coherence |
| where it is exact, compute it exactly; where not, state the deficit | deterministic-in-use |

**The one sentence.** We hand you the answer and the proof of what it knows, and we refuse the rest.

**Why this framing matters.** The quantum work, the certified chemistry, and the uncertainty
adoption are not separate products. They are the same methodology applied to three surfaces:
circuits, molecules, and beliefs. The world-changing part is not any single result. It is that the
method — measure what a claim knows, refuse what it only asserts — transfers from one field to the
next unchanged.
