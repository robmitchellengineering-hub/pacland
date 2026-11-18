# What Pacland is

**The two theses.**

1. **Verification.** Pacland is a reusable methodology for distinguishing what a machine, model,
   or scientific claim actually *knows* from what it merely *asserts*.

2. **Discovery.** Pacland is an attempt to systematise the process of scientific discovery itself —
   the loop of generating hypotheses, testing them against falsifiers, promoting what survives, and
   recording the belief state — so discovery becomes a ratcheting procedure, not a run of lucky
   guesses.

Most claims cannot be checked, and most discovery is a search over a space too large to explore
blindly. The two failure modes are the same shape: an overconfident wrong answer ships because
nothing measured the gap between "asserts" and "knows"; and a search stalls because nothing ranked
*what to test next*.

**The implementation (built, not aspirational):**

| the principle | the machinery |
|---|---|
| a claim is a theorem plus a falsifier | SEXTANT: FORCED / FREE / IMPOSSIBLE |
| a result is unknown until it ran | rule 67 — absent green is not green |
| the answer carries proof it is correct | the certificate + a re-runnable falsifier; a wrong answer is refused |
| confidence must track correctness | calibration: ECE, proper scoring, PAC-Bayes |
| where it cannot be proved, say how much you believe | the belief layer: Bayes, expected information gain, de Finetti coherence |
| where it is exact, compute it exactly; where not, state the deficit | deterministic-in-use |
| discovery is a loop, not a guess | generate → test → promote → record (the SEXTANT runner) |
| rank what to test next | expected information gain per unit cost |
| explore an expensive space in few probes | Bayesian optimization |
| beliefs are posteriors, not pass logs | the belief ledger |

**The one sentence.** We hand you the answer and the proof of what it knows, we refuse the rest,
and we rank the next question by how much it will reduce our uncertainty.

**Why this framing matters.** The quantum work, the certified chemistry, and the uncertainty
adoption are not separate products. They are one methodology applied to three surfaces: circuits,
molecules, and beliefs. The world-changing part is not any single result. It is that the method —
measure what a claim knows, refuse what it only asserts, and rank what to discover next — transfers
from one field to the next unchanged.
