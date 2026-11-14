"""SEXTANT node — a self-contained, no-harness app anyone can download and run.

`python -m pacland.sextant_node` serves a click-through GUI plus the yes/no engine, the
open-question registry (the *global quest* to find the constraint-first ToE), a run-the-falsifier
button, a "contribute a discovery" flow, and a "point at your own AI" hook.

This is the contributor door: no robmesh, no build node, no harness. Download, run, click, add.
Every verdict a visitor reads is kernel-checked (Lean) or live-computed (Phantom), never asserted.

Usage:
    python -m pacland.sextant_node          # serves http://127.0.0.1:8090
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent  # .../pacland/src — so `from pacland import …` works
sys.path.insert(0, str(_SRC))

from pacland import phantom  # noqa: E402
from pacland import sextant  # noqa: E402
from pacland import hypotheses  # noqa: E402
from pacland import runner  # noqa: E402

REPO_ROOT = _SRC.parent  # .../pacland
NODE_HTML = REPO_ROOT / "web" / "node.html"
PROOFS = REPO_ROOT / "proofs"  # PR-able, committed — the global proofs DB directory
PORT = 8090
GH_OWNER = "robmitchellengineering-hub"
GH_REPO = "pacland"


def _proof_markdown(payload: dict) -> str:
    """A contributed claim as a PR-ready Markdown file."""
    return (
        f"# {payload['id']}\n\n"
        f"- **claim:** {payload['claim']}\n"
        f"- **verdict:** {payload['verdict']}\n"
        f"- **falsifier:** {payload['falsifier']}\n"
        f"- **why:** {payload['why']}\n\n"
        "Contributed via the SEXTANT node. Re-check the falsifier or the Lean kernel before trusting.\n"
    )


def _claim_json(name: str) -> dict:
    """A claim with the callable `simulate` stripped (it is not JSON-serializable)."""
    e = sextant.CATALOG[name]
    return {"id": name, **{k: v for k, v in e.items() if k != "simulate"}}


def _state() -> dict:
    return {
        "claims": [_claim_json(name) for name in sextant.CATALOG],
        "hypotheses": [
            {"id": name, **hypotheses.HYPOTHESES[name]} for name in hypotheses.HYPOTHESES
        ],
    }


def _verify(name: str) -> dict:
    """Run one claim's falsifier and return the structured result."""
    e = sextant.CATALOG[name]
    if name in phantom.FALSIFIERS:
        survived, evidence = phantom.FALSIFIERS[name]()
        return {
            "id": name,
            "verdict": e["verdict"],
            "claim": e["claim"],
            "falsifier": e["falsifier"],
            "theorem": e["theorem"],
            "survived": bool(survived),
            "evidence": str(evidence),
        }
    return {
        "id": name,
        "verdict": e["verdict"],
        "claim": e["claim"],
        "falsifier": e["falsifier"],
        "theorem": e["theorem"],
        "survived": None,
        "evidence": f"kernel-checked — {e['theorem']} proves the falsifier impossible (no live oracle)",
    }


def _ask_ai(payload: dict) -> str:
    """Forward a prompt to the visitor's own AI (OpenAI-compatible /chat/completions)."""
    endpoint = payload["endpoint"].rstrip("/")
    key = payload.get("key", "")
    model = payload.get("model", "")
    prompt = payload["prompt"]
    body = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are helping attack an open hypothesis in the constraint-first "
                        "theory-of-everything project. A hypothesis has: the question, what is "
                        "forced, what is open, candidate answers with falsifiers, and an attack "
                        "plan. Suggest a concrete next step or a sharper falsifier."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        }
    ).encode()
    req = urllib.request.Request(
        f"{endpoint}/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    return data["choices"][0]["message"]["content"]


class Handler(BaseHTTPRequestHandler):
    def _json(self, obj: dict, code: int = 200) -> None:
        blob = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(blob)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(blob)

    def _html(self) -> None:
        blob = NODE_HTML.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def do_GET(self) -> None:  # noqa: N802
        from urllib.parse import urlparse, parse_qs

        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        if path in ("/", "/index.html"):
            return self._html()
        if path == "/api/state":
            return self._json(_state())
        if path == "/api/verify":
            name = query.get("name", [""])[0]
            if name not in sextant.CATALOG:
                return self._json({"error": f"unknown claim '{name}'"}, 404)
            return self._json(_verify(name))
        return self._json({"error": "not found"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        from urllib.parse import urlparse

        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if path == "/api/contribute":
            cid = payload.get("id", "").strip()
            if not cid or not payload.get("claim") or not payload.get("falsifier"):
                return self._json({"error": "id, claim and falsifier are required"}, 400)
            md = _proof_markdown(payload)
            PROOFS.mkdir(parents=True, exist_ok=True)
            (PROOFS / f"{cid}.md").write_text(md)
            # one-tap: a pre-filled GitHub "new file" URL that opens a PR — no git needed.
            from urllib.parse import quote

            url = (
                f"https://github.com/{GH_OWNER}/{GH_REPO}/new/main"
                f"?filename=proofs/{quote(cid)}.md&value={quote(md)}"
            )
            return self._json(
                {
                    "saved": str(PROOFS / f"{cid}.md"),
                    "pr_url": url,
                    "share": (
                        "Your discovery is saved locally and ready to join the global quest.\n"
                        "Tap this link to open a pull request (GitHub pre-fills the file):\n"
                        f"{url}"
                    ),
                }
            )
        if path == "/api/ai":
            try:
                return self._json({"reply": _ask_ai(payload)})
            except Exception as exc:  # the visitor's AI is unreachable/misconfigured
                return self._json({"error": f"could not reach your AI: {exc}"}, 502)
        if path == "/api/prove":
            statement = payload.get("statement", "")
            attempts = int(payload.get("attempts", 5))
            if not statement:
                return self._json({"error": "statement (Lean code with a sorry) is required"}, 400)
            result = runner.prove(statement, attempts=attempts)
            return self._json(result, 200 if result.get("ok") else 422)
        return self._json({"error": "not found"}, 404)

    def log_message(self, *args) -> None:  # keep the console quiet
        pass


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"SEXTANT node running — open http://127.0.0.1:{PORT}")
    print("  claims:      browse the kernel-checked FORCED / FREE / IMPOSSIBLE verdicts")
    print("  global quest: the open hypotheses — find the constraint-first ToE")
    print("  contribute:  add a discovery and share it into the proofs DB")
    print("  your AI:     point the node at your own model to help attack a quest")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
