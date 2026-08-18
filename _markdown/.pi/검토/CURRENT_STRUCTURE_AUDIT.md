---
source_path: ".pi/검토/CURRENT_STRUCTURE_AUDIT.md"
source_filename: "CURRENT_STRUCTURE_AUDIT.md"
source_type: "text"
source_size_bytes: 7112
source_modified_at: "2026-08-17T18:38:52+09:00"
source_sha256: "57f5f4f203458efb8a639db608af25d49e05183debfbaa21b458df91a08f791c"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 현재 구조 감사

## 현재 조직 논리

현재 구조는 한 번에 설계된 단일 코퍼스가 아니라 여러 도구가 각자 필요한 폴더를 같은 루트에 만든 결과다.

- `BusinessVault/`: 사업 지식용 Obsidian 볼트
- `HermesWiki/`: 개인·일일기록용 Obsidian 볼트
- `.agents/`: 범용 AI 스킬 저장소
- `.claude/`: 대화·작업·메모리·스킬·자격증명 상태
- `Claude/`: 특정 도구가 만든 사업 산출물
- `.cache/`, `.hermes-sync/`, `.ssh/`, `Intel/`: 실행 환경

BusinessVault 내부는 처음에 `research`, `plans`, `market`, `ideas`, 결정 로그, 프로젝트 추적기로 나눈 것으로 보인다. 이후 문서가 늘면서 `plans/`가 설계·검토·감사·프롬프트·계약까지 받아 경계가 넓어졌다.

## 강점

### 사업 볼트와 개인 위키의 분리

사업 판단은 `BusinessVault/`, 날짜별 흐름은 `HermesWiki/`에 두는 큰 경계가 적절하다. 일지가 사업 문서를 링크하므로 사실 원문과 일상 회고를 논리적으로 분리할 수 있다.

### 사업 간 경계 의식

여러 문서가 Premium MultiShop과 BELLOON을 섞지 말라고 명시한다. `ideas/`와 `market/`도 두 사업을 따로 둔다. 향후 구조 개편에서도 반드시 보존해야 할 원칙이다.

### 구조화된 작성 습관

대부분의 사업 문서는 제목, 날짜, 상태, 한 줄 결론, 표, 하드스탑, 출처를 사용한다. 55개 비어 있지 않은 주요 사업 문서 중 54개에 H1이 있고, 38개에 날짜 필드, 28개에 상태 필드, 24개에 사업 필드가 있다.

### 의미 단위 헤딩

긴 설계 문서도 H2/H3 기준으로 주제가 분명하다. 물리적으로 파일을 잘게 나누지 않아도 검색용 파생 청크를 만들기 좋은 기반이다.

### 현재성 표기를 시작함

`canonical`, `상태: 설계안`, `검증 보류`, `대표 결정 반영` 같은 표기가 존재한다. 정본 관리 체계의 기초로 사용할 수 있다.

## 약점

### 루트가 코퍼스 경계가 아님

303개 파일 중 실제 핵심 지식 Markdown은 67개뿐이다. 루트 전체를 수집하면 실행 파일, 플러그인 코드, 대화 원장, SSH 키 경로, 동기화 인증서가 함께 들어간다. 현재 작업 폴더를 그대로 AI 데이터 소스로 쓰면 안 된다.

### `plans/`의 역할 과부하

다음이 한 폴더에 같이 있다.

- 현재 전략·설계
- 사업모델 타당성 검토
- SEO 기술감사
- 의사결정 문서
- 운영 프롬프트
- 계약 현황
- 과거 버전

파일명에 `review`, `audit`, `decision`, `prompt`, `canonical`이 있어 사람이 추론할 수는 있지만 폴더 자체는 의미를 알려주지 못한다.

### 사업 중심 탐색이 어렵다

Premium MultiShop 자료를 보려면 `research`, `plans`, `market`, `ideas`, 루트 로그, `Claude/`를 모두 돌아야 한다. BELLOON도 마찬가지다. 현재 폴더는 문서 유형이 사업보다 먼저다.

### 인덱스 계층이 중복됨

`ideas/belloon.md`와 `ideas/belloon/index.md`, `market/premium-multishop.md`와 `market/premium-multishop/index.md`가 동시에 있다. 실제 본문과 하위 인덱스의 역할이 명확히 갈리지 않는다.

### 시간·버전·정본 관계가 불완전함

Revenue Commerce OS는 v1, v2 master, v3, v3 canonical이 있다. v3 초안 날짜가 2026-08-14이고 v2 master가 2026-08-15라 버전 번호와 날짜 순서만으로 흐름을 해석하기 어렵다. 각 파일에 `supersedes`, `superseded_by`, `canonical_as_of`가 없다.

### 결정 로그의 구조가 깨짐

`04-decision-log.md`의 첫 `## 2026-08-15 | PMS Revenue Commerce OS 9-Agent 확정` 아래에는 신뢰상품, 온라인 신뢰, 이중 재고, BELLOON 집중, 홍콩 보세, 온라인 피보팅, SEO, 자동화 등 다수 결정이 별도 헤딩 없이 이어진다. 파일에 `## YYYY-MM-DD | 결정 제목` 템플릿도 그대로 남아 있다. H2 기준 청킹 시 여러 결정이 한 덩어리가 된다.

## 불일치와 겹치는 범주

| 문제 | 증거 | 영향 |
| --- | --- | --- |
| `logs` 대 `journal` | Hermes 인덱스·설치 스킬은 `logs/`, 실제 일지는 `journal/` | 링크와 자동화 경로 혼란 |
| `_archive` 대 `_archiv` | BusinessVault에 두 폴더가 공존 | 보관 위치가 둘로 갈림 |
| `business-wiki` 대 `BusinessVault` | Hermes 일지와 절대경로는 `business-wiki`, 로컬은 `BusinessVault` | 교차 볼트 링크 다수 미해결 |
| `research` 대 `market` | 원자료는 research, 요약 인덱스는 market | 최신성 이중 관리 |
| `plans` 대 `review/audit` | 검토 보고서가 plans에 포함 | 확정안과 평가안 혼동 |
| `Claude/` 대 `BusinessVault/` | 같은 Premium MultiShop 주제 산출물 분산 | 도구별 사일로 |

## 잘못 놓였거나 재분류가 필요한 자료

- `BusinessVault/research/belloon-linkedin-sourcing-ops.md`: 조사 결과보다 운영 표준·스키마·템플릿 성격이 강함
- `BusinessVault/plans/belloon-b2b-beauty-focus-decision-2026-08-15.md`: 계획보다 결정 기록
- `BusinessVault/plans/pms-ai-detailpage-agent-master-prompt-v1-2026-08-15.md`: 전략 문서보다 AI 운영 템플릿
- `BusinessVault/plans/contracts.md`: 사업 공통 상태 원장
- `BusinessVault/plans/*review*.md`, `*audit*.md`: 실행 계획보다 타당성·품질 검토
- `BusinessVault/2026-08-14.md`: 빈 날짜 파일이며 개인 일지와 혼동
- `Claude/Projects/...docx`, `Claude/Artifacts/...html`: 사업 산출물이 생성 도구 폴더에 고립

## 과도하게 쪼개졌거나 과도하게 뭉친 부분

### 과도하게 쪼개짐

- `ideas/<business>.md`와 `ideas/<business>/index.md`
- `market/<business>.md`와 `market/<business>/index.md`
- 조사 → 계획 → 결정 로그 → 일지에서 같은 결론이 반복 요약되지만 관계 유형이 메타데이터로 표시되지 않음

### 과도하게 뭉침

- `plans/` 33개 전체
- `04-decision-log.md` 첫 섹션
- `belloon-buyer-person-sourcing-2026-08-12.md`의 여러 인물 레코드
- `.claude/` 안의 재사용 스킬과 민감 런타임 상태

## 사람이 결정해야 할 영역

1. Hermes 일지의 표준 폴더를 `logs`와 `journal` 중 무엇으로 할지
2. 보관 폴더명을 `_archive`로 통일할지 현재 `_archiv`를 유지할지
3. Revenue Commerce OS와 Revenue Ladder에서 어떤 파일을 현재 정본으로 확정하고 나머지를 이력으로 둘지
4. `Claude/`의 DOCX·HTML이 단순 참고 산출물인지, 공식 사업 기록인지
5. 현재 없는 Revenue SEO 워크북과 사업 스킬을 복구할지, 참조를 폐기할지
6. 두 Obsidian 볼트의 플러그인 복제를 독립성 비용으로 유지할지 중앙 관리할지

## 종합 판정

현재 구조는 **내용 자체의 품질은 높지만 코퍼스 경계와 현재성 관리가 약한 상태**다. 대규모 재작성보다 먼저 코퍼스/운영자산/민감상태를 분리하고, 사업별로 모은 뒤 문서 역할과 정본 상태를 표시하는 것이 효과가 가장 크다.

