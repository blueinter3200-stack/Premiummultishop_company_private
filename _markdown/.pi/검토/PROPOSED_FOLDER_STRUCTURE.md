---
source_path: ".pi/검토/PROPOSED_FOLDER_STRUCTURE.md"
source_filename: "PROPOSED_FOLDER_STRUCTURE.md"
source_type: "text"
source_size_bytes: 8567
source_modified_at: "2026-08-17T18:43:40+09:00"
source_sha256: "746019c5b515ade28fbb925eb0f3fe71c2addd4b77ec4d4592f86cf4bc0ce39a"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 권장 폴더 구조

## 전체 구조

```text
reorganized-workspace/
├─ knowledge-corpus/
│  ├─ README.md
│  ├─ _metadata/
│  │  ├─ document-index.jsonl
│  │  ├─ relationships.jsonl
│  │  └─ collection-rules.md
│  ├─ business/
│  │  ├─ premium-multishop/
│  │  │  ├─ index.md
│  │  │  ├─ 01-evidence-and-research/
│  │  │  │  ├─ source-artifacts/
│  │  │  │  ├─ market-and-sourcing/
│  │  │  │  └─ feasibility-and-audits/
│  │  │  ├─ 02-decisions/
│  │  │  ├─ 03-strategy-and-design/
│  │  │  ├─ 04-execution/
│  │  │  ├─ 05-reference-and-templates/
│  │  │  └─ 99-history/
│  │  ├─ belloon/
│  │  │  ├─ index.md
│  │  │  ├─ 01-evidence-and-research/
│  │  │  │  ├─ research-snapshots/
│  │  │  │  ├─ company-leads/
│  │  │  │  └─ people-leads/
│  │  │  ├─ 02-decisions/
│  │  │  ├─ 03-strategy-and-design/
│  │  │  ├─ 04-execution/
│  │  │  ├─ 05-reference-and-templates/
│  │  │  └─ 99-history/
│  │  └─ shared/
│  │     ├─ governance/
│  │     ├─ contracts/
│  │     └─ portfolio-tracking/
│  ├─ personal/
│  │  ├─ index.md
│  │  ├─ journal/YYYY-MM/
│  │  ├─ inbox/
│  │  ├─ profile/
│  │  ├─ areas/
│  │  ├─ projects/
│  │  ├─ concepts/
│  │  └─ archive/
│  └─ _derived-index/
│     ├─ chunks/
│     ├─ embeddings/
│     └─ build-manifest.json
├─ ai-operating-assets/
│  ├─ marketing-skills/
│  └─ hermes-vps-setup/
├─ app-state-no-index/
│  ├─ obsidian-vault-state/
│  ├─ tasknotes-views/
│  ├─ conversation-history/
│  └─ sync-state/
├─ machine-cache-no-index/
│  ├─ browser-runtime/
│  └─ installer-logs/
└─ private-credentials-no-index/
   └─ README-security-boundary.md
```

`private-credentials-no-index/`는 개념적 경계다. 실제 키와 자격증명은 이 재구성된 공유 워크스페이스 밖의 OS 보안 위치에 두는 것을 권장한다.

## knowledge-corpus/

사람이 읽고 AI가 사실·판단 검색에 사용할 정본 문서만 둔다. 앱 플러그인, 대화 원장, 실행 파일, 키는 넣지 않는다.

## knowledge-corpus/_metadata/

문서 ID, 사업, 역할, 상태, 버전 관계, 현재 경로를 보관한다. 본문을 중복 저장하지 않는다. 인간은 `collection-rules.md`를 보고 어떤 자료가 검색 대상인지 이해할 수 있다.

## business/premium-multishop/

Premium MultiShop 자료만 둔다. BELLOON 화장품 자료를 넣지 않는다.

### 01-evidence-and-research/

조사 당시 근거와 검토 보고서가 들어간다.

- `source-artifacts/`: DOCX·HTML·이미지 등 로컬 산출물 원형
- `market-and-sourcing/`: 시장, 경쟁사, 채널, 공급망 조사
- `feasibility-and-audits/`: 리셀·구매대행·YesStyle·SEO·수익성 검토

확정 전략이나 실행 체크리스트는 넣지 않는다.

### 02-decisions/

대표가 확정한 결정 또는 중단·보류 판정을 한 건씩 둔다. 단순 검토안은 넣지 않는다. 전체 인덱스는 날짜·ID·상태·근거 링크를 제공한다.

### 03-strategy-and-design/

현재 사업 구조, 데이터 구조, Agent 구조, 수익 구조, 통합 아키텍처를 둔다. 기본 검색은 `status: canonical|active`만 사용하고 과거 버전은 `99-history/`로 보낸다.

### 04-execution/

로드맵, 프로젝트 추적, D+7/D+14/D+30 테스트, 담당·마감·KPI가 있는 자료를 둔다. 아이디어와 장기 설계는 넣지 않는다.

### 05-reference-and-templates/

상세페이지 프롬프트, 운영 체크리스트, 반복 사용 스키마 등 실행을 돕는 템플릿을 둔다. 사업 사실의 정본으로 색인하지 않고 참조 인덱스로 분리할 수 있다.

### 99-history/

v1·v2·비정본 초안, 교체된 전략, 과거 보고서를 보존한다. 삭제하지 않는다. 기본 RAG 검색에서는 제외한다.

## business/belloon/

BELLOON의 화장품 B2B, OEM·ODM, 브랜드 수권 자료만 둔다.

`research-snapshots/`는 조사 당시 보고서를 보존하고, `company-leads/`와 `people-leads/`는 갱신 가능한 개별 레코드다. 사람과 회사를 한 파일에 섞지 않는 기존 운영 표준을 그대로 살린다.

## business/shared/

두 사업 모두에 적용되는 규칙만 둔다.

- `governance/`: 승인, 검증, 공통 의사결정 규칙
- `contracts/`: 계약 상태 원장. 사업별 항목에는 business 필드 필수
- `portfolio-tracking/`: 전사 프로젝트 인덱스와 사업 간 우선순위

Premium MultiShop에만 적용되는 문서를 편의상 넣지 않는다.

## personal/

개인·일상 위키다. 사업 사실을 본문에 다시 복사하지 않고 안정적인 사업 문서 ID로 링크한다. 일지 표준 폴더는 `journal/` 또는 `logs/` 중 사용자 결정 후 하나만 사용한다. 이 제안은 현재 실제 파일이 있는 `journal/`을 기본값으로 추천한다.

## _derived-index/

사람이 직접 편집하지 않는 검색 파생물이다. 정본 문서에서 언제든 재생성할 수 있어야 한다.

- `chunks/`: 헤딩 기반 텍스트 청크
- `embeddings/`: 벡터 인덱스 또는 포인터
- `build-manifest.json`: 생성 시각, 모델, 소스 해시, 제외 규칙

원본 Markdown을 이 폴더로 옮기지 않는다.

## ai-operating-assets/

AI의 행동 지침과 설치 패키지다. 사업 지식과 별도 인덱스를 사용한다.

- `.agents/skills/*`는 `marketing-skills/`
- `.claude/skills/hermes-vps-setup/`은 패키지 전체를 `hermes-vps-setup/`

채워진 환경 파일, 자격증명, 개인키는 포함하지 않는다.

## app-state-no-index/

Obsidian 설정, TaskNotes 뷰, Claude 대화 JSONL, Syncthing 상태처럼 앱이 필요로 하지만 사실 검색에는 부적합한 자료다. 보존·백업 정책은 둘 수 있으나 AI 색인 대상이 아니다.

## machine-cache-no-index/

Chromium, Syncthing 실행 파일, Intel 설치 로그 같은 재생성 가능한 시스템 파일이다. 문서 백업과 코퍼스 통계에서 제외한다.

## private-credentials-no-index/

SSH 개인키, `.credentials.json`, `setup.env`, Syncthing 키가 속하는 보안 경계다. 실제 값은 공유 문서 루트 밖에 두고 OS 권한·비밀 저장소로 관리한다.

## Keep

- 두 사업을 섞지 않는 원칙
- 조사일·상태·검증 한계·출처
- 날짜 기반 영문 슬러그 파일명
- 일일기록의 YAML과 날짜별 1파일
- H2/H3 의미 구조
- 정본 `canonical` 표기
- Obsidian 볼트 독립성이 필요할 때 볼트별 설정

## Rename

- `BusinessVault` → `knowledge-corpus/business`의 의미 있는 하위 구조로 개념 변경
- `HermesWiki/journal` 또는 `logs` 중 하나로 표준화. 기본 추천은 실제 자료가 있는 `journal`
- `_archiv`와 `_archive` → `archive` 하나로 통일
- `Claude/` → 생성 도구명이 아니라 해당 사업의 `source-artifacts` 또는 `history`

## Move

- `plans/*review*.md`, `*audit*.md` → `01-evidence-and-research/feasibility-and-audits`
- 현재 전략·아키텍처 → `03-strategy-and-design`
- 로드맵·추적기 → `04-execution`
- 프롬프트·운영 스키마 → `05-reference-and-templates`
- 과거 버전 → `99-history`
- `.agents`와 Hermes 설치 스킬 → `ai-operating-assets`
- 대화·앱 상태 → `app-state-no-index`

## Split

- `04-decision-log.md`: 향후 결정별 파일 + 연대기 인덱스
- BELLOON 갱신형 회사·사람 리드: 개별 레코드
- `.claude/`: 재사용 스킬과 민감 런타임 상태의 보존 경계

## Merge logically

- `ideas/<business>.md`와 `ideas/<business>/index.md`
- `market/<business>.md`와 `market/<business>/index.md`
- 두 곳에 반복된 시장 인덱스와 실제 `research/` 목록
- 조사 → 결정 → 실행 → 일지 관계를 메타데이터 링크로 연결. 본문을 한 파일로 합치지는 않음

## Needs user decision

- Revenue Commerce OS·Revenue Ladder의 정본과 이력 판정
- `logs` 대 `journal`
- `_archiv` 대 `_archive`
- `Claude/` DOCX·HTML의 공식성
- 누락된 `/opt/data/` 워크북·스킬을 복구할지 참조를 제거할지
- Obsidian 플러그인의 중복을 휴대성 비용으로 유지할지 중앙 관리할지

