#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request


def get_proxy_url() -> str:
    return os.environ.get("LITELLM_PROXY_URL", "http://localhost:8080").rstrip("/")


def get_master_key() -> str:
    return os.environ["LITELLM_MASTER_KEY"]


def get_json(path: str) -> object:
    request = urllib.request.Request(
        url=f"{get_proxy_url()}{path}",
        headers={"Authorization": f"Bearer {get_master_key()}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="List LiteLLM virtual keys.")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    query = urllib.parse.urlencode({"page": 1, "size": args.limit})
    response = get_json(f"/key/list?{query}")
    print(json.dumps(response, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
