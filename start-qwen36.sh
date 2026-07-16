#!/usr/bin/env bash
set -euo pipefail

docker compose --profile qwen36 up -d
docker compose ps

echo
echo "Qwen3.6-35B-A3B stack start requested."
echo "OpenAI API: http://localhost:8080/v1"
echo "Recommended model: qwen36-coder"
