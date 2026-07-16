from pathlib import Path

import yaml


def test_litellm_config_contains_expected_aliases():
    config = yaml.safe_load(Path("config/litellm/config.yaml").read_text(encoding="utf-8"))

    model_names = [item["model_name"] for item in config["model_list"]]

    assert "coder" in model_names
    assert "coder-fast" in model_names
    assert "deepseek-coder" in model_names
    assert "qwen36-coder" in model_names


def test_compose_contains_required_services():
    compose = yaml.safe_load(Path("docker-compose.yml").read_text(encoding="utf-8"))

    services = compose["services"]

    assert "postgres" in services
    assert "adminer" in services
    assert "litellm" in services
    assert "vllm-qwen32b" in services
    assert "vllm-qwen14b" in services
    assert "nginx" in services

    assert services["litellm"]["depends_on"]["postgres"]["condition"] == "service_healthy"
    assert services["postgres"]["logging"]["options"]["max-size"] == "20m"
    assert services["nginx"]["ports"] == ["${HOST_HTTP_PORT}:80"]


def test_vllm_env_files_exist_with_model_ids():
    qwen32b = Path("config/vllm/qwen32b.env").read_text(encoding="utf-8")
    qwen14b = Path("config/vllm/qwen14b.env").read_text(encoding="utf-8")
    deepseek = Path("config/vllm/deepseek.env").read_text(encoding="utf-8")
    qwen36 = Path("config/vllm/qwen36.env").read_text(encoding="utf-8")

    assert "MODEL_ID=${QWEN32B_MODEL_ID}" in qwen32b
    assert "MODEL_ID=${QWEN14B_MODEL_ID}" in qwen14b
    assert "MODEL_ID=${DEEPSEEK_MODEL_ID}" in deepseek
    assert "MODEL_ID=${QWEN36_MODEL_ID}" in qwen36


def test_qwen36_nvfp4_profile_uses_compatible_runtime_settings():
    env_example = Path(".env.example").read_text(encoding="utf-8")
    compose = yaml.safe_load(Path("docker-compose.yml").read_text(encoding="utf-8"))
    qwen36 = compose["services"]["vllm-qwen36"]

    assert "QWEN36_MODEL_ID=unsloth/Qwen3.6-35B-A3B-NVFP4" in env_example
    assert "QWEN36_MODEL_PATH=/models/local/unsloth-Qwen3.6-35B-NVFP4" in env_example
    assert qwen36["build"]["dockerfile"] == "Dockerfile.vllm-qwen36"
    assert "--dtype" in qwen36["command"]
    assert "bfloat16" in qwen36["command"]
    assert qwen36["command"][qwen36["command"].index("--reasoning-parser") + 1] == "qwen3"
    assert qwen36["command"][qwen36["command"].index("--tool-call-parser") + 1] == "qwen3_xml"


def test_litellm_only_depends_on_postgres_not_inactive_model_profiles():
    compose = yaml.safe_load(Path("docker-compose.yml").read_text(encoding="utf-8"))

    assert set(compose["services"]["litellm"]["depends_on"]) == {"postgres"}
