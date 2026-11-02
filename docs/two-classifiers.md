# Two classifiers, one dataset: where pacland and AirMatrix disagree

AirMatrix's `rob-site` and this repo's `scripts/apply_measurements.py` both turn ARCore sessions into rooms. **They were run
on the same five sessions on 2026-11-02, and they disagreed on two of them.** That is the most useful thing either has
produced this week, because a room dimension is a number a certificate may later rest on.

## The comparison

| session | measured lines (m) | **pacland** | **rob-site** | agree? |
|---|---|---|---|---|
| `…3945165` | 2.67, 2.62, 5.98, 2.74 | 2.62 × 2.67 (2.74 and 5.98 suspect) | **refused**: no floor-to-ceiling line | ✗ |
| `…170120` | 5.28, 5.03, 3.81, 3.36, 3.27, 1.14, 2.65 | 5.03 × 5.28, ceiling 2.65 | 5.28 × 5.03, ceiling 2.65 | ✓ |
| `…230339` | 2.14, 3.85, 2.24, 2.70 | **2.24 × 3.85**, ceiling 2.70 | 3.85 × 2.24, ceiling 2.70 | ✓ *(after the fixes below)* |
| `…1742211` | 4.73 | refused: one line | refused | ✓ |
| `…3834335` | 4.15 | refused: one line | refused | ✓ |

## Two real bugs in this repo's classifier, found by the comparison

1. **`room_from_walls` said "the two longest" and took the first one measured.** Sessions upload in measurement order, so
   "first" was whatever the phone happened to record first. **`…230339` came out as 2.14 × 2.24 m — the two *shortest*
   lines of a 3.85 × 2.24 m room.** Fixed: sort by length, then take the two longest that are not the same line in space.

2. **A long wall in a rectangular room was rejected as an outlier.** The rule threw out any wall longer than 1.6× the
   session's median, which is exactly what the long wall of a normal room is. **The same session lost its 3.85 m wall and
   the room came back as 2.14 × 2.24.** Fixed: the outlier bound is now against the *shortest* wall at 3×, plus an absolute
   15 m cap — a 1.8:1 room is not an anomaly.

**A third change, smaller**: a line under 1.5 m is a door or a partial drag, not a wall. The 1.14 m line in the 5 × 5 m room
was being treated as one of its dimensions.

## The one remaining disagreement, and why it is not a bug

**`…3945165`**: 2.62, 2.67, 5.98 and 2.74. A 2.62 × 2.67 m room has a **diagonal of 3.74 m**, so **no wall of it can be
5.98 m** — but is 5.98 a mis-tap, or is the room bigger than the pair suggests?

- **`rob-site` refuses the session**, because it did not find a floor-to-ceiling line: 2.74 is not confidently vertical.
- **pacland accepts it** as 2.62 × 2.67 with 5.98 as a suspect.

**A diagonal bound was tried and removed.** It rejected the bedroom's impossible 5.98 m line and **also** rejected the spare
room's genuine 3.85 m wall (the diagonal of its two short walls is 3.10 m), turning a correct room into a wrong one.
**A rule that fixes one session by breaking another is not a rule.**

**So `pairing_alternatives()` now reports every defensible pair.** For `…230339` that is *both* (2.24, 3.85) and (2.14,
2.24); for `…3945165` it is (2.67, 5.98), (2.62, 5.98) and (2.62, 2.67). **The operator knows which room it is, and a fourth
wall settles it without asking anybody** — the capture flow already says four walls make this trivial.

## What this means for the product

- **A room needs four walls, not two.** Two is enough to *propose*; four is what makes it *certain*. The app should say so at
  the end of a scan: *"two walls found — a third and fourth make this unambiguous."*
- **The two implementations should share fixtures.** `rob-site`'s tests already carry real ARCore coordinates; this repo's
  now do too. **A divergence between them is a defect in one of them, and the only way to know which is to run both on the
  same file.**
- **The floor-to-ceiling line requirement is a product decision, not a bug.** It costs rooms and buys certainty. **Rob should
  pick one and both implementations should follow it.**

## The falsifier

> **If a tape measure shows `…3945165` really is 2.62 × 2.67 m, then `rob-site` is refusing a room that pacland gets
> right, and its floor-to-ceiling rule is too strict.** One tape measurement on that room settles which classifier is
> right — and it is the same tape that settles the ARCore-versus-steps question.
