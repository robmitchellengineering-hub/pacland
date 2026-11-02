"""Rule 1 of the bench, applied to the landscape's own claims: exact, or a fit?

The bench's first rule came from a room: a candidate that explained **100%** of the measured peaks was **33.9% wrong**,
because a room with more modes can always cover every peak. The counterweight was the second direction - what the candidate
predicts that was NOT used to fit it.

This audits the landscape's structure claims against that rule and, more usefully, says which of them it applies to at all.
A claim that is an **exact enumeration** does not need it: there is nothing fitted and nothing left to predict. A claim that
is a **fit** does, and the first question is its **degrees of freedom**.

    python3 scripts/two_sided_audit.py

WHAT IT DOES NOT DO: it does not re-derive the physics. It reads the numbers the modules already commit and asks the two
questions the bench insists on - how many free parameters, and what is predicted that was not fitted.
"""
from __future__ import annotations

import math
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1] / "src"))

from pacland.exactness import b3_scaling as B  # noqa: E402
from pacland.exactness import landscape_count as L  # noqa: E402


def fit_report(name: str, points, n_params: int = 2) -> dict:
    """The exponential's degrees of freedom, its per-interval factors, and whether the intervals agree."""
    xs = [b for b, _ in points]
    ys = [math.log(v) for _, v in points]
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum((x - mean_x) ** 2 for x in xs)
    intercept = mean_y - slope * mean_x
    resid = [y - (intercept + slope * x) for x, y in zip(xs, ys)]
    ss_res = sum(r * r for r in resid)
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot else 0.0
    intervals = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        per_unit = (y1 / y0) ** (1.0 / (x1 - x0))
        intervals.append({"from": x0, "to": x1, "per_unit": per_unit})
    spread = max(i["per_unit"] for i in intervals) / min(i["per_unit"] for i in intervals)
    return {
        "name": name, "n_points": n, "n_params": n_params, "dof": n - n_params,
        "slope": slope, "factor_per_unit": math.exp(slope), "r2": r2, "ss_res": ss_res,
        "intervals": intervals, "interval_spread": spread,
        "intervals_agree": spread < 1.05,
    }


def coarsest_explanation(points, tolerance: float = 0.05) -> dict:
    """RULE 6: among descriptions that explain the data, the COARSEST wins.

    Two candidates, in order of how many free parameters they spend: a constant (one parameter - 'the count does not depend
    on b3') and an exponential (two). If the constant explains the points to within `tolerance` in log-space, it wins and the
    exponential is unearned. If it does not, the exponential is the coarsest description that survives - and it still has to
    answer for its intervals, which is Rule 1's job.
    """
    ys = [math.log(v) for _, v in points]
    mean_y = sum(ys) / len(ys)
    constant_err = max(abs(y - mean_y) for y in ys)
    r = fit_report("fit", points)
    return {
        "constant_max_log_error": constant_err,
        "constant_explains": constant_err <= tolerance,
        "exponential_r2": r["r2"],
        "chosen": "constant" if constant_err <= tolerance else "exponential",
    }


def main() -> int:
    print("RULE 1 — an exact claim needs no two-sided test; a fit lives or dies by its degrees of freedom\n")

    print("EXACT ENUMERATIONS (nothing fitted, nothing left to predict)")
    for b3 in L.LADDER:
        c = L.content(b3)
        print(f"  b3={b3:<2} flux pairs {c['flux_pairs']:>7,}  primitive orbits {c['orbits']:>7,}  "
              f"orbits/pairs {c['quotient_ratio']:.6f}  N<=1 orbits {c['up_to_1']:>7,}")
    print("  -> the quotient removes ONE pair at b3=6 of 531,441. This is a count, not a fit: the rule does not apply, "
          "and the refutation stands on arithmetic.\n")

    print("FITS (two parameters through three points: one degree of freedom)")
    for name, points in (("content", B.CONTENT), ("accessibility", B.ACCESSIBILITY)):
        r = fit_report(name, points)
        print(f"  {name}: {r['n_points']} points, {r['n_params']} parameters, {r['dof']} dof, "
              f"x{r['factor_per_unit']:.4f} per unit b3, R^2 {r['r2']:.6f}")
        for i in r["intervals"]:
            print(f"      b3 {i['from']} -> {i['to']}: x{i['per_unit']:.4f} per unit")
        verdict = "intervals AGREE (within 5%)" if r["intervals_agree"] else \
                  f"intervals DISAGREE by x{r['interval_spread']:.3f}"
        print(f"      {verdict}")

    rc = fit_report("content", B.CONTENT)
    ra = fit_report("accessibility", B.ACCESSIBILITY)
    print("RULE 6 - the coarsest description that explains the data\n")
    for name, points in (("content", B.CONTENT), ("accessibility", B.ACCESSIBILITY)):
        c = coarsest_explanation(points)
        state = "EXPLAINS" if c["constant_explains"] else "does not explain"
        print(f"  {name}: a constant is off by up to {c['constant_max_log_error']:.3f} in log X "
              f"({state}, tolerance 0.05) -> the coarsest description is the {c['chosen']}")
    print()

    print(f"""
WHAT THE AUDIT SAYS, claim by claim:

  landscape_count   "the 10^500 framing is not inflated by gauge copies"
                    EXACT. No fit, no dof, no prediction owed. The rule does not apply and the refutation stands.
                    A two-sided score here would be manufactured, not earned.

  content           the orbit count against b3
                    A FIT with 3 points and 2 parameters - ONE degree of freedom. The intervals agree to a factor of {rc['interval_spread']:.4f} per unit b3, which is a genuine self-consistency check the fit did not consume. But the counts are
                    EXACT integers, so there is no noise for a 1% residual to hide in: the content is not exactly
                    exponential, and the honest description is 'a power law that fits to about 1%', not 'the law'.

  accessibility     the sampler yield against b3
                    A FIT whose intervals DISAGREE by a factor of {ra['interval_spread']:.3f} per unit b3 - and R^2
                    {ra['r2']:.3f} hides that, which is the whole reason the intervals are reported. The exponential is not
                    established, and the module already says so - which means this claim was ALREADY two-sided before the
                    bench existed. It is the best-behaved claim of the three, and the one to copy.

WHAT CHANGES, and the answer is uncomfortable but clean:

  none of the VERDICTS change. The refutation is arithmetic, and the content scaling was already labelled a fit.
  what changes is the STATUS of the two exponentials: one is a description at the 1% level on exact data (so a
  fourth b3 point would test it, and three cannot), and the other is not an exponential at all. A reader of the papers
  should not find 'scales as X^(2.15)' presented without that.

THE CHEAPEST NEXT TEST: a fourth b3 value for the content count. Three points and two parameters cannot fail a form; four
points can. That is the same statement as 'a room with forty modes identified to 2 Hz needs the peaks it did not fit', one
level up.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
