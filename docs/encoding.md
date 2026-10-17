# Encoding — the genotype (L1)

A concrete, honest encoding for a *starting* subclass, not the whole landscape. The
principle: **get one small, well-defined genotype in hand before generalizing.**

## 1. Starting subclass: IIB orientifold flux vacua on a Calabi-Yau threefold

This is the best-studied corner and has real tooling (CY databases, flux enumerators).

### Genotype fields

| Field | Type | Cardinality / source |
|---|---|---|
| `h^{1,1}`, `h^{2,1}` | discrete integers | Kreuzer–Skarke database |
| Triple intersection numbers `d_{ijk}` | discrete integers | CY database |
| Flux vectors `F₃, H₃ ∈ H³(Z)` | integer vectors, tadpole-bounded | enumeration |
| D3/D7 brane wrapping classes | discrete | construction |
| Complex-structure moduli `zᵃ` | continuous | moduli space |
| Kähler moduli `tⁱ` | continuous | Kähler cone |

The phenotype (what L2 computes and L3 verifies against) is: gauge group, charged
spectrum, Yukawa couplings, and Λ after moduli stabilization.

## 2. Separation principle

- **Discrete part** (topology + flux + branes): distance is Hamming-like. Two vacua
  differing by one flux unit are "close" in a way that has nothing to do with metric
  distance on moduli.
- **Continuous part** (moduli): distance is Euclidean (or Kähler) on the moduli space.

Mutation and neighborhood structure must respect this split, or the search treats
topology change and moduli drift as if they were the same operation.

## 3. Mutation operators

| Operator | Acts on | Effect | Landscape geometry |
|---|---|---|---|
| Flux nudge | `F₃, H₃` within tadpole bound | new stabilized moduli, new Λ | local (same topology) |
| Brane move | wrapping classes | changes gauge group / spectrum | local |
| Conifold transition | topology | changes `h^{1,1}`/`h^{2,1}` | **jump** (different node of landscape graph) |
| Moduli re-solve | continuous part | relax to new minimum | local |

The conifold transition is the important one: it makes the landscape a *graph* whose
nodes are topologies and whose edges are transitions, so L4 is a search on a graph, not
a search on a fixed Euclidean space.

## 4. Redundancies to quotient

- **SL(2,ℤ) duality** acts on the flux vectors; many integer vectors are the same vacuum.
- **Monodromies / discrete symmetries** of the CY.
- **Equivalent presentations** of the same brane configuration.

These must be quotiented out of the genotype, or L3 will count the *same* vacuum many
times and inflate the apparent class size (which feeds directly into the VC-dimension
estimate in `verification.md`).

## 5. Normalization

A genotype must be hashable and comparable so L5 can dedupe and cluster. Design decision
to fix later:

- Canonical form for flux under SL(2,ℤ).
- Integer overflow discipline — flux vectors and intersection numbers are large
  integers; no floating-point encoding of discrete data.

## 6. Explicit non-goal for now

- No attempt to encode *all* compactifications (G₂, non-geometric, F-theory). The
  learnability question in `verification.md` is answerable on the IIB flux corner first;
  generalization is a later step and may not even be needed to ask the governing
  question.
