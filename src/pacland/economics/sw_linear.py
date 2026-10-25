"""SW's linearised model, as the authors wrote it — parsed and checked.

The paper's technical appendix is not openly posted, but the **authors' own Dynare
implementation** of the linearised model is: `Smets_Wouters_2007.mod`, written by Smets and
Wouters and maintained by Johannes Pfeifer, published (GPL) as part of the DSGE_mod
replication library. That file *is* the linearised system in machine-readable form, and it
is a better source than any transcription of mine.

This module parses it and asks the two questions that can be settled mechanically:

1. **Does every equilibrium condition vanish at the steady state?** A linearised model is
   by construction an expansion about a point where all deviations are zero, so each
   behavioural equation must reduce to `0 = 0` there. If one does not, the steady-state
   ratios and the equation disagree — a transcription error, caught without knowing the
   economics.
2. **Does its steady-state block reproduce the paper's own reported rates** — "about 3%"
   real and "about 6%" nominal — from the published posterior parameters?

The six equations that do *not* vanish are the **measurement equations** (`dy`, `dc`,
`dinve`, `dw`, `pinfobs`, `robs`): they carry the steady-state constants (`ctrend`,
`constepinf`, `conster`) because they map deviations to observables. Separating them is part
of the check, not an exemption from it.

The GPL file is fetched at verification time and never committed; its sha256 is recorded so
the parse is reproducible.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

#: Published posterior means (Table 1a) for the parameters the estimation version leaves
#: free. The Dynare file sets priors, not posteriors, for these.
POSTERIOR = {
    "constepinf": 0.78,   # steady-state inflation, % per quarter
    "constebeta": 0.16,   # 100(1/beta - 1)
    "ctrend": 0.43,       # trend growth, % per quarter
    "csigma": 1.38,
    "calfa": 0.19,
    "cfc": 1.60,
    "ctou": 0.025,
    "cg": 0.18,
    "clandaw": 1.5,
}

#: Measurement equations: they contain a steady-state constant, so they are not expected
#: to vanish at the steady state. Named explicitly rather than discovered by outcome.
MEASUREMENT = ("dy", "dc", "dinve", "dw", "pinfobs", "robs")


@dataclass(frozen=True)
class Parsed:
    params: dict[str, float]
    definitions: dict[str, float]
    equations: list[str]
    equilibrium: list[str]
    measurement: list[str]


def _numeric(text: str) -> dict[str, float]:
    return {k: float(v) for k, v in
            re.findall(r"^\s*(\w+)\s*=\s*([-\d.eE+]+)\s*;", text, re.M)}


def _block(text: str) -> str:
    m = re.search(r"model\(linear\);(.*?)^end;", text, re.S | re.M)
    if not m:
        raise ValueError("no model(linear) block found")
    return re.sub(r"//[^\n]*", "", m.group(1))


def parse(text: str, overrides: dict[str, float] | None = None,
          use_posterior: bool = True) -> Parsed:
    """Parse a Dynare model.

    ``use_posterior`` substitutes the paper's published posterior means for the
    parameters the estimation version leaves free (the file carries priors there). Set it
    False to test the parser on a self-contained sample.
    """
    params = _numeric(text)
    if use_posterior:
        params.update(POSTERIOR)
    params.update(overrides or {})
    statements = [re.sub(r"\s+", " ", s.strip()) for s in _block(text).split(";") if s.strip()]
    raw_defs = [s[1:] for s in statements if s.startswith("#")]
    equations = [s for s in statements if not s.startswith("#")]
    env = dict(params)
    for d in raw_defs:
        name, expr = d.split("=", 1)
        env[name.strip()] = eval(expr.replace("^", "**"), {"__builtins__": {}}, env)
    # the definitions are the #c... block: keep them as their evaluated values
    definitions = {k: env[k] for k in env if k not in params}
    eq = [e for e in equations if _lhs(e) not in MEASUREMENT]
    meas = [e for e in equations if _lhs(e) in MEASUREMENT]
    return Parsed(params=params, definitions=definitions, equations=equations,
                  equilibrium=eq, measurement=meas)


def _lhs(equation: str) -> str:
    return equation.split("=", 1)[0].strip()


def to_python(equation: str) -> str:
    """Translate Dynare timing notation: ``x(+1)`` -> ``x_lead``, ``x(-1)`` -> ``x_lag``."""
    e = equation.replace("^", "**")
    e = re.sub(r"(\w+)\(\s*\+?1\s*\)", r"\1_lead", e)
    e = re.sub(r"(\w+)\(\s*-1\s*\)", r"\1_lag", e)
    return e


def variable_names(p: Parsed) -> set[str]:
    names = set(re.findall(r"[a-zA-Z_]\w*", " ".join(to_python(e) for e in p.equations)))
    return names - set(p.params) - set(p.definitions) - {"lead", "lag"}


def residuals(p: Parsed) -> list[tuple[str, float]]:
    """Each equation's residual at the steady state (all deviations zero)."""
    scope = {**p.params, **p.definitions, **{n: 0.0 for n in variable_names(p)}}
    out = []
    for e in p.equations:
        py = to_python(e)
        lhs, rhs = py.split("=", 1)
        value = eval(lhs, {"__builtins__": {}}, scope) - eval(rhs, {"__builtins__": {}}, scope)
        out.append((e, value))
    return out


def steady_state_rates(p: Parsed) -> dict[str, float]:
    """The rates the model's own steady-state block implies, annualised."""
    d = p.definitions
    real = (d["cr"] / d["cpie"] - 1.0) * 400.0
    return {"real_annual_pct": real,
            "nominal_annual_pct": (d["cr"] - 1.0) * 400.0,
            "inflation_annual_pct": (d["cpie"] - 1.0) * 400.0,
            "capital_output": d["cky"], "investment_share": d["ciy"],
            "consumption_share": d["ccy"],
            "shares_sum": d["ccy"] + POSTERIOR["cg"] + d["ciy"]}


def check(p: Parsed, tol: float = 1e-10) -> dict:
    """The machine check: equilibrium equations vanish, measurement ones carry constants."""
    res = residuals(p)
    by_eq = {e: v for e, v in res}
    eq_bad = [(e, v) for e in p.equilibrium for v in [by_eq[e]] if abs(v) > tol]
    meas_zero = [(e, by_eq[e]) for e in p.measurement if abs(by_eq[e]) <= tol]
    return {
        "n_equations": len(p.equations),
        "n_equilibrium": len(p.equilibrium),
        "n_measurement": len(p.measurement),
        "equilibrium_bad": eq_bad,
        "measurement_without_constant": meas_zero,
        "ok": not eq_bad and not meas_zero,
    }
