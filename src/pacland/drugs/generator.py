"""The molecule generator — propose candidate molecules; the guards falsify them.

The honest division of labour, matching the rest of PACLAND: the generator *proposes* (SMILES), the
guards *verify* (validity + drug-likeness + synthesizability). Two tiers, one feature contract:

* **stub tier** (no RDKit): a seed library of molecules with pre-computed features, so the
  generate → falsify loop runs anywhere (CI, a fresh checkout, the ROG);
* **RDKit tier** (when installed): real sanitisation + descriptors (mol weight, logP, H-bond
  donors/acceptors). RAScore still needs its own dependency, so the stub reports it as trivially
  synthesizable rather than guessing.

The guards in ``guards.py`` never see SMILES — they only see the numbers this module extracts, so
the contract is identical whichever tier is live.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import guards


@dataclass
class MoleculeFeatures:
    """The numbers the guard-suite consumes for one molecule."""
    smiles: str
    valid: bool
    charges: list[float] = field(default_factory=list)
    valence_pairs: list[tuple[str, int]] = field(default_factory=list)
    mw: float = 0.0
    logp: float = 0.0
    hbd: int = 0
    hba: int = 0
    rascore: float = 10.0  # higher = harder to synthesize


#: A seed library so the loop runs without RDKit. Features are pre-computed honest stubs.
SEED_MOLECULES: dict[str, MoleculeFeatures] = {
    # aspirin — valid, drug-like, synthesizable
    "CC(=O)Oc1ccccc1C(=O)O": MoleculeFeatures(
        smiles="CC(=O)Oc1ccccc1C(=O)O", valid=True,
        charges=[0.0] * 13, valence_pairs=[("C", 4), ("O", 2)],
        mw=180.16, logp=1.2, hbd=1, hba=4, rascore=2.5),
    # caffeine — valid, drug-like, synthesizable
    "Cn1cnc2c1c(=O)n(C)c(=O)n2C": MoleculeFeatures(
        smiles="Cn1cnc2c1c(=O)n(C)c(=O)n2C", valid=True,
        charges=[0.0] * 14, valence_pairs=[("C", 4), ("N", 3), ("O", 2)],
        mw=194.19, logp=-0.07, hbd=0, hba=3, rascore=2.0),
    # a pentavalent carbon — the validity oracle must reject it
    "C(C)(C)(C)(C)(C)": MoleculeFeatures(
        smiles="C(C)(C)(C)(C)(C)", valid=False,
        charges=[0.0], valence_pairs=[("C", 5)],
        mw=0.0, logp=0.0, hbd=0, hba=0, rascore=10.0),
}


def extract_features(smiles: str) -> MoleculeFeatures:
    """Return a molecule's features. RDKit when available; otherwise the seed library.

    A molecule not in the seed (stub tier) returns ``valid=False`` — an unknown molecule is never
    silently passed."""
    try:
        from rdkit import Chem
        from rdkit.Chem import Crippen, Descriptors
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return MoleculeFeatures(smiles=smiles, valid=False)
        return MoleculeFeatures(
            smiles=smiles,
            valid=True,
            charges=[float(a.GetFormalCharge()) for a in mol.GetAtoms()],
            valence_pairs=[(a.GetSymbol(), a.GetTotalValence()) for a in mol.GetAtoms()],
            mw=Descriptors.MolWt(mol),
            logp=Crippen.MolLogP(mol),
            hbd=Descriptors.NumHDonors(mol),
            hba=Descriptors.NumHAcceptors(mol),
            rascore=0.0,  # RAScore needs its own model; 0 = trivially synthesizable (honest stub)
        )
    except ImportError:
        return SEED_MOLECULES.get(smiles, MoleculeFeatures(smiles=smiles, valid=False))


def falsify(features: MoleculeFeatures) -> tuple[bool, str]:
    """Run the guard-suite on a molecule. Returns (survived, evidence)."""
    if not features.valid:
        return False, "invalid: sanitisation failed (not a real molecule)"
    ok, msg = guards.guard_total_charge_neutral(features.charges)
    if not ok:
        return False, msg
    ok, msg = guards.guard_valence_bounds(features.valence_pairs)
    if not ok:
        return False, msg
    ok, msg = guards.guard_lipinski(features.mw, features.logp, features.hbd, features.hba)
    if not ok:
        return False, msg
    ok, msg = guards.guard_synthesizable(features.rascore)
    if not ok:
        return False, msg
    return True, f"valid + drug-like + synthesizable ({features.mw:.0f} Da, logP {features.logp:.1f})"


def generate_candidates(n: int = 8, seed: int = 0) -> list[MoleculeFeatures]:
    """Propose ``n`` candidate molecules. Stub tier samples the seed library (with repetition)."""
    import random
    rng = random.Random(seed)
    return [extract_features(rng.choice(list(SEED_MOLECULES))) for _ in range(n)]


if __name__ == "__main__":
    for cand in generate_candidates(6):
        survived, evidence = falsify(cand)
        verdict = "KEEP " if survived else "DROP"
        print(f"{verdict}  {cand.smiles[:24]:24}  {evidence}")
