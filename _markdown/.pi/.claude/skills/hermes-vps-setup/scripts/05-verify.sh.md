---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/05-verify.sh"
source_filename: "05-verify.sh"
source_type: "text"
source_size_bytes: 5803
source_modified_at: "2026-08-12T14:19:56+09:00"
source_sha256: "0aa7512346945207a22beec160ab25bd720836e0ecfd2d7fe781d21fd5da34e6"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# 5단계: 전체 검증 — 서버 설정·Syncthing·크론·로컬 연동 상태 점검
. "$(dirname "$0")/lib.sh"

FAIL=0
ok()   { echo "✅ $1"; }
warn() { echo "·  $1"; }
bad()  { echo "❌ $1"; FAIL=1; }

discover
ok "SSH 접속 + 컨테이너 실행 중 ($CONTAINER)"

# 서버: 소유권 — root 소유면 Hermes(uid 10000)가 .env를 못 읽거나 게이트웨이가 기동 실패 (실사례)
BADOWN="$(hssh "find $DATA_DIR/.env $DATA_DIR/config.yaml $DATA_DIR/logs -maxdepth 1 -not -uid 10000 2>/dev/null | head -3" || true)"
if [ -z "$BADOWN" ]; then
  ok "데이터 파일 소유권 (uid 10000)"
else
  bad "root 소유 파일 있음 → 02단계 재실행(소유권 스윕) 후 재시작: $BADOWN"
fi

# 서버: 게이트웨이 프로세스 (컨테이너는 떠 있어도 게이트웨이만 죽어 있을 수 있음)
if hssh "docker exec $CONTAINER pgrep -f 'gateway' >/dev/null 2>&1"; then
  ok "게이트웨이 실행 중"
else
  bad "게이트웨이 죽어 있음 — $DATA_DIR/logs/gateway.log 끝부분 확인 후 재시작 필요"
fi

# 서버: .env 키
if hssh "grep -q '^GROQ_API_KEY=.' $DATA_DIR/.env 2>/dev/null"; then
  ok "GROQ_API_KEY 등록됨"
else
  warn "GROQ 키 없음 (STT 미사용이면 정상)"
fi

# 서버: 모델 프로바이더 — OAuth(auth.json) 또는 .env 키 중 하나는 있어야 응답 가능
if hssh "test -s $DATA_DIR/auth.json 2>/dev/null || grep -qE '^(OPENCODE_ZEN_API_KEY|OPENCODE_GO_API_KEY|OPENROUTER_API_KEY|ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN)=.' $DATA_DIR/.env 2>/dev/null"; then
  ok "모델 프로바이더 연결 (OAuth 또는 API 키)"
else
  warn "모델 프로바이더 없음 — Hermes 채팅 /auth(OAuth) 또는 setup.env에 키 채우고 02단계"
fi

# 서버: config.yaml 항목 (컨테이너 안 python으로 판독)
CHECKS="$(hssh "docker exec -i -u 10000 $CONTAINER python3 -" <<'PY'
import yaml
c = yaml.safe_load(open('/opt/data/config.yaml')) or {}
print('stt', 1 if (c.get('stt') or {}).get('enabled') else 0)
print('composio', 1 if 'composio' in (c.get('mcp_servers') or {}) else 0)
print('image', 1 if (c.get('image_gen') or {}).get('provider') == 'openai-codex' else 0)
print('wikipath', 1 if c.get('WIKI_PATH') == '/opt/data/wiki' else 0)
print('tz', 1 if c.get('timezone') == 'Asia/Seoul' else 0)
print('webddgs', 1 if (c.get('web') or {}).get('backend') == 'ddgs' else 0)
import importlib.util
print('ddgspkg', 1 if importlib.util.find_spec('ddgs') else 0)
PY
)"
flag() { echo "$CHECKS" | grep -q "^$1 1$"; }
flag stt      && ok "STT(groq) 활성"        || warn "STT 꺼짐 (키 넣고 02단계 재실행)"
flag composio && ok "Composio MCP 등록"     || warn "Composio 미설정 (선택)"
flag image    && ok "이미지 생성(openai-codex)" || warn "이미지 생성 미설정 (openai-codex 인증 후 02단계)"
flag wikipath && ok "위키 경로 설정"         || bad  "WIKI_PATH 미설정 — 02단계 재실행"
flag tz       && ok "시간대 Asia/Seoul (크론 KST)" || bad "시간대 미설정 — 크론이 UTC로 돎. 02단계 재실행"
if flag webddgs && flag ddgspkg; then
  ok "웹 검색 기본 DuckDuckGo"
elif flag webddgs; then
  bad "web.backend=ddgs인데 ddgs 패키지 없음(컨테이너 재생성으로 소실) — 02단계 재실행"
else
  warn "웹 검색 기본 미설정 — 02단계 재실행"
fi

# 서버: Composio MCP 실연결 (설정돼 있을 때만 — 키는 VPS 밖으로 안 나옴)
if flag composio; then
  MCP_HTTP="$(hssh "docker exec -u 10000 $CONTAINER python3 -c \"
import yaml, urllib.request, json
k = yaml.safe_load(open('/opt/data/config.yaml'))['mcp_servers']['composio']['headers']['x-consumer-api-key']
body = json.dumps({'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'verify','version':'1'}}}).encode()
r = urllib.request.Request('https://connect.composio.dev/mcp', data=body, headers={'content-type':'application/json','accept':'application/json, text/event-stream','x-consumer-api-key':k})
try: print(urllib.request.urlopen(r, timeout=10).status)
except Exception as e: print(getattr(e,'code',0))
\"" || echo 0)"
  case "$MCP_HTTP" in
    200) ok "Composio MCP 실연결 (핸드셰이크 200)" ;;
    401) bad "Composio 키 무효 (401) — setup.env의 COMPOSIO_API_KEY 확인 후 02단계 재실행" ;;
    *)   warn "Composio 연결 확인 불가 (HTTP $MCP_HTTP) — 네트워크 일시 문제일 수 있음" ;;
  esac
fi

# 서버: 위키·Syncthing·크론
hssh "test -f $DATA_DIR/wiki/index.md" \
  && ok "위키 스캐폴드" || bad "위키 없음 — 03단계 실행"
hssh "docker exec $CONTAINER pgrep -f 'syncthing --no-browser' >/dev/null 2>&1" \
  && ok "서버 Syncthing 실행 중" || warn "서버 Syncthing 꺼짐 (워치독이 5분 내 재기동)"
hssh "grep -q syncthing-watchdog $DATA_DIR/cron/jobs.json 2>/dev/null" \
  && ok "워치독 크론 등록" || bad "워치독 크론 없음 — 03단계 실행"

# 로컬: Syncthing + wiki 폴더
CFG="$(local_st_config || true)"
if [ -n "$CFG" ]; then
  APIKEY="$(st_apikey "$CFG")"
  GUI="$(st_gui_addr "$CFG")"
  if curl -fsS -H "X-API-Key: $APIKEY" "http://$GUI/rest/system/status" >/dev/null 2>&1; then
    ok "로컬 Syncthing 실행 중"
    if curl -fsS -H "X-API-Key: $APIKEY" "http://$GUI/rest/config/folders" | grep -q '"wiki"'; then
      ok "로컬 wiki 폴더 연결"
    else
      warn "로컬 wiki 폴더 미연결 — 04단계 실행"
    fi
  else
    warn "로컬 Syncthing 꺼져 있음 — 04단계 실행"
  fi
else
  warn "로컬 Syncthing 미설치 — 04단계 실행"
fi

echo ""
if [ "$FAIL" = 0 ]; then
  echo "🎉 검증 통과 — 셋업 완료"
else
  echo "⛔ 일부 항목 실패 — 위 안내대로 해당 단계를 재실행하세요."
  exit 1
fi
