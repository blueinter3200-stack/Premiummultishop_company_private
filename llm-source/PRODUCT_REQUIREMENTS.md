# Product Requirements

- Repository: `blueinter3200-stack/Premiummultishop_company_private`
- Branch: `main`
- Updated: 2026-09-07
- Authority: official confirmed requirements
- Release: `GOV-20260907-02`

현재 확정된 요구사항이다. 아이디어 저장·업무 요청·자료 정제만으로 변경되지 않는다.

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
협업 역할은 representative, admin, assistant다. 프로젝트에 고정된 자기 역할 하나만 사용한다. 최종 결재자는 admin/Jin이다.

### GOV-002 — single work source
개별 `work/items/<work_id>.json`을 업무 상태 원장으로 사용한다. CURRENT_WORK, WORK_STATUS_MAP과 assistant/30-working은 파생 조회판이다.

### GOV-003 — review before submission
업무요청·업무계획안 제출 전 최신 공식 기준·현재 업무·관련 기록/과거 결정을 검토한다. `/업무검토`는 읽기 전용이며 전달 영수증도 쓰지 않는다.

### GOV-004 — pending selection
`records/PENDING_INDEX.md`에서 관련 기록을 선택한다. 평소 전체 원문을 자동 조회하지 않는다.

### GOV-005 — atomic index maintenance
기록과 pending index를 같은 변경 단위로 갱신한다. 부분 실패를 전체 성공으로 보고하지 않는다.

### GOV-006 — review is not authorization
PASS/REVISION/HOLD를 구분한다. PASS는 제출 적합성 검토이지 자동 저장·관리자 승인·업무 착수 허가가 아니다.

### GOV-007 — approved work updates
`/업무업데이트`는 관리자·배정 부사수만 기존 W-ID의 실제 수행·상태·결과를 갱신한다. 계획 준비와 승인된 본 작업을 구분하고 새로운 업무·승인·범위 확대를 만들지 않는다.

### GOV-008 — policy confirmation
`/기준확정`은 관리자 전용 회사 기준 변경이다. 업무 채택·작업 배정·계획 결의·일반 결과물 수락과 별개다.

### GOV-009 — saved input
등록된 세 actor는 허용 범위에서 아이디어·문제를 저장할 수 있다. 대표님 요청은 지출·게시·공식화 승인으로 확대하지 않는다.

### GOV-010 — reflection authority
공식 반영·역할 변경·승인 규칙 변경은 관리자만 수행한다. 부사수는 계획안을 제출하되 자체 확정하지 않는다.

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
결정은 대상 R/SUB/결과물의 내용 버전과 업무채택/계획준비/계획실행/조사/제작/결과수락/게시/지출/정책변경 범위에 연결한다. 정확한 범위의 과거 승인은 새 버전에 자동 적용하지 않는다.

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
`/업무검토`는 idea/problem/work/mixed/policy_change를 구분한다. 아이디어·문제는 각 기록으로, 유효 PASS인 실제 후보만 `/업무요청` 또는 상세 `/업무계획안제출`로 제출한다.

### GOV-028 — assistant idea/problem records
부사수도 자기 actor_id로 아이디어와 문제를 저장할 수 있다. 저장만으로 현재 업무·공식 정책·승인이 바뀌지 않는다. 현재 업무 중 발견한 문제는 `related_work_id`로 연결하고 실제 영향이 있을 때만 work 상태를 별도로 변경한다.

### GOV-029 — idea and adopted work separation
아이디어 I와 조사 요청 R은 별개이며 연결 가능하다. W 등록은 관리자 업무 채택 승인 뒤다. 배정과 계획 실행 권한은 별도로 확인하며 조사 완료가 아이디어 채택을 뜻하지 않는다.

### GOV-030 — local command discovery
트리거 이름·용도·추천 조건·자기 권한을 프로젝트 지침과 PROJECT_COMMON/ROLE에 둔다. 명령 추천·설명·대화 내 출력은 GitHub 없이 한다. 최신 사실·실제 원격 실행은 최신 정본을 확인한다.

### GOV-031 — explicit decisions without aliases
정식 명령은 TRIGGER_REGISTRY의 17개다. 업무결정/업무계획안결의에는 승인·수정요청·보류·반려를 명시한다. 기본 승인은 없고 구명령·별칭은 실행하지 않는다. 과거 원문은 보존한다.

### GOV-032 — durable requests
명확한 회사 업무 배정·수행·지속 지시는 원문·요청자 actor·R-ID로 보존하여 관련 업무에서 다시 읽는다. 단순 질문·탐색·읽기 전용 명령·저장 금지는 자동 기록하지 않는다. 요청 보존은 승인·정책 확정이 아니다.

### GOV-033 — detailed workflows
아이디어·문제·업무·요청·계획안·배정·점검·결재의 상세 절차와 실패 처리를 llm-source/workflows에 유지하고 LLM_RUNTIME에서 연결한다. 로컬 추천과 원격 실행 절차를 분리한다.

### GOV-034 — inspection integrity
업무점검은 대상별 읽기 전용이다. 전체 기록과 pending 건수를 구분하고 legacy 경로·정제본 중복을 대조한다. 기록 밖의 실제 행동을 추정하지 않는다.

### GOV-035 — request and execution plan
업무요청은 일의 제안이고 업무계획안제출은 같은 R 또는 배정된 W에 대한 실행방법 제출이다. W 없는 사전 계획안도 가능하다. 계획 제출은 착수 승인·자동 담당 배정이 아니다.

### GOV-036 — adoption assignment execution gates
관리자만 업무 채택을 결정하여 W를 생성/연결한다. 담당 배정은 별도 ASG 사건이고 본 작업은 정확한 계획 버전의 실행 결의와 현재 담당이 일치해야 한다. 기존 W/원문/결정은 일괄 재작성하지 않는다.

### GOV-037 — immutable decisions and views
원문 파일은 상태별로 이동·삭제하지 않는다. 보류→승인/반려 등은 새 D로 연결한다. 상태함은 동일 대상·내용 버전·범위의 최신 유효 결정에서 파생한다. 승인 변경은 명시적 재결재다.

### GOV-038 — actor decision notifications
새 결정 변화는 요청자·계획안 작성자와 직접 관련 담당자의 N 이벤트·INBOX로 연결한다. 같은 사건은 중복 생성하지 않고 과거 결정을 소급 방송하지 않는다. 생성·표시·사용자 확인은 별개다.

### GOV-039 — bounded notification checks
실제 회사 업무 시작·재개·필요 트리거·명시적 최신 문의에서 자기 INBOX만 선택 조회한다. 잡담/로컬 출력·매 메시지 반복 조회는 하지 않는다. 핵심 실행 전 최신 대상 승인은 별도로 확인한다.

### GOV-040 — receipt and read-only boundary
실제 표시 후 허용된 쓰기 상황에서만 전달 영수증을 남긴다. fetch만으로 읽음 처리하지 않는다. 읽기 전용/저장 금지는 영수증도 쓰지 않고 대화 내에서만 중복을 막는다. 영속 기록 없이 새 대화의 중복 방지를 보장하지 않는다.

### GOV-041 — relevant historical decisions
같은 R/SUB의 현재 결정·사유와 직접 중복되는 과거 건만 검토한다. 이전 사유·현재 차이·해소 근거를 보고한다. 옛 반려는 영구 금지가 아니며 유효한 지속 제한만 별도 적용한다.

### GOV-042 — plan command names
계획 제출은 `/업무계획안제출`, 관리자 결의는 `/업무계획안결의`로 통일한다. 이전 품의서 명령은 호환하지 않고 과거 객체·원문만 보존한다.

### GOV-043 — oral representative requests
대표님이 부사수에게 구두로 직접 요청하면 부사수는 source_type=reported_oral_request로 보존·검토 후 계획안을 바로 제출할 수 있다. 선행 업무요청·업무채택 승인을 강제하지 않는다. 요청자 ACT-002와 기록/제출자 ACT-003, 미독립검증 여부를 구분한다.

### GOV-044 — proxy record ownership
대리 기록은 ACT-003 기록 영역에 저장하고 원 요청자는 ACT-002로 보존한다. 다른 대표 요청을 읽거나 직접 대표 발언·승인을 사칭할 권한을 추가하지 않는다. 알려진 실제 R는 연결하고 중복을 방지한다.

### GOV-045 — administrator assignments
업무결정 승인과 담당 배정은 별개다. ACT-001 직접 수행·ACT-003 위임·담당 null 모두 가능하다. 나중 배정/재배정은 같은 W에 새 ASG로 연결하고 관리자 근거·승인된 지시 요약·범위·다음 행동을 보존한다.

### GOV-046 — assignment delivery and persistence
새 배정·재배정은 해당 수신자에게 사건별 최초 알림을 생성한다. 대표님 구두 지시를 알고 있어도 공식 관리자 배정은 별도다. 전달한 알림은 반복 독촉하지 않으며 미완료 지시는 자기 작업지시 조회판에 계속 남긴다.

### GOV-047 — preparation not substantive execution
계획안 작성에는 받은 자료 정리·검토·방법 작성이 포함된다. 본 조사·제작·개발·게시·지출은 승인된 계획·현재 배정·정확한 범위 확인 후에만 한다. 계획에 필요한 본 조사도 먼저 해당 범위를 제출한다.

### GOV-048 — combined decision without duplicate work
아직 결정 없는 요청의 직접 제출 계획안은 관리자가 업무채택·담당·계획실행을 명시하여 한 번에 연결할 수 있다. 기존 보류·반려를 계획안으로 우회하지 않는다. 같은 R는 한 W를 재사용하고 담당/내용 변경에는 실행승인을 재확인한다.

### GOV-049 — assignment-scoped visibility
대표님이 관리자에게 직접 제출한 미배정 요청은 부사수의 자동 조회/할 일 대상이 아니다. 부사수는 자기 기록·계획안·배정된 지시 요약과 승인된 관련 자료만 읽는다. 인사·개인화·관리자 비공개 메모를 전달하지 않는다. 폴더 구분은 실제 계정 ACL을 대체하지 않는다.

### GOV-050 — company-wide work status map
`/업무진행현황`은 admin·representative·assistant 모두가 사용하는 읽기 전용 명령이며 대상 생략 시 회사 전체를 `working/WORK_STATUS_MAP.json`에서 조회한다. 공용 요약은 공유하되 비공개 요청 원문·상세 결재·개인자료 권한은 확대하지 않는다.

### GOV-051 — atomic status projection maintenance
업무요청·업무결정·배정/재배정·업무계획안 제출/결의·업무업데이트·완료·관련 요청 변경을 저장할 때 정본과 `WORK_STATUS_MAP`을 같은 검증된 변경 집합에서 갱신한다. 맵은 정본이나 승인 증거가 아니다.

### GOV-052 — direct administrator work adoption
ACT-001이 기존 R-ID 없이 `/업무결정 승인`과 구체적인 새 업무·담당을 함께 명시하면 실제 원문을 ACT-001 요청으로 보존하고 최신 검토→결정→W→명시된 담당 ASG/알림→업무현황 맵을 중복 없이 한 처리로 연결할 수 있다. 기존 요청이 대상이면 원 R-ID와 요청자를 보존한다.

### GOV-053 — cross-repository implementation references
회사 업무 원장과 구현 저장소는 별도 정본이다. W와 공용 맵에는 등록된 관련 저장소의 repo/branch/commit 또는 PR·실제 확인시점·근거만 연결하며, 커밋·PR을 배포·실행 승인·업무완료로 해석하지 않는다.