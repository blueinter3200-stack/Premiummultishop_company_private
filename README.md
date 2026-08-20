# Miracle Company Private

미라클 회사 대표님과 관리자가 함께 사용하는 **회사 OS 기준·진행업무·아이디어·문제·자료 저장소**입니다.

- Canonical repository: `https://github.com/jintonic1010/miracle_company_private`
- Clone: `gh repo clone jintonic1010/miracle_company_private`
- Canonical branch: `main`
- Visibility: private

## 핵심 원칙

1. `llm-source/` = 현재 확정된 회사 기준. 평소 LLM이 우선 읽습니다.
2. `llm-source/PROJECT_REPOSITORIES.md` = 현재 회사와 연결된 GitHub 저장소명/역할 레지스트리입니다.
3. `working/CURRENT_WORK.md` = 현재 진행·협의 중인 회사 업무의 최신판. 평소 LLM이 함께 읽습니다.
4. `records/PENDING_INDEX.md` = 아직 반영되지 않은 아이디어·문제를 짧게 찾기 위한 인덱스입니다. `/업무검토`에서 사용합니다.
5. `records/` = 아직 공식 반영되지 않은 아이디어·문제 원문 기록. PENDING_INDEX에서 관련된 것만 선택해 읽습니다.
6. `materials/normalized/` = 첨부자료를 LLM이 읽기 좋게 정제한 Markdown. 관련 요청이 있을 때만 읽습니다.
7. `materials/originals/` = 첨부 원본 보존. 기본 읽기 금지입니다.
8. `archive/` = 과거/레거시 자료. 기본 읽기 금지입니다.
9. 실제 고객 개인정보, 운영 DB, API 키, 비밀번호, 토큰, SSH 개인키는 이 저장소에 넣지 않습니다.

## 작성자와 권한

회사 기록 작성자는 두 역할로 구분합니다.

- 대표님: `representative`
- 관리자: `admin`

역할은 대화 내용으로 추론하지 않고 ChatGPT 프로젝트에 넣는 역할 소스로 고정합니다.

대표님과 관리자는 모두 아이디어·문제 저장, 업무검토, 업무공유가 가능합니다. 공식 반영과 업무확정은 관리자만 수행합니다.

## 업무 대화 흐름

```text
자유로운 업무 대화
   ↓
/업무검토       ← 공식 기준 + CURRENT_WORK + 관련 미반영 아이디어/문제 검토
   ↓ PASS
/업무공유       ← CURRENT_WORK 전체 최신화
   ↓
계속 진행/협의
   ↓
관리자 /업무확정
   ↓
llm-source/ 공식 기준으로 승격
```

`/업무검토 PASS`는 공식 확정이 아닙니다. 현재 진행업무판에 공유해도 된다는 의미입니다.

업무 상세 규칙은 `llm-source/WORK_GOVERNANCE.md`를 따릅니다.

## 평소 LLM 기본 읽기 순서

1. `FILE_MAP.json`
2. `llm-source/COMPANY_OS.md`
3. `llm-source/PRODUCT_REQUIREMENTS.md`
4. `llm-source/PROJECT_REPOSITORIES.md`
5. `working/CURRENT_WORK.md`
6. 질문과 직접 관련된 부서 문서만 선택적으로 읽기

저장된 아이디어·문제 원문, 정제자료, 원본, 아카이브는 기본적으로 읽지 않습니다.

## /업무검토 읽기 흐름

`/업무검토`에서는 평소 기본 읽기 항목에 더해:

1. `llm-source/WORK_GOVERNANCE.md`
2. `records/PENDING_INDEX.md`
3. PENDING_INDEX에서 현재 업무와 관련된 아이디어·문제 기록만
4. 필요한 경우에만 그 기록이 연결한 normalized 자료

를 확인합니다.

따라서 미반영 아이디어·문제를 업무검토에서 놓치지는 않지만, 전체 기록을 매번 읽지도 않습니다.

프로젝트의 실제 개발 진척·코드·구현 여부가 필요한 질문에서는 `PROJECT_REPOSITORIES.md`에서 저장소를 찾은 뒤 해당 저장소의 최신 `main`을 직접 확인합니다.
