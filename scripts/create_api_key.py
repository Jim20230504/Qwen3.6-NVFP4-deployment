#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request


def get_proxy_url() -> str:
    return os.environ.get("LITELLM_PROXY_URL", "http://localhost:8080").rstrip("/")


def get_master_key() -> str:
    return os.environ["LITELLM_MASTER_KEY"]


def build_key_generate_payload(
    name: str,
    owner: str,
    models: list[str],
    rpm: int,
    tpm: int,
    max_concurrent: int,
) -> dict[str, object]:
    return {
        "key_alias": name,
        "duration": None,
        "models": models,
        "rpm_limit": rpm,
        "tpm_limit": tpm,
        "max_parallel_requests": max_concurrent,
        "metadata": {
            "owner_name": owner,
            "managed_by": "local-ai-platform",
        },
        "user_id": owner or name,
    }


def post_json(path: str, payload: dict[str, object]) -> dict[str, object]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url=f"{get_proxy_url()}{path}",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_master_key()}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a LiteLLM virtual key.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--owner", default="")
    parser.add_argument("--models", nargs="+", default=["coder-fast"])
    parser.add_argument("--rpm", type=int, default=int(os.environ.get("DEFAULT_RPM", "30")))
    parser.add_argument("--tpm", type=int, default=int(os.environ.get("DEFAULT_TPM", "120000")))
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=int(os.environ.get("DEFAULT_MAX_CONCURRENT", "2")),
    )
    args = parser.parse_args()

    payload = build_key_generate_payload(
        name=args.name,
        owner=args.owner,
        models=args.models,
        rpm=args.rpm,
        tpm=args.tpm,
        max_concurrent=args.max_concurrent,
    )

    try:
        response = post_json("/key/generate", payload)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"LiteLLM key generation failed: {exc.code} {detail}") from exc

    print(json.dumps(response, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
