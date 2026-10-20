#!/usr/bin/env bash
# shard_vacua.sh — shard the h12=25 flux-vacua sampling across the mesh's Linux nodes.
#
# The sampler (JAXVacua + cytools) is Linux-only, so the shard nodes are the mesh's
# Linux VMs (studio-linux, studio-linux2). Each node runs /home/rob/sample_h12_25.py
# on its share and echoes the JSON to stdout; the mesh loop writes that to
# runs/<host>/<id>/stdout.txt, which this script collects and merges.
#
# Usage:  scripts/shard_vacua.sh <n_total> [node ...]
#         scripts/shard_vacua.sh 30 studio-linux studio-linux2
#
# Self-asserting: exits non-zero if a shard's result is missing or empty.
set -euo pipefail

HARNESS="${HARNESS:-$HOME/harness-mesh}"
DISPATCH=(python3 "$HARNESS/scripts/dispatch.py")

n_total="${1:?usage: shard_vacua.sh <n_total> [node ...]}"
shift
nodes=("$@")
if [ ${#nodes[@]} -eq 0 ]; then
  nodes=(studio-linux studio-linux2)
fi

k=${#nodes[@]}
base=$((n_total / k))
rem=$((n_total % k))

# --- dispatch one shard per node ---
declare -a job_ids node_of shard_of
for i in "${!nodes[@]}"; do
  node="${nodes[$i]}"
  shard=$base
  [ "$i" -lt "$rem" ] && shard=$((shard + 1))
  out="/home/rob/shard-$i-vacua.json"
  # sampler writes the JSON, then `cat` puts it on stdout so the mesh captures it.
  cmd="/home/rob/cytools-venv/bin/python /home/rob/sample_h12_25.py $shard $out && cat $out"
  echo "dispatching $shard vacua -> $node"
  job_id=$("${DISPATCH[@]}" --node "$node" --needs shell:posix --timeout 3600 --push \
      --slug "vacua-shard-$i" --note "pacland flux sampling shard $i/$k ($shard vacua, $node)" \
      --command "$cmd" 2>&1 | awk '/^id/{print $2; exit}')
  if [ -z "$job_id" ]; then
    echo "FAILED to dispatch to $node" >&2
    exit 1
  fi
  job_ids+=("$job_id")
  node_of+=("$node")
  shard_of+=("$shard")
  echo "  job $job_id"
done

# --- wait for the results to come back over the mesh bus ---
echo "waiting for results (the node loop pulls, runs, and pushes back)..."
deadline=$((SECONDS + 3600))
merged="data/h12_25_sharded.json"
all_rows="[]"
for i in "${!job_ids[@]}"; do
  id="${job_ids[$i]}"
  node="${node_of[$i]}"
  found=""
  while [ $SECONDS -lt $deadline ]; do
    git -C "$HARNESS" pull --rebase origin main >/dev/null 2>&1 || true
    result=$(git -C "$HARNESS" ls-files "runs/$node/$id/stdout.txt" 2>/dev/null || true)
    if [ -n "$result" ]; then
      found="$HARNESS/$result"
      break
    fi
    sleep 30
  done
  if [ -z "$found" ]; then
    echo "timed out waiting for shard $id ($node)" >&2
    exit 1
  fi
  # the stdout is the sampler's progress lines, then `cat` of the JSON (one line, `{...`).
  json=$(grep '^{' "$found" | head -1)
  if [ -z "$json" ] || ! echo "$json" | python3 -c 'import json,sys; json.load(sys.stdin)' >/dev/null 2>&1; then
    echo "shard $id ($node): no valid JSON in stdout.txt" >&2
    exit 1
  fi
  rows=$(echo "$json" | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin).get("vacua", [])))')
  all_rows=$(python3 -c "import json,sys; a=json.loads('$all_rows'); b=json.loads('$rows'); print(json.dumps(a+b))")
  echo "  $node: collected (shard of ${shard_of[$i]})"
done

python3 - "$n_total" "$merged" "$all_rows" <<'PY'
import json, sys
n_total, path, rows_json = sys.argv[1], sys.argv[2], sys.argv[3]
rows = json.loads(rows_json)
susy = sum(1 for r in rows if r.get("is_susy"))
with open(path, "w") as f:
    json.dump({"h12": 25, "n_requested": int(n_total), "n": len(rows), "vacua": rows}, f)
print(f"MERGED {len(rows)} critical points ({susy} SUSY) -> {path}")
PY
