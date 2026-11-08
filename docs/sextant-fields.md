# SEXTANT — the fields that rely on these fundamentals (full map)

A 6-way fan-out enumerated the downstream fields that are **load-bearing** on SEXTANT's 27
machine-checked proofs. Only **genuine** connections are listed (tangential ones were dropped and
are named in the notes). This is the honest answer to "how much can we really cover": **~33
established fields** build on these fundamentals.

---

## 1 · Quantum information & cryptography

| field | relies on | why |
|---|---|---|
| Quantum key distribution (QKD) | `no-cloning`, `bell-classical`, `chsh` | interception is detectable because a qubit cannot be copied without disturbance |
| Device-independent QKD & randomness | `chsh`, `bell-classical`, `pr-box` | a Bell violation above 2 is the *only* evidence of non-classicality when devices are untrusted |
| Quantum money & unforgeable tokens | `no-cloning` | unforgeability *is* the no-cloning theorem |
| Entanglement theory & quantum networks | `locc-no-entanglement` | entanglement is a resource only because LOCC cannot create it |
| Quantum error correction (fault-tolerant) | `no-cloning`, `no-broadcasting`, `clifford-polynomial` | no copying forces redundant entangled encoding; stabilizer codes are Clifford-tractable |
| Quantum foundations (ψ-realism) | `pbr`, `mermin`, `born-rule` | PBR/Mermin are the load-bearing theorems of the ψ-ontic debate; Gleason fixes the probability rule |
| Reconstructions of QM ("why quantum") | `pr-box`, `chsh`, `born-rule` | these fix which non-signaling theory and which probability rule are "quantum" |

## 2 · Quantum computing & benchmarking

| field | relies on | why |
|---|---|---|
| Randomized benchmarking | `clifford-polynomial` | Cliffords are simulable (ideal output computable) and form a 2-design |
| Loophole-free Bell tests | `bell-classical`, `chsh` | 2 is the threshold to rule out local hidden variables; 2√2 the quantum maximum |
| Device-independent randomness & self-testing | `chsh`, `bell-classical` | a Bell violation certifies un-predetermined outcomes and the state up to isometry |
| Tensor-network simulation (DMRG/MPS/PEPS) | `entanglement-area` | the area law is the guarantee that low bond dimension is exact, not heuristic |

## 3 · Geometry & holography

| field | relies on | why |
|---|---|---|
| Holographic duality (AdS/CFT) | `mera-hyperbolic`, `entanglement-area` | the 0-hyperbolic causal cone is the discrete bulk; the area law is the discrete Ryu–Takayanagi |
| Holographic quantum error correction | `mera-hyperbolic`, `entanglement-area` | HaPPY codes' distance/threshold follow from the RT-style area bound |
| Tensor networks for critical systems | `mera-hyperbolic`, `entanglement-area` | MPS fails at criticality *because* the area law breaks; MERA works because its cone is hyperbolic |
| Spacetime emergence from entanglement | `mera-hyperbolic`, `entanglement-area` | MERA is the working model where cutting entanglement removes the emergent radial direction |

## 4 · Gravity & quantum gravity

| field | relies on | why |
|---|---|---|
| Numerical relativity | `adm`, `bianchi` | the ADM constraints are the code's evolution equations; ∇·G=0 keeps them satisfied |
| Quantum cosmology | `wdw`, `dirac` | Ĥ|ψ⟩=0 is the defining equation (Hartle–Hawking/Vilenkin are its solutions) |
| Loop quantum gravity | `adm`, `dirac`, `wdw` | LQG quantizes the ADM/Ashtekar constraints and must recover WDW in the continuum limit |
| Modified gravity / Horndeski | `lovelock` | every viable modified theory is defined by *which* Lovelock assumption it breaks |
| Higher-dimensional gravity | `lovelock` | Gauss–Bonnet/Lovelock series are the unique divergence-free actions in D>4 |
| EFT of gravity | `coupling-free` | the EFT is organized around G as a free, underived coupling |
| QG phenomenology (BMV) | `gravity-quantum` | ruling out classical hybrid gravity is the premise of entanglement-via-gravity tests |

## 5 · Standard Model & beyond

| field | relies on | why |
|---|---|---|
| Beyond-SM model building | `anomaly-cancellation`, `hypercharge-uniqueness` | every new gauge sector must keep anomalies cancelled and reproduce the unique hypercharge |
| Grand unification | `hypercharge-uniqueness`, `anomaly-cancellation` | hypercharge quantization + exact cancellation are the classic GUT signatures |
| String phenomenology | `sm-index`, `generation-free` | N_gen=3 as a topological index is the bridge to a compactification prediction |
| Axion physics / strong CP | `the-19`, `anomaly-cancellation` | θ_QCD is one of the 19; the axion resolves the anomaly that couples to it |
| Precision electroweak / global fits | `the-19` | a well-posed fit needs the exactly-known free-parameter count |

## 6 · Landscape, ToE & the method (relations never values, applied anywhere)

| field | relies on | why |
|---|---|---|
| String flux landscape | `mitchell-uniqueness`, `constraint-first`, `completeness` | the unique invariant separates vacua; "no exact selector" is why enumeration resists |
| Topological quantum error correction | `mitchell-uniqueness`, `completeness` | topological order is the absence of a local order parameter — the "no selector" theorem |
| Lattice gauge theory | `mitchell-uniqueness`, `completeness` | the unique invariant fixes loop classes; "no selector" is the math of Gribov ambiguity |
| Model identifiability | `completeness`, `mitchell-uniqueness` | identifiability is exactly whether a complete invariant + exact selector exists |
| Geometric deep learning | `constraint-first`, `mitchell-uniqueness` | equivariant nets are built on invariant theory; "one generator" is the minimal separating feature |
| Graph isomorphism | `mitchell-uniqueness`, `completeness` | GI is the search for a complete invariant + selector; the no-go is its hardness boundary |

---

## Honest notes (the tangential ones, dropped)

- **Quantum advantage demonstrations** — rely on Clifford only as the *boundary being crossed*, not load-bearing.
- **Complexity=volume** and **QCNN** — borrow MERA's *shape*, not its hyperbolicity/area-law theorems.
- **Weyl semimetals** and **lattice chiral gauge theory** — use the *general* anomaly/index theorems, not the SM-specific claims these proofs certify.

## The point, stated once

Every proof is a **constraint**; every field above is things built *on* that constraint. SEXTANT
does not hand a field a result — it hands the field its **provable floor** and the honest boundary
of what it can claim. Across all six sectors the sentence is the same: **relations, never values**
— and these 27 proofs are the relations.
