"""The execution-attempt gate: an agent may not hand the operator a command it could have run itself.

Rob, 2026-10-31: *"asking me to enter cmd line and not knowing how to complete the job on the mesh when I asked
you the first time"* — a reply that asked him to run `iw ... > survey.txt` when a `radio:wifi` node and a working
SSH key were both available.

The rule this module enforces:

    a command reaches the operator ONLY IF no execution path exists

and a path is only "absent" when it was TRIED and recorded. The three paths, in the order they must be attempted:

    local   can this machine run it?
    ssh     does a key work for a host that can?      `ssh -o BatchMode=yes <host> true`
    mesh    is there a node whose capabilities fit?   `dispatch.py --list` + `--needs`

A refusal is a complete answer. "Please run this" is not.
"""
from __future__ import annotations

PATHS = ("local", "ssh", "mesh")
OUTCOMES = ("ran", "refused_by_environment", "no_path_exists", "asked_operator")


class ExecutionGateError(AssertionError):
    """A command was handed to the operator while a path to run it existed, or the record is incomplete."""


def check(paths: dict[str, bool], outcome: str) -> dict:
    """Validate an execution attempt and return it in the certificate shape.

    `paths` maps each of `local`, `ssh`, `mesh` to whether it was TRIED AND WORKED. A path not mentioned is
    treated as not tried, which is the safe default: silence is not an attempt.
    """
    if outcome not in OUTCOMES:
        raise ExecutionGateError(f"outcome {outcome!r} is not one of {OUTCOMES}")
    tried = {p: bool(paths.get(p, False)) for p in PATHS}

    if outcome == "asked_operator" and any(tried.values()):
        available = ", ".join(p for p, ok in tried.items() if ok)
        raise ExecutionGateError(
            f"asked the operator to run it while these paths existed: {available}. "
            "The mesh exists for this — dispatch it.")

    if outcome == "no_path_exists" and any(tried.values()):
        raise ExecutionGateError(
            "claimed no path exists while a path was tried and worked — the record contradicts itself")

    if outcome in ("ran", "refused_by_environment") and not any(tried.values()):
        raise ExecutionGateError(
            f"outcome {outcome!r} needs at least one path tried; nothing was recorded as attempted")

    return {"gate": "execution-attempt@1", "paths_tried": tried, "outcome": outcome,
            "conformant": True}


def check_operator_ask(reach: dict[str, bool], outcome: str, *, what: str = "") -> dict:
    """The harder gate: if the agent can REACH the device, an operator ask is non-conformant.

    Rob, 2026-10-31, after being asked to run `iw` and then told to plug a laptop's Ethernet out:

        "what is this you have the power and authority to do whatever you want on the robmesh
         you have that ssid and password just get it done stop hitting walls
         you know what we do with them"

    The first gate (`check`) asks whether an execution PATH was tried. That is not enough: a session can honestly
    report `local=False, ssh=False, mesh=False` and still be able to act, because it never thought to try the
    credential store, the saved profile, the device's own control channel, or its API.

    So this gate asks a different question — **can the agent reach the machine?** — and refuses an operator ask
    when it can. `reach` maps each channel to whether the agent has working access:

        ssh        a key that authenticates to the device
        mesh       a node in the mesh that can run the job
        api        a control API the agent is authorised to call (router, hypervisor, cloud console)
        stored_cred  a saved credential or profile the agent may use without a human

    If ANY of these is true, the agent does the work. Reporting that a path was "not tried" is not an excuse; that
    is the failure mode this gate exists to catch.
    """
    channels = ("ssh", "mesh", "api", "stored_cred")
    have = {c: bool(reach.get(c, False)) for c in channels}
    if outcome == "asked_operator" and any(have.values()):
        available = ", ".join(c for c, ok in have.items() if ok)
        raise ExecutionGateError(
            f"asked the operator to {what or 'act'} while the agent can reach the device via: {available}. "
            "Reaching it and declining to act is a wall of the agent's own making - break it.")
    if outcome == "asked_operator" and not any(have.values()):
        return {"gate": "operator-ask@1", "reach": have, "outcome": outcome, "conformant": True,
                "note": "no channel open: the ask is legitimate and must say which channels were checked"}
    return {"gate": "operator-ask@1", "reach": have, "outcome": outcome, "conformant": True}


def summary(record: dict) -> str:
    tried = [p for p, ok in record["paths_tried"].items() if ok]
    if record["outcome"] == "asked_operator":
        return "asked the operator (no path existed)"
    return f"{record['outcome']} via {', '.join(tried) or 'nothing recorded'}"
