from pathlib import Path


def test_chinese_deployment_guide_mentions_qwen_and_deepseek():
    content = Path("docs/zh-deployment-guide.md").read_text(encoding="utf-8")

    assert "一键部署" in content
    assert "start-qwen.sh" in content
    assert "start-deepseek.sh" in content
    assert "deepseek-coder" in content
    assert "QWEN32B_MAX_MODEL_LEN" in content
    assert "create_api_key.py" in content
