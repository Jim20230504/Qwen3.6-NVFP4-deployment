#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import urllib.error

try:
    from .create_api_key import build_key_generate_payload, post_json
except ImportError:
    from create_api_key import build_key_generate_payload, post_json


DEFAULT_MODELS = ["coder-fast", "coder", "deepseek-coder", "qwen36-coder"]


def build_key_specs(
    count: int, name_prefix: str, owner_prefix: str
) -> list[tuple[str, str]]:
    if count < 1:
        raise ValueError("count must be at least 1")

    return [
        (f"{name_prefix}{index}", f"{owner_prefix}{index}")
        for index in range(1, count + 1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create multiple LiteLLM virtual keys.")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--name-prefix", default="dev")
    parser.add_argument("--owner-prefix", default="dev")
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--rpm", type=int, default=int(os.environ.get("DEFAULT_RPM", "30")))
    parser.add_argument("--tpm", type=int, default=int(os.environ.get("DEFAULT_TPM", "120000")))
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=int(os.environ.get("DEFAULT_MAX_CONCURRENT", "2")),
    )
    args = parser.parse_args()

    try:
        key_specs = build_key_specs(args.count, args.name_prefix, args.owner_prefix)
    except ValueError as exc:
        parser.error(str(exc))

    for name, owner in key_specs:
        payload = build_key_generate_payload(
            name=name,
            owner=owner,
            models=args.models,
            rpm=args.rpm,
            tpm=args.tpm,
            max_concurrent=args.max_concurrent,
        )
        try:
            response = post_json("/key/generate", payload)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise SystemExit(
                f"Key creation stopped at {name}: {exc.code} {detail}"
            ) from exc

        print(json.dumps({"name": name, "response": response}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
