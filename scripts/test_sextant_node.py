#!/usr/bin/env python3
"""SEXTANT node guard — the downloadable node actually serves and the falsifier runs.

A guard that cannot fail is not a guard: this starts the node, fetches its endpoints, asserts the
claim/quest counts and the CHSH falsifier verdict, then stops the node. Fails if the server does not
serve, if the counts drift, or if the falsifier does not report SURVIVES."""
import json
import subprocess
import sys
import time
import urllib.request

PORT = 8090


def get(path: str) -> dict:
    with urllib.request.urlopen(f"http://127.0.0.1:{PORT}{path}", timeout=10) as r:
        return json.load(r)


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, "src/pacland/sextant_node.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(20):
            try:
                state = get("/api/state")
                break
            except OSError:
                time.sleep(0.25)
        else:
            print("FAIL: node did not come up")
            return 1

        n_claims = len(state["claims"])
        n_quests = len(state["hypotheses"])
        assert n_claims >= 28, f"claims drifted: {n_claims}"
        assert n_quests >= 11, f"hypotheses drifted: {n_quests}"

        chsh = get("/api/verify?name=chsh")
        assert chsh["verdict"] == "FORCED", chsh
        assert chsh["survived"] is True, chsh
        assert "2.828" in chsh["evidence"], chsh

        print(f"sextant node OK: {n_claims} claims, {n_quests} quests, CHSH falsifier SURVIVES")
        return 0
    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
