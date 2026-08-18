---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/01-ssh-setup.sh"
source_filename: "01-ssh-setup.sh"
source_type: "text"
source_size_bytes: 3767
source_modified_at: "2026-08-12T14:19:56+09:00"
source_sha256: "630c9b0f3d9a884b27f53386c85347db4fd8abe4a9a96e697c493132d47baebd"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# 1단계: SSH 키 생성 → alias 등록 → 접속 확인 → Hermes 탐색 → 관리용 CLAUDE.md 생성
. "$(dirname "$0")/lib.sh"

# 1) SSH 키 (없으면 생성)
KEY="$HOME/.ssh/id_ed25519"
mkdir -p "$HOME/.ssh"; chmod 700 "$HOME/.ssh"
if [ ! -f "$KEY" ]; then
  ssh-keygen -t ed25519 -f "$KEY" -N "" -q
  echo "🔑 새 SSH 키 생성: $KEY"
fi

# 2) VPS IP
VPS_IP="${VPS_IP:-${1:-}}"
if [ -z "$VPS_IP" ]; then
  echo "❌ setup.env 에 VPS_IP 를 채우세요. (setup.env.example 참고)" >&2
  exit 1
fi

# 3) ~/.ssh/config alias 등록 (멱등)
CONF="$HOME/.ssh/config"
touch "$CONF"; chmod 600 "$CONF"
if ! grep -qE "^Host[[:space:]]+$SSH_ALIAS([[:space:]]|\$)" "$CONF"; then
  {
    echo ""
    echo "Host $SSH_ALIAS"
    echo "  HostName $VPS_IP"
    echo "  User root"
    echo "  IdentityFile ~/.ssh/id_ed25519"
    echo "  ServerAliveInterval 30"
  } >> "$CONF"
  echo "📝 SSH alias '$SSH_ALIAS' 등록 ($CONF)"
else
  echo "· SSH alias '$SSH_ALIAS' 이미 있음"
fi

# 4) 접속 테스트 — 실패 시 공개키 등록 안내 후 종료
if ! ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "$SSH_ALIAS" 'echo ok' >/dev/null 2>&1; then
  echo ""
  echo "⛔ 아직 접속이 안 됩니다 — 아래 공개키를 VPS에 등록하세요."
  echo ""
  echo "── 공개키 (한 줄 전체 복사) ─────────────────────"
  cat "$KEY.pub"
  echo "────────────────────────────────────────────────"
  echo ""
  echo "등록: Hostinger 패널 → VPS → Settings → SSH keys → Add SSH key 에 붙여넣기"
  echo "등록 후 이 스크립트를 다시 실행하면 이어서 진행됩니다."
  exit 2
fi
echo "✅ SSH 접속 OK ($SSH_ALIAS → $VPS_IP)"

# 5) Hermes 컨테이너 탐색
discover
echo "✅ 컨테이너: $CONTAINER"
echo "✅ Compose:  $COMPOSE_DIR"

# 6) 현재 폴더에 관리용 CLAUDE.md 생성 (이미 있으면 HERMES-CONNECTION.md 로)
TARGET="./CLAUDE.md"
[ -f "$TARGET" ] && TARGET="./HERMES-CONNECTION.md"
if [ ! -f "$TARGET" ]; then
  cat > "$TARGET" <<EOF
# Hermes Agent 원격 관리

## 접속
\`\`\`bash
ssh $SSH_ALIAS                  # root@$VPS_IP
ssh $SSH_ALIAS '<명령>'          # 비대화식 원커맨드
\`\`\`

## 컨테이너
- 컨테이너명: \`$CONTAINER\`
- Compose 디렉토리: \`$COMPOSE_DIR\`
- 설정 파일: \`$DATA_DIR/config.yaml\` (수정 전 백업 필수)
- 시크릿: \`$DATA_DIR/.env\` (로그·커밋에 노출 금지)
- 영속 데이터: 호스트 \`$DATA_DIR\` ↔ 컨테이너 \`/opt/data\`

## 자주 쓰는 명령
\`\`\`bash
ssh $SSH_ALIAS 'docker logs --since 30m $CONTAINER 2>&1 | tail -200'   # 로그
ssh $SSH_ALIAS 'docker exec -u 10000 $CONTAINER <cmd>'                 # 컨테이너 안 실행
ssh $SSH_ALIAS 'cd $COMPOSE_DIR && docker compose restart'             # 재시작(중단됨, 확인 후)
\`\`\`

## 안전 수칙
- \`/opt/hermes/*\` 는 이미지 레이어라 컨테이너 재생성 시 사라짐 — 영구 변경은 \`/opt/data\` 쪽에.
- 컨테이너 내부 실행은 반드시 \`docker exec -u 10000\` (root 실행 시 파일 소유권 오염).
- stdin 파이프가 필요하면 \`docker exec -i\` (빠뜨리면 무음 실패).
- config.yaml 수정 전: \`cp config.yaml config.yaml.bak.\$(date +%Y%m%d_%H%M%S)\`
- 크론 잡 수정은 \`flock $DATA_DIR/cron/.jobs.lock\` 잡고 jobs.json 편집 (틱마다 재로드, 재시작 불필요).
EOF
  echo "📄 $TARGET 생성 — 이 폴더에서 Claude Code가 Hermes 관리도구로 동작 가능"
else
  echo "· $TARGET 이미 있음 — 건너뜀"
fi

echo ""
echo "다음 단계: bash scripts/02-configure.sh"
