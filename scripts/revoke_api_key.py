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


def build_delete_payload(key: str) -> dict[str, str]:
    return {"key": key}


def post_json(path: str, payload: dict[str, str]) -> dict[str, object]:
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
    parser = argparse.ArgumentParser(description="Delete a LiteLLM virtual key.")
    parser.add_argument("--key", required=True, help="Full virtual key returned by LiteLLM")
    args = parser.parse_args()

    try:
        response = post_json("/key/delete", build_delete_payload(args.key))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"LiteLLM key deletion failed: {exc.code} {detail}") from exc

    print(json.dumps(response, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
