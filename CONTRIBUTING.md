# Contribute to the global quest — find the constraint-first theory of everything

The quest: for any system, ask what is **FORCED**, what is **FREE**, what is **IMPOSSIBLE** — and
kernel-check the answer. You don't need a lab or a supercomputer; you need a laptop and curiosity.
This page is the whole door.

## 1. Download and run (about two minutes)

```bash
git clone https://github.com/robmitchellengineering-hub/pacland.git
cd pacland
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
sextant-node          # then open http://127.0.0.1:8090
```

Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -e .; sextant-node`

## 2. What the node does

- **Browse the 28 kernel-checked claims** — click any to see FORCED / FREE / IMPOSSIBLE, its falsifier,
  its theorem, and the plain-speak "why".
- **Browse the global quest** — the open hypotheses (the questions no one has closed yet).
- **Run a falsifier** — click "run falsifier" and watch the real computation (e.g. CHSH → 2√2).
- **Point it at your own AI** — paste any OpenAI-compatible endpoint + key, pick a quest, and your model
  helps attack it.

## 3. Contribute a discovery

1. Open **"Contribute a discovery"** in the node.
2. Fill in: **id**, **claim** (one sentence), **falsifier** (what experiment would refute it),
   **verdict** (FORCED / FREE / IMPOSSIBLE), **why** (plain words).
3. Click **"Add to the quest"** — it writes `proofs/<id>.md` and hands you a one-tap link.
4. Tap the link → GitHub opens the file pre-filled → **"Propose new file"** → a pull request.
5. CI re-checks it. It merges when green — and your discovery is part of the global quest.

## 4. The rules (so it stays a *proofs* database, not a *claims* database)

- **Every claim has a falsifier.** No falsifier = `NOT_DEMONSTRATED`.
- **The verdict is FORCED / FREE / IMPOSSIBLE — never a value.** We ask for constraints, counts and
  deficits, never for the number the universe won't give.
- **It is kernel-checked or falsifier-run — never asserted.** `scripts/validate_proofs.py` enforces the
  shape; the Lean kernel or the falsifier enforces the truth.
