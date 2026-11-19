"""Generate more DISGUISED real-physics discovery examples to thicken the discovery skill.

The model hallucinated on perihelion and scored 1/3; the discovery data is only ~23 real pairs.
This generates ~60 more (pre-state -> jump) pairs for famous physics discoveries NOT in the
existing DATASET, each with a REWORDED pre-state so the model learns anomaly->discovery, not
memorised wording.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from pacland import benchmarks as b  # noqa: E402

# discoveries NOT already in DATASET/DISGUISED/POST_CUTOFF, phrased as (plain pre-state, jump)
TARGETS = [
    ("superconductivity: below a critical temperature, mercury's resistance vanishes", "electrons pair into Cooper pairs and move without resistance"),
    ("the specific heat of solids at low temperature deviates from the classical value", "lattice vibrations are quantised (phonons)"),
    ("Compton scattering: X-rays scattered off electrons shift to longer wavelength", "the photon carries momentum h/lambda"),
    ("the hydrogen spectrum lines are not evenly spaced but cluster toward a limit", "the Bohr model quantises angular momentum"),
    ("weak decays seem to violate parity", "the weak interaction couples only to left-handed particles"),
    ("the muon lifetime is much longer than a naive strong-decay estimate", "the weak force is carried by massive W/Z bosons"),
    ("cosmic rays produce an unexpected long-lived particle in cloud chambers", "the muon is a heavier copy of the electron (second generation)"),
    ("nuclear binding energy per nucleon saturates instead of growing with A", "the strong force is short-ranged (Yukawa pion exchange)"),
    ("the neutron decays into a proton and electron but the electron spectrum is continuous", "a neutrino carries away the missing energy and momentum"),
    ("superfluid helium flows through tiny capillaries with no viscosity", "bosons condense into a single quantum ground state (Bose-Einstein condensate)"),
    ("the Lamb shift splits two hydrogen levels that Dirac predicts degenerate", "the vacuum fluctuates and the electron self-energy depends on the orbital (QED)"),
    ("a metal's resistance drops in discrete steps as a magnetic field changes", "the quantum Hall conductance is quantised in units of e^2/h"),
    ("the Casimir force attracts two uncharged plates in vacuum", "the zero-point energy of the electromagnetic field is modified by boundaries"),
    ("alpha decay tunnelling rates are far faster than classical escape", "the wavefunction tunnels through the Coulomb barrier (Gamow)"),
    ("the cosmic microwave background is remarkably uniform across the sky", "a period of inflationary expansion smoothed the early universe"),
    ("galaxy rotation curves stay flat at large radii instead of falling", "an unseen dark matter halo provides the missing gravitational mass"),
    ("the universe's expansion is accelerating, not decelerating", "a cosmological constant / dark energy drives the acceleration"),
    ("the ratio of baryons to photons today is far lower than thermal equilibrium predicts", "matter-antimatter asymmetry arose from CP violation in the early universe"),
    ("the proton's spin is not fully accounted for by its valence quarks", "gluon and sea-quark angular momentum contribute to the proton spin"),
    ("neutral kaons oscillate between K0 and anti-K0", "the weak eigenstates are superpositions of mass eigenstates (mixing)"),
    ("electrons in a crystal behave as if they have a much smaller effective mass", "the lattice potential renormalises the electron dispersion (effective mass)"),
    ("the spectrum of the radiation from a synchrotron is polarised and sharply beamed", "relativistic beaming of accelerated charges"),
    ("a particle and its antiparticle annihilate into exactly two photons", "conservation of momentum forbids a single-photon decay"),
    ("the atomic mass of a nucleus is less than the sum of its nucleons", "the binding energy is released as E=mc^2 (mass defect)"),
    ("an electron beam diffracts off a crystal", "matter has a wavelength (de Broglie)"),
    ("the conductivity of a semiconductor rises sharply with temperature", "a thermal band gap separates the valence and conduction bands"),
    ("muons produced at altitude reach the ground despite a short half-life", "time dilation lengthens the muon's proper lifetime (relativity)"),
    ("the perihelion of Mercury precesses by 43 arcseconds/century beyond Newton", "spacetime is curved by mass (general relativity)"),
    ("a spinning electron in a magnetic field splits into two, not three, levels", "the electron has intrinsic spin 1/2 with two projections"),
    ("the pressure of a relativistic electron gas can support a white dwarf up to a mass limit", "the Chandrasekhar limit from electron degeneracy pressure"),
    ("a free neutron is unstable but a bound neutron is stable", "nuclear binding makes the neutron energetically stable inside the nucleus"),
    ("two identical fermions never occupy the same quantum state", "the Pauli exclusion principle from antisymmetric wavefunctions"),
    ("the wavelength of light from receding galaxies is systematically shifted red", "the expansion of the universe stretches the photon wavelength"),
    ("a superconductor expels a magnetic field entirely", "the Meissner effect from a persistent screening current"),
    ("certain atoms emit light only at discrete, reproducible wavelengths", "atomic energy levels are quantised"),
    ("the kinetic energy of ejected photoelectrons is independent of light intensity", "light is quantised into photons of energy h nu"),
    ("a current flows with zero voltage across a Josephson junction", "Cooper pairs tunnel coherently (Josephson effect)"),
    ("the heat capacity of a metal at low temperature is linear in T, not T^3", "the conduction electrons form a degenerate Fermi gas"),
    ("the Sun's neutrino count is about a third of the solar-model prediction", "neutrinos oscillate between three flavours"),
    ("an isolated quantum system returns arbitrarily close to its initial state", "the Poincare recurrence of a bounded quantum state"),
    ("the spectrum of a black hole is thermal with a temperature", "Hawking radiation from the event horizon"),
    ("a particle's position and momentum cannot both be sharply measured", "the Heisenberg uncertainty principle"),
    ("an electron in a periodic potential has energy bands and gaps", "Bloch's theorem: crystal eigenstates are plane waves times periodic functions"),
    ("the entropy of a system always increases in an isolated process", "the second law of thermodynamics from statistical mechanics"),
    ("an accelerated charge radiates electromagnetic waves", "the Larmor formula from Maxwell's equations"),
    ("a magnetic monopole would quantise electric charge", "Dirac quantisation condition from a singular gauge potential"),
    ("the Aharonov-Bohm phase shifts electrons passing a solenoid with zero field", "the vector potential is physical, not just a gauge artifact"),
    ("a relativistic electron's gyromagnetic ratio is not 1", "the Dirac equation predicts g=2 from spin"),
    ("two electrons are always entangled after scattering", "quantum correlations from the antisymmetry of the wavefunction"),
    ("the vacuum has a non-zero energy density", "the cosmological constant / vacuum energy from quantum fields"),
    ("a quantum measurement collapses the wavefunction to an eigenstate", "the Born rule gives the probability of each outcome"),
    ("the orbit of a satellite shifts slightly from Newton's prediction", "frame-dragging / Lense-Thirring from rotating mass"),
    ("a charged particle in a uniform field moves in a circle", "the Lorentz force bends the trajectory"),
    ("the fine-structure constant appears in many unrelated QED processes", "a single dimensionless coupling governs electromagnetism"),
    ("a nucleus can be split releasing large energy", "the binding energy per nucleon peaks near iron (fission)"),
    ("light nuclei fuse releasing energy and neutrons", "fusion toward higher binding energy per nucleon"),
]

INSTRUCTION = (
    "Rewrite this physics-discovery pair as a DISGUISED training example: give a pre-state "
    "(the puzzling observation, reworded so the historical answer is not named) and a one-line "
    "jump (the discovery). Output exactly two lines:\nPRE: <reworded pre-state>\nJUMP: <one-line discovery>"
)


def main() -> int:
    endpoint = os.environ.get("SEXTANT_LLM_ENDPOINT", "https://api.deepseek.com/v1")
    key = os.environ.get("SEXTANT_LLM_KEY", "")
    model = os.environ.get("SEXTANT_LLM_MODEL", "deepseek-chat")
    if not key:
        print("set SEXTANT_LLM_KEY to generate the data")
        return 1

    rows = []
    for pre, jump in TARGETS:
        out = b._ask_llm(INSTRUCTION + "\n\nPRE: " + pre + "\nJUMP: " + jump, endpoint, key, model)
        lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
        pre2, jump2 = pre, jump
        for ln in lines:
            if ln.upper().startswith("PRE:"):
                pre2 = ln[4:].strip()
            elif ln.upper().startswith("JUMP:"):
                jump2 = ln[5:].strip()
        rows.append({"pre": pre2, "jump": jump2, "source": "generated-disguised"})

    Path("runs/peft-discovery-extra.jsonl").parent.mkdir(parents=True, exist_ok=True)
    with open("runs/peft-discovery-extra.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"wrote {len(rows)} disguised discovery examples to runs/peft-discovery-extra.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
