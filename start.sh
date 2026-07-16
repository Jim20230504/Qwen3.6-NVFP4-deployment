#!/usr/bin/env bash
set -euo pipefail

choice="${1:-}"

if [[ -z "${choice}" ]]; then
  echo "请选择启动模式："
  echo "1) Qwen"
  echo "2) DeepSeek"
  echo "3) Qwen14B"
  echo "4) Qwen3.6-35B-A3B"
  read -r -p "输入 1、2、3 或 4: " selection
  case "${selection}" in
    1) choice="qwen" ;;
    2) choice="deepseek" ;;
    3) choice="qwen14b" ;;
    4) choice="qwen36" ;;
    *)
      echo "无效选择，请重新运行 start.sh。"
      exit 1
      ;;
  esac
fi

case "${choice}" in
  qwen|Qwen)
    bash start-qwen.sh
    ;;
  deepseek|DeepSeek)
    bash start-deepseek.sh
    ;;
  qwen14b|Qwen14B|Qwen14b)
    bash start-qwen14b.sh
    ;;
  qwen36|Qwen36|Qwen3.6-35B-A3B)
    bash start-qwen36.sh
    ;;
  *)
    echo "不支持的启动模式：${choice}"
    echo "可用值：qwen、deepseek、qwen14b 或 qwen36"
    exit 1
    ;;
esac

echo
echo "Waiting for nginx health endpoint..."
for _ in $(seq 1 30); do
  if command -v curl >/dev/null 2>&1 && curl -fsS http://localhost:${HOST_HTTP_PORT:-8080}/health >/dev/null 2>&1; then
    break
  fi
  sleep 5
done

cat <<'EOF'

Platform start requested.

Health:
  curl http://localhost:8080/health

Adminer:
  http://localhost:8080/adminer/

OpenAI API:
  http://localhost:8080/v1
EOF
