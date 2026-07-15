#!/usr/bin/env bash
set -euo pipefail

swap_size_gb="${1:-32}"
swap_file="/swapfile"

if swapon --show | grep -q "${swap_file}"; then
  echo "Swap already enabled at ${swap_file}."
  exit 0
fi

sudo fallocate -l "${swap_size_gb}G" "${swap_file}"
sudo chmod 600 "${swap_file}"
sudo mkswap "${swap_file}"
sudo swapon "${swap_file}"
sudo sysctl vm.swappiness=10 >/dev/null

if ! grep -q "^${swap_file} " /etc/fstab; then
  echo "${swap_file} none swap sw 0 0" | sudo tee -a /etc/fstab >/dev/null
fi

echo "Swap configured: ${swap_size_gb}G"
