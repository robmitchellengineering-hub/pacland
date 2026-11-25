"""A minimal MCP (Model Context Protocol) stdio server exposing SEXTANT + VVS as tools.

No SDK dependency — MCP over stdio is JSON-RPC on newline-delimited stdin/stdout. Claude Code and
Cursor spawn this process and talk to it, so a harness can *call* SEXTANT (verify a claim, read the
knowledge graph, measure a deficit) and VVS (the valiant CLI) instead of pasting text.

Run directly:  python -m pacland.mcp_server
"""
from __future__ import annotations

import json
import subprocess
import sys

SERVER_NAME = "sextant"
SERVER_VERSION = "0.1.0"
PROTOCOL_VERSION = "2024-11-05"

TOOLS = [
    {
        "name": "sextant_verify",
        "description": "Classify a research claim as FORCED / FREE / IMPOSSIBLE / IRREDUCIBLE, "
                       "with the evidence (kernel-checked theorem or live falsifier). Pass a claim "
                       "id (e.g. ym-volume-uniform-su2) or a fragment of the claim text.",
        "inputSchema": {"type": "object",
                        "properties": {"claim": {"type": "string",
                                                "description": "a claim id or a fragment of its text"}},
                        "required": ["claim"]},
    },
    {
        "name": "sextant_claims",
        "description": "List the kernel-checked claims and their verdicts (the registry).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "sextant_graph",
        "description": "Read the discovery knowledge graph — the reusable mechanisms and the pending "
                       "cross-field transfer hypotheses.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "sextant_deficit",
        "description": "The verification deficit for a domain — how much of a decision is measured "
                       "versus predicted. domain: 'drugs' or 'climate'.",
        "inputSchema": {"type": "object",
                        "properties": {"domain": {"type": "string"}},
                        "required": ["domain"]},
    },
    {
        "name": "valiant_status",
        "description": "Run the Valiant Verification SDK's status — the gate/guard/ledger counts for "
                       "the current repo.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def _tool_sextant_verify(args: dict) -> str:
    from pacland import sextant
    claim = args.get("claim", "")
    try:
        return sextant.verify(claim)
    except Exception:
        # a fragment, not an id — find the closest claim by substring
        from pacland.sextant import classify
        for name in sextant.CATALOG:
            if claim.lower() in name.lower() or claim.lower() in str(sextant.CATALOG[name]).lower():
                return f"{name}: {sextant.verify(name)}"
        return f"no claim matches {claim!r}; run sextant_claims to list them"


def _tool_sextant_claims(_: dict) -> str:
    from pacland import sextant
    return "\n".join(f"- {name}: {sextant.CATALOG[name].get('verdict', '?')}"
                     for name in sorted(sextant.CATALOG))


def _tool_sextant_graph(_: dict) -> str:
    from pacland.discovery_graph import DiscoveryGraph, seed_mass_gap
    g = DiscoveryGraph.load()
    if not g.nodes:
        g = seed_mass_gap()
    return g.reusable_context() or "(graph is empty)"


def _tool_sextant_deficit(args: dict) -> str:
    domain = args.get("domain", "").lower()
    if domain in ("drug", "drugs"):
        from pacland.drugs.deficit import summary
        return summary()
    if domain in ("climate", "climate-change"):
        from pacland.climate.deficit import climate_deficit_report
        hist, proj = climate_deficit_report()
        return (f"climate: {hist.n_validation}/{hist.n_observables} historical validated "
                f"(radius {hist.radius:.0%}); {proj.n_validation}/{proj.n_observables} projected validated")
    return f"unknown domain {domain!r}; try 'drugs' or 'climate'"


def _tool_valiant_status(_: dict) -> str:
    try:
        return subprocess.run(["valiant", "status"], capture_output=True, text=True,
                              timeout=60).stdout or "(no output)"
    except FileNotFoundError:
        return "valiant is not installed — run: npm install -g <vvs-tarball>"
    except subprocess.TimeoutExpired:
        return "valiant status timed out"


_CALLERS = {
    "sextant_verify": _tool_sextant_verify,
    "sextant_claims": _tool_sextant_claims,
    "sextant_graph": _tool_sextant_graph,
    "sextant_deficit": _tool_sextant_deficit,
    "valiant_status": _tool_valiant_status,
}


def handle(msg: dict) -> dict | None:
    method = msg.get("method")
    if method == "initialize":
        return {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}}
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name = msg["params"]["name"]
        args = msg["params"].get("arguments", {})
        if name not in _CALLERS:
            return {"content": [{"type": "text", "text": f"unknown tool {name!r}"}], "isError": True}
        try:
            text = _CALLERS[name](args)
            return {"content": [{"type": "text", "text": text}]}
        except Exception as e:  # noqa: BLE001 — a tool error is a result, not a crash
            return {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True}
    return None


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "id" not in msg:  # a notification — no response
            continue
        result = handle(msg)
        if result is None:
            continue
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": result}) + "\n")
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
