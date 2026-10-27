"""The plain-speak one-pagers — written for a Year 10 student, read by an adult.

Three pages, one per discipline. No jargon, no symbols, everyday analogies.

Every page answers the same four things in the same order, because a reader comparing
disciplines should not have to hunt:

  1. what we checked, and what we found
  2. **the best model we have right now**, named, with its numbers
  3. **how to refine it** — the concrete fix, not a wish
  4. **what this means for the world** — and, last, what it still cannot do
"""
from __future__ import annotations


def landscape() -> list[tuple[str, str]]:
    """One page: the string landscape (physics), in words a 15-year-old can follow."""
    return [
        ("title", "PACLAND · Physics, in plain words"),
        ("subtitle", "What we checked, what we found, and what to do next. One page, no jargon."),

        ("h", "1 · The question"),
        ("p", "String theory allows about 10^500 different universes, each with different particle masses. "
              "How would you ever know which one is ours? The usual answer is: you can't."),

        ("h", "2 · What we found"),
        ("b", "There is exactly ONE exact number, and it is a total. Picture a household budget: the total "
              "spend is fixed, but the individual receipts are not. The total flux is exact; how it is split "
              "between hidden dimensions is not."),
        ("b", "That is provable, not a hunch. Every quantity that survives the theory's symmetries is a power "
              "of that one number. We machine-checked the proof step by step, so it is \u201cthe computer "
              "verified it\u201d, not \u201cwe believe\u201d."),
        ("b", "The 19 open numbers of particle physics stay open. Nobody derives the electron mass; a final "
              "theory supplies relations between numbers, not the numbers."),

        ("h", "3 · The best we have right now"),
        ("p", "A tower of six results that are machine-checked rather than argued, plus one workable model "
              "universe — a six-dimensional torus — where every rule about quantum gravity can be proved "
              "exactly. Counted honestly, that is nine things we can check against the real world. Not the "
              "answer to string theory; the only part of it that is not opinion."),

        ("h", "4 · How we refine it"),
        ("b", "Finish the proofs: most are checked only to low orders, and the general case is the next slice "
              "of work."),
        ("b", "Use checks that cost nothing: a shape and its mirror carry swapped labels, so every mirror pair is a known "
              "answer to test the tools against — no new data, no new experiment."),
        ("b", "Count the deficit upward only where it can grow: the flux side is saturated at one, so the next "
              "rungs must come from branes and the Standard Model."),

        ("h", "5 · What this means for the world"),
        ("p", "It tells physicists where a final theory can deliver numbers and where it cannot. That is worth "
              "money: a detector built to measure a number the theory can never give is a detector built on a "
              "misreading. And the method — machine-check the invariants, count what is verified, state the "
              "rest as not yet determined — is what we now apply to climate, medicines and economics."),

        ("h", "6 · What this cannot do"),
        ("p", "It cannot say which universe is ours, or what the masses are. Nobody can, yet. What it can do is "
              "say exactly which choices are still open — and that is the part that can be checked."),
    ]


def climate() -> list[tuple[str, str]]:
    """One page: climate, in words a 15-year-old can follow."""
    return [
        ("title", "PACLAND · Climate, in plain words"),
        ("subtitle", "What we checked, what we found, and what to do next. One page, no jargon."),

        ("h", "1 · The question"),
        ("p", "Nobody can check a prediction about the year 2100. So the useful question is smaller: can we "
              "check whether a climate model deserves to be believed at all?"),

        ("h", "2 · What we found"),
        ("b", "Heat leaks, in most models. Of the models with data to check it, 15 of 19 leak heat. One leaks "
              "almost twice as much heat as the warming it is trying to predict. Picture a bucket with a hole: "
              "the level you predict is wrong by the size of the hole."),
        ("b", "The simplest guess is hard to beat. Continue the warming we have already measured in a straight "
              "line — a ruler. On real data most models lose to the ruler, because a ruler cannot be wrong in "
              "complicated ways."),
        ("b", "The leak is in the join, not the ocean. Salt is conserved far better than heat, and salt only "
              "moves in water while heat crosses between air and sea. So the mistake is where the model "
              "connects the two."),

        ("h", "3 · The best we have right now"),
        ("p", "The model GISS-E2-1-G passes all three checks we can run — how warm it says the world gets, how "
              "strongly it traps heat, and whether it leaks. Three out of three, and its certificate says three "
              "things checked. On the simplest comparison, the ruler (the warming so far, continued) beats "
              "guessing that nothing changes, every time we tried. Whether the ruler or one of the better models "
              "wins depends on which years you start from, so we claim the first and not the second."),

        ("h", "4 · How we refine it"),
        ("b", "Fix the join first. Heat and mass leak and salt does not, so the defect sits where the model "
              "couples atmosphere and ocean — a concrete bug in a known place, not a mystery."),
        ("b", "Measure what is missing. Two of the five conservation laws have no measurement in our data yet; "
              "closing them makes the checklist five checks instead of three."),
        ("b", "Score against the ruler before anyone uses a model, and never build on a model with no leak data "
              "at all — 36 of 53 have none."),

        ("h", "5 · What this means for the world"),
        ("p", "Better projections sooner, by repairing a known defect instead of buying more computers: the "
              "missing ingredient is measurement, not number-crunching. And it gives a reader a sentence they "
              "can trust in a headline — this projection comes from a model that passes the tests, or it does "
              "not."),

        ("h", "6 · What this cannot do"),
        ("p", "It has not checked a single model against the actual future. Nobody has. Every projection is an "
              "extrapolation; the difference is whether the model first passed the tests that let you trust "
              "the extrapolation."),
    ]


def economics() -> list[tuple[str, str]]:
    """One page: money and forecasts, in words a 15-year-old can follow."""
    return [
        ("title", "PACLAND · Money and models, in plain words"),
        ("subtitle", "What we checked, what we found, and what to do next. One page, no jargon."),

        ("h", "1 · The question"),
        ("p", "Somebody forecasts growth, inflation or jobs every day. The interesting question is not whether "
              "the forecast is clever, but whether it beats the dumbest possible guess."),

        ("h", "2 · What we found"),
        ("b", "\u201cSame as last time\u201d is hard to beat for inflation. Our textbook model was 3% worse "
              "than simply guessing inflation stays put — and so was the same model using the published "
              "settings of the famous central-bank version. Being clever did not help."),
        ("b", "Some numbers cannot be measured from totals at all. We asked a method to recover a value we knew "
              "in advance, 0.18, from perfect fake data: it answered 1.00. The totals do not contain the "
              "answer, and more data will not put it there."),
        ("b", "The accounts add up; the inflation-adjusted version does not. Total spending equals households + "
              "business + government + trade to within one part in ten thousand — but the inflation-adjusted "
              "version leaks by up to 25 points in 2020, like adding a metre to a yard and calling it a total."),

        ("h", "3 · The best we have right now"),
        ("p", "The Atlanta Fed's GDPNow: four times better than the simplest guess at nowcasting GDP, and still "
              "three times better scored against the revised figures. Second is a plain statistical model, 14% "
              "better than the guess one quarter ahead. The best of our structural models does not beat the "
              "guess at all — that is the finding, not a footnote."),

        ("h", "4 · How we refine it"),
        ("b", "Publish the comparison. No forecast should appear without its \u201csame as last time\u201d "
              "number beside it — ours are published with it, including where they lose."),
        ("b", "Refuse impossible fits. A fitted model is checked against the accounting rules before it gets a "
              "results table; that check has already refused one."),
        ("b", "Change the evidence, not the quantity. The unrecoverable numbers need different data — fast-"
              "moving prices, differences between firms — not more of the same totals."),

        ("h", "5 · What this means for the world"),
        ("p", "A verified-forecast label is now possible: how many things a model was checked against, whether "
              "it passes the accounting rules, and whether it beats the simplest guess. That is what a reader, "
              "a regulator or a journalist actually needs — and nobody publishes it today."),

        ("h", "6 · What this cannot do"),
        ("p", "It cannot give a certified inflation number for next quarter. The exact part of economics is "
              "bookkeeping, and the interesting numbers are not recoverable from the totals. That is not for "
              "want of effort — it is what the data is."),
    ]


def all_pages() -> dict[str, list[tuple[str, str]]]:
    return {"landscape": landscape(), "climate": climate(), "economics": economics()}
