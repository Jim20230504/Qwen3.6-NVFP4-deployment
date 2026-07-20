# 本地 AI 平台

这是一个面向小团队内部使用的本地大模型平台，提供：

- OpenAI 兼容 API
- LiteLLM 网关与虚拟 Key 管理
- vLLM 本地推理
- 严格单模型启动模式
- Qwen / DeepSeek / Qwen3.6 模型切换
- Adminer 数据库管理界面

## 当前可切换模型

- `coder`：Qwen 32B AWQ 主模型
- `coder-fast`：Qwen 14B 快速模型
- `deepseek-coder`：DeepSeek V2 AWQ 备选主模型
- `qwen36-coder`：Qwen3.6-35B-A3B 备选主模型

## 推荐本地模型目录

```text
data/models/
├─ qwen32b-awq/
├─ qwen14b/
├─ deepseek-v2-awq/
└─ unsloth-Qwen3.6-35B-NVFP4/
```

## 快速启动

```bash
cp .env.example .env
bash install.sh
bash start.sh
```

`start.sh` 启动时可选：

- `1`：Qwen
- `2`：DeepSeek
- `3`：Qwen14B
- `4`：Qwen3.6-35B-A3B

也可以直接运行：

```bash
bash start-qwen.sh
bash start-deepseek.sh
bash start-qwen14b.sh
bash start-qwen36.sh
```

## 常用模型名

- `coder`
- `coder-fast`
- `deepseek-coder`
- `qwen36-coder`

## Key 管理

创建支持全部模型的 Key：

```bash
python scripts/create_api_key.py --name dev1 --owner alice --models coder-fast coder deepseek-coder qwen36-coder
```

批量创建 5 个支持全部模型的 Key：

```bash
set -a && source .env && set +a
python scripts/create_api_keys.py
```

可按需要指定数量、名称前缀和模型权限：

```bash
python scripts/create_api_keys.py --count 5 --name-prefix qwen36-dev --owner-prefix qwen36-dev --models qwen36-coder
```

删除 Key：

```bash
python scripts/revoke_api_key.py --key sk-...
```

查看 Key：

```bash
python scripts/list_api_keys.py
```

查看用量：

```bash
python scripts/usage_report.py --days 7
```

## 管理入口

- LiteLLM UI：`http://localhost:8080/ui/`
- Adminer：`http://localhost:8080/adminer/`

## 常用调参

主要通过 `.env` 调整：

- `QWEN32B_MAX_MODEL_LEN`
- `QWEN14B_MAX_MODEL_LEN`
- `DEEPSEEK_MAX_MODEL_LEN`
- `QWEN36_MAX_MODEL_LEN`
- `QWEN32B_MAX_NUM_SEQS`
- `QWEN14B_MAX_NUM_SEQS`
- `DEEPSEEK_MAX_NUM_SEQS`
- `QWEN36_MAX_NUM_SEQS`

推荐起步值：

- Qwen 32B：`8192 / 2`
- Qwen 14B：`8192 / 4`
- DeepSeek：`8192 / 2`
- Qwen3.6 NVFP4：首次启动使用 `4096 / 1`；确认显存稳定后再提高

## 文档

- [部署说明](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/deployment.md)
- [运维说明](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/operations.md)
- [VSCode 接入说明](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/vscode-integration.md)
- [中文一键部署教程](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/zh-deployment-guide.md)
