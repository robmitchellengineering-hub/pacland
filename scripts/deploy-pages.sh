#!/usr/bin/env bash
# deploy-pages.sh — mirror `web/` onto the GitHub Pages branch.
#
# The Pages mirror is a SEPARATE deploy target from Netlify:
#   Netlify  : publish-only, web/ → pacland.morpheus.nz, triggered by a push to main
#   Pages    : legacy build from the `gh-pages` branch → robmitchellengineering-hub.github.io/pacland
#
# So a merge to main updates Netlify automatically and Pages only when this script runs.
# That asymmetry is why the mirror drifted for three slices.
#
#   scripts/deploy-pages.sh            # mirror and push
#   scripts/deploy-pages.sh --dry-run  # show what would change, push nothing
#
# Preserves anything on gh-pages that is not in web/ (pacland-today.html, today.json).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BRANCH="gh-pages"
DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

git -C "$ROOT" fetch --quiet origin "$BRANCH"
# Detached worktree: never conflicts with a `gh-pages` branch that is already checked out
# somewhere, and the push names the destination explicitly.
WT="$(mktemp -d)/pacland-pages"
git -C "$ROOT" worktree add --quiet --detach "$WT" "origin/$BRANCH"
trap 'git -C "$ROOT" worktree remove --force "$WT" 2>/dev/null || true' EXIT

changed=0
# *.html AND *.json: the find page fetches index.json, so shipping the page without the
# data reproduces the bug the vision review caught ("index.json failed to load").
for f in "$ROOT"/web/*.html "$ROOT"/web/*.json; do
  name="$(basename "$f")"
  if ! cmp -s "$f" "$WT/$name"; then
    cp "$f" "$WT/$name"
    echo "update  $name"
    changed=1
  fi
done

# vendored assets (plotly for the 3D view) are part of the site, not of the HTML
if [ -d "$ROOT/web/vendor" ]; then
  mkdir -p "$WT/vendor"
  if ! diff -rq "$ROOT/web/vendor" "$WT/vendor" >/dev/null 2>&1; then
    cp -R "$ROOT"/web/vendor/. "$WT/vendor/"
    echo "update  vendor/"
    changed=1
  fi
fi

if [ "$changed" = 0 ]; then
  echo "gh-pages already matches web/ — nothing to deploy"
  exit 0
fi

if [ "$DRY" = 1 ]; then
  echo "--dry-run: would commit and push to $BRANCH"
  exit 0
fi

git -C "$WT" add -A
git -C "$WT" commit --quiet -m "deploy: mirror web/ onto Pages ($(date -u +%Y-%m-%dT%H:%MZ))"
git -C "$WT" push --quiet origin "HEAD:refs/heads/$BRANCH"
echo "deployed gh-pages; Pages builds in ~30-60s"
echo "verify: curl -s https://robmitchellengineering-hub.github.io/pacland/ | grep -c '<your new string>'"
