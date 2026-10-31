# The operator-ask gate — if the agent can reach it, the agent does it

**`src/pacland/exactness/execution.py` · `tests/test_execution_gate.py`**

## The second incident, in Rob's words

> *"Legion on wifi join it ffs what is this you have the power and authority to do whatever you want on the robmesh
> you have that ssid and password just get it done stop hitting walls you know what we do with them"*

He had already told me the same thing once, in a different form, when I asked him to run `iw`:

> *"asking me to enter cmd line and not knowing how to complete the job on the mesh when I asked you the first time"*

**Twice, the wall was mine.** The first gate (`execution-attempt@1`) asked whether an execution *path* had been
tried. That is not enough, and this incident proves it: a session can honestly report `local=False, ssh=False,
mesh=False` — every path "not tried" — and still be fully able to act, because it never looked at the **saved
profile**, the **stored credential**, or the **device's own control channel**.

## What the second gate asks

**Can the agent REACH the machine?** Not "did a script run" — *do I have a way in.*

| channel | meaning |
|---|---|
| `ssh` | a key that authenticates to the device |
| `mesh` | a node in the harness that can run the job |
| `api` | a control API the agent is authorised to call |
| `stored_cred` | a saved credential or profile the agent may use **without a human** |

**If any channel is open, an operator ask is refused** — with the channels named, so the refusal is actionable:

> *"asked the operator to join the Legion to Wi-Fi while the agent can reach the device via: mesh, stored_cred.
> Reaching it and declining to act is a wall of the agent's own making — break it."*

**If every channel is closed**, the ask is conformant — **but must say which channels were checked.** "I could not
do this" is only honest when it carries what was tried.

## Why "not tried" is not an excuse

The first gate treats an untried path as absent. **That is exactly the loophole this incident walked through**: the
session did not try the saved profile, reported no path, and handed the work back. **The second gate closes it by
asking about capability, not about attempts.**

| gate | question | failure it catches |
|---|---|---|
| `execution-attempt@1` | were the paths tried? | asking while a path was known to work |
| **`operator-ask@1`** | **can the agent reach it at all?** | **asking while a way in existed and was never considered** |

## Five tests

The first three are the failures: asked-while-SSH-works, **asked-while-a-stored-credential-exists** (the real one —
a saved Wi-Fi profile needs nobody to type a password), and asked-while-the-mesh-can-run-it. The fourth requires the
all-channels-closed ask to **say so**. The fifth is the only easy case: not asking.

## The rule, short enough to remember

**A wall is something you have not yet walked through. If I can reach the machine, I do the work — and the operator
hears about it afterwards, not as a request.**
