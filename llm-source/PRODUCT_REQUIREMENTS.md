# Product Requirements

- Repository: `jintonic1010/miracle_company_private`
- Branch: `main`
- Updated: 2026-09-06
- Authority: official confirmed requirements
- Release: `GOV-20260906-01`

현재 확정된 요구사항이다. 아이디어 저장·업무 공유·자료 정제만으로 변경되지 않는다. 2026-09-06 이전판은 `archive/migrations/2026-09-06/PRODUCT_REQUIREMENTS.before.md`에 보존한다.

## Company Core

### CORE-001 — n8n backbone
회사 전체 연결·자동화 뼈대는 n8n을 사용한다.
### CORE-002 — department model
ERP/재고·물류, 시장리서치, 마케팅, CS, 세무·법률 부서 시스템을 가진다.
### CORE-003 — ERP operational core
ERP는 상품·SKU·재고·주문·판매·고객·구매·물류 운영 데이터의 핵심 원장이다.

## ERP / Commerce Integration

### ERP-001
ERP 기반은 ERPNext 또는 InvenTree 중 비교 후 확정한다. 아직 미선택이다.
### ERP-002
카페24와 ERP는 실제 API 허용 범위에서 판매·상품·재고·주문·고객·물류 데이터를 IN/OUT 연결한다.
### ERP-003
네이버 스마트스토어와 ERP는 실제 API 허용 범위에서 필요한 데이터를 IN/OUT 연결한다.
### ERP-004
Google Shopping/Merchant/Ads 등 API는 역할별 실제 기능을 조사한 뒤 ERP와 필요한 IN/OUT 연결을 구성한다.
### ERP-005
해외 공급처 API의 필요한 상품·SKU·가격·재고·공급 데이터를 ERP로 입력한다.
### ERP-006
고객·주문·구매이력은 법적·보안 경계 안에서 ERP/운영 데이터 계층에 연결한다.

## Department Data Exchange

### DEPT-001
ERP와 시장리서치는 필요한 데이터를 양방향 교환한다.
### DEPT-002
ERP와 마케팅은 필요한 데이터를 양방향 교환한다.
### DEPT-003
ERP와 CS는 필요한 데이터를 양방향 교환한다.
### DEPT-004
ERP와 세무·법률은 필요한 데이터를 양방향 교환한다.

## Data / Integration

### DATA-001
상품·SKU/옵션·주문·고객·공급처는 내부 기준 ID와 채널별 ID 매핑을 가진다.
### DATA-002
외부 채널·공급처·ERP의 읽기/쓰기/Webhook/인증/rate-limit 실제 명세를 구현 전에 만든다.
### DATA-003
n8n은 연결·자동화를 담당하고 ERP 운영 원장을 대체하지 않는다.
### DATA-004
고객 개인정보·운영 DB·인증정보·API 키·비밀번호·토큰·SSH 개인키는 GitHub에 저장하지 않는다.

## Knowledge / LLM Governance

### GOV-001 — three roles
작성·협업 역할은 representative, admin, assistant다. 프로젝트에 고정된 자기 역할 하나만 사용한다. 품의 최종 결재자는 admin(Jin)이다. 일반 직원 프로젝트와 혼동하지 않는다.
### GOV-002 — single work source
개별 `work/items/<work_id>.json`을 업무 상태 원장으로 사용한다. CURRENT_WORK와 assistant/30-working은 파생 조회판이다. 동일 상태를 독립적으로 이중 작성하지 않는다.
### GOV-003 — review gate
공유·상신 전 최신 공식 기준·현재 업무·관련 미반영 기록을 실제로 검토한다. `/업무검토`는 읽기 전용이다.
### GOV-004 — pending selection
`records/PENDING_INDEX.md`에서 관련 기록을 선택한다. 평소 전체 원문을 자동 조회하지 않는다.
### GOV-005 — atomic index maintenance
기록과 pending index를 같은 변경 단위로 갱신한다. 부분 실패를 전체 성공으로 보고하지 않는다.
### GOV-006 — review result
PASS/REVISION/HOLD를 구분한다. PASS는 공유·상신 적합성 검토이지 회사 확정이나 관리자 결재가 아니다.
### GOV-007 — shared update
`/업무공유`는 유효한 검토 후 원장을 갱신하고 조회판을 재생성한다. 본질적 변경·근거 변경·main 충돌 시 재검토한다. 원문·이력을 보존한다.
### GOV-008 — policy confirmation
`/업무확정`은 관리자 전용 회사 기준 변경이다. 일반 결과물 수락은 별도 결재로 기록하며 자동으로 공식 요구사항을 바꾸지 않는다.
### GOV-009 — saved input
세 역할은 허용 범위에서 아이디어·문제를 저장할 수 있다. 대표님 요청은 입력이며 지출·게시·공식화 승인으로 확대하지 않는다.
### GOV-010 — reflection authority
공식 반영·역할 변경·승인 규칙 변경은 관리자만 수행한다. 부사수는 품의를 상신하되 자체 확정하지 않는다.
### GOV-011 — source preservation
실제 확보한 비민감 원본과 정제본을 분리한다. 기존 materials 경로는 보존하며 새 자료는 source_id로 연결한다. 원본 미확보는 missing, 링크만 확인한 것은 reference_only로 표시한다.
### GOV-012 — selective reads
공식 기준·현재 업무를 우선 읽고 필요한 지시·플레이북·정제본·원본만 확장 조회한다. 사용자가 저장소 감사·전처리를 명시한 경우 그 범위의 전수 점검을 할 수 있다.
### GOV-013 — distinguish authority
현재 확정 기준, 협의/진행, 미반영 제안, 미검증 주장을 분리한다.
### GOV-014 — current main
중요 판단·쓰기 전 최신 main을 조회한다. 과거 대화나 첨부 스냅샷을 최신 상태로 간주하지 않는다.
### GOV-015 — implementation registry
PROJECT_REPOSITORIES는 위치 정보다. 실제 코드·개발·최근 변경은 대상 저장소에서 확인한다.
### GOV-016 — explicit admin change
공식 변경은 검토 → 변경안 기록 → 관리자 명시 승인 → 저장·재조회 순서다. 관리자가 현재 메시지에서 범위가 명확한 검토·최종 반영을 함께 명시하면 한 작업에서 순서대로 수행할 수 있다. 슬래시 입력 부재만으로 명백한 관리자 반영 요청을 거부하지 않는다. 일반 대화에서 자동 저장·확정하지 않는다.
### GOV-017 — history
요구사항의 추가·교체·삭제·중요한 의미 변경은 changelog와 해당 결재 기록에 남긴다.
### GOV-018 — normalization
원본 의미·단위·조건·시점·수치를 보존한다. 전처리, 조사, 해석, 제안을 분리하고 원본 버전·위치·변환 이력을 남긴다.
### GOV-019 — evidence
핵심 주장과 실제 열어 확인한 근거를 연결한다. 영상 미시청을 시청으로, 조회수를 인과관계로, 내부 일부 판매를 전체 시장 순위로 표현하지 않는다.
### GOV-020 — scoped decisions
결재는 업무·품의·결과물 버전과 조사/제작/결과수락/게시/지출/정책변경 범위에 연결한다. 수정·취소·조건은 새 기록으로 남긴다.
### GOV-021 — approval provenance
부사수의 '승인받았다'는 전달은 승인 주장일 뿐이다. 실제 관리자 결재 원문과 대상 버전을 확인하기 전 승인 상태로 바꾸지 않는다.
### GOV-022 — execution truth
승인, GitHub 저장, 제작, 공개, 통합 도구 연결을 각각 검증한다. 실패·불확실 결과를 완료로 쓰지 않는다.
### GOV-023 — main and status
main에는 초안·미반영 기록도 공존할 수 있다. main에 있다는 사실만으로 회사 공식 정책 또는 게시 승인으로 보지 않는다.
### GOV-024 — implementation boundary
문서 지침은 기술적 접근제어가 아니다. 계정별 권한·승인 인증·자동 실행·알림은 별도 구현·검증하며 미구현을 구현됐다고 보고하지 않는다.
