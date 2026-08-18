---
source_path: ".pi/.claude/skills/hermes-vps-setup/CLAUDE.md"
source_filename: "CLAUDE.md"
source_type: "text"
source_size_bytes: 1473
source_modified_at: "2026-08-12T15:41:08+09:00"
source_sha256: "734c441e9916710bb3bb7a574c9e8c2390df0aee7c50344e38fa2f8573c11456"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# Hermes Agent 원격 관리

## 접속
```bash
ssh hermes                  # root@187.52.115.143
ssh hermes '<명령>'          # 비대화식 원커맨드
```

## 컨테이너
- 컨테이너명: `hermes-agent-0cmi-hermes-agent-1`
- Compose 디렉토리: `/docker/hermes-agent-0cmi`
- 설정 파일: `/docker/hermes-agent-0cmi/data/config.yaml` (수정 전 백업 필수)
- 시크릿: `/docker/hermes-agent-0cmi/data/.env` (로그·커밋에 노출 금지)
- 영속 데이터: 호스트 `/docker/hermes-agent-0cmi/data` ↔ 컨테이너 `/opt/data`

## 자주 쓰는 명령
```bash
ssh hermes 'docker logs --since 30m hermes-agent-0cmi-hermes-agent-1 2>&1 | tail -200'   # 로그
ssh hermes 'docker exec -u 10000 hermes-agent-0cmi-hermes-agent-1 <cmd>'                 # 컨테이너 안 실행
ssh hermes 'cd /docker/hermes-agent-0cmi && docker compose restart'             # 재시작(중단됨, 확인 후)
```

## 안전 수칙
- `/opt/hermes/*` 는 이미지 레이어라 컨테이너 재생성 시 사라짐 — 영구 변경은 `/opt/data` 쪽에.
- 컨테이너 내부 실행은 반드시 `docker exec -u 10000` (root 실행 시 파일 소유권 오염).
- stdin 파이프가 필요하면 `docker exec -i` (빠뜨리면 무음 실패).
- config.yaml 수정 전: `cp config.yaml config.yaml.bak.$(date +%Y%m%d_%H%M%S)`
- 크론 잡 수정은 `flock /docker/hermes-agent-0cmi/data/cron/.jobs.lock` 잡고 jobs.json 편집 (틱마다 재로드, 재시작 불필요).
