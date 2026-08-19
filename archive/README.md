# Archive / Legacy Import Note

## 2026-08-18 import

과거 `_markdown/` 아래에는 약 488개 원본을 Markdown으로 변환한 대규모 import가 들어왔습니다.

해당 import에는 다음이 혼합되어 있었습니다.

- BusinessVault 사업 자료
- HermesWiki 일지
- Claude 원시 대화/상태
- 브라우저/Chromium 캐시와 바이너리 메타데이터
- Intel 설치 로그
- Obsidian 플러그인 파일
- nested `.git` 메타데이터
- SSH/인증/환경 관련 민감 가능 자료
- 중복 변환 자료

## 현재 보존한 것

사업적으로 다시 참고할 가치가 높은 `BusinessVault`의 핵심 문서만 현재 트리의 `archive/business-vault/` 아래에 보존했습니다.

보존 범위:

- `index.md`
- `04-decision-log.md`
- `07-project-tracker.md`
- `ideas/`
- `market/`
- `plans/`
- `research/`

이 자료는 **legacy/reference only**이며 현재 회사 OS 정본을 자동으로 덮어쓰지 않습니다.

## 제거한 것

현재 작업 트리에서는 cache, logs, raw Claude state/conversations, SSH/credential 관련 변환물, plugin runtime files, nested git metadata, 중복 사업자료 등을 제거했습니다.

Git history는 보존되어 있으므로 과거 commit 자체는 남아 있습니다. 과거 이력에 포함된 민감자료의 완전 제거/history rewrite와 자격증명·키 회전은 별도 보안 작업입니다.
