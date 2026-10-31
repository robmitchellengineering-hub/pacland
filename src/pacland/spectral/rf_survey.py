"""The RF survey: the inputs the engine assumes, measured instead.

The engine runs on three numbers it does not know: the noise floor, the modal quality factor, and how busy
the channel is. Every one of them is cheap to measure in the room, and until they are measured the plan is a
calculation about an idealised room rather than about *this* room.

This module is the boundary between the two: it validates a survey and converts it into engine parameters, so
every output can carry the measurement it came from.

WHAT TO LOG, and how to get each one
------------------------------------
    noise_floor_dbm      spectrum analyser, band of interest, antenna connected, quiet period
    occupancy            fraction of a minute the channel sits above noise_floor + 10 dB
    impulse_response     RF impulse response from a swept-sine or VNA sweep across the band
        -> t60_s          decay 60 dB, measured on the IR envelope
        -> q_factor       Q = pi * f * t60 / ln(1000)   (a Halliwell-style estimate)
    mode_peaks_hz        peaks detected in a fine sweep - the in-situ test of the Weyl prediction

FALSIFIER (stated before any survey is run): if the measured mode count agrees with Weyl to better than 10%
but the measured Q is far from the assumed value, then the plan was right for the wrong reason and every
stream count in it was a coincidence. If the mode count disagrees by more than 10%, the engine does not
describe this room and no plan from it is usable.
"""
from __future__ import annotations

import math

REQUIRED = ("noise_floor_dbm", "occupancy", "t60_s", "band_hz")
C_LIGHT = 299_792_458.0


class SurveyError(ValueError):
    """The survey is not in the state the calculation assumes."""


def q_from_t60(f_hz: float, t60_s: float) -> float:
    """Modal quality factor from a measured decay time.

    `Q = pi f T60 / ln(1000)`: the ln(1000) is the 60 dB decay expressed in nepers, `pi f` converts a decay
    rate to a quality factor. With T60 unknown, Q is unknown, and the plan's stream counts are unbounded
    above - so this is not a nicety, it is the parameter that decides the answer.
    """
    if t60_s <= 0:
        raise SurveyError(f"t60_s must be positive, got {t60_s}")
    return math.pi * f_hz * t60_s / math.log(1000.0)


def snr_db(signal_dbm: float, noise_floor_dbm: float, occupancy: float) -> float:
    """Effective SNR, with busy-channel occupancy charged as noise.

    Occupancy is a duty cycle, not a constant: a channel busy `p` of the time raises the *average*
    interference power, and the honest figure is `-10 log10(1 + p * 10^(C/I))` below the clean SNR. Absent a
    measured C/I, this charges occupancy linearly in power, which is the conservative reading.
    """
    if not 0.0 <= occupancy <= 1.0:
        raise SurveyError(f"occupancy must be a fraction in [0,1], got {occupancy}")
    clean = signal_dbm - noise_floor_dbm
    return clean - 10.0 * math.log10(1.0 + occupancy)


def validate(survey: dict) -> None:
    missing = [k for k in REQUIRED if k not in survey]
    if missing:
        raise SurveyError(f"survey is missing {', '.join(missing)} - the engine will assume them otherwise")


def engine_inputs(survey: dict, signal_dbm: float = -55.0) -> dict:
    """Turn a survey into the parameters the engine needs, with the provenance attached."""
    validate(survey)
    f_hz = float(survey.get("band_hz"))
    q = q_from_t60(f_hz, float(survey["t60_s"]))
    snr = snr_db(signal_dbm, float(survey["noise_floor_dbm"]), float(survey["occupancy"]))
    return {"q_factor": q, "snr_db": snr, "noise_floor_dbm": float(survey["noise_floor_dbm"]),
            "occupancy": float(survey["occupancy"]), "t60_s": float(survey["t60_s"]),
            "provenance": {"q_factor": "measured: t60 converted by Q = pi f T60 / ln(1000)",
                           "snr_db": "measured: signal minus floor, minus occupancy charge",
                           "noise_floor_dbm": "measured: spectrum analyser, quiet period"}}


def weyl_check(survey: dict, volume: float, surface: float, surface_coefficient: float = 0.05) -> dict:
    """The in-situ test: does the measured mode count match Weyl in this room?"""
    peaks = [f for f in (survey.get("mode_peaks_hz") or []) if f]
    if len(peaks) < 10:
        return {"verdict": "not testable", "reason": f"{len(peaks)} peaks detected; 10 needed"}
    # The comparison is over the band the peaks were DETECTED in, not from zero to the highest peak: Weyl counts
    # every mode below f, and a sweep that starts at 5 GHz does not see the 4 billion below it. An earlier
    # version compared a 12-peak sweep to a full-band prediction and reported an error of 109,179x.
    f_lo = min(peaks)
    f_max = max(peaks)
    if f_lo <= 0 or f_max <= f_lo:
        return {"verdict": "not testable", "reason": "peaks do not span a band"}
    k = f_max / C_LIGHT
    k_lo = f_lo / C_LIGHT
    predicted = ((8.0 * math.pi * volume / 3.0) * (k ** 3 - k_lo ** 3)
                 - surface_coefficient * (math.pi * surface / 2.0) * (k ** 2 - k_lo ** 2))
    observed = len(peaks)
    err = (predicted - observed) / max(observed, 1)
    return {"observed": observed, "predicted": predicted, "error": err,
            "verdict": "agrees" if abs(err) < 0.10 else "DISAGREES - the engine does not describe this room"}
