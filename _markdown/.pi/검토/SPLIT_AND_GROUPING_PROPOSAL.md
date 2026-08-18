---
source_path: ".pi/검토/SPLIT_AND_GROUPING_PROPOSAL.md"
source_filename: "SPLIT_AND_GROUPING_PROPOSAL.md"
source_type: "text"
source_size_bytes: 10490
source_modified_at: "2026-08-17T18:43:40+09:00"
source_sha256: "ca616cab028f4e8eb85f8a0f316eef72ea7d0d25652ce7f7224bb7085162ae9e"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 분할 및 그룹화 제안

## Recommended Primary Principle

**주 분류 기준: 정보의 역할과 수명주기**

자료를 먼저 다음 역할로 나눈다.

1. 사람이 사실·판단·실행에 사용하는 지식 코퍼스
2. AI가 행동할 때 사용하는 스킬·프롬프트·설치 패키지
3. 앱이 동작할 때 필요한 설정·대화·동기화 상태
4. 코퍼스에서 반드시 제외할 캐시·실행 파일·자격증명

지식 코퍼스 안에서는 사업 단위를 2차 기준으로 사용하고, 각 사업에서 `근거·조사 → 결정 → 전략·설계 → 실행 → 참고 → 이력` 순서로 나눈다.

## Why

현재 가장 큰 혼란은 확장자나 파일 크기가 아니라 **같은 Markdown이라도 역할이 다르다**는 점이다.

- 조사 문서는 “무엇을 확인했는가”를 답한다.
- 결정 문서는 “그래서 무엇을 하기로 했는가”를 답한다.
- 설계 문서는 “어떤 구조로 할 것인가”를 답한다.
- 실행 문서는 “누가 언제 무엇을 하고 있는가”를 답한다.
- 일지는 “그날 무엇이 일어났는가”를 답한다.
- 스킬은 “AI가 어떻게 행동해야 하는가”를 답한다.
- 대화 JSONL은 “도구가 어떤 이벤트를 남겼는가”를 답한다.

이들을 한 검색 공간에 두면 AI가 스킬 지침을 사업 사실로, 과거 초안을 현재 결정으로, 일지 요약을 독립 근거로 잘못 사용할 수 있다. 역할과 수명주기를 먼저 나누면 이런 오류를 직접 줄일 수 있다.

## File-Level Splitting

### 하나의 원문으로 유지할 자료

다음은 한 파일로 유지하는 것이 좋다.

- Premium MultiShop의 각 설계 문서: 하나의 아키텍처나 운영 모델을 완결된 문맥으로 설명함
- 시장 스캔·경쟁사·공급망 조사 보고서: 조사일·방법·한계·출처가 한 세트임
- `HermesWiki/journal/YYYY-MM/YYYY-MM-DD.md`: 하루 단위가 자연스러운 경계임
- `BusinessVault/07-project-tracker.md`: 전체 포트폴리오 상태를 한눈에 보는 원장 역할
- Hermes 설치 스킬 패키지: `SKILL.md`, 스크립트, 가이드, 예제 설정이 함께 있어야 재현 가능함
- Obsidian 볼트의 `.obsidian`, `TaskNotes`, `.stfolder`, `.stignore`: 기능상 함께 있어야 함. 단, AI 색인 제외

### 물리적 분할을 권장하는 자료

#### `BusinessVault/04-decision-log.md`

기존 파일은 변경하지 않고 역사적 스냅샷으로 보존한다. 향후에는 결정 하나당 파일 하나를 만든다.

```text
decisions/
├─ DEC-2026-08-15-pms-revenue-commerce-os.md
├─ DEC-2026-08-15-belloon-b2b-focus.md
└─ DEC-2026-08-16-resale-arbitrage-stop.md
```

각 결정은 `decision_id`, `business`, `date`, `status`, `evidence`, `supersedes`, `related_execution`을 가진다. 전체 연대기는 `decisions/index.md`가 링크로 제공한다.

#### BELLOON 회사·인물 리드

`belloon-linkedin-sourcing-ops.md`가 이미 `company-leads/<slug>.md`, `people-leads/<slug>.md` 구조를 제안한다. 현재의 대형 후보 보고서는 조사 스냅샷으로 유지하고, 실제 갱신되는 리드만 개별 레코드로 분리한다.

- 보고서: 조사 당시 후보군과 방법을 보존
- 개별 리드: 회사·사람의 최신 검증 상태를 갱신
- 인덱스: 보고서와 개별 리드의 관계를 연결

#### 동명 파일·인덱스 쌍

`ideas/belloon.md`와 `ideas/belloon/index.md` 같은 쌍은 하나의 사업 폴더 안에서 `ideas.md` 또는 `ideas/index.md` 하나로 합리화한다. 내용이 다른 부분은 삭제하지 않고 하나의 탐색 인덱스로 논리 병합한다.

### 물리적으로 나누지 말고 검색용으로만 청크할 자료

긴 설계·조사 문서는 H2/H3 기준으로 파생 청크를 만든다.

- 부모 파일은 그대로 유지
- 청크에는 `parent_document_id`, `section_path`, `business`, `document_role`, `status`, `date`를 붙임
- 각 청크 앞에 문서 제목과 섹션 경로를 짧게 반복
- 문단 전체를 임의 토큰 수로 자르지 않음
- 표는 헤더와 관련 설명을 같은 청크에 유지
- Sources는 해당 주장의 본문과 연결 가능한 상태로 유지

## Chunk Size and Overlap

현재 자료에는 임의 숫자 기준을 먼저 적용할 이유가 없다. 우선순위는 다음과 같다.

1. H2/H3 의미 경계
2. 표·체크리스트·결정 블록의 완결성
3. 너무 긴 섹션만 문단 묶음으로 2차 분할
4. 겹침은 이전 문단 복사보다 제목·부모 ID·섹션 경로 제공으로 해결

수치형 최대 길이는 실제 RAG 모델의 컨텍스트 제한이 정해진 뒤 보조 파라미터로 정한다.

## Folder-Level Grouping

### 1차: 정보 역할

- `knowledge-corpus/`: 사람과 AI가 사실·판단에 사용하는 문서
- `ai-operating-assets/`: 스킬·프롬프트·설치 패키지
- `app-state-no-index/`: Obsidian 설정, 대화 이력, 동기화 상태
- `machine-cache-no-index/`: 브라우저·드라이버·실행 파일
- `private-credentials-no-index/`: 키·자격증명. 공유 루트 밖에 두는 것이 기본

### 2차: 사업·개인 영역

`knowledge-corpus/business/`에서 Premium MultiShop, BELLOON, 공통을 나눈다. `knowledge-corpus/personal/`에는 일지와 개인 지식을 둔다.

### 3차: 지식 수명주기

각 사업은 같은 얕은 구조를 쓴다.

- `01-evidence-and-research`
- `02-decisions`
- `03-strategy-and-design`
- `04-execution`
- `05-reference-and-templates`
- `99-history`

## Original / Processed / Derived Boundary

현재 컬렉션에는 완전한 raw-cleaned-chunked 계층이 없다. 따라서 억지로 `raw/cleaned/processed`를 만들지 않는다.

### Original / source representation

로컬에 실제 존재하는 Word·HTML·PDF와 조사 당시 보고서 스냅샷이다. 원래 웹페이지 원문이 없는 경우 “원문”이라고 부르지 않고 `source-artifacts` 또는 `research-snapshots`로 표시한다.

### Curated knowledge representation

현재 BusinessVault와 HermesWiki의 사람이 읽는 Markdown이다. 이 층이 인간 기준의 정본이다.

### Derived representation

향후 생성할 섹션 청크, 임베딩, 검색 인덱스, 관계 그래프다. 원문과 같은 폴더에 두지 않고 `_derived-index/`에 둔다. 언제든 정본 문서에서 재생성할 수 있어야 한다.

### Metadata / index representation

`_metadata/document-index.jsonl`과 `relationships.jsonl`에 문서 ID, 역할, 사업, 상태, 버전 관계, 원본 경로를 둔다. 본문을 복제하지 않는다.

## 최소 메타데이터 제안

BusinessVault 문서에 실제로 도움이 되는 필드만 권장한다.

| 필드 | 이유 |
| --- | --- |
| `document_id` | 파일 이동·이름 변경 뒤에도 안정적 식별 |
| `business` | Premium MultiShop, BELLOON, shared 분리 |
| `document_role` | research, decision, design, execution, reference 구분 |
| `date` | 조사·결정·기준 시점 |
| `status` | draft, active, canonical, hold, superseded |
| `supersedes` / `superseded_by` | 버전 정본 관계 |
| `source_refs` | 근거 문서와 파생 관계 |

모든 문서에 작성자, 언어, 토큰 수 같은 필드를 강제할 필요는 없다. 현재 문제를 해결하는 필드가 아니다.

## What Should Stay Together

- 조사 보고서와 그 조사일·한계·Sources
- 하나의 아키텍처 문서와 그 내부 표·승인 규칙·하드스탑
- 하나의 날짜 일지와 YAML·고정 섹션
- 한 결정과 근거·실행 링크·정본 상태
- 한 Obsidian 볼트와 해당 설정·동기화 표식. 단, 지식 색인과 앱 파일 색인은 분리
- Hermes 설치 스킬의 설명·스크립트·가이드
- HTML 아키텍처와 썸네일 이미지
- 원본 보고서와 그 파생 청크. 파일은 다른 폴더에 있어도 `parent_document_id`로 연결

## What Should Be Separated

- 사업 지식과 `.claude/projects/*.jsonl` 대화 원장
- 사업 지식과 `.agents/skills/*` 일반 마케팅 지침
- Premium MultiShop과 BELLOON
- 조사 근거와 최종 결정
- 현재 canonical 문서와 과거 버전
- 실행 추적과 장기 전략
- 앱 플러그인·TaskNotes 생성물과 사람이 쓴 Markdown
- 자격증명·SSH 키·Syncthing 키와 모든 공유·AI 색인 영역
- BELLOON 리드 스냅샷 보고서와 갱신형 개별 리드 레코드

## What Should Not Be Changed

- 사업별 분리 원칙
- 조사일·기준일·상태·검증 한계를 적는 습관
- Markdown 헤딩·표·목록 구조
- 출처 URL과 위키링크
- 일지의 날짜별 1파일과 YAML 템플릿
- `canonical`이라는 정본 표기 관행
- 안정적인 영문 슬러그 파일명과 날짜 `YYYY-MM-DD`
- 원본 문서를 의미 없는 고정 크기 파일로 물리 분할하지 않는 현재 선택
- 독립 볼트가 필요하다면 각 볼트의 Obsidian 설정을 보존하는 선택

## Benefits

### 사람 탐색

사업을 선택한 뒤 근거, 결정, 설계, 실행을 순서대로 읽을 수 있다. 현재 정본이 무엇인지 파일명 추리 없이 알 수 있다.

### 유지보수

인덱스가 두 군데에서 낡는 문제와 동명 파일·폴더 중복이 줄어든다. 새 문서가 들어갈 위치를 결정하기 쉽다.

### 출처 추적

조사 보고서와 파생 결정의 관계가 명시된다. 같은 결론이 일지와 결정 로그에 있어도 독립 근거로 오인하지 않는다.

### 향후 전처리

정본 Markdown만 대상으로 섹션 청크를 재생성할 수 있다. 플러그인 코드·대화 원장·키가 청크에 섞이지 않는다.

### RAG/LLM

질문 목적에 따라 `research`, `decision`, `canonical design`, `execution` 인덱스를 선택할 수 있다. 과거 버전은 기본 검색에서 제외하고 필요할 때만 조회할 수 있다.

## Tradeoffs

- 현재 경로를 참조하는 위키링크를 나중에 일괄 갱신해야 한다.
- 사업별 폴더로 옮기면 일부 공통 문서를 어느 사업에 둘지 판단이 필요하다.
- 결정별 파일은 파일 수가 늘어나지만 검색 정확성과 변경 이력이 좋아진다.
- Obsidian 플러그인을 두 볼트에 유지하면 중복 용량은 남는다. 중앙화하면 볼트 휴대성이 떨어질 수 있다.
- 메타데이터 도입에는 초기 정본 판정 작업이 필요하다. 자동 추론으로 상태를 확정하면 안 된다.

