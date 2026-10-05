#!/usr/bin/env bash
# 将本仓库安装为 Agent Skill。
# 用法:
#   bash install.sh
#   bash install.sh /path/to/skills/nosurvey-lab   # 自定义目标
set -euo pipefail

NAME="nosurvey-lab"
DEST="${1:-$HOME/.doubao/agent_mode/workspace/.skills/$NAME}"
HERE="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$DEST"
# 用 git archive 只导出已跟踪文件（自动排除 .git、原图、缓存）
( cd "$HERE" && git archive HEAD ) | tar -x -C "$DEST"

echo "已安装 Skill「$NAME」到: $DEST"
