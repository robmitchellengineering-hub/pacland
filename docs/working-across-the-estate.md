# Working across the estate from this repo

**For a session that starts in `pacland` and needs the other repositories.** Everything here was learned by doing it and
paying for it; each line names the failure that bought it. All of them are mirrored on the Mac.

## The repositories, and which one owns what

| repo | Mac path | owns | do not put here |
|---|---|---|---|
| **pacland** (this one) | `~/code/pacland` | **the numbers**: mode count, streams, identifiability, the chamber, the channel plan, the per-AP health table, the placement model, and the measurement chain that feeds them | anything that talks to a router, or to a phone |
| **airmatrix** | `~/code/airmatrix` | **the desk and the radio**: `rob-probe` (surveys, the optimizer, the `Backend` trait for router control), `rob-io` (the engine), the 3D/GUI work, and designs 01–42 | the analysis — it reads pacland's outputs |
| **robmesh-android** | `/tmp/robmesh-android` (**a clone in /tmp — GitHub is the source of truth**) | **the instrument**: the phone node, ARCore room scans, spot scans, 41 sensors, the homing meter, photos | analysis or router control |
| **harness-mesh** | `~/harness-mesh` | **the bus**: the board (`:8081`), job files, node cards, dispatch, and the 3D board idiom (`board/ships.js`) | product decisions |
| **morpheus-self-hosted** | `~/code/morpheus-self-hosted` | its own product; its rules live in its own `AGENTS.md` | pacland's physics |

**A session in pacland that needs a measurement from a machine, a router setting, or a phone capability should dispatch it,
not re-implement it.** The interface is the bus, described below.

## The bus, exactly

**Post a result** (this is what the phone does, and what any node does):

```
POST http://<board>:8081/node/<host>/result      header: x-board-pin: <~/.dsh/board-pin>
{ "id": "...", "state": "pass|suspect|fail", "stdout": "<a JSON string>", "stderr": "why" }
```

**The board writes** `runs/<host>/<id>/{result.json, stdout.txt, stderr.txt}` and, when the body carries `photo_b64`,
`photo.jpg` beside them. **Read the run directory; do not ask anybody to retype an answer.**

**Queue a job** for a node:

```json
// jobs/<host>/<YYYY-MM-DDTHHMMZ>-<host>-<slug>.json
{ "id": "...", "capability": "sensor:read", "args": {"type": "android.sensor.pressure", "samples": 5},
  "note": "what it answers, and what would make it wrong", "dispatched_by": "mac" }
```

**Then push to the `hub` remote** — a job that is only committed locally never reaches the node.

**Capability naming is `family:verb`**, and a node advertises **only what it can actually do**, generated from the device:
`wifi:scan`, `wifi:link`, `radio:wifi`, `sensor:list`, `sensor:read`, `sensor:<family>`, `imu:track`, `photo`, `measure`,
`measure_diag`, `homing`.

**A refused capability answers `pass` with `REFUSED: …` in stdout. A capability that ran and produced nothing answers
`suspect` with the reason.** Never a fake pass — that shape has bitten this mesh more than once (the WiFi scan that returned
zero BSS after a reboot and was posted as `pass`).

## The measurement semantics that must not be re-derived

| fact | value | where it came from |
|---|---|---|
| **step distance is not a metre** | 17–48% error: three 30 m walks gave 92, 92, 62 counts | `docs/arcore-over-pdr.md` |
| **ARCore is the metre** | two walls of one room agree to **1 cm**; ARCore's world is **per session**, so lengths from two sessions cannot be combined | `docs/arcore-over-pdr.md` |
| **the ceiling** | **2.58 m ± 0.09 m** for this house — the spread of three identical ceilings is the *phone's* error | `scripts/height_error.py` |
| **fading at a fixed spot** | **16 dB**, at rest, power is exponential (std/mean **1.21** against Rayleigh's 1.00) | `docs/fading-is-rayleigh.md` |
| **the action floor** | **6 dB** — nothing below this is a finding, because it is inside the instrument's own noise | `docs/channel-plan.md` |
| **a room needs two walls from ONE session** | one measurement is a line; a duplicate wall is caught from the coordinates, not from the lengths | `scripts/apply_measurements.py` |

## The gates that will stop a PR, and what each wants

**pacland**

- **the test count is quoted in five documents** (`README.md`, `docs/arxiv-submission.md`,
  `docs/swampland-connection.md`, `docs/t6-exact-oracle.md`, `docs/ai-verified-badge.md`) and `test_doc_claims` compares
  them against the suite. **Adding tests breaks it; update all five in the same commit.** It reports the number it
  collects, so use that, not a local run.
- **`web/index.json` is generated**: run `python3 scripts/build_site_index.py` in the same commit as anything that adds a
  script or a doc.
- **`docs/known-positives.md` is generated** by `scripts/positives.py`; a quoted residual must be an **order-of-magnitude
  bound** (`below 1e-15`), never a value at 1e-16 — that printed `3.4e-16` on macOS and `1.7e-16` on CI and the file
  differed between machines.

**airmatrix**

- **`scripts/check.sh`** runs fmt, clippy and the workspace tests. `cargo fmt --all` before committing; a rustfmt diff
  fails the Windows gate and the file *looks* fine.
- **the unbuilt register** (`docs/UNBUILT.md`) must carry every open `## Build order` item of every design note. **Rows
  need all six columns** (`id | item | note | state | done when | public`) — a five-column row is not parsed at all — and
  **ids must be unique**; a collision and a missing column both look like "not registered".
- **`rob-sync`'s loopback tests are timing-sensitive**: they fail on a loaded machine (twice here) and pass on a quiet one.
  **Re-run before diagnosing.**
- **the Windows check runs on the self-hosted laptop runner (RME1)**, not GitHub's queue. **Read the job, not `gh pr
  checks`'s status word** — "pending" once meant "ran 11 s ago and failed".

**robmesh-android**

- **ARCore metadata must be `<meta-data name="com.google.ar.core">` INSIDE `<application>`.** At manifest level the parser
  ignores it and ARCore throws a fatal exception while the file visibly contains the line.
- **`checkAvailability()` lies**: it returns `unknown_error` on a supported handset (S24 Ultra). **The test is opening a
  `Session`**, and its exception name is the diagnosis.
- **the camera permission** is needed by ARCore and was never needed by the photo path (which hands off to the system
  camera app), so a fresh install fails with a message that reads "ARCore is not installed".
- **one code path**: the probe button and the launch probe had separate implementations and drifted immediately; the same
  happened to the label (the spot scan read the text field, the room scan read a preference that was never written).
- **install and release**: `JAVA_HOME=~/jdk17/Contents/Home`, `ANDROID_HOME=~/android-sdk`, `~/gradle/bin/gradle`; verify a
  string in the APK with `aapt2 dump xmltree`, **not** `strings` on resources — that gives false negatives.

**harness-mesh**

- **never `git add -A`**; stage the job or result paths explicitly.
- **a stale `.git/index.lock`** blocks commits; check for the process before deleting it.
- **the board's `readBody` defaulted to 64 KB** and silently refused every full-rate trace. It is 4 MB for the node result
  route now; **if an upload fails, check the board log for `REJECTED`, which now names the reason**.
- **push jobs to the `hub` remote** (`git push hub main`), which is what the nodes pull.

## The delivery rules

- **a link Rob can open from outside the Mac**: `https://github.com/robmitchellengineering-hub/<repo>/raw/main/<path>`, or a
  tailnet URL (`http://100.90.120.32:<port>/<file>`) when a file is not in a repo.
- **never print a secret.** Router and AP credentials are resolved from `~/.dsh/*.env` (mode 600) at the moment of use; the
  repository records the **reference**, never the value.
- **merge on green**; ask before `--admin` for a hung check, and say which check and why.

## What not to touch from here

**VVS and the audio work belong to other sessions.** `morpheus-self-hosted` has its own protocol. **Do not restart or kill
`dsh web`, Tailscale, `cloudflared` or the tunnel.**
