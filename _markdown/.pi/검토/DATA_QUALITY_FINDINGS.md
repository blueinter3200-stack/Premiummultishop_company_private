---
source_path: ".pi/검토/DATA_QUALITY_FINDINGS.md"
source_filename: "DATA_QUALITY_FINDINGS.md"
source_type: "text"
source_size_bytes: 10224
source_modified_at: "2026-08-17T18:43:40+09:00"
source_sha256: "8d8bd2b483daf97cf594f06b104aaff2b689ade3e924b847f8a424324bfbcf2b"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 데이터 품질 발견사항

## 요약

핵심 사업 문서의 내용 중복은 생각보다 심하지 않다. 품질 문제의 중심은 **앱 자산의 대량 중복, 불완전한 링크·경로, 정본 관계 누락, 헤딩 경계 붕괴, 민감한 비코퍼스 혼입**이다.

## 정확한 중복

SHA-256 기준으로 25개 중복 그룹, 54개 파일이 중복 그룹에 속한다. 한 그룹당 한 사본만 남긴다고 가정한 중복 용량은 9,228,681바이트다. 삭제를 수행하지 않았다.

### 주요 중복군

| 중복군 | 위치 | 판정 |
| --- | --- | --- |
| TaskNotes 기본 뷰 7개 | `BusinessVault/TaskNotes/Views/`, `HermesWiki/TaskNotes/Views/` | 의도적 볼트별 복제로 보임 |
| TaskNotes 안내 | 두 볼트의 `TaskNotes/Start Here.md` | 정확한 중복, 앱 안내 |
| Dataview 플러그인 | 두 볼트 `.obsidian/plugins/dataview/` | 정확한 앱 번들 복제 |
| Obsidian Tasks 플러그인 | 두 볼트 `.obsidian/plugins/obsidian-tasks-plugin/` | 정확한 앱 번들 복제 |
| TaskNotes 플러그인 | 두 볼트 `.obsidian/plugins/tasknotes/` | 정확한 앱 번들 복제 |
| Obsidian core/community 설정 일부 | 두 볼트 `.obsidian/` | 독립 볼트 설정 복제 |
| `.stignore` | 두 볼트 | 동일 동기화 제외 규칙 |
| 셸 스냅샷 2개 | `.claude/shell-snapshots/` | 정확한 중복 |
| 0바이트 파일 4개 | 아래 빈 파일 목록 | 내용 없음의 동일 해시일 뿐 의미 중복 아님 |

핵심 사람이 읽는 Markdown에서 내용이 있는 정확한 중복은 두 TaskNotes 안내 파일뿐이다. BusinessVault의 사업 문서끼리 완전히 같은 파일은 발견되지 않았다.

## 가능성이 높은 근접 중복·중첩

정확한 복사는 아니지만 같은 개념을 다른 버전·요약 단계에서 반복한다.

### 버전 계열

- `pms-9-agent-revenue-commerce-os-v1-2026-08-15.md`
- `pms-revenue-commerce-os-v2-master-2026-08-15.md`
- `pms-revenue-commerce-os-v3-2026-08-14.md`
- `pms-revenue-commerce-os-v3-canonical-2026-08-16.md`

삭제 후보가 아니라 정본·이력 관계를 붙일 대상이다.

### Revenue Ladder 계열

- `pms-revenue-ladder-level0-level4-v1-2026-08-15.md`
- `pms-revenue-ladder-profitability-redesign-v2-2026-08-16.md`

v2가 v1을 보완하거나 교체한 것으로 보이지만 직접적인 `supersedes` 필드가 없어 확인이 필요하다.

### 인덱스 쌍

- `ideas/belloon.md`와 `ideas/belloon/index.md`
- `ideas/premium-multishop.md`와 하위 index
- `market/belloon.md`와 하위 index
- `market/premium-multishop.md`와 하위 index

본문 중복보다 역할 중복이다. 하나의 인덱스로 논리 병합하는 것이 좋다.

### 요약 계층 중첩

조사 보고서의 결론이 plans, 결정 로그, 프로젝트 추적기, 일일기록에 반복된다. 이는 목적상 유용하지만 파생 관계가 없으면 AI가 다섯 개의 독립 근거로 계산할 수 있다.

### 도구 산출물과 사업 문서

`Claude/Projects/...docx`의 상세페이지 신뢰·반품·배송·USP 주제는 8월의 상세페이지·신뢰 문서와 겹친다. `Claude/Artifacts/...html`의 구매대행·면세 모델은 이후 홍콩 보세·리셀 수익성 검토와 겹친다. 과거 자료인지 현재 제안인지 표시가 필요하다.

## 빈 파일과 비정상적으로 작은 파일

### 0바이트 4개

- `.claude/tasks/.../.lock`: 정상적인 빈 잠금 파일일 수 있음
- `.hermes-sync/home/.syncthing.tmp.780941286`: 임시 파일
- `BusinessVault/2026-08-14.md`: 코퍼스 안의 빈 날짜 파일
- `BusinessVault/무제.md`: 코퍼스 안의 빈 무제 파일

마지막 두 개는 의미가 없고 탐색을 방해하지만 감사에서는 삭제하지 않았다.

### 2바이트 JSON

두 볼트의 `.obsidian/app.json`, `appearance.json`은 `{}`만 가진 정상적인 빈 설정이다.

## 비정상적으로 큰 파일

### 코퍼스 밖

- `.cache/.../interactive_ui_tests.exe`: 약 216MB
- `.cache/.../chrome.dll`: 약 206MB
- `.hermes-sync/bin/syncthing.exe`: 약 27.7MB
- 두 볼트의 TaskNotes `main.js`: 각각 약 5.2MB
- Hermes 설치 PDF: 약 5MB

### 사람이 읽는 Markdown

- `BusinessVault/04-decision-log.md`: 32,799바이트
- `BusinessVault/research/belloon-buyer-person-sourcing-2026-08-12.md`: 27,450바이트
- `BusinessVault/plans/premium-multishop-ecommerce-transition.md`: 20,353바이트

크기 자체는 문제 아니지만 결정 로그는 의미 경계가 깨졌고, 인물 소싱 문서는 갱신형 레코드 분리를 고려할 만하다.

## 인코딩

비밀 가능 파일을 제외한 텍스트형 파일 194개를 엄격 UTF-8로 검사했다.

- 핵심 BusinessVault/HermesWiki Markdown: UTF-8 오류 없음
- UTF-8이 아닌 파일 3개: `Favorites/desktop.ini`, Intel MSI 로그 2개
- 대체 문자 U+FFFD가 있는 파일 1개: `.claude/projects/...Hermes-Manage....jsonl`
- BOM은 발견되지 않음

UTF-8 문제는 핵심 코퍼스가 아니라 OS·대화 상태에 국한된다.

## 링크와 누락 참조

### BusinessVault 내부 링크

단순 Obsidian 링크 해석 검사에서 148개 중 145개가 현재 파일로 해석됐다. 해석되지 않은 3개는 폴더 이름을 파일처럼 링크한 `research`, `plans`, `../research`다. 폴더용 `index.md`와 정확한 링크를 두는 편이 안전하다.

### HermesWiki 링크

25개 중 20개가 현재 HermesWiki 안에서 해석되지 않았다.

- 비어 있는 `inbox`, `profile`, `logs`, `areas`, `projects`, `concepts`, `_archive`
- `business-wiki/...` 교차 볼트 경로
- 파일명만 적은 BusinessVault 문서 링크

Obsidian에서 볼트를 별도로 열면 교차 볼트 링크가 자동 해결되지 않는다. 로컬 별칭 또는 안정적 문서 ID가 필요하다.

### 현재 컬렉션에 없는 중요 자료

- `/opt/data/Premium_MultiShop_Revenue_SEO_Workbook_v2.xlsx`
- `/opt/data/Premium_MultiShop_Revenue_SEO_Workbook_v3_Architecture.xlsx`
- `/opt/data/premium_multishop_competitor_benchmark_2026-08-15.md`
- `/opt/data/skills/business/belloon-global-beauty/SKILL.md`
- `/opt/data/skills/business/belloon-global-beauty/scripts/margin_check.py`
- `/opt/data/skills/business/premium-multishop/SKILL.md`

이 자료가 실제로 존재하지만 현재 복사본에 빠진 것인지, 과거 경로인지 `Needs verification`이다.

## 헤딩과 구조 불일치

### 결정 로그

`BusinessVault/04-decision-log.md`의 첫 H2 아래 다수의 서로 다른 결정이 이어진다. BELLOON 결정도 PMS 헤딩 아래 들어 있다. 결정별 제목·ID·날짜가 없어 사람과 AI 모두 경계를 잃는다.

### 템플릿 잔존

같은 파일에 `## YYYY-MM-DD | 결정 제목` 템플릿이 실데이터 사이에 남아 있다.

### 인덱스 최신성

`BusinessVault/market/premium-multishop/index.md`는 별도 시장 자료가 없다고 쓰지만 `BusinessVault/research/`에는 여러 PMS 시장·경쟁·공급망 파일이 있다.

### 경로 규칙

- Hermes 표준 안내: `logs/YYYY-MM/`
- 실제 일지: `journal/YYYY-MM/`
- Business 보관: `_archiv/`와 `_archive/`
- 서버 경로: `business-wiki/`
- 로컬 폴더: `BusinessVault/`

## 메타데이터 일관성

비어 있지 않은 주요 사업 문서 55개 기준이다.

| 항목 | 보유 문서 수 | 평가 |
| --- | ---: | --- |
| H1 | 54 | 매우 양호 |
| YAML frontmatter | 0 | 공통 기계 인덱싱에는 불리 |
| 날짜 필드 | 38 | 부분적 |
| 상태 필드 | 28 | 부족 |
| 사업 필드 | 24 | 부족 |
| Sources/출처 헤딩 | 10 | 조사 문서 외에는 불균일 |
| 위키링크 포함 | 20 | 핵심 관계는 있으나 전체적이지 않음 |

모든 필드를 강제하기보다 `document_id`, `business`, `document_role`, `date`, `status`, 버전 관계를 우선해야 한다.

## 이름 규칙

### 좋은 점

- 날짜는 주로 `YYYY-MM-DD`
- 영문 슬러그가 안정적
- PMS, Premium MultiShop, BELLOON 접두사가 내용 구분에 도움
- v1/v2/v3, canonical 표기가 있음

### 문제

- `pms-`와 `premium-multishop-`가 같은 사업에서 혼용됨
- 57개 주요 BusinessVault 파일 중 38개만 날짜가 파일명에 있음
- `index.md`가 9개라 경로 없이는 의미가 없음
- 숫자 접두사 `04`, `07`의 전체 번호 체계가 보이지 않음
- `_archiv` 철자와 `_archive`가 공존
- `log.md`가 변경 로그인지 일지인지 이름만으로 불명확

## 잘못 분류되거나 혼합된 내용

- `plans/`: 리뷰·감사·프롬프트·계약 포함
- `research/belloon-linkedin-sourcing-ops.md`: 운영 절차 포함
- 결정 로그 첫 섹션: PMS와 BELLOON 결정 혼합
- `Claude/`: 사업 산출물이 도구 이름 아래 고립
- `.claude/`: 재사용 스킬과 자격증명·대화 원장이 함께 있음

## 개인정보·보안 경계

다음은 코퍼스 품질 이전에 색인 금지 대상이다. 내용은 보고서에 복사하지 않았다.

- `.ssh/id_ed25519`
- `.claude/.credentials.json`
- `.claude/skills/hermes-vps-setup/setup.env`
- `.hermes-sync/home/key.pem`과 인증서·설정
- `.claude/backups/*`
- `.claude/projects/**/*.jsonl`: 개인 대화, 도구 입력·출력, 외부 경로가 포함될 수 있음

AI 코퍼스 수집기는 allowlist 방식으로 `knowledge-corpus/`만 읽어야 한다. exclude 패턴에만 의존하면 새 비밀 파일을 놓칠 수 있다.

## 의심되는 잘림·손상

- 핵심 Markdown에서 파일 중간 잘림이나 비정상 인코딩은 확인되지 않았다.
- 0바이트 BusinessVault 파일 2개는 손상인지 빈 노트 생성 흔적인지 확인 필요하다.
- `.claude` JSONL 1개에는 대체 문자가 있어 완전한 이벤트 복원이 어려울 수 있다.
- DOCX는 전체 문단·표 추출에 성공했다. LibreOffice 부재로 레이아웃 렌더링은 확인하지 못했다.
- PDF는 9페이지 전부 렌더링됐고 읽을 수 있었다.

## 삭제 전 주의

이 감사는 중복을 삭제하라는 의미가 아니다. 특히 Obsidian 플러그인·TaskNotes 중복은 각 볼트의 독립 실행을 위한 복제일 수 있다. 먼저 색인 제외만 적용하고, 용량 최적화는 별도 운영 결정으로 다룬다.

