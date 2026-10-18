"""Dispatch the deficit climber to the mesh and read back the climb report.

The climber (``scripts/climb_deficit.py``) needs CYTools, which lives only on the
mesh's ``studio-linux`` VM. This module drives it there over the documented route
``mac -> win-2 (100.86.50.6) -> studio-linux (192.168.28.128)``, base64-encoding
the script and corpus so no quoting survives the PowerShell hop, and returns the
parsed JSON climb report.
"""
from __future__ import annotations

import base64
import json
import os
import subprocess

HOP = "robmi@100.86.50.6"
VM = "rob@192.168.28.128"
VM_KEY = r"C:\Users\robmi\.ssh\mesh-vm"
SSH_KEY = os.path.expanduser("~/.ssh/mesh-admin")
VENV_PY = "/home/rob/cytools-venv/bin/python"


def _remote_script(climber_path, corpus_path) -> str:
    script_b64 = base64.b64encode(open(climber_path, "rb").read()).decode()
    corpus_b64 = base64.b64encode(open(corpus_path, "rb").read()).decode()
    return (
        f"echo {script_b64} | base64 -d > /tmp/climb.py; "
        f"echo {corpus_b64} | base64 -d > /tmp/corpus.json; "
        f"{VENV_PY} /tmp/climb.py /tmp/corpus.json"
    )


def run_climb(climber_path: str, corpus_path: str, timeout: int = 180) -> dict:
    """Run the climber on studio-linux and return the parsed report."""
    remote = _remote_script(climber_path, corpus_path)
    inner = f"ssh -i {VM_KEY} {VM} '{remote}'"
    cmd = ["ssh", "-i", SSH_KEY, "-o", "BatchMode=yes", HOP, inner]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0 and not proc.stdout.strip():
        return {"error": "mesh climb failed", "stderr": proc.stderr[-500:]}
    for line in reversed(proc.stdout.strip().splitlines()):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return {"error": "no JSON report", "stdout": proc.stdout[-500:]}
