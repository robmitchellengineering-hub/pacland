"""The plain-speak one-pagers — written for a Year 10 student, read by an adult.

Two pages, one per discipline. No jargon, no symbols, everyday analogies, and the honest
limit stated last. They exist because the full explainers are written for someone who
already knows the field; these are written for someone who does not, and for a specialist
who has two minutes.

Each ends on the sentence that matters: what was checked, not what was predicted.
"""
from __future__ import annotations


def climate() -> list[tuple[str, str]]:
    """One page: climate, in words a 15-year-old can follow."""
    return [
        ("title", "PACLAND · Climate, in plain words"),
        ("subtitle", "What we checked, what we found, and what it means. One page, no jargon."),

        ("h", "1 · The question"),
        ("p", "Climate models predict the future. Nobody can check a prediction about the year 2100, because "
              "2100 has not happened. So the useful question is smaller, and answerable: can we check whether "
              "a model deserves to be believed at all?"),

        ("h", "2 · What we did"),
        ("p", "We borrowed a rule from physics: don't ask a model for its answer — ask what it is not allowed "
              "to do. Physics says energy cannot be created or destroyed. So the heat a climate model takes in "
              "must turn up somewhere: the ocean, the air, the land, the ice. If it doesn't, the model is "
              "leaking. Leaking is not a matter of opinion, and it is easy to check."),

        ("h", "3 · What we found"),
        ("b", "Heat leaks, in most models. Of the models with the data to check it, 15 of 19 leak heat. "
              "One leaks almost twice as much heat as the amount of warming it is trying to predict. "
              "Picture a bucket with a hole: the level you predict is wrong by the size of the hole."),
        ("b", "The simplest guess is hard to beat. We asked whether a model beats a ruler — take the warming "
              "we have already measured and continue it in a straight line. On real data, most models lose. "
              "A ruler often beats a supercomputer, because a ruler cannot be wrong in complicated ways."),
        ("b", "The leak is in the join, not the ocean. Salt is conserved far better than heat. Salt only moves "
              "in water; heat crosses between the air and the sea. So the mistake is where the model connects "
              "atmosphere and ocean — which is good news, because that tells you what to fix."),

        ("h", "4 · How we score a model"),
        ("p", "For each model we count what it was actually checked against: how warm it says the world will "
              "get, how strongly it traps heat, and whether it leaks. The best of our three models scores "
              "three checks. A model that leaks scores two. The worst scores one. That count is the "
              "model's certificate: it says how much of the model is checked, not how clever it is."),

        ("h", "5 · What it means"),
        ("p", "Don't build on a leaking model, however good its graphs look. Spend money on measurements rather "
              "than on bigger computers: what is missing is data, not number-crunching. And say the honest "
              "sentence out loud — a projection for 2100 is an educated guess. What can be checked is whether "
              "the model is allowed to be believed."),

        ("h", "6 · What this cannot do"),
        ("p", "We have not checked a single model against the actual future. Nobody has. Every projection "
              "you read is an extrapolation. The difference between a good one and a bad one is whether the "
              "model first passed the tests that would let you trust the extrapolation."),
    ]


def economics() -> list[tuple[str, str]]:
    """One page: money and forecasts, in words a 15-year-old can follow."""
    return [
        ("title", "PACLAND · Money and models, in plain words"),
        ("subtitle", "What we checked, what we found, and what it means. One page, no jargon."),

        ("h", "1 · The question"),
        ("p", "Every day somebody forecasts growth, inflation, jobs. The usual question is whether the forecast "
              "is clever. The useful question is whether it can be checked at all — and whether it beats the "
              "dumbest possible guess."),

        ("h", "2 · What we did"),
        ("p", "We took six real models — a textbook one, the workhorse central banks use, a plain statistical "
              "one, the Atlanta Fed's published nowcast, and two reference points — and scored them all the "
              "same way. Every check uses data as it was published at the time, never today's revised numbers. "
              "That matters: scoring a forecast against numbers it never had is cheating by accident."),

        ("h", "3 · What we found"),
        ("b", "\u201cSame as last time\u201d is hard to beat for inflation. Our textbook model was 3% worse than "
              "simply guessing that inflation stays where it is. So was the same model using the published "
              "settings of the famous central-bank version. Being clever did not help."),
        ("b", "Simple statistics beat theory here. A plain statistical model beat the same-as-last-time guess by "
              "14% at one quarter ahead, and by 37% at a year ahead."),
        ("b", "A professional nowcast wins clearly. The Atlanta Fed's GDPNow was four times better than the "
              "simplest guess at nowcasting GDP — and still three times better when scored against the "
              "revised figures."),
        ("b", "Some numbers cannot be measured from totals at all. There is a number in the model for how much "
              "prices respond to spare capacity. We asked: if the true value were 0.18, could our method find "
              "it? Fed perfect fake data, it answered 1.00. The totals simply do not contain the answer. More "
              "data will not help; different evidence will."),
        ("b", "The accounts add up; the inflation-adjusted version does not. Total spending equals households + "
              "business + government + trade, to within one part in ten thousand. But the version adjusted for "
              "inflation leaks, by up to 25 percentage points in 2020, because adjusted dollars are not "
              "addable — like adding a metre to a yard and calling it a total."),

        ("h", "4 · What we built"),
        ("p", "Three gates, and all three have already refused something real. The null gate: no forecast is "
              "published without its same-as-last-time comparison. The identification gate: no estimate is "
              "published unless the method can first recover a known answer from fake data. The admissibility "
              "gate: no model gets a results table if it breaks the accounting rules."),

        ("h", "5 · What it means"),
        ("p", "A verified-forecast label is now possible for any economic model: how many things it was checked "
              "against, whether it passes the accounting rules, and whether it beats the simplest guess. "
              "Nobody publishes that today. And the honest limit: we cannot give you a certified inflation "
              "number for next quarter. The exact part of economics is bookkeeping, and the interesting "
              "numbers are not recoverable from the totals. That is not for want of effort — it is what the "
              "data is."),
    ]


def all_pages() -> dict[str, list[tuple[str, str]]]:
    return {"climate": climate(), "economics": economics()}
