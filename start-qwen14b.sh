#!/usr/bin/env bash
set -euo pipefail

docker compose --profile qwen14b up -d
docker compose ps

echo
echo "Qwen14B stack start requested."
echo "OpenAI API: http://localhost:8080/v1"
echo "Recommended model: coder-fast"
