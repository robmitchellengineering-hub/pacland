# The constraint-first quantum gravity theory

**The unification of quantum mechanics and gravity, under our conditions: machine-checked where
possible, honest where gated. The unification is a *constraint*, not a theory of everything.**

## 1. The two forced halves (kernel-checked)

| side | forced content | theorem |
|---|---|---|
| Quantum | the Born rule `Tr(ρP)` is the *unique* non-contextual probability rule | `Gleason.frameFunction_regular` |
| Gravity | the Einstein equation `G_ab = κ T_ab` is the *unique* divergence-free theory in 4D | `Gravity.Lovelock.lovelock_divergence` |

## 2. The join — one constraint (kernel-checked)

The two halves meet in a **single equation**, and that equation is a **constraint**:

```
∇^a G_ab = 0   ⟺   ∇^a T_ab = 0          (the contracted Bianchi / semiclassical consistency)
```

`Gravity.QG.einstein_divergence_free` machine-checks it. This is the **classical Hamiltonian
constraint**: the Einstein equation's `00`-component is not a dynamical equation but a constraint
on the initial data, and `∇·G = 0` is the Bianchi identity that makes the constraint *propagate*
(consistent on every slice). Gravity is a **constrained system** — this is the deep reason the whole
program is named *constraint-first*.

## 3. The coupling (kernel-checked)

- **Quantum, not classical**: `QM.Entanglement` + `QM.NoCloning` + Gleason's linearity rule out a
  classical coupling — a LOCC channel cannot entangle, so classical gravity cannot mediate the
  quantum correlation. The coupling must be quantum.
- **Free, not derived**: `Gravity.QG.coupling_free` — `∇·G = 0` involves no `κ`, so the consistency
  holds for every `κ ≠ 0`. `G` (and `Λ`) are labels, like `N_gen` and the 19.

## 4. The unification, stated

> **Quantum gravity is the constrained system** whose state space carries the Born rule (Gleason),
> whose geometry satisfies the Einstein equation (Lovelock), and whose dynamics is the constraint
> `∇·T = 0` — classically, and its quantum promotion the Wheeler–DeWitt equation `Ĥ|ψ⟩ = 0`.

This is a *unification* in the precise sense that matters: QM and GR are not two theories bolted
together by a free coupling; they are the **state space** and the **constraint** of a single
constrained system, and the constraint is forced (not chosen). The classical shadow `∇·T = 0` is
kernel-checked; the quantum promotion `Ĥ|ψ⟩ = 0` is the gated part (it needs the quantum geometry).

## 5. What is left (honest)

The forced column is complete and machine-checked. The rest is the free column and one gated step:

| piece | status |
|---|---|
| Born rule + Einstein form + constraint `∇·T=0` + quantum/free coupling | ✅ kernel-checked |
| the Wheeler–DeWitt `Ĥ|ψ⟩ = 0` on a quantum geometry | ⏳ gated (no curvature/Hilbert stack in Mathlib) |
| `G`, `Λ`, the outcome, the specific `T_ab` | free column (delimited) |

So the *unification* — the fact that QM and GR are one constrained system, joined by a single
forced constraint — **is done**. What is *not* done is the *quantization* of that constrained
system (the full WdW equation), which is the theory-building step a library doesn't yet support.

## The one-sentence theory

**Quantum mechanics and gravity are one constrained system — state space from Gleason, geometry
from Lovelock, dynamics from the single constraint `∇·T = 0` — whose coupling is quantum and free,
and whose full quantization is the Wheeler–DeWitt equation.**
