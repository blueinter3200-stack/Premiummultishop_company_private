---
source_path: ".pi/검토/PREPROCESSING_ANALYSIS.md"
source_filename: "PREPROCESSING_ANALYSIS.md"
source_type: "text"
source_size_bytes: 7821
source_modified_at: "2026-08-17T18:38:52+09:00"
source_sha256: "d46aa8d1905dade211cc6d955e2e04e3ac35c5e3ffb6c2ae3a81b5d34a41bf94"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 전처리 및 생성 방식 분석

## 결론

현재 컬렉션에는 전통적인 의미의 텍스트 전처리 파이프라인이 없다. 핵심 자료는 원문을 기계적으로 청크한 결과가 아니라, AI와 사람이 조사·요약·설계한 **구조화 Markdown 지식 문서**에 가깝다.

## 직접 확인된 전처리·생성 행동

### Obsidian Markdown 볼트

`BusinessVault/`와 `HermesWiki/` 모두 `.obsidian/`, `.stfolder/`, `.stignore`, 위키링크를 가진다. 따라서 두 컬렉션이 독립 Obsidian 볼트로 운영된다는 점은 확인됐다.

### Hermes 위키 스캐폴드

`.claude/skills/hermes-vps-setup/scripts/03-server-syncthing.sh`는 위키 인덱스와 기본 폴더를 만드는 스크립트다. `SKILL.md`도 `logs/YYYY-MM/YYYY-MM-DD.md` 규칙과 중복 대신 위키링크 사용을 명시한다.

### BusinessVault 스캐폴드 이력

`.claude/tasks/35d535d3-411d-4c67-b6b7-d7758c5f2225/7.json`은 BusinessVault에 결정 로그와 프로젝트 추적기 스캐폴드를 만드는 작업을 기록한다. `.claude/projects/...Hermes-Manage...jsonl`에는 두 번째 사업 볼트와 그 운영 규칙을 추가한 이벤트가 있다. 적어도 볼트 골격과 일부 운영 문서는 에이전트 설치·설정 흐름에서 만들어졌음이 확인된다.

### 설치된 AI 스킬의 원본 식별

`.agents/.skill-lock.json`에는 각 스킬의 로컬 설치 출처, 경로, 설치 시각, 폴더 해시가 있다. 스킬 Markdown은 일반 사업자료가 아니라 설치된 명령 패키지다.

### TaskNotes 생성물

두 볼트의 `TaskNotes/Views/*.base`와 TaskNotes 설정은 기본 뷰와 수식이 포함된 생성 파일이다. `mini-calendar-default.base`, `pomodoro-stats.base`에는 생성됨을 나타내는 주석도 있다.

### 날짜별 일지 템플릿

Hermes 일지는 모두 YAML frontmatter와 같은 6개 본문 섹션을 사용한다. 날짜별 요약을 정해진 템플릿에 채우는 생성 방식이 확인된다.

## 강하게 추정되는 행동

### AI 보조 작성·요약

BusinessVault 문서는 짧은 기간에 통일된 어조, 상태 표기, 하드스탑, 승인 규칙을 반복한다. 작업·대화 기록도 볼트 작성 흐름을 보여 준다. 따라서 다수 문서가 AI 보조로 작성되었을 가능성이 높다. 다만 문서별 인간 편집 범위와 정확한 생성 모델은 `Needs verification`이다.

### 계층적 요약

같은 주제가 대체로 다음 순서로 다시 표현된다.

```text
공개 조사·사용자 관찰
→ research 조사 보고서
→ plans 검토·설계 문서
→ 04-decision-log 결론
→ 07-project-tracker 실행 상태
→ HermesWiki 일일 요약
```

이는 중복 제거 실패라기보다 서로 다른 사용 목적을 위한 계층적 요약으로 보인다. 문제는 이 관계가 문서 메타데이터에 명시되지 않아 AI가 같은 주장을 독립 근거 여러 개로 오인할 수 있다는 점이다.

### 의미 경계 중심 분할

긴 문서는 고정 길이가 아니라 제목과 섹션으로 나뉜다. 후보 인물은 `###`, 설계 요소는 번호형 H2/H3, 일지는 고정 섹션을 사용한다. 현재 파일은 의미 경계 우선으로 작성됐다고 보는 것이 타당하다.

## 확인되지 않은 행동

- 고정 토큰 수 또는 문자 수 청킹
- 청크 간 겹침 크기
- 임베딩 생성 또는 벡터 DB 적재
- OCR 처리
- HTML/Markdown 정규화 도구
- 원문 웹페이지의 자동 수집·보존 방식
- 모든 BusinessVault 문서의 정확한 생성 작업과 작성자
- `/opt/data/` 원본과 현재 로컬 복사본의 완전성

## 텍스트 정리 규칙

### 확인된 규칙

- UTF-8 Markdown 사용. 핵심 볼트 Markdown에서 인코딩 오류는 발견되지 않음
- Markdown 헤딩, 목록, 표, 코드 블록 유지
- 외부 URL과 조사 한계 유지
- Obsidian 위키링크 사용
- 사업 문서에서는 `확인된 사실`, `검증 불가`, `보류`, `중단 조건`을 구분하려는 경향
- 개인 일지에서는 YAML 메타데이터 유지

### 일관되지 않은 규칙

- BusinessVault는 YAML frontmatter를 전혀 쓰지 않음
- 날짜는 파일명, 인라인 목록, 인용 블록, 본문에 서로 다른 방식으로 표시
- 상태 필드는 55개 주요 문서 중 28개에만 존재
- 사업 필드는 24개에만 존재
- Sources/출처 섹션은 10개 문서에서만 헤딩으로 명확히 확인
- 일부는 절대경로 `/opt/data/...`, 일부는 `business-wiki/...`, 일부는 상대 위키링크 사용

## 분할과 청킹 행동

### 현재 파일 단위

- 사업 설계: 하나의 설계 주제를 한 파일에 유지
- 조사: 한 조사 캠페인 또는 후보군을 한 파일에 유지
- 일지: 하루 한 파일
- 결정: 한 로그 파일에 여러 결정을 누적
- 스킬: 한 기능 패키지당 `SKILL.md`와 부속 파일

### 현재 청크 파일

별도의 검색용 청크 파일은 없다. 따라서 현재 폴더명이나 파일명을 보고 `chunked corpus`라고 부르면 부정확하다.

### 청크 겹침

물리적 청크 겹침은 확인되지 않았다. 다만 조사·계획·결정·일지가 같은 내용을 다른 길이로 요약하므로 개념적 중첩은 많다.

## 보존된 메타데이터

- 파일 경로와 파일명
- 많은 문서의 사업명, 날짜, 상태
- 제목과 섹션 계층
- 조사 출처 URL
- 위키링크
- 일지의 title, created, type, tags, mood
- 스킬의 name, description, 설치 출처·해시
- 대화 JSONL의 이벤트 유형과 시간 정보

## 손실되었거나 약한 메타데이터

- 문서 전체에 공통인 안정적인 `document_id`
- `document_role`: 조사·결정·설계·실행·템플릿 구분
- `canonical`/`superseded` 관계
- 어떤 조사 문서에서 어떤 결정이 파생됐는지 나타내는 명시적 관계
- 원본 파일명과 원본 보존 위치
- 현재 없는 워크북·스킬의 로컬 식별자
- 교차 볼트 링크가 가리키는 실제 로컬 경로

## 원문 복원 가능성

### 사업 설계·조사 문서

현재 Markdown 자체는 완전한 읽기 문서로 재구성 가능하다. 그러나 외부 웹 원문이나 원래의 데이터 시트가 함께 보존되지 않아 조사 과정을 원자료 수준으로 재현할 수는 없다.

### 일일기록

날짜·고정 헤딩·요약은 잘 보존되어 있다. 원 대화의 일부는 `.claude/projects/*.jsonl`에 있으나 개인정보·도구 출력이 섞여 있고 일지와의 안정적 ID 연결이 없다.

### 버전 문서

각 파일은 독립적으로 읽을 수 있지만 v1→v2→v3 관계와 변경점은 자동 복원하기 어렵다. 파일명 외에 관계 메타데이터가 필요하다.

## 가능한 전처리 산물과 오류

- `04-decision-log.md`에서 여러 결정 헤딩이 빠진 것은 누적 append 과정의 산물일 가능성이 높다.
- `## YYYY-MM-DD | 결정 제목`은 스캐폴드 템플릿 잔존물이다.
- `market/premium-multishop/index.md`의 “별도 자료 없음” 문구는 이후 파일 추가 뒤 갱신되지 않은 인덱스다.
- `logs`와 `journal` 불일치는 설치 스캐폴드와 이후 실제 기록 경로가 달라진 결과로 보인다.
- `BusinessVault/2026-08-14.md`와 `무제.md`는 빈 노트 생성 흔적이다.
- 두 Obsidian 볼트의 동일 플러그인·TaskNotes 파일은 전처리 중복이 아니라 독립 볼트 배포 중복이다.

## 런타임 검증

Runtime verification: not applicable to corpus-structure audit

대신 읽기 전용으로 해시 중복, 링크 해석, UTF-8 검증, JSONL 레코드 유형, DOCX 텍스트·표 추출, PDF 9페이지 렌더링을 수행했다. 원본을 생성하거나 바꾸는 전처리 스크립트는 실행하지 않았다.

