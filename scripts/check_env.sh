#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This installer targets Linux hosts." >&2
  exit 1
fi

if [[ ! -f /etc/os-release ]]; then
  echo "Cannot detect Linux distribution." >&2
  exit 1
fi

. /etc/os-release

if [[ "${ID:-}" != "ubuntu" ]]; then
  echo "Expected Ubuntu. Detected: ${ID:-unknown}" >&2
  exit 1
fi

if [[ "${VERSION_ID:-}" != "24.04" ]]; then
  echo "Expected Ubuntu 24.04. Detected: ${VERSION_ID:-unknown}" >&2
  exit 1
fi

command -v docker >/dev/null || {
  echo "docker is not installed." >&2
  exit 1
}

command -v nvidia-smi >/dev/null || {
  echo "nvidia-smi is not installed or NVIDIA driver is unavailable." >&2
  exit 1
}

docker info >/dev/null
nvidia-smi >/dev/null
docker compose version >/dev/null

if ! docker run --rm --gpus all nvidia/cuda:12.9.0-base-ubuntu24.04 nvidia-smi >/dev/null 2>&1; then
  echo "Docker cannot access the GPU. Check NVIDIA Container Toolkit configuration." >&2
  exit 1
fi

echo "Environment looks ready."
