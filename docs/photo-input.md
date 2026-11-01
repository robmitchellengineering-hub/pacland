# Photo input — the path works, end to end

**First real photo from the phone: 1600 × 1200, 194 KB, one POST, stored as a real file.**

```
runs/phone/photo-1793509531757-spot_847/photo.jpg   199,140 bytes   1600x1200
```

That is the whole chain: **camera intent → downscale → JPEG quality 60 → base64 → board → file on disk.** The image
was a photo of a dog in a car, which is exactly the right kind of test: it proves the pipeline, and it says nothing
about a room.

## What took three releases to get right

| release | what it fixed |
|---|---|
| **0.8.0** | capture, downscale to a 1600 px long edge, compress, base64, upload; board decodes to `photo.jpg` |
| **0.8.1** | **the camera URI grant** — on API 21+ the write permission must travel in the `ClipData` **and** be granted to each camera package; without it the camera returns `RESULT_OK` having written nothing |
| — | plus a thumbnail fallback, and failures that **name themselves** |

**The first photo attempt produced nothing at all** — no request reached the hub — which is why the grant, not the
upload, was the fault.

## What a room needs, and why

| requirement | reason |
|---|---|
| **2–4 photos per room** | one view cannot show the room; opposite corners give the wall lines |
| **landscape, phone level** | a tilted phone skews every inferred line |
| **two corners visible** | corner geometry is what fixes the room's scale and shape |
| **the spot label matches the scan** | so the photo, the level and the walk belong to the same place |

## What this buys, and when

**Not a floor plan by itself.** A photo gives wall *lines* and a field of view; with the focal length it gives
**angles**, and with two corners it gives **relative proportions**. That is enough to place rooms relative to each
other — the frame the walks could not supply.

**The order that works:** photos → room rectangles → the 12 measured levels and the walk paths land on a real plan →
a coverage map that is a map, not a demonstration.

`scripts/photo_index.py` lists what has arrived per spot and flags anything too small to use, so the set can be
checked before an atlas is attempted.

## The two scripts that turn a photo set into a layout

**`scripts/photo_glue.py`** — matches each uploaded photo to a room **by the spot label the phone already sends**, and
with `--write` records the hub directory names into the template's `photos` list. It also prints the rooms with **no**
photo, which are the ones that cannot be measured yet.

```
1 usable photos on the hub, 0 rooms matched, 11 rooms with none
```

That is the honest state today: **one test photo, no room matched**, and the script says so rather than reporting
success at a count of zero.

**`scripts/layout_check.py`** — refuses to let an invented or half-filled layout become a picture:

- every room needs four numbers, or it is **not placed** (and is named)
- rooms must not **overlap** (a wall in two places is two rooms drawn over each other)
- rooms must not **float** (a house whose rooms do not touch is a diagram)
- a room's area must be **plausible for its name**

```
11 rooms: 0 placed, 11 unplaced
NOT READY: 11 rooms have no position: ...
```

**It cannot tell whether the dimensions are the right house** — those are consistency checks, not measurements, and
the script says so on its last line. That distinction is the whole reason it exists: the failure mode it prevents is a
confident-looking coverage map drawn on invented rooms.

## The measurement endpoint, proved with a synthetic payload

**`scripts/apply_measurements.py`** — reads capability `measure` from the hub, groups by room, and fills the template's
`w`/`h`. Proved end to end with a posted measurement: `POST` returned 200, the script reported
`usable as a room: 2.61 x 3.42 m`, and `--write` put **2.61 x 3.42** into the kitchen row. The synthetic record was then
deleted and the template restored, so nothing invented survives in the tree.

**What it refuses to do matters more than what it does.** It cannot know which line is a width and which is a diagonal,
so it will not guess:

- one measurement is **a line, not a room** — it says so and leaves the room blank;
- two measurements **within 25% of each other** are probably the same wall measured twice, and it says that instead of
  calling them a room;
- if any room fails, **`--write` refuses the whole file**, because a layout half-filled from bad numbers is worse than an
  empty one.

**This is the loop closing**: tap two points on the phone, press UPLOAD, run one command, and the blank `w`/`h` in the
template become real metres with their provenance recorded.
