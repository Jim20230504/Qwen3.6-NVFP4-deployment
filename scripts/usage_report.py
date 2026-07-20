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


def build_spend_report_path(
    days: int,
    api_key: str | None,
    internal_user_id: str | None,
    summarize: bool = True,
) -> str:
    end_date = date.today()
    start_date = end_date - timedelta(days=max(days - 1, 0))
    params: dict[str, str] = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    if api_key:
        params["api_key"] = api_key
    if internal_user_id:
        params["user_id"] = internal_user_id
    params["summarize"] = str(summarize).lower()
    return f"/spend/logs?{urllib.parse.urlencode(params)}"


def summarize_token_usage(logs: list[dict[str, object]]) -> dict[str, object]:
    summary: dict[str, object] = {
        "requests": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "models": {},
    }
    models: dict[str, dict[str, int]] = summary["models"]  # type: ignore[assignment]

    for log in logs:
        model = str(log.get("model") or "unknown")
        prompt_tokens = int(log.get("prompt_tokens") or 0)
        completion_tokens = int(log.get("completion_tokens") or 0)
        total_tokens = int(log.get("total_tokens") or prompt_tokens + completion_tokens)
        model_summary = models.setdefault(
            model,
            {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        )
        for target in (summary, model_summary):
            target["requests"] += 1  # type: ignore[operator]
            target["prompt_tokens"] += prompt_tokens  # type: ignore[operator]
            target["completion_tokens"] += completion_tokens  # type: ignore[operator]
            target["total_tokens"] += total_tokens  # type: ignore[operator]

    return summary


def get_json(path: str) -> object:
    request = urllib.request.Request(
        url=f"{get_proxy_url()}{path}",
        headers={"Authorization": f"Bearer {get_master_key()}"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Print LiteLLM spend logs summary.")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--api-key")
    parser.add_argument("--internal-user-id")
    parser.add_argument(
        "--tokens",
        action="store_true",
        help="Print token totals from individual request logs.",
    )
    args = parser.parse_args()

    path = build_spend_report_path(
        args.days,
        args.api_key,
        args.internal_user_id,
        summarize=not args.tokens,
    )
    response = get_json(path)
    if args.tokens:
        if isinstance(response, dict):
            response = response.get("data", [])
        if not isinstance(response, list):
            raise SystemExit("LiteLLM returned an unexpected spend logs response.")
        response = summarize_token_usage(response)
    print(json.dumps(response, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
