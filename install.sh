#!/usr/bin/env bash
set -euo pipefail

bash scripts/init_dirs.sh

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

set -a
source .env
set +a

if ! command -v docker >/dev/null 2>&1; then
  echo "Installing Docker Engine and Docker Compose plugin..."
  bash scripts/install_docker_ubuntu.sh
fi

if ! command -v nvidia-ctk >/dev/null 2>&1; then
  echo "Installing NVIDIA Container Toolkit..."
  bash scripts/install_nvidia_container_toolkit.sh
fi

if [[ "${ENABLE_SWAP_SETUP:-true}" == "true" ]]; then
  bash scripts/setup_swap.sh "${SWAP_SIZE_GB:-32}"
fi

bash scripts/check_env.sh

echo "Install complete. Review .env before first startup."
