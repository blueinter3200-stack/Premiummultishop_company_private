# Approval Governance — GOV-20260906-03

최종 결재자: ACT-001 / admin / Jin. 대표님은 방향·요청, 부사수는 조사·실무·품의서 작성이다. 누구도 대표 발언이나 부사수의 전달로 관리자 결재를 대체하지 않는다.
정식 명령은 /품의서승인, /결과승인, 회사 기준 변경은 /업무확정·/아이디어반영·/문제반영이다. 상세 절차는 `llm-source/workflows/ADMIN_REFLECTION_WORKFLOW.md`다.

## 범위

research(조사), production(제작), deliverable(결과물 수락), publication(게시 대상/문구/일정/버전), expenditure(금액/통화/기간/사용처), policy_change(회사 기준 변경)를 구분한다. 여러 범위를 한 번에 승인할 수 있으나 명시해야 한다. 초안 수락을 게시·추가 비용·영구 규칙 변경으로 확대하지 않는다.

## 기록

decision_id, work_id, submission_id/revision, artifact_refs/version/hash, requested_scopes, granted_scopes, decision, approver_actor_id, approver_role/name, approval_source, principal_verification, decided_at, conditions, recheck_conditions를 기록한다. 요청 R-ID가 있으면 request_refs도 연결한다.
승인·수정요청·보류·반려를 구분한다. 승인 아닌 결정의 granted_scopes는 비운다. 구 /품의승인은 새 명령의 동일 권한 별칭이다.
다른 사람의 “Jin 승인”은 approval_claim이다. 실제 관리자 발언 또는 확인 가능한 리뷰·서명과 정확한 대상 버전을 확인하지 못하면 pending이다. 역할 기반 대화 결재를 독립 계정 인증으로 과장하지 않는다.

## 변경·실행

영상·상품·가격·자막·음원·게시대상·비용 또는 근거가 달라지면 영향 범위를 재결재한다. 같은 URL도 내용 버전이 다르면 승인본이 아니다. 취소·수정은 새 결정으로 연결하고 과거 결재를 덮어쓰지 않는다. 자기 참조 해시를 만들지 않는다.
결재와 실행은 별개다. 관리자 승인 → 범위 확인 → 명확히 요청된 실행 → 실제 결과·commit/파일/게시 재조회 순서를 지킨다. 승인됐어도 저장 실패는 approved/failed다. 먼저 실행하고 사후 품의하지 않는다.
품의서 작성은 승인대기 기록이지 승인·알림·게시가 아니다. 일반 결과물 수락은 회사 정책으로 승격하지 않는다. 부사수는 확인된 승인 범위의 허용 작업만 수행하고 공식 역할·정책 반영은 관리자만 한다.
