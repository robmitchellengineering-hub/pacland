#!/usr/bin/env bash
# Publish a merged HF model to Ollama: convert to GGUF, quantize to Q4_K_M, import.
#
# Usage: bash scripts/publish_ollama.sh [MERGED_DIR] [OLLAMA_NAME]
#   MERGED_DIR  the merged model from scripts/merge_lora.py (default runs/peft-merged)
#   OLLAMA_NAME the Ollama model name (default qwen2.5-discovery)
set -euo pipefail

MERGED="${1:-runs/peft-merged}"
NAME="${2:-qwen2.5-discovery}"

echo "== 1. GGUF conversion (llama.cpp) =="
pip install -q gguf || true
if [ ! -d llama.cpp ]; then
  git clone --depth 1 https://github.com/ggml-org/llama.cpp
else
  (cd llama.cpp && git pull --ff-only) || true
fi
python3 llama.cpp/convert_hf_to_gguf.py "$MERGED" --outfile "$MERGED-f16.gguf" --outtype f16

echo "== 2. quantize to Q4_K_M =="
if [ ! -x llama.cpp/build/bin/llama-quantize ]; then
  echo "llama-quantize not built — run: (cd llama.cpp && cmake -B build && cmake --build build -j)"
  exit 1
fi
llama.cpp/build/bin/llama-quantize "$MERGED-f16.gguf" "$MERGED-q4_k_m.gguf" q4_k_m

echo "== 3. import into Ollama as '$NAME' =="
cat > Modelfile <<EOF
FROM $MERGED-q4_k_m.gguf
EOF
ollama create "$NAME" -f Modelfile
echo "imported as '$NAME' — run: ollama run $NAME"
