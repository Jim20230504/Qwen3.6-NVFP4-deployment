#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from datetime import date, timedelta


def get_proxy_url() -> str:
    return os.environ.get("LITELLM_PROXY_URL", "http://localhost:8080").rstrip("/")


def get_master_key() -> str:
    return os.environ["LITELLM_MASTER_KEY"]


def build_spend_report_path(days: int, api_key: str | None, internal_user_id: str | None) -> str:
    end_date = date.today()
    start_date = end_date - timedelta(days=max(days - 1, 0))
    params: dict[str, str] = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    if api_key:
        params["api_key"] = api_key
    if internal_user_id:
        params["internal_user_id"] = internal_user_id
    return f"/global/spend/report?{urllib.parse.urlencode(params)}"


def get_json(path: str) -> object:
    request = urllib.request.Request(
        url=f"{get_proxy_url()}{path}",
        headers={"Authorization": f"Bearer {get_master_key()}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Print LiteLLM spend report.")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--api-key")
    parser.add_argument("--internal-user-id")
    args = parser.parse_args()

    path = build_spend_report_path(args.days, args.api_key, args.internal_user_id)
    response = get_json(path)
    print(json.dumps(response, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
