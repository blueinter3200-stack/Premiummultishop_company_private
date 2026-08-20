# Product Requirements

- Repository: `https://github.com/jintonic1010/miracle_company_private`
- Branch: `main`
- Updated: 2026-08-20
- Authority: official confirmed requirements

이 문서는 **현재 확정된 회사 OS 요구사항**만 기록합니다. `working/`, 아이디어 저장, 문제 저장만으로 자동 변경하지 않습니다.

## Company Core

### CORE-001 — n8n backbone
회사 전체 연결·자동화 뼈대는 n8n을 사용한다.

### CORE-002 — department model
회사는 최소 다음 부서 시스템을 가진다.
- ERP / 재고·물류
- 시장리서치
- 마케팅
- CS
- 세무·법률

### CORE-003 — ERP operational core
ERP는 상품·SKU·재고·주문·판매·고객·구매·물류 운영 데이터의 핵심 원장 역할을 한다.

## ERP / Commerce Integration

### ERP-001
ERP 기반은 `ERPNext` 또는 `InvenTree` 중 하나를 사용하며 최종 선택은 비교 후 확정한다.

### ERP-002
카페24와 ERP는 필요한 판매·상품·재고·주문·고객·물류 데이터를 실제 API 허용 범위 안에서 IN/OUT 연결한다.

### ERP-003
네이버 스마트스토어와 ERP는 필요한 판매·상품·재고·주문·고객·물류 데이터를 실제 API 허용 범위 안에서 IN/OUT 연결한다.

### ERP-004
Google Shopping/Merchant/Ads 등 관련 API는 역할별 실제 기능을 조사한 뒤 ERP와 필요한 IN/OUT 연결을 구성한다.

### ERP-005
해외 공급처 API에서 필요한 상품·SKU·가격·재고·공급 데이터를 ERP로 입력한다.

### ERP-006
판매 과정에서 획득되는 고객·주문·구매이력 데이터는 법적·보안 경계 안에서 ERP/운영 데이터 계층에 연결한다.

## Department Data Exchange

### DEPT-001
ERP와 시장리서치 부서는 필요한 데이터를 양방향으로 교환한다.

### DEPT-002
ERP와 마케팅 부서는 필요한 데이터를 양방향으로 교환한다.

### DEPT-003
ERP와 CS 부서는 필요한 데이터를 양방향으로 교환한다.

### DEPT-004
ERP와 세무·법률 부서는 필요한 데이터를 양방향으로 교환한다.

## Data / Integration

### DATA-001
상품, SKU/옵션, 주문, 고객, 공급처 등 핵심 엔티티는 내부 기준 ID와 채널별 ID 매핑 구조를 가진다.

### DATA-002
카페24, 네이버, Google, 해외 공급처, ERP의 읽기/쓰기/Webhook/인증/rate-limit 등 실제 API IN/OUT 명세를 구현 전에 만든다.

### DATA-003
n8n은 회사 전체 연결과 자동화를 담당하지만 ERP 운영 데이터의 기준 원장을 대체하지 않는다.

### DATA-004
실제 고객 개인정보, 운영 DB, 인증정보, API 키, 비밀번호, 토큰, SSH 개인키는 이 GitHub 저장소에 저장하지 않는다.

## Knowledge / LLM Governance

### GOV-001 — authors
회사 기록 작성자는 `representative`와 `admin` 두 역할이다. 역할은 대화에서 추론하지 않고 ChatGPT 프로젝트 역할 소스로 고정한다.

### GOV-002 — current work
진행·협의 중 업무와 요구사항 후보는 `working/CURRENT_WORK.md` 한 파일의 최신 상태로 관리한다. 부서별 자동 분류를 강제하지 않는다.

### GOV-003 — work review gate
대표님과 관리자는 진행 업무를 자유롭게 대화할 수 있지만 `working/CURRENT_WORK.md`에 쓰기 전 `/업무검토`를 실행한다. 업무검토는 최신 `main`의 공식 회사 방향, 확정 요구사항, 현재 업무판과 함께 관련 미반영 아이디어·문제를 확인하는 읽기 전용 단계다.

### GOV-004 — pending idea/problem index
미반영 아이디어와 문제는 `records/PENDING_INDEX.md`에 제목·요약·키워드·경로만 경량 색인한다. `/업무검토`는 이 인덱스를 먼저 보고 현재 업무와 직접 관련된 기록만 읽는다. 저장 기록 전체를 매번 훑지 않는다.

### GOV-005 — pending index maintenance
`/아이디어저장`과 `/문제저장`이 실제 저장에 성공하면 `records/PENDING_INDEX.md`도 갱신한다. 관리자 `/아이디어반영` 또는 `/문제반영` 성공 시 해당 항목을 pending index에서 제거한다. 실제 기록 저장/반영이 실패하면 인덱스만 먼저 변경하지 않는다.

### GOV-006 — work review result
업무검토 결과는 `PASS / 공유 가능`, `REVISION / 수정 필요`, `HOLD / 보류`로 구분한다. `PASS`는 진행업무판에 공유 가능하다는 뜻이며 회사 공식 요구사항 확정을 의미하지 않는다.

### GOV-007 — shared work update
`/업무공유`는 같은 대화에서 가장 최근 `/업무검토`가 PASS인 경우에만 실행한다. 검토 후 핵심 내용이 실질적으로 바뀌면 다시 검토한다. 공유 시 기존 `CURRENT_WORK.md`를 읽고 새 내용·변경·삭제·보류·완료를 반영해 파일 전체를 단일 최신판으로 갱신한다.

### GOV-008 — admin confirmation
`CURRENT_WORK.md`의 내용은 자동으로 공식 요구사항이 되지 않는다. 관리자가 `/업무확정`으로 확정한 항목만 공식 소스와 요구사항으로 승격한다.

### GOV-009 — idea/problem save
대표님과 관리자 모두 아이디어·문제를 저장할 수 있다. 저장 기록은 공식 요구사항이 아니다.

### GOV-010 — reflection authority
아이디어·문제의 공식 반영과 업무 확정은 관리자만 수행한다.

### GOV-011 — attachments
아이디어·문제 저장 또는 업무공유 메시지에 관련 첨부파일이 있으면 가능한 경우 원본을 `materials/originals/`에 보존하고 별도로 LLM용 Markdown 정제본을 `materials/normalized/`에 만든다. 기록 또는 CURRENT_WORK는 필요한 경우 정제본 경로를 연결한다.

업무 첨부 경로는 다음을 사용한다.

```text
materials/originals/<author-role>/work/YYYY-MM-DD/<original-file>
materials/normalized/<author-role>/work/YYYY-MM-DD/<original-file>.md
```

### GOV-012 — selective read
평소 LLM은 공식 소스, 프로젝트 저장소 레지스트리, `CURRENT_WORK.md`만 읽는다. 미반영 아이디어·문제는 업무검토 시 `PENDING_INDEX.md`로 관련성을 먼저 판단한 뒤 필요한 기록만 읽는다. 정제자료는 관련 기록이 연결하거나 사용자가 요구할 때만 읽고, 원본은 명시적인 원본 확인 또는 정제본 오류가 있을 때만 읽는다.

### GOV-013 — status distinction
공식 기준과 진행·협의 중 내용이 다르면 답변에서 반드시 `현재 확정 기준`과 `현재 협의/진행 중`을 구분한다.

### GOV-014 — current official context during review
업무검토는 과거 대화 기억에 의존하지 않고 최신 `main`의 `COMPANY_OS.md`, `PRODUCT_REQUIREMENTS.md`, `PROJECT_REPOSITORIES.md`, `CURRENT_WORK.md`, `PENDING_INDEX.md`와 직접 관련된 공식 부서 문서를 기준으로 수행한다.

### GOV-015 — project repository registry
현재 회사와 연결된 GitHub 저장소는 `llm-source/PROJECT_REPOSITORIES.md`에서 관리한다. 프로젝트의 실제 개발 진척·구현 여부·최근 변경이 필요한 질문에서는 레지스트리 설명만으로 답하지 않고 대상 저장소의 최신 `main`을 직접 확인한다.

### GOV-016 — change existing official requirement
기존 공식 기준의 변경안도 바로 공식 문서를 수정하지 않는다. 먼저 업무 대화 → `/업무검토` → PASS → `/업무공유`로 CURRENT_WORK에 변경 협의안으로 올리고, 이후 관리자 `/업무확정`으로 공식 기준을 교체한다.

### GOV-017 — change history
확정 요구사항의 추가·교체·삭제·중요한 의미 변경은 `docs/requirement-changelog.md`에 기록한다.

세부 업무검토·업무공유 규칙은 `llm-source/WORK_GOVERNANCE.md`를 따른다.
