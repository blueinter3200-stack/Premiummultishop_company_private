---
source_path: ".pi/.claude/skills/hermes-vps-setup/SKILL.md"
source_filename: "SKILL.md"
source_type: "text"
source_size_bytes: 9970
source_modified_at: "2026-08-12T14:19:56+09:00"
source_sha256: "b74bc7137382e312c7f522a68e5faf8c6c6d979769d61d9f70270bdb9572bd52"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
---
name: hermes-vps-setup
description: Hostinger VPS의 Hermes 에이전트 초기 셋업 자동화 — SSH 연결, Groq STT/TTS, Composio MCP, 이미지 생성, 위키(세컨브레인) 스캐폴드, Obsidian+Syncthing 양방향 동기화. "헤르메스 셋업", "hermes setup", "헤르메스 설치", "헤르메스 초기설정" 요청 시 사용.
---

# Hermes VPS 셋업

Hostinger 앱 카탈로그로 설치한 Hermes 에이전트를 로컬(맥/윈도우)에서 관리·확장 가능한 상태로 만드는 셋업 스킬. 판단이 필요한 부분만 Claude가 대화로 처리하고, 절차는 전부 멱등 스크립트가 수행한다.

## 전제조건

- Hostinger VPS에 앱 카탈로그로 Hermes agent가 설치·실행 중
- 로컬: 맥 또는 윈도우(Git Bash — Claude Code가 쓰는 셸). `ssh`, `curl` 필요 (윈도우 10+ / 맥 기본 내장)

## 🔒 절대 규칙 (Claude가 반드시 지킬 것)

1. **API 키를 채팅으로 받지 않는다.** 사용자가 키를 채팅에 붙여넣으려 하면 중단시키고 `setup.env` 파일에 적게 안내한다. 키는 `setup.env → ssh stdin` 경로로만 이동하며, 전송 후 파일에서 자동 삭제된다.
2. **키 값을 절대 화면에 출력하지 않는다.** `cat setup.env`, `cat .env` 같은 명령 금지. 확인이 필요하면 키 이름 존재 여부만 grep.
3. **이미 운영 중인 Hermes 인스턴스에는 사용자의 명시적 확인 없이 실행하지 않는다.** 시작 전에 대상 VPS IP를 사용자에게 확인받는다.
4. **컨테이너 재시작은 서비스 중단이다.** 재시작 전 반드시 사용자 동의를 받는다 (`--restart` 플래그가 그 동의의 표현).
5. 스크립트가 실패하면 같은 스크립트를 고쳐서 재실행한다 — 전부 멱등이라 재실행 안전. 스크립트를 우회해 수동 ssh 명령으로 대체하지 않는다.

## 실행 순서

| 단계 | 명령 | Claude가 할 일 | 사용자가 할 일 |
|---|---|---|---|
| 0 | — | `setup.env.example`을 `setup.env`로 복사해 주고 채우게 안내 | VPS IP(필수)·API 키(선택)를 에디터로 입력 |
| 1 | `bash scripts/01-ssh-setup.sh` | 실행. exit 2면 출력된 공개키 등록 안내 후 재실행 | Hostinger 패널 → VPS → SSH keys에 공개키 붙여넣기 |
| 2 | `bash scripts/02-configure.sh` | 실행. 재시작 필요 시 동의 받고 `--restart`로 재실행 | 재시작 동의 |
| 3 | `bash scripts/03-server-syncthing.sh` | 실행 (서버측 위키+Syncthing+워치독 크론) | — |
| 4 | `bash scripts/04-local-setup.sh` | 실행 (로컬 Syncthing·Obsidian 자동 설치+양방향 페어링) | (드물게) 설치 창 확인 |
| 5 | `bash scripts/05-verify.sh` | 실행, 실패 항목 있으면 해당 단계 재실행 | — |
| 6 | — | 아래 "SOUL.md 인터뷰" 진행 | 취향 답변 |

각 스크립트는 끝에서 다음 단계를 안내한다. 항상 스킬 폴더를 기준 디렉토리로 실행할 것.

## 모델 연결 (LLM 프로바이더)

- **1순위: 구독 OAuth** — 사용자가 Hermes 채팅에서 `/auth`로 인증 (ChatGPT·Grok·Copilot 등). 키 파일 불필요.
- **키 경로**: `setup.env`의 모델 프로바이더 키(OpenCode Zen/Go·OpenRouter·Anthropic·Claude 구독 토큰)를 채우고 02단계 실행 — `data/.env`로 전송된다 (전송 후 setup.env에서 값 자동 삭제).
- 이미지 생성: GPT 구독 OAuth가 있으면 자동(gpt-image-2), 없으면 `FAL_KEY`.
- 어느 경로든 하나도 없으면 Hermes가 응답할 모델이 없다 — 05-verify가 경고한다.

## 단계 6: SOUL.md 인터뷰 (스크립트 없음 — Claude의 판단 작업)

`SOUL.md`(호스트 경로: `<COMPOSE_DIR>/data/SOUL.md`)는 Hermes의 성격·운영 원칙 파일이다. 사용자에게 아래를 인터뷰한 뒤 **섹션 단위로 추가**한다 (통째 재작성 금지):

- 호칭·반말/존댓말·언어, 성격 컨셉(차분한 비서/장난기 있는 친구 등), 이모지 사용량
- 주 용도 (일상 비서 / 업무 자동화 / 학습 / 구직 등)

인터뷰 결과로 성격 섹션을 쓰고, 아래 **위키 운영 규칙 블록을 그대로 append**한다:

```markdown
## 위키(세컨브레인) 운영 원칙
- 위키 루트: /opt/data/wiki (index.md가 시작점, 폴더: inbox/profile/logs/areas/projects/concepts/_archive)
- 대화 중 기록 가치가 생기면 그 순간에 해당 폴더에 기록한다. 하루 한 번 몰아 쓰지 않는다.
- 데일리 노트: logs/YYYY-MM/YYYY-MM-DD.md (월별 폴더)
- 같은 내용을 두 곳에 쓰지 않는다 — 겹치면 병합하고 위키링크로 잇는다.
- 경로를 추측하지 말고 index.md 또는 검색으로 찾은 뒤 기록한다.

## 자기 수정 규칙
- SOUL.md는 섹션 단위로만 수정하고 통째로 재작성하지 않는다.
- 파일 편집 후 형식이 깨지지 않았는지(열린 주석 태그 등) 확인한다.
```

편집 방법: `ssh <alias>` 로 호스트에서 직접 편집하거나 heredoc append. 편집 후 `docker logs`로 에러 없는지 확인.

## 보안 노트 (Claude가 사용자에게 필요 시 안내)

- **config.yaml 백업(`config.yaml.bak.*`)에는 Composio 키가 포함된다.** `data/` 디렉토리를 외부에 공유·미러링(레포 업로드 등)하기 전엔 반드시 백업 파일과 `.env`를 제외할 것.
- **SSH 키는 패스프레이즈 없이 생성된다** (자동화 목적). 이 키 파일(`~/.ssh/id_ed25519`)이 곧 VPS root 권한이므로, 로컬 컴퓨터 자체의 잠금·디스크 암호화가 전제다. 사용자가 원하면 패스프레이즈 있는 키를 직접 만들어 써도 된다 (스크립트는 기존 키를 재사용).
- **첫 SSH 접속은 TOFU**(`accept-new`) — 최초 1회는 호스트 지문을 자동 신뢰한다. 민감한 사용자는 Hostinger 패널의 호스트 키 지문과 대조 가능.
- **Syncthing/Obsidian 바이너리는 GitHub 공식 릴리스에서 HTTPS로 받는다** (체크섬 검증은 생략 — brew/winget과 동일한 신뢰 수준). 위키 동기화는 Syncthing 기기 ID(인증서 기반) 상호 등록이라 제3자가 끼어들 수 없다.
- 서버 Syncthing GUI는 컨테이너 내부 127.0.0.1 전용, 로컬 GUI도 127.0.0.1 전용 — 외부 노출 없음.

## 트러블슈팅

| 증상 | 원인/처치 |
|---|---|
| `docker exec` 파이프가 조용히 실패 | `-i` 플래그 누락 — stdin 쓰는 exec엔 반드시 `-i` |
| 컨테이너 안 파일이 root 소유가 됨 | `docker exec -u 10000` 안 씀 — 반드시 `-u 10000`, 오염 시 `chown -R 10000:10000` |
| config.yaml 수정 후 Hermes 이상 | 스크립트가 만든 `config.yaml.bak.*` 복원 후 재시작 |
| 크론이 반영 안 됨 | jobs.json은 틱마다 재로드 — 재시작 불필요. 편집은 반드시 `flock <data>/cron/.jobs.lock` 하에 |
| `/opt/hermes/` 수정이 사라짐 | 이미지 레이어라 재생성 시 휘발 — 영구 변경은 `/opt/data`(호스트 `<COMPOSE_DIR>/data`) 쪽에만 |
| Syncthing 페어링 됐는데 동기화 안 됨 | 양쪽 재시작 대기(1~2분). 로컬 GUI `http://127.0.0.1:8384`에서 상태 확인 |
| 윈도우에서 경로 문제 | Git Bash 경로(`/c/...`)와 네이티브 경로(`C:\...`) 혼용 — 스크립트가 `cygpath`로 변환하므로 수동 개입 시에만 주의 |
| STT가 안 됨 | 02단계 후 재시작했는지 확인 → `05-verify.sh`로 stt 활성 여부 점검. 02가 Groq 키 유효성을 즉시 검증하므로 키 오타는 그 시점에 잡힘 |
| 크론/알림 메시지가 안 옴 | `DISCORD_HOME_CHANNEL` 미설정 — setup.env에 채우고 02 재실행+재시작. 채널 ID는 디스코드 개발자 모드 → **채널**(스레드 아님) 우클릭 → ID 복사 |
| 재시작 후 게이트웨이가 안 뜸 | `data/.env`·`data/logs/*`가 root 소유(호스트에서 root로 파일을 만졌을 때) — Hermes(uid 10000)가 못 읽어 기동 실패. 02 재실행(소유권 스윕) 후 재시작. 05-verify가 감지함 |
| 웹 검색이 갑자기 다른 엔진/실패로 바뀜 | 컨테이너 **재생성**(업데이트 등)으로 ddgs 패키지 소실 — 02 재실행이면 재설치+복구. `web.backend: ddgs` 설정 자체는 볼륨이라 살아 있음 |
| 크론이 9시간 어긋난 시각에 돎 | `timezone: Asia/Seoul` 미설정(UTC 해석) — 02 재실행 후 재시작. 05-verify가 검사함 |
| 동기화 충돌 사본(`파일 2.md`) 생김 | 서버가 쓰는 동안 로컬에서 같은 파일 편집 — `.stignore`가 워크스페이스 노이즈는 막지만 같은 노트 동시 편집은 못 막음. 충돌 사본 발견 시 내용 비교 후 병합·삭제 |

## 파일 구조

```
hermes-vps-setup/
├── SKILL.md                      # 이 문서
├── README.txt                    # 받은 사람용 안내 (설치 위치·시작 방법)
├── setup.env.example             # 설정 템플릿 (setup.env로 복사해 사용)
└── scripts/
    ├── lib.sh                    # 공용 함수 (OS 감지·VPS 탐색·Syncthing 헬퍼)
    ├── 01-ssh-setup.sh           # SSH 키·alias·접속 확인·관리용 CLAUDE.md
    ├── 02-configure.sh           # 시크릿 주입 + config 패치(웹검색 ddgs 포함) + 소유권 스윕 (+재시작)
    ├── 03-server-syncthing.sh    # 서버: 위키 스캐폴드 + Syncthing + 워치독 크론
    ├── 04-local-setup.sh         # 로컬: Syncthing·Obsidian 설치 + 자동 페어링
    ├── 05-verify.sh              # 전체 검증
    └── remote/                   # VPS에서 실행되는 헬퍼 (스크립트가 자동 업로드)
        ├── env_set.py            # .env 키 설정 (값은 stdin으로만)
        ├── patch_config.py       # config.yaml 점 경로 패치
        ├── st_pair.py            # 서버 Syncthing 기기 등록+폴더 공유
        └── syncthing-watchdog.sh # 5분 간격 Syncthing 생존 감시
```
