---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/04-local-setup.sh"
source_filename: "04-local-setup.sh"
source_type: "text"
source_size_bytes: 10007
source_modified_at: "2026-08-12T16:10:05+09:00"
source_sha256: "c73bce50f13875f58cbe805c0b6d2d2c88c95a777e633d77bbda4520acbad239"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# 4단계(로컬): Syncthing·Obsidian 설치(없으면) + 서버↔로컬 자동 페어링 + 볼트 연결
# 맥/윈도우(Git Bash) 겸용.
. "$(dirname "$0")/lib.sh"
discover

VAULT="${LOCAL_VAULT_PATH:-$HOME/HermesWiki}"
mkdir -p "$VAULT"
# 동기화 노이즈·충돌 방지: 옵시디언이 상시 갱신하는 파일은 동기화 제외
if [ ! -f "$VAULT/.stignore" ]; then
  printf '(?d).obsidian/workspace*\n(?d).trash/\n(?d).DS_Store\n(?d)Thumbs.db\n' > "$VAULT/.stignore"
fi

# ---------- 1) 로컬 Syncthing 확보 ----------
gh_latest_tag() {
  curl -fsSL "https://api.github.com/repos/$1/releases/latest" \
    | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -1
}

install_syncthing_portable() {
  echo "▶ Syncthing 설치 중 ($PORTABLE_ST_DIR)..."
  mkdir -p "$PORTABLE_ST_DIR/bin" "$PORTABLE_ST_DIR/home"
  local TAG PKG EXT ARCH TMP
  TAG="$(gh_latest_tag syncthing/syncthing)"
  [ -n "$TAG" ] || { echo "❌ syncthing 버전 조회 실패 (네트워크 확인)"; exit 1; }
  case "$OS" in
    mac)
      case "$(uname -m)" in arm64) ARCH=arm64 ;; *) ARCH=amd64 ;; esac
      PKG="syncthing-macos-$ARCH-$TAG"; EXT=zip ;;
    win)
      PKG="syncthing-windows-amd64-$TAG"; EXT=zip ;;
    *)
      case "$(uname -m)" in aarch64) ARCH=arm64 ;; *) ARCH=amd64 ;; esac
      PKG="syncthing-linux-$ARCH-$TAG"; EXT=tar.gz ;;
  esac
  TMP="$(mktemp -d)"
  curl -fsSL -o "$TMP/st.$EXT" "https://github.com/syncthing/syncthing/releases/download/$TAG/$PKG.$EXT"
  # zip은 unzip으로(윈도 Git Bash tar=GNU tar는 zip 미지원), tar.gz는 tar로
  if [ "$EXT" = zip ]; then
    if command -v unzip >/dev/null 2>&1; then
      unzip -q "$TMP/st.$EXT" -d "$TMP"
    elif command -v powershell >/dev/null 2>&1; then
      powershell -NoProfile -Command "Expand-Archive -Force -LiteralPath '$(cygpath -w "$TMP/st.$EXT")' -DestinationPath '$(cygpath -w "$TMP")'"
    else
      tar -xf "$TMP/st.$EXT" -C "$TMP"
    fi
  else
    tar -xf "$TMP/st.$EXT" -C "$TMP"
  fi
  if [ "$OS" = win ]; then
    cp "$TMP/$PKG/syncthing.exe" "$PORTABLE_ST_DIR/bin/"
  else
    cp "$TMP/$PKG/syncthing" "$PORTABLE_ST_DIR/bin/"
    chmod +x "$PORTABLE_ST_DIR/bin/syncthing"
  fi
  rm -rf "$TMP"
  echo "✅ syncthing $TAG 설치"
}

portable_bin() {
  if [ "$OS" = win ]; then echo "$PORTABLE_ST_DIR/bin/syncthing.exe"; else echo "$PORTABLE_ST_DIR/bin/syncthing"; fi
}

register_autostart() {
  case "$OS" in
    mac)
      local PLIST="$HOME/Library/LaunchAgents/net.hermes.syncthing.plist"
      [ -f "$PLIST" ] && return 0
      mkdir -p "$HOME/Library/LaunchAgents"
      cat > "$PLIST" <<XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>net.hermes.syncthing</string>
  <key>ProgramArguments</key><array>
    <string>$PORTABLE_ST_DIR/bin/syncthing</string>
    <string>--no-browser</string>
    <string>--home=$PORTABLE_ST_DIR/home</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict></plist>
XML
      launchctl load "$PLIST" 2>/dev/null || true
      echo "✅ 로그인 시 자동 시작 등록 (launchd)"
      ;;
    win)
      local STARTUP="${APPDATA:-$HOME/AppData/Roaming}/Microsoft/Windows/Start Menu/Programs/Startup"
      local VBS="$STARTUP/hermes-syncthing.vbs"
      [ -f "$VBS" ] && return 0
      mkdir -p "$STARTUP"
      local WBIN WHOME
      WBIN="$(cygpath -w "$(portable_bin)")"
      WHOME="$(cygpath -w "$PORTABLE_ST_DIR/home")"
      printf 'CreateObject("WScript.Shell").Run """%s"" --no-browser --home=""%s""", 0\r\n' "$WBIN" "$WHOME" > "$VBS"
      echo "✅ 로그인 시 자동 시작 등록 (시작 프로그램)"
      ;;
  esac
}

start_portable_if_needed() {
  local GUI_TRY="${1:-127.0.0.1:8384}"
  if curl -fsS "http://$GUI_TRY/rest/noauth/health" >/dev/null 2>&1; then return 0; fi
  local BIN; BIN="$(portable_bin)"
  if [ "$OS" = win ]; then
    ( "$BIN" --no-browser --home="$(cygpath -w "$PORTABLE_ST_DIR/home")" >/dev/null 2>&1 & )
  else
    nohup "$BIN" --no-browser --home="$PORTABLE_ST_DIR/home" >/dev/null 2>&1 &
  fi
  sleep 5
}

CFG="$(local_st_config || true)"
PORTABLE=0
if [ -z "$CFG" ]; then
  install_syncthing_portable
  # Syncthing v2는 generate에서 --no-default-folder 제거 → 플래그 없이 생성 후 기본 폴더 제거
  "$(portable_bin)" generate --home="$PORTABLE_ST_DIR/home" >/dev/null 2>&1
  CFG="$PORTABLE_ST_DIR/home/config.xml"
  sed -i '/<folder /,/<\/folder>/d' "$CFG" 2>/dev/null || true
  PORTABLE=1
  register_autostart
else
  echo "· 기존 Syncthing 설치 발견: $CFG"
  case "$CFG" in "$PORTABLE_ST_DIR"*) PORTABLE=1 ;; esac
fi

APIKEY="$(st_apikey "$CFG")"
GUI="$(st_gui_addr "$CFG")"

# 실행 확인 (꺼져 있으면 기동 시도)
if ! curl -fsS -H "X-API-Key: $APIKEY" "http://$GUI/rest/system/status" >/dev/null 2>&1; then
  if [ "$PORTABLE" = 1 ]; then
    start_portable_if_needed "$GUI"
  elif [ "$OS" = mac ]; then
    open -a Syncthing 2>/dev/null || true; sleep 5
  fi
fi
if ! curl -fsS -H "X-API-Key: $APIKEY" "http://$GUI/rest/system/status" >/dev/null 2>&1; then
  echo "❌ 로컬 Syncthing이 실행되지 않습니다. Syncthing 앱을 직접 실행한 뒤 이 스크립트를 재실행하세요." >&2
  exit 3
fi
echo "✅ 로컬 Syncthing 실행 중 (http://$GUI)"

LOCAL_ID="$(curl -fsS -H "X-API-Key: $APIKEY" "http://$GUI/rest/system/status" | sed -n 's/.*"myID" *: *"\([A-Z0-9-]*\)".*/\1/p' | head -1)"
[ -n "$LOCAL_ID" ] || { echo "❌ 로컬 기기 ID를 읽지 못함"; exit 1; }
echo "· 로컬 기기 ID: ${LOCAL_ID:0:7}…"

# ---------- 2) 서버측 페어링 (기기 등록 + wiki 폴더 공유) ----------
hssh "mkdir -p $DATA_DIR/tmp"
scp -q "$SKILL_DIR/scripts/remote/st_pair.py" "$SSH_ALIAS:$DATA_DIR/tmp/"
PAIR_OUT="$(hssh "docker exec -u 10000 $CONTAINER python3 /opt/data/tmp/st_pair.py $LOCAL_ID my-computer")"
echo "$PAIR_OUT" | grep -v '^SERVER_ID='
SERVER_ID="$(echo "$PAIR_OUT" | sed -n 's/^SERVER_ID=//p')"
[ -n "$SERVER_ID" ] || { echo "❌ 서버 기기 ID를 받지 못함 — 03단계가 완료됐는지 확인"; exit 1; }

# ---------- 3) 로컬측 페어링 (서버 기기 등록 + wiki 폴더 = 볼트 경로) ----------
api() { curl -fsS -X "$1" -H "X-API-Key: $APIKEY" -H "Content-Type: application/json" ${3:+-d "$3"} "http://$GUI/$2"; }

if ! api GET rest/config/devices | grep -q "$SERVER_ID"; then
  api POST rest/config/devices "{\"deviceID\":\"$SERVER_ID\",\"name\":\"hermes-vps\"}" >/dev/null
  echo "✅ 서버 기기 등록(로컬)"
else
  echo "· 서버 기기 이미 등록됨(로컬)"
fi

VAULT_NATIVE="$VAULT"
if [ "$OS" = win ] && command -v cygpath >/dev/null 2>&1; then
  VAULT_NATIVE="$(cygpath -w "$VAULT" | sed 's/\\/\\\\/g')"
fi
if ! api GET rest/config/folders | grep -q '"id" *: *"wiki"'; then
  api POST rest/config/folders "{\"id\":\"wiki\",\"label\":\"hermes-wiki\",\"path\":\"$VAULT_NATIVE\",\"type\":\"sendreceive\",\"devices\":[{\"deviceID\":\"$SERVER_ID\"},{\"deviceID\":\"$LOCAL_ID\"}],\"rescanIntervalS\":60,\"fsWatcherEnabled\":true}" >/dev/null
  echo "✅ wiki 폴더 연결(로컬): $VAULT"
else
  echo "· 로컬에 'wiki' 폴더가 이미 있음 — Syncthing 화면(http://$GUI)에서 hermes-vps와 공유 중인지 확인하세요."
fi

# ---------- 4) Obsidian 설치 (없으면) ----------
obsidian_installed() {
  case "$OS" in
    mac) [ -d "/Applications/Obsidian.app" ] || [ -d "$HOME/Applications/Obsidian.app" ] ;;
    win) [ -f "${LOCALAPPDATA:-$HOME/AppData/Local}/Obsidian/Obsidian.exe" ] \
      || [ -f "${LOCALAPPDATA:-$HOME/AppData/Local}/Programs/Obsidian/Obsidian.exe" ] ;;
    *) command -v obsidian >/dev/null 2>&1 ;;
  esac
}

if ! obsidian_installed; then
  echo "▶ Obsidian 설치 중..."
  case "$OS" in
    mac)
      if command -v brew >/dev/null 2>&1; then
        brew install --cask obsidian
      else
        URL="$(curl -fsSL https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest \
          | sed -n 's/.*"browser_download_url": *"\([^"]*universal\.dmg\)".*/\1/p' | head -1)"
        [ -n "$URL" ] || URL="$(curl -fsSL https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest \
          | sed -n 's/.*"browser_download_url": *"\([^"]*\.dmg\)".*/\1/p' | head -1)"
        TMP="$(mktemp -d)"
        curl -fsSL -o "$TMP/obsidian.dmg" "$URL"
        MNT="$(hdiutil attach -nobrowse "$TMP/obsidian.dmg" | sed -n 's/.*\(\/Volumes\/.*\)/\1/p' | head -1)"
        cp -R "$MNT/Obsidian.app" /Applications/
        hdiutil detach "$MNT" >/dev/null
        rm -rf "$TMP"
      fi
      echo "✅ Obsidian 설치"
      ;;
    win)
      if command -v winget.exe >/dev/null 2>&1 || command -v winget >/dev/null 2>&1; then
        winget install -e --id Obsidian.Obsidian --accept-source-agreements --accept-package-agreements
        echo "✅ Obsidian 설치"
      else
        URL="$(curl -fsSL https://api.github.com/repos/obsidianmd/obsidian-releases/releases/latest \
          | sed -n 's/.*"browser_download_url": *"\([^"]*\.exe\)".*/\1/p' | grep -vi arm | head -1)"
        TMP="$(mktemp -d)"
        curl -fsSL -o "$TMP/ObsidianSetup.exe" "$URL"
        cmd //c start "" "$(cygpath -w "$TMP/ObsidianSetup.exe")" || true
        echo "· 설치 창이 뜨면 완료해 주세요."
      fi
      ;;
    *)
      echo "· Linux는 https://obsidian.md/download 에서 수동 설치"
      ;;
  esac
else
  echo "· Obsidian 이미 설치됨"
fi

# ---------- 5) 볼트 열기 (베스트 에포트) ----------
case "$OS" in
  mac) open "obsidian://open?path=$VAULT" 2>/dev/null || true ;;
  win) cmd //c start "" "obsidian://open?path=$(cygpath -w "$VAULT")" 2>/dev/null || true ;;
esac

echo ""
echo "🎉 로컬 셋업 완료 — 첫 동기화에 1~2분 걸릴 수 있습니다."
echo "   Obsidian에서 볼트가 안 열리면: Obsidian 실행 → 'Open folder as vault' → $VAULT 선택"
echo ""
echo "다음 단계: bash scripts/05-verify.sh"
