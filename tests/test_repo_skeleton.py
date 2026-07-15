from pathlib import Path


def test_env_template_contains_core_values():
    content = Path(".env.example").read_text(encoding="utf-8")

    assert "HOST_HTTP_PORT=8080" in content
    assert "QWEN32B_MODEL_ID=" in content
    assert "QWEN14B_MODEL_ID=" in content
    assert "QWEN32B_MODEL_PATH=" in content
    assert "QWEN14B_MODEL_PATH=" in content
    assert "DEEPSEEK_MODEL_PATH=" in content
    assert "HTTP 对外端口" in content
    assert "本地模型目录" in content


def test_vscode_doc_contains_base_url_and_model_names():
    content = Path("docs/vscode-integration.md").read_text(encoding="utf-8")

    assert "Base URL" in content
    assert "coder-fast" in content
    assert "coder" in content


def test_readme_is_chinese_and_mentions_key_topics():
    content = Path("README.md").read_text(encoding="utf-8")

    assert "本地 AI 平台" in content
    assert "start.sh" in content
    assert "create_api_key.py" in content


def test_init_dirs_script_exists():
    assert Path("scripts/init_dirs.sh").exists()
