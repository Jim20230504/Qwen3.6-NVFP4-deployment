# 本地 AI 平台

这是一个面向小团队内部使用的本地大模型平台，提供：

- OpenAI 兼容 API
- LiteLLM 网关与虚拟 Key 管理
- vLLM 本地推理
- Qwen / DeepSeek 主模型切换
- Adminer 数据库管理界面
- 一键安装与启动脚本

## 当前模型

- `coder`：Qwen 32B AWQ 主模型
- `coder-fast`：Qwen 14B 快速模型
- `deepseek-coder`：DeepSeek V2 AWQ 备选主模型

## 本地模型目录

当前项目已经改成“本地模型目录优先”模式，推荐目录如下：

```text
data/models/
├─ qwen32b-awq/
├─ qwen14b/
└─ deepseek-v2-awq/
```

目前我检查到你的模型目录已经存在，体积大致如下：

- `qwen32b-awq`：约 `18.01 GB`
- `qwen14b`：约 `27.52 GB`
- `deepseek-v2-awq`：约 `8.47 GB`

从目录和核心权重文件来看，三套模型看起来都是完整的。

## 快速部署

在 Ubuntu 24.04 新电脑上：

```bash
cp .env.example .env
bash install.sh
bash start.sh
```

`start.sh` 会提示你选择：

- `1`：启动 `Qwen`
- `2`：启动 `DeepSeek`
- `3`：启动 `Qwen14B`

也可以直接使用：

```bash
bash start-qwen.sh
bash start-deepseek.sh
bash start-qwen14b.sh
```

## 部署后怎么用

### 1. 查看健康状态

```bash
curl http://localhost:8080/health
docker compose ps
```

### 2. 创建管理 Key / 调用 Key

创建一个可调用 `coder`、`coder-fast`、`deepseek-coder` 的 Key：

```bash
python scripts/create_api_key.py --name dev1 --owner alice --models coder-fast coder deepseek-coder
```

删除一个 Key：

```bash
python scripts/revoke_api_key.py --key sk-...
```

查看所有 Key：

```bash
python scripts/list_api_keys.py
```

查看近 7 天用量：

```bash
python scripts/usage_report.py --days 7
```

### 3. 管理界面

- LiteLLM UI：`http://localhost:8080/ui/`
- Adminer：`http://localhost:8080/adminer/`

### 4. OpenAI 兼容调用

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <API_KEY>" \
  -d '{
    "model": "coder-fast",
    "messages": [
      {"role": "user", "content": "请写一个 Python 读取 JSON 文件的函数"}
    ],
    "temperature": 0.2
  }'
```

## 怎么调整上下文和并发

主要改 `.env` 里的这些值：

- `QWEN32B_MAX_MODEL_LEN`
- `QWEN32B_MAX_NUM_SEQS`
- `QWEN14B_MAX_MODEL_LEN`
- `QWEN14B_MAX_NUM_SEQS`
- `DEEPSEEK_MAX_MODEL_LEN`
- `DEEPSEEK_MAX_NUM_SEQS`

推荐理解方式：

- `MAX_MODEL_LEN`：单次请求可用上下文上限
- `MAX_NUM_SEQS`：同一时刻服务端允许的序列并发规模，越大越吃显存

推荐起步值：

- Qwen 32B：`8192` / `2`
- Qwen 14B：`8192` / `4`
- DeepSeek：`8192` / `2`

如果你遇到 OOM、重启、响应很慢，先优先降低：

1. `MAX_NUM_SEQS`
2. `MAX_MODEL_LEN`

改完后重启：

```bash
bash stop.sh
bash start.sh
```

## 文档

- [部署说明](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/deployment.md)
- [运维说明](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/operations.md)
- [VSCode 接入说明](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/vscode-integration.md)
- [中文一键部署教程](C:/Users/jim/Desktop/work/DAMOXINGBUSHU/docs/zh-deployment-guide.md)
