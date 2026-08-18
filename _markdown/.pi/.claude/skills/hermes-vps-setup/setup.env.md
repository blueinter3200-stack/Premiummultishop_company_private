---
source_path: ".pi/.claude/skills/hermes-vps-setup/setup.env"
source_filename: "setup.env"
source_type: "text"
source_size_bytes: 4011
source_modified_at: "2026-08-12T16:53:26+09:00"
source_sha256: "b4d4b797cc68ef83a3d1d2b4b154bdc0eee210e16fe196a1b29d21a99ff9aa8a"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# ===== Hermes VPS 셋업 설정 =====
# 이 파일을 같은 폴더에 setup.env 라는 이름으로 복사한 뒤 값을 채우세요.
# ⚠️ API 키는 채팅(Claude)에 붙여넣지 말고 반드시 이 파일에만 적으세요.
#    키는 전송이 끝나면 이 파일에서 자동으로 지워집니다.
# ⚠️ 이 폴더를 OneDrive/iCloud/구글드라이브 등 클라우드 동기화 폴더나
#    git 저장소 안에 두지 마세요 — 키가 외부로 복제될 수 있습니다.

# [필수] Hostinger VPS 공인 IP
VPS_IP=187.52.115.143

# SSH 접속 별칭 (보통 그대로 두면 됨)
SSH_ALIAS=hermes

# 시간대
TIMEZONE=Asia/Seoul

# [선택] Groq API 키 — 음성 인식(STT)용. https://console.groq.com/keys 에서 발급
GROQ_API_KEY=  # (VPS로 전송 완료 — 값 제거됨)

# [선택] Composio MCP 키 — Gmail 등 외부 앱 연동. https://app.composio.dev 에서 발급
COMPOSIO_API_KEY=  # (VPS로 전송 완료 — 값 제거됨)

# TTS 목소리 (edge-tts, 무료·키 불필요. 다른 목소리: ko-KR-SunHiNeural 등)
TTS_VOICE=ko-KR-HyunsuMultilingualNeural

# ── [선택] 모델 프로바이더 키 — 전부 data/.env 로 전송됨 ──
# 1순위는 구독 OAuth (Hermes 채팅에서 /auth — ChatGPT·Grok·Copilot 등).
# OAuth를 쓴다면 아래는 전부 비워도 된다. 키 경로가 필요할 때만 채우기:
# OpenCode Zen — 무료 모델 게이트웨이(deepseek-v4-flash-free 등). https://opencode.ai
OPENCODE_ZEN_API_KEY=  # (VPS로 전송 완료 — 값 제거됨)
# OpenCode Go — 유료 구독 게이트웨이(claude-sonnet·GLM·Kimi 등). https://opencode.ai
OPENCODE_GO_API_KEY=

# OpenRouter — 키 하나로 20+ 프로바이더(종량제). https://openrouter.ai/keys
OPENROUTER_API_KEY=
# Anthropic API 키(종량제). https://console.anthropic.com
ANTHROPIC_API_KEY=
# Claude 구독(Pro/Max) — 내 컴퓨터에서 `claude setup-token` 실행 후 토큰 붙여넣기
CLAUDE_CODE_OAUTH_TOKEN=

# ── [선택] 기타 ──
# 이미지 생성용 fal.ai 키 — GPT 구독 OAuth(/auth)가 있으면 비워도 됨(gpt-image-2 사용)
FAL_KEY=
# 스크래퍼·유튜브 자막 전용 프록시 (형식: http://user:pass@host:port)
# 클라우드 IP가 채용보드·유튜브에 차단될 때만 필요. 추천: webshare.io 무료 개별 프록시
HERMES_SCRAPER_PROXY=  # (VPS로 전송 완료 — 값 제거됨)
# Webshare API 키 — 죽은 프록시 자동 교체용(hermes-agent-kit 구직 파이프라인 사용 시)
WEBSHARE_API_KEY=  # (VPS로 전송 완료 — 값 제거됨)

# ── [선택] 메신저 봇 토큰 — 설치 때 이미 넣었다면 비워두세요 (덮어쓰지 않음) ──
# Discord: Developer Portal > Bot > Reset Token. ⚠️ Message Content Intent 반드시 ON
DISCORD_BOT_TOKEN=
# 본인 Discord 유저 ID(숫자). 설정 > 고급 > 개발자 모드 ON → 내 프로필 우클릭 → ID 복사
# 미설정이면 아무도 봇을 못 쓴다 (기본 차단 = 보안 기본값)
DISCORD_ALLOWED_USERS=
# [권장] 디스코드 기본 배달 채널 ID — 크론/알림 메시지가 갈 곳.
# 얻는 법: 디스코드 설정 → 고급 → 개발자 모드 켜기 → 채널 우클릭 → "ID 복사"
# ⚠️ 스레드가 아니라 채널을 우클릭해야 합니다.
DISCORD_HOME_CHANNEL=

# Telegram: @BotFather 에게 /newbot
TELEGRAM_BOT_TOKEN=  # (VPS로 전송 완료 — 값 제거됨)
# 본인 숫자 ID: @userinfobot 에게 아무 메시지
TELEGRAM_ALLOWED_USERS=7626145305

# Slack (Socket Mode: 토큰 2개 모두 필요)
# OAuth & Permissions > Bot User OAuth Token (xoxb-…)
SLACK_BOT_TOKEN=
# Basic Information > App-Level Tokens (xapp-…, scope: connections:write)
SLACK_APP_TOKEN=
# 본인 Slack 멤버 ID (프로필 > ⋮ > Copy member ID)
SLACK_ALLOWED_USERS=

# 로컬 Obsidian 볼트(위키가 동기화될 폴더) 경로 — 공백 없는 경로 권장
LOCAL_VAULT_PATH=$HOME/HermesWiki

# 설정 후 컨테이너 자동 재시작 여부: yes | ask
RESTART=ask
