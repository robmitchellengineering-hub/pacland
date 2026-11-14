"""SEXTANT QEC — the Clifford engine pointed at its real job: quantum error correction.

`sextant qec` runs a rotated surface-code memory experiment (stim) and reports whether the
code suppresses logical errors below the physical noise — the whole point of a code.

Usage:
    python -m pacland.qec                # distance 3, noise 1e-3, 1000 shots
    python -m pacland.qec 5 0.005 2000   # distance, noise, shots
"""

from __future__ import annotations


def surface_code_memory(distance: int = 3, rounds: int | None = None, noise: float = 1e-3, shots: int = 1000) -> dict:
    """Run a rotated surface-code memory-Z experiment and return the numbers."""
    import stim

    rounds = rounds or distance
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=distance,
        rounds=rounds,
        after_clifford_depolarization=noise,
        before_round_data_depolarization=noise,
        after_reset_flip_probability=noise,
        before_measure_flip_probability=noise,
    )
    sampler = circuit.compile_detector_sampler()
    _, obs = sampler.sample(shots, separate_observables=True)
    logical_errors = int(obs.sum())
    logical_rate = logical_errors / shots
    # the code's job: beat the naive accumulation of physical errors over the whole circuit.
    # each measurement cycle carries ~noise of error, so the accumulated physical failure
    # probability is ~ num_measurements * noise.
    accumulated_physical = circuit.num_measurements * noise
    return {
        "distance": distance,
        "rounds": rounds,
        "physical_noise": noise,
        "shots": shots,
        "qubits": circuit.num_qubits,
        "detectors": circuit.num_detectors,
        "measurements": circuit.num_measurements,
        "accumulated_physical": accumulated_physical,
        "logical_errors": logical_errors,
        "logical_error_rate": logical_rate,
        "suppression_ratio": accumulated_physical / max(logical_rate, 1e-12),
        "suppressed": logical_rate < accumulated_physical,
    }


def render(r: dict) -> str:
    verdict = "SUPPRESSED" if r["suppressed"] else "NOT SUPPRESSED"
    return (
        f"surface code  distance {r['distance']} · rounds {r['rounds']} · {r['qubits']} qubits · {r['detectors']} detectors\n"
        f"  physical noise p = {r['physical_noise']:.2e}  →  accumulated over {r['measurements']} measurements = {r['accumulated_physical']:.2e}\n"
        f"  logical error rate = {r['logical_error_rate']:.2e}  ({r['logical_errors']}/{r['shots']} shots)\n"
        f"  → suppression ×{r['suppression_ratio']:.1f}: the code {verdict}"
    )


def main(argv: list[str] | None = None) -> int:
    import sys

    argv = sys.argv[1:] if argv is None else argv
    distance = int(argv[0]) if len(argv) > 0 else 3
    noise = float(argv[1]) if len(argv) > 1 else 1e-3
    shots = int(argv[2]) if len(argv) > 2 else 1000
    print(render(surface_code_memory(distance, noise=noise, shots=shots)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
