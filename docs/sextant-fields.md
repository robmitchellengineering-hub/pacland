# SEXTANT — the fields that rely on these fundamentals

These 27 proofs are not isolated results; they are the **load-bearing foundations** that entire
fields build on top of. This is the dependency map: for each field, the proofs it leans on, and
the one-line reason why it cannot do without them.

---

| field | relies on (SEXTANT claim) | why it needs it |
|---|---|---|
| **Quantum cryptography** | `no-cloning`, `bell-classical`, `chsh`, `locc-no-entanglement` | QKD's security *is* the no-cloning theorem; device-independent security rests on the Bell/CHSH bounds, and no classical line can forge entanglement. |
| **Quantum error correction** | `clifford-polynomial`, `entanglement-area`, `entanglement` | Stabilizer codes are the Clifford class; the area law is *why* correction is tractable — low-entanglement states are compressible. |
| **Quantum computing / benchmarking** | `clifford-polynomial`, `chsh`, `bell-classical`, `no-cloning` | The Clifford/T split is the honest boundary of "quantum advantage": which circuits are classically easy, and which are not. |
| **Quantum information & foundations** | `born-rule`, `pbr`, `no-cloning`, `no-broadcasting`, `mermin`, `pr-box`, `locc-no-entanglement` | These are the provable walls of what information *is*: the Born rule is forced, the state is real, and copying is impossible. |
| **Condensed matter / tensor networks** | `mera-hyperbolic`, `entanglement-area`, `mera-depth` | Critical systems are described by MERA; the area law is why tensor networks work at all. |
| **Holography / AdS–CFT** | `mera-hyperbolic`, `entanglement-area`, `locc-no-entanglement` | "Entanglement = geometry" is the kernel-checked core of AdS/CFT — the causal cone is a discrete hyperbolic space. |
| **Gravity & cosmology** | `lovelock`, `bianchi`, `wdw`, `dirac`, `adm`, `coupling-free`, `gravity-quantum` | These are the *forced* constraints any quantum-gravity theory must satisfy — the content is small and unique. |
| **Particle physics / beyond-SM** | `anomaly-cancellation`, `hypercharge-uniqueness`, `generation-free`, `sm-index`, `the-19` | What the SM forces (charges, anomalies) versus leaves free (N_gen, the 19) is the honest boundary of prediction. |
| **String landscape / ToE** | `mitchell-uniqueness`, `constraint-first`, `completeness` | The theorem tower: the tadpole is the unique invariant, the ring has one generator, and no exact selector exists. |
| **Computational complexity** | `clifford-polynomial` | The Clifford class is the canonical example of a classically-simulable quantum class (Gottesman–Knill). |
| **Machine learning (tensor networks)** | `entanglement-area`, `mera-hyperbolic` | Tensor networks in ML work *because* low-entanglement states are compressible — the area law is the reason. |

---

## The point

Each proof is a **constraint**; each field is a set of things built on those constraints. So the
value of SEXTANT to a field is not "here is a result" — it is "here is the *provable floor* under
your field, and the honest boundary of what your field can and cannot claim."

- A **quantum cryptographer** leans on no-cloning: SEXTANT certifies it, so the security claim is a theorem, not a hope.
- A **quantum-gravity researcher** leans on the constraints: SEXTANT says which are forced and which are free.
- A **beyond-SM physicist** leans on the 19: SEXTANT proves the floor of prediction.

The same sentence runs through all of it: **relations, never values** — and these 27 are the
relations.
