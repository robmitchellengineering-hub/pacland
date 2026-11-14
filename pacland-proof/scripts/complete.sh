#!/usr/bin/env bash
# complete.sh — the mechanical-completion audit (docs/mechanical-completion.md, Stage 1).
#
# The kernel is the source of truth: this runs `lake build` (the verifier) and reports
# sorry/axiom/admit (the "not complete" markers), so "mechanical status" is a number.
#
# Usage:
#   bash scripts/complete.sh                  # audit the whole proof arm
#   bash scripts/complete.sh <ModuleName>     # build one module, e.g. PaclandProof.QM.CayleyGeneral

set -uo pipefail
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")/.." || exit 1

echo "== kernel check (lake build) =="
if [ -n "${1:-}" ]; then
  lake build "$1"
else
  lake build
fi
rc=$?

# A real sorry/axiom/admit is a standalone term, e.g. `by sorry`, `:= sorry`, `axiom x : P`.
# Doc-strings and comments wrap the word in backticks — exclude those.
echo
echo "== sorry / axiom / admit audit (backtick-wrapped = comment, not a term) =="
total=0
while IFS= read -r f; do
  n=0
  while IFS=: read -r ln text; do
    # skip if the whole trimmed line is a comment (starts with -- or is inside a /- block)
    case "$text" in
      *\`sorry\`*|*\`axiom\`*|*\`admit\`*) continue ;;   # doc-string mention
    esac
    if printf '%s' "$text" | grep -qE '(^|[^A-Za-z`])(sorry|axiom|admit)([^A-Za-z]|$)'; then
      printf '  %s:%s  %s\n' "${f#./}" "$ln" "$(printf '%s' "$text" | sed 's/^[[:space:]]*//' | cut -c1-70)"
      n=$((n + 1))
    fi
  done < <(grep -nE '\b(sorry|axiom|admit)\b' "$f" || true)
  total=$((total + n))
done < <(find PaclandProof -name '*.lean' | sort)

echo "  ---"
printf '  %d total sorry/axiom/admit\n' "$total"

echo
echo "== size =="
printf '  %s theorems/lemmas/defs, %s files\n' \
  "$(grep -rE '^(theorem|lemma|def) ' PaclandProof --include='*.lean' | wc -l | tr -d ' ')" \
  "$(find PaclandProof -name '*.lean' | wc -l | tr -d ' ')"

echo
if [ "$total" -gt 0 ]; then
  echo "RESULT: NOT-COMPLETE ($total sorry/axiom/admit; kernel build exit $rc)"
  exit 1
elif [ "$rc" -ne 0 ]; then
  echo "RESULT: KERNEL-RED (0 sorry, but lake build exit $rc)"
  exit "$rc"
else
  echo "RESULT: COMPLETE (kernel green, 0 sorry/axiom/admit)"
  exit 0
fi
