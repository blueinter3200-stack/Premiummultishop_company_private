# Work Lifecycle — 업무 생명주기

- Version: 1.1 / 2026-09-06
- Release: GOV-20260906-02

## 객체 연결

Input/Idea/Problem → NormalizedSource → Evidence → Work → Artifact → Submission → Decision → ExecutionReceipt.

모든 단계는 안정적인 ID로 연결한다. 사람은 actor_id, 아이디어는 idea_id, 문제는 problem_id, 업무는 work_id, 결재는 decision_id를 쓴다. 지시 원문은 directive, 상태는 work/items, 결과는 handoff, 결재는 approvals에 둔다.

아이디어·문제·업무는 서로 다른 객체다. 아이디어를 조사하는 업무가 생기면 `idea_id ↔ work_id`를 연결하고, 문제 때문에 업무가 차단되면 `problem_id ↔ work_id`를 연결한다.

## 원장 필수값

새 업무 원장은 `schema_version, id, revision, title, requested_by_actor_id, assigned_to_actor_id, created_at, updated_at, information_as_of, work_status, evidence_status, approval_status, persistence_status, execution_status, priority, due_at, next_action, source_refs, directive_refs, evidence_refs, artifact_refs, submission_refs, decision_refs, related_idea_ids, related_problem_ids, unknowns, completion_criteria`를 사용한다.

알 수 없는 담당·기한·완료일은 null이다. role/name은 표시용으로 파생할 수 있지만 actor_id가 소유자·행위자 기준이다. 기존 schema_version 1 업무의 `requested_by`, `assigned_to`는 legacy 필드로 유지할 수 있고 수정 시 가능한 범위에서 actor_id를 추가한다.

## 상태 축

- work_status: draft, queued, in_progress, submitted, revision_required, blocked, done, cancelled.
- evidence_status: pending, partial, passed, failed.
- approval_status: not_requested, pending, approved, revision_required, rejected, revoked.
- persistence_status: pending_commit, verified, failed, partial.
- execution_status: not_requested, running, succeeded, failed, uncertain.

외부 게시가 있으면 publication_status와 publication_receipt를 추가한다. 파일 저장은 품의 승인·실무 완료가 아니다.

## 상신·완료

상신 시 대상 work revision·결과물 버전·근거·요청 승인 범위를 고정하고 `submitted_by_actor_id`를 남긴다. 수정본은 새 submission revision으로 올린다. 관리자 결정·실행 결과는 이력을 보존한다.

완료는 지정 산출물·검수·승인·필요한 저장/실행 증거가 실제로 충족된 경우다. 단순 파일 생성으로 제작·게시·구현을 완료 처리하지 않는다. 정책 변경이 없는 업무는 회사 정본을 바꾸지 않는다.

## 조회판

CURRENT_WORK는 전체 활성 업무, ACTIVE는 assigned_to_actor_id=ACT-003인 활성 업무, BLOCKED는 차단 업무, DECISION_NEEDED는 관리자 결정이 필요한 품의/미정 항목을 참조한다. 원장을 읽고 재생성하며 원장과 충돌하면 원장을 따른다.
