---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/02-configure.sh"
source_filename: "02-configure.sh"
source_type: "text"
source_size_bytes: 5968
source_modified_at: "2026-08-12T14:19:57+09:00"
source_sha256: "95a4db142ff036e073c9d28879dad4d1e9cde924ad8db66a5b488570257e2b76"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# 2단계: 시크릿 주입(Groq) + config.yaml 패치(STT/TTS/Composio MCP/이미지생성/웹검색 DuckDuckGo/시간대/위키경로) + 소유권 스윕
# 키 값은 setup.env → ssh stdin 으로만 이동. argv/화면/채팅에 노출되지 않음.
. "$(dirname "$0")/lib.sh"
discover
echo "▶ 대상: $CONTAINER"

# 원격 헬퍼 업로드 (/opt/data/tmp = 컨테이너에서도 보이는 경로)
hssh "mkdir -p $DATA_DIR/tmp"
scp -q "$SKILL_DIR/scripts/remote/env_set.py" "$SKILL_DIR/scripts/remote/patch_config.py" "$SSH_ALIAS:$DATA_DIR/tmp/"

# config.yaml 백업
hssh "cp $DATA_DIR/config.yaml $DATA_DIR/config.yaml.bak.\$(date +%Y%m%d_%H%M%S)"
echo "· config.yaml 백업 완료"

# 0) 소유권 스윕 — root 소유 파일이 있으면 Hermes(uid 10000)가 .env를 못 읽거나
#    게이트웨이가 로그 파일을 못 열어 기동 실패한다 (실사례 2건). 멱등.
hssh "chown 10000:10000 $DATA_DIR/.env $DATA_DIR/config.yaml 2>/dev/null; chown -R 10000:10000 $DATA_DIR/logs $DATA_DIR/tmp 2>/dev/null; true"
echo "· 데이터 파일 소유권 정렬 (uid 10000)"

# 1) Groq 키 → data/.env (stdin 전송) + 유효성 즉시 검증
if [ -n "${GROQ_API_KEY:-}" ]; then
  printf '%s' "$GROQ_API_KEY" | hssh "python3 $DATA_DIR/tmp/env_set.py $DATA_DIR/.env GROQ_API_KEY"
  # 검증 호출은 VPS에서 실행 — 키는 VPS 밖으로 나오지 않음
  HTTP="$(hssh "KEY=\$(sed -n 's/^GROQ_API_KEY=//p' $DATA_DIR/.env); curl -s -o /dev/null -w '%{http_code}' -H \"Authorization: Bearer \$KEY\" https://api.groq.com/openai/v1/models" || echo 000)"
  if [ "$HTTP" = "200" ]; then
    echo "✅ Groq 키 유효 확인"
  else
    echo "❌ Groq 키가 유효하지 않습니다 (HTTP $HTTP)." >&2
    echo "   setup.env 의 GROQ_API_KEY 를 다시 확인하고 이 스크립트를 재실행하세요." >&2
    exit 1
  fi
else
  echo "· GROQ_API_KEY 비어 있음 — STT 설정 건너뜀 (setup.env에 채우고 재실행하면 반영)"
fi

# 1b) 디스코드 기본 배달 채널 (크론/알림이 갈 곳 — 없으면 배달 실패 잡이 생길 수 있음)
if [ -n "${DISCORD_HOME_CHANNEL:-}" ]; then
  printf '%s' "$DISCORD_HOME_CHANNEL" | hssh "python3 $DATA_DIR/tmp/env_set.py $DATA_DIR/.env DISCORD_HOME_CHANNEL"
  echo "✅ DISCORD_HOME_CHANNEL 설정 (재시작 후 반영)"
fi

# 1c) 모델 프로바이더·기타 키 → data/.env (채워진 것만, stdin 전송)
#     구독 OAuth(/auth)가 1순위 — 이 키들은 키 경로를 쓸 때만 채워진다.
for K in OPENCODE_ZEN_API_KEY OPENCODE_GO_API_KEY OPENROUTER_API_KEY ANTHROPIC_API_KEY \
         CLAUDE_CODE_OAUTH_TOKEN FAL_KEY HERMES_SCRAPER_PROXY WEBSHARE_API_KEY \
         DISCORD_BOT_TOKEN DISCORD_ALLOWED_USERS TELEGRAM_BOT_TOKEN TELEGRAM_ALLOWED_USERS \
         SLACK_BOT_TOKEN SLACK_APP_TOKEN SLACK_ALLOWED_USERS; do
  V="${!K:-}"
  if [ -n "$V" ]; then
    printf '%s' "$V" | hssh "python3 $DATA_DIR/tmp/env_set.py $DATA_DIR/.env $K"
    echo "✅ $K 등록 (재시작 후 반영)"
  fi
done

# 2) openai-codex 인증 여부 (이미지 생성 활성 조건)
HAVE_CODEX=0
if hssh "grep -q codex $DATA_DIR/auth.json 2>/dev/null"; then
  HAVE_CODEX=1
fi

# 3) config.yaml 패치 ops 조립
SET_PAIRS=(
  "\"timezone\": \"${TIMEZONE:-Asia/Seoul}\""
  '"WIKI_PATH": "/opt/data/wiki"'
  '"OBSIDIAN_VAULT_PATH": "/opt/data/wiki"'
)
[ -n "${GROQ_API_KEY:-}" ] && SET_PAIRS+=('"stt": {"enabled": true, "provider": "groq"}')
[ -n "${COMPOSIO_API_KEY:-}" ] && SET_PAIRS+=("\"mcp_servers.composio\": {\"url\": \"https://connect.composio.dev/mcp\", \"headers\": {\"x-consumer-api-key\": \"$COMPOSIO_API_KEY\"}}")

DEF_PAIRS=(
  "\"tts\": {\"provider\": \"edge\", \"edge\": {\"voice\": \"${TTS_VOICE:-ko-KR-HyunsuMultilingualNeural}\", \"speed\": 1.1}}"
  '"web": {"backend": "ddgs"}'
)

# 2b) 웹 검색 기본 백엔드 = DuckDuckGo (키 불요). ddgs 패키지는 이미지에 없어 설치 필요.
#     ⚠️ 이미지 레이어 설치라 컨테이너 "재생성"(recreate) 시 사라짐 — 05-verify가 감지하며, 이 스크립트 재실행으로 복구.
if hssh "docker exec $CONTAINER uv pip install --python /opt/hermes/.venv/bin/python3 -q ddgs" 2>/dev/null; then
  echo "✅ 웹 검색: DuckDuckGo(ddgs) 설치·기본 설정"
else
  echo "⚠️  ddgs 설치 실패 — 웹 검색은 다른 백엔드 폴백. 재실행으로 재시도 가능" >&2
fi
if [ "$HAVE_CODEX" = 1 ]; then
  DEF_PAIRS+=('"image_gen": {"provider": "openai-codex", "model": "gpt-image-2-low"}')
else
  echo "· openai-codex 미인증 — 이미지 생성 설정 건너뜀 (Hermes 채팅에서 /auth 로 인증 후 재실행)"
fi

join() { local IFS=,; echo "$*"; }
OPS="{\"set\": {$(join "${SET_PAIRS[@]}")}, \"setdefault\": {$(join "${DEF_PAIRS[@]}")}}"

# 4) 패치 실행 (docker exec -i 필수: stdin 파이프)
printf '%s' "$OPS" | hssh "docker exec -i -u 10000 $CONTAINER python3 /opt/data/tmp/patch_config.py"

# 5) 컨테이너 재시작 (설정 반영)
if [ "${RESTART:-ask}" = "yes" ] || [ "${1:-}" = "--restart" ]; then
  echo "♻️  컨테이너 재시작 중 (약 30초 서비스 중단)..."
  hssh "cd $COMPOSE_DIR && docker compose restart" >/dev/null 2>&1
  echo "✅ 재시작 완료"
else
  echo "⚠️  설정 반영엔 재시작이 필요합니다: bash scripts/02-configure.sh --restart"
fi

# 6) 전송 완료된 키를 setup.env에서 제거 (파일에 평문으로 남기지 않음)
if [ -f "$SETUP_ENV" ]; then
  awk '/^(GROQ_API_KEY|COMPOSIO_API_KEY|OPENCODE_ZEN_API_KEY|OPENCODE_GO_API_KEY|OPENROUTER_API_KEY|ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN|FAL_KEY|HERMES_SCRAPER_PROXY|WEBSHARE_API_KEY|DISCORD_BOT_TOKEN|TELEGRAM_BOT_TOKEN|SLACK_BOT_TOKEN|SLACK_APP_TOKEN)=./{sub(/=.*/, "=  # (VPS로 전송 완료 — 값 제거됨)")} {print}' \
    "$SETUP_ENV" > "$SETUP_ENV.tmp" && mv "$SETUP_ENV.tmp" "$SETUP_ENV"
  echo "🧹 setup.env 의 키 값 제거 완료"
fi

echo ""
echo "다음 단계: bash scripts/03-server-syncthing.sh"
