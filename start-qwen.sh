#!/usr/bin/env bash
set -euo pipefail

docker compose --profile qwen up -d
docker compose ps

echo
echo "Qwen stack start requested."
echo "OpenAI API: http://localhost:8080/v1"
echo "Recommended models: coder, coder-fast"
