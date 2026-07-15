#!/usr/bin/env bash
set -euo pipefail

docker compose --profile deepseek up -d
docker compose ps

echo
echo "DeepSeek stack start requested."
echo "OpenAI API: http://localhost:8080/v1"
echo "Recommended models: deepseek-coder, coder-fast"
