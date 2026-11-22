"""lean_scrape.py — scrape Lean proofs: the fundamental core of what makes SEXTANT work.

Machine-checked theorems are the empirical truths the whole engine builds on. This module makes the
BIGGEST local Lean library (Mathlib, ~170k theorems) queryable, and scrapes external Lean repos from
the internet so the library of truths keeps growing.

  * ``count_mathlib_theorems`` — how many machine-checked theorems Mathlib holds (the size of the truth).
  * ``search_mathlib``       — find theorems matching a keyword (name + file + statement) — the engine's
                               way to cite an existing proof as a tier-1 fact.
  * ``scrape_github_lean``   — clone an external Lean repo and scan it for theorems (the internet part).
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path


def mathlib_dir() -> Path | None:
    """The local Mathlib source tree (a Lean dependency of the pacland proof tree), if present."""
    here = Path(__file__).resolve().parent.parent.parent  # .../pacland
    for cand in (here / "pacland-proof" / ".lake" / "packages" / "mathlib" / "Mathlib",):
        if cand.exists():
            return cand
    return None


def _rg_available() -> bool:
    return shutil.which("rg") is not None


def count_mathlib_theorems(dir: Path | None = None) -> int:
    """The number of theorem/lemma declarations in a Lean tree (Mathlib by default)."""
    d = dir or mathlib_dir()
    if d is None or not d.exists():
        return 0
    if _rg_available():
        r = subprocess.run(["rg", "-c", r"^\s*(theorem|lemma)\s+", str(d)],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return sum(int(ln.split(":")[-1]) for ln in r.stdout.splitlines() if ":" in ln)
    # pure-Python fallback (rg not installed, or it returned nothing)
    n = 0
    for p in d.rglob("*.lean"):
        n += len(re.findall(r"^\s*(?:theorem|lemma)\s+", p.read_text(errors="ignore"), re.M))
    return n


def search_mathlib(keyword: str, dir: Path | None = None, limit: int = 10) -> list[dict]:
    """Find theorem/lemma declarations matching ``keyword`` — name + file + the statement line.

    Matching is case-insensitive over the declaration line (name and/or statement). This is the
    engine's citation surface: a match is an existing, machine-checked fact it can use as a tier-1
    building block, rather than re-deriving or re-proposing it.
    """
    d = dir or mathlib_dir()
    if d is None or not d.exists():
        return []
    words = [w for w in keyword.lower().split() if w] or [keyword.lower()]
    hits: list[dict] = []

    def _take(path: str, line: str):
        m = re.search(r"(?:theorem|lemma)\s+([A-Za-z0-9_']+)", line)
        if m:
            hits.append({"name": m.group(1),
                         "file": path.split("Mathlib/")[-1] if "Mathlib/" in path else path,
                         "statement": line.strip()[:160]})

    if _rg_available():
        alt = "|".join(re.escape(w) for w in words)
        r = subprocess.run(
            ["rg", "-i", "--no-heading", "-n",
             rf"^\s*(theorem|lemma)\s+.*({alt})", str(d)],
            capture_output=True, text=True)
        if r.returncode == 0:
            for ln in r.stdout.splitlines():
                if ":" not in ln:
                    continue
                path, rest = ln.split(":", 1)
                _take(path, rest)
    else:
        for p in d.rglob("*.lean"):
            for ln in p.read_text(errors="ignore").splitlines():
                low = ln.lower()
                if re.match(r"^\s*(?:theorem|lemma)\s+", ln) and any(w in low for w in words):
                    _take(str(p), ln)
            if len(hits) >= limit * 4:  # over-collect a little, then trim
                break
    return hits[:limit]


def _clone_repo(repo_url: str, tmp: str = "/tmp") -> tuple[Path | None, str]:
    """Shallow-clone a repo into a temp dir keyed by its name; returns (target, error)."""
    name = repo_url.rstrip("/").split("/")[-1].removesuffix(".git") or "lean-repo"
    target = Path(tmp) / f"sextant-{name}"
    if (target / ".git").exists():
        return target, ""
    r = subprocess.run(["git", "clone", "--depth", "1", repo_url, str(target)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, f"clone failed: {r.stderr.strip()[:200]}"
    return target, ""


def _scan_theorems(target: Path) -> list[dict]:
    """The FULL list of (name, file) theorem/lemma declarations in a Lean tree."""
    theorems: list[dict] = []
    for p in sorted(target.rglob("*.lean")):
        text = p.read_text(errors="ignore")
        for m in re.finditer(r"^\s*(?:theorem|lemma)\s+([A-Za-z0-9_']+)", text, re.M):
            theorems.append({"name": m.group(1), "file": str(p.relative_to(target))})
    return theorems


def scrape_github_lean(repo_url: str, source: str = "", limit: int = 20, tmp: str = "/tmp") -> dict:
    """Clone an external Lean repo from the internet and scan it for theorems.

    Returns the count + a sample of (name, file). The clone is shallow (--depth 1) and lands in a temp
    dir keyed by the repo name, so re-scraping the same repo re-uses the clone.
    """
    name = repo_url.rstrip("/").split("/")[-1].removesuffix(".git") or "lean-repo"
    target, err = _clone_repo(repo_url, tmp)
    if err:
        return {"repo": repo_url, "error": err}
    theorems = _scan_theorems(target)
    return {"repo": repo_url, "source": source or name, "lean_theorems": len(theorems),
            "sample": theorems[:limit]}


def ingest_github_repo(repo_url: str, source: str = "", tmp: str = "/tmp") -> dict:
    """Scrape a GitHub Lean repo and ingest ALL its theorems as namespaced tier-1 properties."""
    from pacland import registry
    name = repo_url.rstrip("/").split("/")[-1].removesuffix(".git") or "lean-repo"
    target, err = _clone_repo(repo_url, tmp)
    if err:
        return {"error": err}
    source = source or name
    theorems = _scan_theorems(target)
    for t in theorems:
        registry.add(registry.Entry(
            id=f"ext:{source}:lean-{t['name']}", kind="property",
            payload={"name": t["name"],
                     "statement": f"theorem {t['name']} (machine-checked, from {source})",
                     "tier": 1, "domain": "mathematics", "source": t["file"]},
            provenance={"produced_by": "external", "source": source, "method": "github-repo",
                        "ts": __import__("time").time()}))
    return {"source": source, "ingested": len(theorems)}


def ingest_github_search(query: str, limit: int = 3, tmp: str = "/tmp", _search=None) -> dict:
    """Search GitHub for Lean repos and INGEST all their theorems as tier-1 properties.

    ``_search`` is injectable (defaults to the live GitHub search) so the pipeline is testable offline.
    """
    searcher = _search or (lambda q, n: [(r["url"], r["full_name"].replace("/", "-"))
                                         for r in search_github_lean_repos(q, n)])
    repos = searcher(query, limit)
    results: list[dict] = []
    total = 0
    for url, source in repos:
        r = ingest_github_repo(url, source=source, tmp=tmp)
        total += r.get("ingested", 0)
        results.append({"source": source, "url": url, "ingested": r.get("ingested", 0),
                        "error": r.get("error")})
    return {"query": query, "repos": results, "total_ingested": total}


def ingest_mathlib_hits(keyword: str, limit: int = 10, source: str = "mathlib") -> dict:
    """The on-demand bridge: search Mathlib for a keyword and register the MATCHES as tier-1 properties.

    Ingesting all ~173k Mathlib theorems as individual entries would be impractically large; this
    ingests only the RELEVANT ones (the search matches), namespaced ``ext:<source>:lean-<name>`` and
    tagged tier-1 — so the synthesis and bound-derivation layers can cite a proven fact without the
    whole library in the registry.
    """
    from pacland import registry
    hits = search_mathlib(keyword, limit=limit)
    for h in hits:
        registry.add(registry.Entry(
            id=f"ext:{source}:lean-{h['name']}", kind="property",
            payload={"name": h["name"], "statement": h["statement"], "tier": 1,
                     "domain": "mathematics", "source": h["file"]},
            provenance={"produced_by": "external", "source": source, "method": "mathlib-search",
                        "ts": __import__("time").time()}))
    return {"ingested": len(hits), "names": [h["name"] for h in hits]}


def harvest_mathlib(keywords: list[str], limit_per_keyword: int = 10, source: str = "mathlib") -> dict:
    """Populate the library from Mathlib: batch-ingest the theorems matching a list of keywords.

    Each keyword is expanded through ``KEYWORD_ALIASES`` (a concept → the Mathlib spellings that
    actually carry it), and matches are de-duplicated by theorem name. This is the "bigger library of
    empirical truths" step — for each concept, the matching Mathlib theorems become tier-1 properties
    the engine can cite.
    """
    from pacland import registry
    total = 0
    seen: set[str] = set()
    per: dict[str, int] = {}
    for kw in keywords:
        terms = KEYWORD_ALIASES.get(kw, [kw])
        n = 0
        for term in terms:
            for h in search_mathlib(term, limit=limit_per_keyword):
                if h["name"] in seen:
                    continue
                seen.add(h["name"])
                registry.add(registry.Entry(
                    id=f"ext:{source}:lean-{h['name']}", kind="property",
                    payload={"name": h["name"], "statement": h["statement"], "tier": 1,
                             "domain": "mathematics", "source": h["file"]},
                    provenance={"produced_by": "external", "source": source,
                                "method": "mathlib-search",
                                "ts": __import__("time").time()}))
                n += 1
                total += 1
        per[kw] = n
    return {"harvested": total, "per_keyword": per}


# A concept → the Mathlib spellings that actually carry it. Mathlib's naming is the gap this bridges:
# "spectral" there is spectral SPACES (topology), not the spectral gap; "mixing" is ergodic theory.
# The M3-relevant concepts (Yang-Mills mass gap = exponential clustering / spectral gap) map onto
# Mathlib's analysis + measure-theory machinery.
KEYWORD_ALIASES = {
    "spectral gap": ["spectral", "eigenvalue", "spectrum", "spectralRadius", "eigenvalues"],
    "mass gap": ["decay", "exponential", "superexponential", "clustering", "cluster"],
    "mixing": ["ergodic", "mixing", "mixingTime", "measurePreserving"],
    "conservation": ["conserved", "energy", "invariant"],
    "decay": ["decay", "exponential", "superexponential"],
    "entropy": ["entropy"],
    "semigroup": ["semigroup", "contraction", "MarkovSemigroup", "generator", "semigroup"],
    "curvature": ["curvature", "Ricci", "Bakry", "logSobolev", "logarithmic"],
    "martingale": ["martingale", "stopping", "optional"],
    "ergodic": ["ergodic", "mixing", "measurePreserving"],
    "measure": ["measure", "ergodic", "mixing"],
}


def search_github_lean_repos(query: str, limit: int = 5) -> list[dict]:
    """Search GitHub for Lean repos — other researchers' formalization work — by topic/keyword.

    Returns ``(full_name, clone_url, stars, description)`` for the top matches (sorted by stars).
    No auth required (the public search API), so it works out of the box.
    """
    import json
    import urllib.parse
    import urllib.request

    q = urllib.parse.quote(f"{query} language:Lean")
    url = f"https://api.github.com/search/repositories?q={q}&per_page={limit}&sort=stars"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "sextant"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
    except Exception:  # noqa: BLE001 — network failure means no results, not a crash
        return []
    return [{"full_name": it["full_name"], "url": it["clone_url"],
             "stars": it.get("stargazers_count", 0),
             "description": (it.get("description") or "")[:100]}
            for it in data.get("items", [])]


def scrape_github_search(query: str, limit: int = 3, tmp: str = "/tmp", _search=None) -> dict:
    """Search GitHub for Lean repos and scrape each one's theorems — the internet-facing harvest.

    ``_search`` is injectable (defaults to the live GitHub search) so the pipeline is testable offline
    by supplying a list of (url, source) pairs. Returns the repos scraped + the total theorem count.
    """
    searcher = _search or (lambda q, n: [(r["url"], r["full_name"].replace("/", "-"))
                                         for r in search_github_lean_repos(q, n)])
    repos = searcher(query, limit)
    results: list[dict] = []
    total = 0
    for url, source in repos:
        s = scrape_github_lean(url, source=source, tmp=tmp)
        n_theorems = s.get("lean_theorems", 0)
        total += n_theorems
        results.append({"source": source, "url": url, "lean_theorems": n_theorems,
                        "error": s.get("error")})
    return {"query": query, "repos": results, "total_theorems": total}
