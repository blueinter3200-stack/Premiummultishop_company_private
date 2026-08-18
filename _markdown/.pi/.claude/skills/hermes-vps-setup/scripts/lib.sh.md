---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/lib.sh"
source_filename: "lib.sh"
source_type: "text"
source_size_bytes: 2165
source_modified_at: "2026-08-12T14:19:57+09:00"
source_sha256: "0b115b586a3be33692ca7ec2748bbe108c58c91af069e4b3b65fc9eeea22ce38"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# 공용 함수 — 각 스크립트가 source. 직접 실행하는 파일 아님.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SETUP_ENV="$SKILL_DIR/setup.env"
if [ -f "$SETUP_ENV" ]; then
  chmod 600 "$SETUP_ENV" 2>/dev/null || true   # 키가 담기는 파일 — 소유자만 읽게
  set -a
  # shellcheck disable=SC1090
  . "$SETUP_ENV"
  set +a
fi

SSH_ALIAS="${SSH_ALIAS:-hermes}"

case "$(uname -s)" in
  Darwin) OS=mac ;;
  MINGW*|MSYS*|CYGWIN*) OS=win ;;
  *) OS=linux ;;
esac

hssh() { ssh -o ConnectTimeout=15 "$SSH_ALIAS" "$@"; }

# VPS에서 Hermes compose 디렉토리/컨테이너 자동 탐색 → COMPOSE_DIR, CONTAINER, DATA_DIR
discover() {
  COMPOSE_DIR="$(hssh 'ls -d /docker/hermes-agent-* 2>/dev/null | head -1')"
  if [ -z "$COMPOSE_DIR" ]; then
    echo "❌ VPS에 /docker/hermes-agent-* 가 없습니다 — Hostinger 앱 카탈로그로 Hermes를 먼저 설치하세요." >&2
    exit 1
  fi
  CONTAINER="$(hssh 'docker ps --format "{{.Names}}" | grep "^hermes-agent" | head -1')"
  if [ -z "$CONTAINER" ]; then
    echo "❌ hermes 컨테이너가 실행 중이 아닙니다 — Hostinger 패널에서 상태를 확인하세요." >&2
    exit 1
  fi
  DATA_DIR="$COMPOSE_DIR/data"
}

# ---- 로컬 Syncthing 헬퍼 ----
PORTABLE_ST_DIR="$HOME/.hermes-sync"

# 기존 설치 우선으로 로컬 config.xml 경로 탐색 (없으면 실패 리턴)
local_st_config() {
  local candidates=()
  case "$OS" in
    mac) candidates=("$HOME/Library/Application Support/Syncthing/config.xml") ;;
    win) candidates=("${LOCALAPPDATA:-$HOME/AppData/Local}/Syncthing/config.xml") ;;
    *)   candidates=("$HOME/.local/state/syncthing/config.xml" "$HOME/.config/syncthing/config.xml") ;;
  esac
  candidates+=("$PORTABLE_ST_DIR/home/config.xml")
  local c
  for c in "${candidates[@]}"; do
    if [ -f "$c" ]; then printf '%s' "$c"; return 0; fi
  done
  return 1
}

st_apikey()   { sed -n 's/.*<apikey>\(.*\)<\/apikey>.*/\1/p' "$1" | head -1; }
st_gui_addr() {
  local a
  a="$(sed -n 's/.*<address>\([0-9][0-9.:]*\)<\/address>.*/\1/p' "$1" | head -1)"
  printf '%s' "${a:-127.0.0.1:8384}"
}
