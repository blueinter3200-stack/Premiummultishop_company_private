# Approval Governance — 관리자 결재

- Version: 1.1 / 2026-09-06
- Release: GOV-20260906-02
- Final approver: ACT-001 / admin / Jin

## 원칙

대표님은 요청·방향을 입력하고 부사수는 조사·작업·상신한다. 이 체계의 최종 결재자는 관리자 Jin(ACT-001)이다. LLM과 부사수는 자기 품의를 스스로 승인하지 않는다. 대표님 발언도 이 체계의 관리자 결재 기록을 대신하지 않는다.

## 승인 범위

research, production, deliverable, publication, expenditure, policy_change.

한 번에 여러 범위를 승인할 수 있으나 범위를 명시한다. `초안 좋아`를 게시·추가 비용·영구 규칙 변경의 승인으로 확대하지 않는다.

## 결재 기록

decision_id, work_id, submission_id/revision, artifact_refs/version/hash, requested_scopes, granted_scopes, decision, `approver_actor_id`, approver_role, approver_name, approval_source, principal_verification, decided_at, conditions, recheck_conditions.

다른 사람이 `Jin이 승인했다`고 말한 것은 approval_claim이며 승인 증거가 아니다. 실제 관리자 프로젝트의 결재 원문이나 확인 가능한 관리자 리뷰·서명과 대상 버전을 대조한다. 확인할 수 없으면 승인대기다.

## 변경·취소

승인된 영상 v1이 v2로 바뀌거나 상품·가격·자막·음원·게시 대상·비용이 바뀌면 영향 범위를 재결재한다. 같은 URL이라도 내용 버전이 다르면 같은 승인본이 아니다. 승인 취소·수정은 새 이벤트로 연결한다.

## 승인과 반영

관리자 승인 → 승인 범위 확인 → 도구 실행 → commit/파일/게시 결과 재조회 순서다. 승인됐지만 저장 실패했다면 approved/failed로 남긴다. 승인 없이 먼저 외부 실행하고 나중에 품의하지 않는다.

`/업무확정`은 회사 기준 개정에 사용한다. 영상 결과 수락은 결재·업무 기록으로 남기고 회사 정책으로 자동 승격하지 않는다. 부사수는 검증된 결재 범위의 작업을 수행할 수 있지만 공식 역할·정책 파일 반영은 관리자 작업이다.
