# The execution gate — a command only reaches the operator if no path exists

**`src/pacland/exactness/execution.py` · `tests/test_execution_gate.py`**

**The incident this closes.** On 2026-10-31 this session asked Rob to run `iw dev wlan0 survey dump > survey.txt`
and drop the file in Downloads — while a `radio:wifi` node with a working SSH key was sitting on the mesh. His
words: *"asking me to enter cmd line and not knowing how to complete the job on the mesh when I asked you the
first time."*

**The rule:** a command reaches the operator **only if no execution path exists**, and a path counts as absent
only when it was **tried and recorded.**

## The three paths, in the order they must be attempted

| path | question | probe |
|---|---|---|
| `local` | can this machine run it? | run it |
| `ssh` | does a key work for a host that can? | `ssh -o BatchMode=yes <host> true` |
| `mesh` | is there a node whose capabilities fit? | `dispatch.py --list` + `--needs` |

## What the gate refuses

| situation | why it is refused |
|---|---|
| `asked_operator` while **any** path works | *"the mesh exists for this — dispatch it"* |
| `no_path_exists` while a path was tried and worked | the record contradicts itself |
| `ran` or `refused_by_environment` with **nothing** recorded as attempted | silence is not an attempt |
| an outcome outside the four allowed values | the vocabulary is the guarantee |

## The four honest outcomes

- **`ran`** — executed, somewhere, by the agent.
- **`refused_by_environment`** — tried and the environment said no (the `iw`-not-installed case, which returned
  exit 0 with the reason rather than a fake pass).
- **`no_path_exists`** — all three tried and none worked. Then, and only then, the operator is asked.
- **`asked_operator`** — permitted **only** with an empty path record.

## Seven tests, and the first one is the incident

`check({"ssh": True, "mesh": True}, "asked_operator")` **raises**. So does the mesh-only variant. So does a
claimed run with no attempt, and a claimed "no path" when a path worked.

## Why this belongs in the engine and not in a style guide

**A style rule is followed when remembered.** This is a function with a test, so a session that asks the operator
to type a command while a node is available fails its own conformance check — the same mechanism as the claims
registry, applied to the agent's behaviour instead of its numbers.

It is also the `execution-attempt@1` gate proposed in
[VVS issue #112](https://github.com/robmitchellengineering-hub/valiant-verification-sdk/issues/112); this is the
reference implementation, in the repo that has to live with it.
