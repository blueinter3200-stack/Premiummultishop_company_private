---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/remote/syncthing-watchdog.sh"
source_filename: "syncthing-watchdog.sh"
source_type: "text"
source_size_bytes: 778
source_modified_at: "2026-08-12T14:19:57+09:00"
source_sha256: "b838d5c301c09bbeeafd9faa12497e5a1ecc3cd686dff1e2b78205d1b3d1cc61"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# Syncthing 워치독 — Hermes 크론(no_agent, 5분 간격)이 컨테이너 안에서 실행.
# 죽어 있으면 재기동, 살아 있으면 무음 종료.
set -euo pipefail

ST_BIN="/opt/data/.local/bin/syncthing"
ST_HOME="/opt/data/.config/syncthing"
LOG_DIR="/opt/data/logs"
LOG_FILE="$LOG_DIR/syncthing-watchdog.log"
mkdir -p "$LOG_DIR"

if pgrep -f "syncthing --no-browser --home=$ST_HOME" >/dev/null 2>&1 || pgrep -f "syncthing.*$ST_HOME" >/dev/null 2>&1; then
  exit 0
fi

if [ ! -x "$ST_BIN" ] || [ ! -f "$ST_HOME/config.xml" ]; then
  echo "syncthing watchdog: binary or config missing" >&2
  exit 1
fi

nohup "$ST_BIN" --no-browser --home="$ST_HOME" >> "$LOG_FILE" 2>&1 &
echo "syncthing watchdog: restarted at $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
