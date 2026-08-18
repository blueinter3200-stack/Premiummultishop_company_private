---
source_path: ".pi/검토/CORPUS_OVERVIEW.md"
source_filename: "CORPUS_OVERVIEW.md"
source_type: "text"
source_size_bytes: 6263
source_modified_at: "2026-08-17T18:38:52+09:00"
source_sha256: "1d97c21308b406368fbf0bbf6aeeae48b5192b97c98f966dfe2d397e2108b3e3"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 코퍼스 전체 개요

## 한 문장 결론

지금 자료는 **사업 지식 볼트, 개인 일지 위키, AI 운영 자산, 프로그램 실행 잔여물**이 한 폴더에 함께 들어 있는 컬렉션이다. 사람이 보거나 AI가 활용하려면 먼저 **정보의 역할과 수명주기**에 따라 코퍼스와 비코퍼스를 분리하고, 사업 자료 안에서는 Premium MultiShop과 BELLOON을 나눈 뒤 `근거·조사 → 결정 → 설계 → 실행 → 이력` 순서로 정리하는 것이 가장 좋다.

## 대략적인 규모

`검토/` 생성 전 원본 기준이다.

| 항목 | 수치 |
| --- | ---: |
| 전체 파일 | 303개 |
| 전체 하위 디렉터리 | 212개 |
| 최상위 디렉터리 | 59개 |
| 비어 있는 최상위 디렉터리 | 49개 |
| 전체 용량 | 595,318,619바이트, 약 568MB |
| Markdown | 96개 |
| 두 지식 볼트의 사람이 읽는 Markdown | 67개, 약 545KB |
| `BusinessVault/` | 85개 파일 |
| `HermesWiki/` | 34개 파일 |
| 정확한 중복 해시 그룹 | 25개 그룹, 54개 파일 |

전체 용량은 문서량을 뜻하지 않는다. 약 535MB의 Chromium 캐시와 28MB의 Syncthing 실행 파일, 두 볼트에 복제된 Obsidian 플러그인이 대부분이다.

## 이 자료는 전체적으로 무엇인가

### 1. 사업 지식

`BusinessVault/`는 Premium MultiShop 명품 유통 사업과 BELLOON 화장품 B2B 사업의 세컨브레인이다. 시장조사, 해외 공급처·바이어 조사, 수익성 검토, AI·데이터 구조, 실행 로드맵, 결정 로그가 들어 있다.

자료의 중심은 2026-08-12부터 2026-08-16 사이에 집중되어 있다. Premium MultiShop 문서가 다수이고, BELLOON 문서는 바이어 소싱과 B2B 집중 결정 중심이다.

### 2. 개인·업무 일지

`HermesWiki/`는 2026-08-11부터 2026-08-16까지의 일일 요약이다. 하루의 흐름, 결정, 진행, 감상, 대화 하이라이트, 다음 할 일을 같은 틀로 기록한다. 사업 문서를 다시 요약하고 링크하는 역할도 한다.

### 3. AI 운영 자산

`.agents/skills/`에는 SEO·콘텐츠·소셜 플랫폼 관련 스킬 21개가 있다. `.agents/.skill-lock.json`은 로컬 설치 출처, 설치 시각, 해시를 보존한다. `.claude/skills/hermes-vps-setup/`은 Hermes 에이전트 설치 스킬·스크립트·PDF 가이드의 한 패키지다.

### 4. 대화·앱·시스템 상태

`.claude/projects/`는 8개 JSONL 대화 기록으로 총 1,437개 레코드를 가진다. `.cache/`, `.hermes-sync/`, `.ssh/`, `Intel/`은 브라우저, 동기화, 보안키, 설치 로그다. 이들은 현재 루트에는 있지만 사업 코퍼스에는 포함하면 안 된다.

## 현재 어떤 방식으로 전처리되어 보이는가

전형적인 `원문 → 정제 → 청크` 파이프라인은 확인되지 않았다. 대신 다음 방식이 확인된다.

- Obsidian용 Markdown으로 직접 작성 또는 AI 보조 작성
- 헤딩, 목록, 표, 위키링크를 사용한 의미 단위 구조화
- 사업 문서는 조사 결과가 `research/`, 해석·설계가 `plans/`, 결론 요약이 `04-decision-log.md`, 실행 상태가 `07-project-tracker.md`에 반복 요약되는 방식
- 개인 위키는 YAML frontmatter와 고정된 일일 템플릿 사용
- TaskNotes가 `.base` 뷰 파일을 생성하고 Obsidian 플러그인 설정이 두 볼트에 각각 존재
- Syncthing으로 별도 볼트를 동기화

고정 토큰 청크, 의미 청크 파일, 임베딩 인덱스, OCR 처리, HTML 정규화 파이프라인은 발견되지 않았다.

## 가장 큰 문제

1. **코퍼스와 프로그램 상태가 한 루트에 섞여 있다.** AI가 루트 전체를 색인하면 브라우저 번들, 대화 원문, 개인키 경로, 플러그인 코드까지 함께 들어간다.
2. **사업별 분리보다 문서 유형 폴더가 먼저다.** `plans/`에 설계, 감사, 수익성 검토, 프롬프트, 계약 현황이 함께 있다.
3. **현재 정본과 과거 버전의 관계가 명시되지 않았다.** Revenue Commerce OS v1·v2·v3·canonical, Revenue Ladder v1·v2가 같은 폴더에 있다.
4. **의사결정 로그가 한 헤딩 아래 여러 결정을 연속 기록한다.** 사람도 경계를 찾기 어렵고 헤딩 기반 AI 청킹도 잘못된다.
5. **경로 규칙이 충돌한다.** `logs` 대 `journal`, `_archive` 대 `_archiv`, `business-wiki` 대 `BusinessVault`가 함께 쓰인다.
6. **현재 컬렉션에 없는 자료를 참조한다.** 두 개의 Revenue SEO 워크북, 사업 스킬, 계산기, 일부 벤치마크 파일이 없다.

## 잘 되어 있는 부분

- Premium MultiShop과 BELLOON을 섞지 말라는 경계가 여러 문서에 명시되어 있다.
- 조사일, 상태, 검증 한계, 승인 필요 조건, 출처를 적으려는 습관이 좋다.
- 주요 문서는 H1/H2/H3, 표, 목록을 사용해 의미 단위가 비교적 선명하다.
- 일일기록은 날짜별 1파일과 일관된 YAML frontmatter를 사용한다.
- 위키링크로 조사 → 계획 → 결정 → 실행 자료를 연결한다.
- `pms-revenue-commerce-os-v3-canonical-2026-08-16.md`처럼 정본 표기를 도입한 시도는 유용하다.
- 핵심 사업 Markdown 사이에서 완전 중복은 발견되지 않았다. 중복은 주로 앱 플러그인과 기본 TaskNotes 자산이다.

## 가장 추천하는 정리 방향

**주 분류 기준은 정보의 역할과 수명주기**로 한다.

1. 먼저 `corpus/`, `ai-operating-assets/`, `app-state/`, `excluded-sensitive/`를 분리한다.
2. `corpus/business/` 안에서는 사업 단위로 Premium MultiShop, BELLOON, 공통 자료를 분리한다.
3. 각 사업 안에서는 `evidence-and-research`, `decisions`, `strategy-and-design`, `execution`, `reference`, `history` 순서로 둔다.
4. 원문 문서는 의미 단위 그대로 유지하고, 검색용 청크는 별도 파생 인덱스로 만든다.
5. AI 색인 기본 범위는 `corpus/`만 허용하고 대화 기록, 키, 플러그인 코드, 캐시는 명시적으로 제외한다.

이 구조는 현재의 좋은 사업 경계를 보존하면서, 무엇이 사실 근거인지, 현재 결정인지, 설계안인지, 실행 상태인지, 과거 버전인지 바로 알 수 있게 한다.

