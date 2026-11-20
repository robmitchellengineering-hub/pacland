#!/usr/bin/env python3
"""Phase 2 — run the discovery benchmark against the real LLM (DeepSeek).

Blind historical-rediscovery: the generator sees only the PRE-STATE (the anomaly); the withheld jump is
scored by a keyword rubric. Two arms — untyped baseline ("propose hypotheses") vs the five-jump taxonomy
(each of the five questions is asked and its candidate recorded). The metric is recall (did the arm
generate the jump) — the honest first measurement of whether the taxonomy helps.

Usage: python3 scripts/benchmark_llm.py [n_problems]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from pacland.runner import _ask_llm, _llm_config  # noqa: E402

endpoint, key, model = _llm_config()

# pre-state -> (withheld jump, rubric keywords that count as "found")
DATASET = {
    "blackbody": ("the blackbody spectrum diverges at short wavelength (Rayleigh-Jeans)",
                  "energy is quantised, E = h nu", ["quantis", "quantiz", "quanta", "planck", "discrete energy"]),
    "photoelectric": ("the photoelectric threshold depends on frequency, not intensity",
                      "light is made of quanta (photons)", ["photon", "quanta", "light quant", "particle of light"]),
    "perihelion": ("Mercury's perihelion precesses 43 arcsec/century beyond Newton",
                   "gravity is spacetime curvature (GR)", ["curvature", "spacetime", "relativity", "general relativity", "GR"]),
    "michelson": ("no aether drift is detected at any velocity",
                  "Lorentz invariance (special relativity)", ["lorentz", "relativity", "constant speed", "speed of light constant", "invariant"]),
}

FIVE_QUESTIONS = [
    ("anomaly", "What contradiction is the field quietly ignoring?"),
    ("inversion", "Which assumption, if flipped, changes the problem?"),
    ("unification", "Which two 'different' objects are secretly one?"),
    ("analogy", "What structure from another domain maps here?"),
    ("principle", "What single postulate would reorganize everything?"),
]


def ask(prompt: str) -> str:
    return _ask_llm(prompt, endpoint, key, model)


def untyped_candidates(pre: str) -> list[str]:
    r = ask(f"Propose up to 5 distinct candidate explanations for this scientific anomaly, one per line, no numbering:\n{pre}")
    return [ln.strip("-•* 1234567890.()") for ln in r.splitlines() if ln.strip()]


def typed_candidates(pre: str) -> list[str]:
    out = []
    for tag, q in FIVE_QUESTIONS:
        r = ask(f"{q}\nAnomaly:\n{pre}\n\nPropose ONE specific candidate hypothesis, one short sentence.")
        out.append(r.strip().strip('"'))
    return out


def found(cands: list[str], keywords: list[str]) -> bool:
    joined = " ".join(cands).lower()
    return any(kw.lower() in joined for kw in keywords)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(DATASET)
    items = list(DATASET.items())[:n]
    print(f"{'problem':14s} {'untyped':12s} {'five-jump':12s}")
    untyped_recall = typed_recall = 0
    for name, (pre, jump, kws) in items:
        u = untyped_candidates(pre)
        t = typed_candidates(pre)
        uf = found(u, kws)
        tf = found(t, kws)
        untyped_recall += uf
        typed_recall += tf
        print(f"{name:14s} {'FOUND' if uf else 'miss':12s} {'FOUND' if tf else 'miss':12s}")
    print(f"\nrecall: untyped {untyped_recall}/{len(items)}, five-jump {typed_recall}/{len(items)}")


if __name__ == "__main__":
    main()
