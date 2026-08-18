---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/03-server-syncthing.sh"
source_filename: "03-server-syncthing.sh"
source_type: "text"
source_size_bytes: 5519
source_modified_at: "2026-08-12T16:08:32+09:00"
source_sha256: "558031c2ae40a5dc82de4e76a64852ff54e949494e270fa83a8ca771c132d2e5"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env bash
# 3단계: 서버(VPS)측 — 위키 스캐폴드 + Syncthing 설치 + 워치독 크론 등록
. "$(dirname "$0")/lib.sh"
discover
echo "▶ 대상: $CONTAINER"

# 1) 위키 스캐폴드 (있으면 건너뜀)
hssh "bash -s" <<EOF
set -e
W="$DATA_DIR/wiki"
mkdir -p "\$W/inbox" "\$W/profile" "\$W/logs" "\$W/areas" "\$W/projects" "\$W/concepts" "\$W/_archive"
if [ ! -f "\$W/index.md" ]; then
  cat > "\$W/index.md" <<'MD'
# 📚 Wiki Index

세컨브레인의 시작점. Hermes가 대화 중 기록 가치가 생기면 즉시 해당 폴더에 기록한다.

- [[inbox]] — 미분류 수신함 (웹클립·메모·아이디어)
- [[profile]] — 나에 대한 정보 (성향·이력·선호)
- [[logs]] — 데일리 노트 (월별 폴더: logs/YYYY-MM/YYYY-MM-DD.md)
- [[areas]] — 일상 관리 영역 (건강·재정·관계 등, 영역당 파일 1개)
- [[projects]] — 진행 중인 일 (프로젝트당 파일 1개)
- [[concepts]] — 배운 것·개념 정리
- [[_archive]] — 끝난 것 보관

## 규칙
- 폴더를 늘리기 전에 파일 하나로 시작한다 (200줄 넘으면 분할).
- 같은 내용을 두 곳에 쓰지 않는다 — 겹치면 병합하고 링크로 잇는다.
MD
fi
if [ ! -f "\$W/.stignore" ]; then
  printf '(?d).obsidian/workspace*\n(?d).trash/\n(?d).DS_Store\n(?d)Thumbs.db\n' > "\$W/.stignore"
fi
chown -R 10000:10000 "\$W"
echo "✅ 위키 스캐폴드: \$W"
EOF

# 2) Syncthing 바이너리 설치 (VPS, /opt/data 영속 영역 — 재빌드 안전)
hssh "bash -s" <<EOF
set -e
BIN="$DATA_DIR/.local/bin/syncthing"
if [ -x "\$BIN" ]; then echo "· syncthing 바이너리 이미 있음"; exit 0; fi
mkdir -p "$DATA_DIR/.local/bin"
case "\$(uname -m)" in
  x86_64) A=amd64 ;;
  aarch64) A=arm64 ;;
  *) echo "지원하지 않는 아키텍처: \$(uname -m)"; exit 1 ;;
esac
TAG=\$(curl -fsSL https://api.github.com/repos/syncthing/syncthing/releases/latest | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' | head -1)
[ -n "\$TAG" ] || { echo "syncthing 최신 버전 조회 실패"; exit 1; }
cd /tmp
curl -fsSL -o st.tgz "https://github.com/syncthing/syncthing/releases/download/\$TAG/syncthing-linux-\$A-\$TAG.tar.gz"
tar xzf st.tgz
cp "syncthing-linux-\$A-\$TAG/syncthing" "\$BIN"
rm -rf st.tgz "syncthing-linux-\$A-\$TAG"
chown -R 10000:10000 "$DATA_DIR/.local"
echo "✅ syncthing \$TAG 설치"
EOF

# 3) Syncthing 초기 설정 생성 (컨테이너 안, uid 10000 — 소유권 오염 방지)
# Syncthing v2는 generate에서 --no-default-folder 플래그를 제거함 → 플래그 없이 생성 후 기본 폴더 제거
hssh "docker exec -i -u 10000 $CONTAINER bash -s" <<'EOF'
CFG=/opt/data/.config/syncthing/config.xml
if [ ! -f "$CFG" ]; then
  /opt/data/.local/bin/syncthing generate --home=/opt/data/.config/syncthing >/dev/null 2>&1
  sed -i '/<folder /,/<\/folder>/d' "$CFG"
fi
EOF
echo "✅ syncthing 설정 준비"

# 4) 워치독 스크립트 설치
hssh "mkdir -p $DATA_DIR/scripts"
scp -q "$SKILL_DIR/scripts/remote/syncthing-watchdog.sh" "$SSH_ALIAS:$DATA_DIR/scripts/"
hssh "chmod +x $DATA_DIR/scripts/syncthing-watchdog.sh && chown 10000:10000 $DATA_DIR/scripts/syncthing-watchdog.sh"

# 5) 워치독 크론 등록 (flock 하에 jobs.json 편집 — 틱마다 재로드라 재시작 불필요)
hssh "python3 - $DATA_DIR/cron/jobs.json" <<'PY'
import datetime
import fcntl
import json
import os
import secrets
import sys

path = sys.argv[1]
os.makedirs(os.path.dirname(path), exist_ok=True)
if not os.path.exists(path):
    with open(path, "w") as f:
        f.write('{"jobs": []}')
lock = open(os.path.join(os.path.dirname(path), ".jobs.lock"), "w")
fcntl.flock(lock, fcntl.LOCK_EX)
with open(path) as f:
    data = json.load(f)
jobs = data["jobs"] if isinstance(data, dict) else data
if any(j.get("name") == "syncthing-watchdog" for j in jobs):
    print("· 워치독 크론 이미 등록됨")
    sys.exit(0)
jobs.append({
    "id": secrets.token_hex(6),
    "name": "syncthing-watchdog",
    "prompt": "script-only watchdog for Syncthing wiki sync",
    "skills": [], "skill": None, "model": None, "provider": None,
    "provider_snapshot": None, "model_snapshot": None, "base_url": None,
    "script": "syncthing-watchdog.sh",
    "no_agent": True, "context_from": None,
    "schedule": {"kind": "interval", "minutes": 5, "display": "every 5m"},
    "schedule_display": "every 5m",
    "repeat": {"times": None, "completed": 0},
    "enabled": True, "state": "scheduled",
    "paused_at": None, "paused_reason": None,
    "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "next_run_at": None, "last_run_at": None,
    "last_status": None, "last_error": None, "last_delivery_error": None,
    "deliver": "local", "origin": None, "enabled_toolsets": None,
    "workdir": None, "fire_claim": None,
})
with open(path, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("✅ syncthing-watchdog 크론 등록 (5분 간격)")
PY

# 6) 지금 바로 기동 + 서버 기기 ID 출력
hssh "docker exec -u 10000 -d $CONTAINER bash /opt/data/scripts/syncthing-watchdog.sh" || true
sleep 3
SERVER_ID="$(hssh "sed -n 's/.*<device id=\"\([A-Z0-9-]*\)\".*/\1/p' $DATA_DIR/.config/syncthing/config.xml | head -1")"
echo ""
echo "✅ 서버 Syncthing 준비 완료"
echo "   서버 기기 ID: ${SERVER_ID:-'(config.xml 생성 대기 — 잠시 후 05-verify.sh로 확인)'}"
echo ""
echo "다음 단계: bash scripts/04-local-setup.sh   (내 컴퓨터에 Syncthing·Obsidian 설치 + 자동 페어링)"
