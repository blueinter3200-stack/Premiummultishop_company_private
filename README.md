# Miracle Company Private

미라클 회사 대표님과 관리자가 함께 사용하는 **회사 OS 기준·진행업무·아이디어·문제·자료 저장소**입니다.

- Canonical repository: `https://github.com/jintonic1010/miracle_company_private`
- Clone: `gh repo clone jintonic1010/miracle_company_private`
- Canonical branch: `main`
- Visibility: private

## 핵심 원칙

1. `llm-source/` = 현재 확정된 회사 기준. 평소 LLM이 우선 읽습니다.
2. `working/CURRENT_WORK.md` = 현재 진행·협의 중인 회사 업무의 최신판. 평소 LLM이 함께 읽습니다.
3. `records/` = 아직 공식 반영되지 않은 아이디어·문제 기록. 명시적으로 필요할 때만 읽습니다.
4. `materials/normalized/` = 첨부자료를 LLM이 읽기 좋게 정제한 Markdown. 관련 요청이 있을 때만 읽습니다.
5. `materials/originals/` = 첨부 원본 보존. 기본 읽기 금지입니다.
6. `archive/` = 과거/레거시 자료. 기본 읽기 금지입니다.
7. 실제 고객 개인정보, 운영 DB, API 키, 비밀번호, 토큰, SSH 개인키는 이 저장소에 넣지 않습니다.

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
/업무검토       ← 최신 회사 공식 기준과 현재 업무를 싹 훑는 읽기 전용 게이트
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

## 기본 LLM 읽기 순서

1. `FILE_MAP.json`
2. `llm-source/COMPANY_OS.md`
3. `llm-source/PRODUCT_REQUIREMENTS.md`
4. `working/CURRENT_WORK.md`
5. 질문과 직접 관련된 부서 문서만 선택적으로 읽기

`/업무검토` 때는 `llm-source/WORK_GOVERNANCE.md`를 추가로 읽습니다.

저장된 아이디어·문제, 정제자료, 원본, 아카이브는 기본적으로 읽지 않습니다.
