from pathlib import Path

from scripts.create_api_key import build_key_generate_payload
from scripts.revoke_api_key import build_delete_payload
from scripts.usage_report import build_spend_report_path


def test_build_key_generate_payload_contains_models_and_limits():
    payload = build_key_generate_payload(
        name="dev1",
        owner="alice",
        models=["coder-fast", "coder"],
        rpm=30,
        tpm=120000,
        max_concurrent=2,
    )

    assert payload["key_alias"] == "dev1"
    assert payload["user_id"] == "alice"
    assert payload["models"] == ["coder-fast", "coder"]
    assert payload["rpm_limit"] == 30
    assert payload["tpm_limit"] == 120000
    assert payload["max_parallel_requests"] == 2


def test_build_delete_payload_targets_expected_key():
    payload = build_delete_payload("sk-demo-key")

    assert payload == {"key": "sk-demo-key"}


def test_build_spend_report_path_uses_global_report_endpoint():
    path = build_spend_report_path(7, api_key="sk-demo-key", internal_user_id=None)

    assert path.startswith("/global/spend/report?")
    assert "api_key=sk-demo-key" in path
    assert "start_date=" in path
    assert "end_date=" in path


def test_core_shell_scripts_exist():
    for path in [
        "install.sh",
        "start.sh",
        "stop.sh",
        "logs.sh",
        "start-qwen.sh",
        "start-deepseek.sh",
        "start-qwen14b.sh",
        "scripts/check_env.sh",
        "scripts/install_docker_ubuntu.sh",
        "scripts/install_nvidia_container_toolkit.sh",
        "scripts/setup_swap.sh",
    ]:
        assert Path(path).exists(), path


def test_start_script_prompts_for_qwen_and_deepseek_choices():
    content = Path("start.sh").read_text(encoding="utf-8")

    assert "Qwen" in content
    assert "DeepSeek" in content
    assert "Qwen14B" in content
    assert "start-qwen.sh" in content
    assert "start-deepseek.sh" in content
    assert "start-qwen14b.sh" in content
