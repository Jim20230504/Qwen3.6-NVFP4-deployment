#!/usr/bin/env bash
set -euo pipefail

mkdir -p \
  data/postgres \
  data/huggingface \
  data/models \
  data/logs \
  config/postgres \
  config/litellm \
  config/nginx \
  config/vllm \
  scripts \
  docs \
  tests
