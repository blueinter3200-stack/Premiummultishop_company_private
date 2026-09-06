# Work Governance

- Updated: 2026-09-06
- Release: GOV-20260906-02
- Authority: official

## 흐름

입력/요청 → 의미 보존 전처리 → **기록 종류 분류** → 필요한 ID 생성 → 최신 회사 기준·관련 미반영 기록 검토 → 수행/초안 → 근거 포함 품의 → 관리자 결재 → 승인 범위의 실행 → 실제 결과 확인.

역할, 사람, 방법, 지시, 상태, 결과, 결재를 분리한다. 역할 파일에 모든 업무를 누적하지 않는다. 반복되는 수행 방법은 플레이북, 기간성·1회성 요청은 directive, 권한 변경은 관리자 승인된 role/rule 변경이다.

## 검토

`/업무검토`는 읽기 전용이다. FILE_MAP, ACTOR_REGISTRY, COMPANY_OS, PRODUCT_REQUIREMENTS, PROJECT_REPOSITORIES, CURRENT_WORK, PENDING_INDEX와 직접 관련된 부서·업무·기록·정제자료를 최신 main에서 읽는다. 구현 사실이 중요할 때만 대상 개발 저장소를 실제 확인한다.

현재 공식 기준과 충돌, 중복, 미반영 경고, 제외·보류 사항, 미검증 수치, 데이터 민감성, 주체·범위·다음 행동, 근거의 실제 접근 여부를 확인한다.

## 검토 라우팅

검토 결과에는 `classification`과 `recommended_next_action`을 포함한다.

- `idea`: 가능성·제안·가설. `/아이디어저장` 권장.
- `problem`: 장애·리스크·이상 발견. `/문제저장` 권장.
- `work`: 실제 실행 의도·범위·다음 행동이 있는 업무. `/업무공유` 또는 `/업무접수`.
- `mixed`: 아이디어와 조사·실행 요청이 함께 있음. 아이디어와 업무를 별도 ID로 저장·연결.
- `policy_change`: 회사 기준 변경 후보. 관리자 확정 전 변경안 단계 유지.

`PASS`는 자동 `/업무공유` 허가가 아니다. 순수 아이디어나 문제를 `/업무공유`하려 하면 `ROUTING_MISMATCH`로 중단하고 적합한 저장을 안내한다.

대표님의 탐색 표현(`이거 어때`, `가능하지 않을까`, `검토해봐`)만으로 실행 업무를 만들지 않는다. 반대로 `조사해서 기획안 만들어봐`, `담당해서 진행해`처럼 수행 요청이 명확하면 관련 아이디어와 조사/실행 업무를 별도 객체로 연결할 수 있다.

## 접수·공유

대표님 요청은 `assistant/20-directives/from-representative/`, Jin 요청은 `assistant/20-directives/from-jin/`에 보존하고 work_id로 연결한다. 요청 발언자, 접수자, 정제자, 수행자, 결재자를 actor_id로 분리해 남긴다. 아이디어만 저장해 달라는 요청을 자동 업무 배정으로 바꾸지 않는다.

검토된 실제 업무 공유는 `work/items/<id>.json`의 revision을 갱신하고 회사·부사수 조회판을 함께 생성한다. 복합 요청은 검토를 먼저 실행해 통과한 범위만 저장한다.

## 업무 원장과 조회판

`work/items/`가 상태 원본이다. `working/CURRENT_WORK.md`, `assistant/30-working/ACTIVE.md`, `BLOCKED.md`, `DECISION_NEEDED.md`는 파생 화면이다. 화면만 수정해 승인·상태를 바꾸지 않는다.

아이디어를 조사하는 업무가 완료돼도 원 아이디어를 reflected/approved로 바꾸지 않는다. 문제를 저장했다고 관련 업무를 자동 blocked로 바꾸지 않는다. 실제 영향이 있을 때만 work 원장을 별도로 갱신한다.

## 품의와 승인

품의에는 요청 출처, 내부·외부 근거, 실제 확인 범위, 판단·선택 이유, 결과물 버전, 미확인·위험, 승인받을 범위를 포함한다. 일반 업무 결과 승인으로 COMPANY_OS나 PRODUCT_REQUIREMENTS를 자동 수정하지 않는다.

대표님 지시와 Jin 지시가 충돌하면 원문을 보존하고 conflicting 항목을 blocked/결정대기로 올린다. 최종 조정자는 관리자다.

## 아이디어·문제 기록

새 기록은 `record_id`와 `author_id`를 가진다.

- idea: `I-YYYYMMDD-NNN`
- problem: `P-YYYYMMDD-NNN`
- author: `ACT-NNN`

새 경로:
- `records/ideas/<actor_id>/...`
- `records/problems/<actor_id>/...`

세 역할 모두 자기 actor_id로 아이디어·문제를 저장할 수 있다. 기존 role 기반 경로의 6개 아이디어는 참조 안정성을 위해 이동하지 않고 PENDING_INDEX와 normalized metadata에 actor_id를 연결한다.

관리자가 특정 항목의 공식 채택을 지시한 경우에만 기록 상태·공식 소스·pending index를 함께 처리한다. 실제 해결 증거 없이는 문제를 resolved로 바꾸지 않는다.

## 저장·실행

APPROVAL_GOVERNANCE와 TOOL_EXECUTION을 따른다. 관리자 승인과 main 반영·게시 완료를 분리한다. 변경 실패 시 pending index나 조회판만 먼저 고치지 않는다.
