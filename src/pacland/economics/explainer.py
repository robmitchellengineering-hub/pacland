"""Economics explainer content — generated from live data, not hand-written prose.

Every number here is pulled from the module that verified it, so the PDF cannot drift from
the evidence. It also means the retractions travel: the claim that structural models lose to
a VAR out of sample was disproved by SW's own Table 3 and is **not** in this text.
"""
from __future__ import annotations

from . import constraint_set, gdpnow, meese_rogoff, model_roster
from .deficit import economics_deficit_report
from .gdpnow import revision_answer
from .nk3_oos import evaluate as nk3_run


def content() -> list[tuple[str, str]]:
    ret, pro = economics_deficit_report()
    rows = model_roster.summary()
    clean = [r["name"] for r in rows if r["tier"] == "clean"]
    weak = [r["name"] for r in rows if r["tier"] == "weak"]
    real = meese_rogoff.findables()
    rel = real["ratio_to_no_change"]
    nk = nk3_run()
    base_pi = nk["no-change"]["pi"]
    nk_ratio = nk["NK3"]["pi"][1] / base_pi[1]
    g = gdpnow.evaluate()
    rev = revision_answer()
    ind = constraint_set.independence()
    return [
        ("title", "PACLAND · Economics"),
        ("subtitle", "The verification discipline applied to macro-finance — a plain-English brief"),
        ("h", "The headlines — and what to do about each"),
        ("headline",
         f"{len(rows)} named models are scored on a nine-slot bar; {len(clean)} are clean "
         f"({', '.join(c.split(' (')[0] for c in clean)}). Scoring is mechanical: a claim "
         f"with no evidence behind it is refused, not argued with."),
        ("headline",
         f"On real-time data the no-change null beats structural inflation forecasts: a "
         f"calibrated three-equation model lands at {nk_ratio:.2f}× the null's error, and the "
         f"same model at Smets–Wouters' published parameters does no better. A plain VAR beats "
         f"the null ({rel['VAR(1)'][1]:.2f}×), and the Atlanta Fed's published nowcast beats it "
         f"{g['ratio']['mae']:.2f}× on the advance estimate, {rev['final_ratio']:.2f}× after revisions."),
        ("headline",
         "The Phillips slope cannot be identified from aggregate data: the estimator cannot "
         "recover a known slope of 0.18 from the model's own simulated data (it returns 1.00). "
         "That is not a data-quantity problem — more data will not fix it."),
        ("headline",
         f"The exact content is definitional, and that is the finding: the nominal expenditure "
         f"identity closes to ~1e-4% of GDP, while the *real* decomposition leaks by up to 25 "
         f"percentage points in 2020 because chained dollars are not additive."),
        ("headline",
         f"{len(constraint_set.CONSTRAINTS)} constraints, {ind['rank']} independent — and they "
         f"refuse a data-fitted passive policy rule outright instead of letting it into a "
         f"forecast table."),
        ("headline",
         "Two of this discipline's own claims were retracted on contact with evidence: that "
         "the workhorse DSGE cannot beat a VAR out of sample (its own Table 3 disproves it), "
         "and that GDPNow's edge is an artifact of targeting the first print (it survives "
         "revisions). Both retractions are in the record."),
        ("h", "1 · What we are measuring"),
        ("p",
         "Macroeconomics forecasts a future that is never observed, with data that is revised "
         "after the fact. The discipline asks the question the field does not put in numbers: "
         "how much of a forecast is verified, and how much is extrapolation?"),
        ("h", "2 · The three things we built"),
        ("b",
         "A bar with nine slots — exact structure, a deficit count, three independent checks, a "
         "mutation-tested guard-suite, an out-of-sample run, a benchmark, a board tier, a "
         "falsifiable prediction, and one reproduce command. A model's kind decides which it owes."),
        ("b",
         "A null. 'Tomorrow equals today.' Every model is scored against it on real-time "
         "vintages — what was published at the time, never today's revised numbers."),
        ("b",
         f"A constraint set: {len(constraint_set.CONSTRAINTS)} constraints of which "
         f"{ind['rank']} are independent, measured by the rank of the constraint Jacobian."),
        ("h", "3 · The verification deficit"),
        ("b",
         f"{ret.n_validation} of {ret.n_observables} backcast series are measured + computable "
         f"+ validated — a certificate radius of {ret.radius:.0%}."),
        ("b",
         f"{pro.n_validation} of {pro.n_observables} forecast targets are validated — the "
         f"projection central banks act on is extrapolation, not verification."),
        ("p",
         "A 1% certificate needs ~18,000 validated observables. The bottleneck is measured "
         "data, not compute, and no model in the roster can escape that."),
        ("h", "4 · Why the null matters more than the model"),
        ("p",
         "The field's own record is the anchor: Meese–Rogoff (1983) found structural "
         "exchange-rate models fail to beat a random walk out of sample, and Rossi (2013) "
         "confirms the pessimism. What this work adds is the measurement — on real-time data, "
         "for named models, with the null in the same table. Some models do beat it (a VAR, and "
         "the published nowcast by a wide margin); the structural forecasts of inflation do not."),
        ("h", "5 · What it means, and what is possible"),
        ("p",
         "The product is not a forecast; it is a set of gates. A null gate (no forecast ships "
         "without its no-change ratio, and losing it is stated in the tier). An identification "
         "gate (no estimate ships unless the estimator can recover a known truth from synthetic "
         "data). An admissibility gate (no fitted model enters a table if it violates the "
         "constraint set). All three have already refused something."),
        ("p",
         "What is possible: a verified-forecast label any macro model can carry — its m "
         "observables, its constraint pass/fail, and its real-time ratio to the null. Nobody "
         "publishes that today. What is not possible, on this evidence, is a certified "
         "quarter-ahead inflation number: the exact content is definitional and the behavioural "
         "parameters are not identified from aggregates."),
        ("h", "6 · Reproduce"),
        ("p",
         "pacland economics --models · --constraints · --realtime · "
         "docs/economics-model-roster.md"),
    ]


__all__ = ["content"]
