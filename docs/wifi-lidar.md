# WiFi as LiDAR — what closes the gap, and what never will

**Status: design.** Written after the first walk produced a blob (see `house-map.md`), and after a research fan-out on
what the field actually does.

## Why the current map is a blob, in one line

**LiDAR measures a distance per point. RSSI measures a scalar with three unknowns inside it** — the transmitter's
power, the path-loss exponent, and a ±5 dB fading term that changes minute to minute. We saw that fading directly:
**83 → 88 → 83 % at a fixed spot in one minute.**

So the reconstruction is not under-sampled, it is **under-constrained**: eleven spots and twenty-three APs, all
positions unknown, from measurements that each lose three parameters on the way in.

## What the field does, and what it costs

| approach | what it adds | what it needs | source |
|---|---|---|---|
| **PDR + radio SLAM** — step count and heading from the phone's IMU, fused with radio measurements | **a metric trajectory** — the missing frame, and it is already in the phone | no new hardware | [PDR + FM/Wi-Fi floorplan SLAM](https://ieeexplore.ieee.org/abstract/document/10945751) |
| **CSI sensing** — per-subcarrier complex channel instead of one RSSI scalar | **multipath**, which is the actual LiDAR-like signal: delay and angle per path | a chipset that exposes CSI, or root | [DualSense: sensing and segmentation of signal scatterers](https://ieeexplore.ieee.org/document/11587427) |
| **Learned 3D body reconstruction** through walls | people, not rooms | CSI plus training data | [Multi-Subject 3D Human Mesh from commodity WiFi](https://dl.acm.org/doi/epdf/10.1145/3643504) · [through-wall keypoint mapping](https://healsecurity.com/wifi-signals-reveal-human-activities-through-walls-by-mapping-body-keypoints/) |
| **mmWave / 60 GHz** | a genuine radar: range and angle | line of sight, and it does not go through walls | standard practice |

**The important ordering:** the room reconstruction needs **PDR**, not more APs. The people phase needs **CSI**, not
more APs. Neither needs a new router.

## The three things that would make the room work

### 1. A metric frame — the phone already has it

`STEP_COUNTER`, `TYPE_ROTATION_VECTOR` and `TYPE_LINEAR_ACCELERATION` give a **walk trajectory** to within a few per
cent over a house. That fixes rotation and scale, which is exactly what RSSI cannot.

**This is the design-36 room editor replaced by a walk**: instead of drawing the plan, walk it.

### 2. Density — and the throttle is the problem

Android allows **~4 foreground scans per 2 minutes**. A walk at 1 m/s therefore gives a multi-AP snapshot every
**30 metres** — useless.

**But `WifiManager.connectionInfo.rssi` is not throttled.** The current link's RSSI updates every few seconds, so:

| signal | rate | what it gives |
|---|---|---|
| scan results (all BSS) | ~4 / 2 min | the full fingerprint, sparse |
| **link RSSI** | **seconds** | **a dense 1-D profile along the walk** |

**A dense walk on link RSSI, anchored by sparse full scans, is the practical LiDAR substitute** — and it costs
software, not hardware.

### 3. An estimator that admits what it doesn't know

Least squares on distance residuals is what produced the blob. The honest version is a **MAP estimate with a fading
likelihood** (Gaussian in dB, σ ≈ 5 dB), a prior that keeps the trajectory smooth, and **PDR as a hard constraint**.
And it must output **a covariance**, so the map arrives with an error ellipse instead of looking certain.

## The ground truth nobody has used yet

**A phone with LiDAR, or an iPhone ARKit scan, is the ruler to score this against.** Walk the same path with both:

- LiDAR gives the real room shape,
- WiFi gives the reconstruction,
- **the difference is the number** — and no paper in the fan-out reports it for a house-sized walk with a commodity
  phone.

**That is the publishable result**: not "WiFi can map a room" — many claim that — but **"how wrong is it, measured
against LiDAR, on a walk anyone can repeat"**.

## The plan, staged, each with a falsifier

| stage | build | falsifier |
|---|---|---|
| **A. trajectory** | `imu:track` — steps, heading, a PDR path per walk | if two walks of the same path disagree by more than 10% in length, PDR is not good enough and the frame must come from the room editor instead |
| **B. dense profile** | continuous link-RSSI logging during a walk, timestamped, anchored by scans | if link RSSI does not vary smoothly along the walk (jumps of >15 dB between adjacent samples), the fading swamps the geometry and the dense profile is noise |
| **C. reconstruction** | MAP fit with PDR constraint, output with covariance | if the reconstructed room disagrees with LiDAR by more than the walls' thickness, the model is a sketch |
| **D. people** | CSI capture, the DualSense/3D-mesh line of work | only after A–C hold — **people are a harder problem on the same instrument, and the room has to be right first** |

## What Rob asked about photos and lenses

A photo from the middle of each room, with focal length and sensor size, gives **a field of view per room** — enough
to place walls at the right distances and to texture the result. That is a **cheap ground truth** and it belongs in
stage C, alongside LiDAR, as a second independent check.

**It does not replace the measurement**: a photo says where a wall is; only the radio says how the signal behaves in
front of it.

## The blunt version

**WiFi will not become LiDAR.** RSSI is a lossy scalar and no estimator recovers what was never measured. What it can
become is a **room-sized 3D sketch with an honest error bar**, produced by walking with a phone — and the difference
from LiDAR, measured, is the product's claim.

**Falsifier for the whole idea:** if a walk with PDR cannot beat the room editor's hand-drawn plan on accuracy, then
the product is the room editor and the walk is a nice demo.
