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
