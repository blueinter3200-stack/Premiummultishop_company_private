# Product Requirements

- Repository: `jintonic1010/miracle_company_private`
- Branch: `main`
- Updated: 2026-09-06
- Authority: official confirmed requirements
- Release: `GOV-20260906-03`

현재 확정된 요구사항이다. 아이디어 저장·업무 공유·자료 정제만으로 변경되지 않는다.

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
협업 역할은 representative, admin, assistant다. 프로젝트에 고정된 자기 역할 하나만 사용한다. 품의 최종 결재자는 admin/Jin이다.
### GOV-002 — single work source
개별 `work/items/<work_id>.json`을 업무 상태 원장으로 사용한다. CURRENT_WORK와 assistant/30-working은 파생 조회판이다.
### GOV-003 — review gate
공유·상신 전 최신 공식 기준·현재 업무·관련 미반영 기록을 실제로 검토한다. `/업무검토`는 읽기 전용이다.
### GOV-004 — pending selection
`records/PENDING_INDEX.md`에서 관련 기록을 선택한다. 평소 전체 원문을 자동 조회하지 않는다.
### GOV-005 — atomic index maintenance
기록과 pending index를 같은 변경 단위로 갱신한다. 부분 실패를 전체 성공으로 보고하지 않는다.
### GOV-006 — review result
PASS/REVISION/HOLD를 구분한다. PASS는 내용 검토 통과이지 자동 `/업무공유` 승인이나 회사 확정·관리자 결재가 아니다.
### GOV-007 — shared update
`/업무공유`는 실제 실행 중이거나 실행하기로 명확히 요청된 업무에만 사용한다. 유효한 검토 후 원장을 갱신하고 조회판을 재생성한다.
### GOV-008 — policy confirmation
`/업무확정`은 관리자 전용 회사 기준 변경이다. 일반 결과물 수락은 별도 결재로 기록한다.
### GOV-009 — saved input
등록된 세 actor는 허용 범위에서 아이디어·문제를 저장할 수 있다. 대표님 요청은 지출·게시·공식화 승인으로 확대하지 않는다.
### GOV-010 — reflection authority
공식 반영·역할 변경·승인 규칙 변경은 관리자만 수행한다. 부사수는 품의를 상신하되 자체 확정하지 않는다.
### GOV-011 — source preservation
실제 확보한 비민감 원본과 정제본을 분리한다. 원본 미확보는 missing, 링크만 확인한 것은 reference_only로 표시한다.
### GOV-012 — selective reads
공식 기준·현재 업무를 우선 읽고 필요한 지시·플레이북·정제본·원본만 확장 조회한다.
### GOV-013 — distinguish authority
현재 확정 기준, 협의/진행, 미반영 제안, 미검증 주장을 분리한다.
### GOV-014 — current main
중요 판단·쓰기 전 최신 main을 조회한다. 과거 대화나 첨부 스냅샷을 최신 상태로 간주하지 않는다.
### GOV-015 — implementation registry
PROJECT_REPOSITORIES는 위치 정보다. 실제 코드·개발·최근 변경은 대상 저장소에서 확인한다.
### GOV-016 — explicit admin change
관리자가 범위가 명확한 검토·최종 반영을 현재 메시지에서 함께 명시하면 한 작업에서 순서대로 수행할 수 있다. 일반 대화에서 자동 저장·확정하지 않는다.
### GOV-017 — history
요구사항의 추가·교체·삭제·중요한 의미 변경은 changelog와 해당 결재 기록에 남긴다.
### GOV-018 — normalization
원본 의미·단위·조건·시점·수치를 보존한다. 전처리, 조사, 해석, 제안을 분리한다.
### GOV-019 — evidence
핵심 주장과 실제 열어 확인한 근거를 연결한다. 영상 미시청을 시청으로, 조회수를 인과관계로 표현하지 않는다.
### GOV-020 — scoped decisions
결재는 업무·품의·결과물 버전과 조사/제작/결과수락/게시/지출/정책변경 범위에 연결한다.
### GOV-021 — approval provenance
부사수의 '승인받았다'는 전달은 승인 주장일 뿐이다. 실제 관리자 결재 원문과 대상 버전을 확인한다.
### GOV-022 — execution truth
승인, GitHub 저장, 제작, 공개, 통합 도구 연결을 각각 검증한다.
### GOV-023 — main and status
main에는 초안·미반영 기록도 공존할 수 있다. main에 있다는 사실만으로 회사 공식 정책 또는 게시 승인으로 보지 않는다.
### GOV-024 — implementation boundary
문서 지침은 기술적 접근제어가 아니다. 계정별 권한·승인 인증·자동 실행·알림은 별도 구현·검증한다.
### GOV-025 — stable actor identity
사람/행위자는 `llm-source/ACTOR_REGISTRY.json`의 `ACT-NNN`으로 식별한다. actor_id는 재사용하지 않고 역할 변경과 분리한다. 사람 교체 시 새 actor_id를 발급한다.
### GOV-026 — per-actor record ownership
새 아이디어·문제와 관련 자료는 `actor_id` 경로에 저장하고 record_id와 actor_id를 함께 남긴다. 기존 role 기반 기록은 이동하지 않고 actor registry와 normalized metadata로 소유자를 연결한다.
### GOV-027 — review routing
`/업무검토`는 대상을 `idea / problem / work / mixed / policy_change`로 분류하고 다음 저장 동작을 추천한다. 순수 아이디어는 `/아이디어저장`, 순수 문제는 `/문제저장`, 실제 실행 범위가 있는 업무만 `/업무공유`한다.
### GOV-028 — assistant idea/problem records
부사수도 자기 actor_id로 아이디어와 문제를 저장할 수 있다. 저장만으로 현재 업무·공식 정책·승인이 바뀌지 않는다. 현재 업무 중 발견한 문제는 `related_work_id`로 연결하고 실제 영향이 있을 때만 work 상태를 별도로 변경한다.
### GOV-029 — idea and research work separation
아이디어 자체와 아이디어를 조사·검증하는 업무는 서로 다른 객체다. 대표님이 아이디어와 함께 조사·기획을 명시하면 아이디어 기록과 조사 work_id를 연결할 수 있으나 조사 완료가 아이디어 채택을 의미하지 않는다.

### GOV-030 — local command discovery
트리거 이름·용도·추천 조건·자기 권한을 프로젝트 지침과 PROJECT_COMMON/ROLE에 둔다. 명령 추천·설명·대화 내 출력은 GitHub 없이 한다. 최신 사실·실제 원격 실행은 최신 정본을 확인한다.
### GOV-031 — plain command names
/업무점검 <대상>, /품의서작성, /품의서승인을 정식 이름으로 쓴다. 구명령은 동일 권한의 별칭으로 유지하고 새 이름만 추천한다. 점검·최종 승인·공식 반영은 관리자 전용이다.
### GOV-032 — durable requests
명확한 회사 업무 배정·수행·지속 지시는 원문·요청자 actor·R-ID로 보존하여 관련 업무에서 다시 읽는다. 단순 질문·탐색·읽기 전용 명령·저장 금지는 자동 기록하지 않는다. 요청 보존은 승인·정책 확정이 아니다.
### GOV-033 — detailed workflows
아이디어·문제·업무·요청·품의·점검·결재의 상세 절차와 실패 처리를 llm-source/workflows에 유지하고 LLM_RUNTIME에서 연결한다. 로컬 추천과 원격 실행 절차를 분리한다.
### GOV-034 — inspection integrity
업무점검은 대상별 읽기 전용이다. 전체 기록과 pending 건수를 구분하고 legacy 경로·정제본 중복을 대조한다. 기록 밖의 실제 행동을 추정하지 않는다.
### GOV-035 — submission and decision
품의서작성은 근거·버전·요청 범위의 승인대기 저장이며 본문만 요청은 미저장이다. 품의서승인은 관리자만 특정 버전·범위를 결정하며 저장·게시·지출 실행과 구분한다.
