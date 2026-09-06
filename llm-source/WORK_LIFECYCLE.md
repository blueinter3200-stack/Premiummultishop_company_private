# Work Lifecycle — GOV-20260906-05

## 생명주기
원문 R(captured) → 검토 PASS → R/SUB(submitted) → D(관리자 결정) → work_start 승인 범위 W → 수행 갱신 → 결과 검증/수락이다. 품의 SUB는 W가 없을 때도 R에 연결할 수 있다. 원문 I/P와 조사 업무는 별개다.

## 버전과 상태
request.revision은 객체 갱신 횟수, content_revision은 결정 대상 내용 버전이다. 상태·연결만 갱신할 때 content_revision은 유지한다. proposal/current_requirements 등 의미 내용 변경에는 content_revision을 올리고 검토를 다시 받는다. 과거 schema 1/2는 원문·기존 필드를 보존하고 건별로 필요한 선택 필드만 추가한다.
R의 request_status(captured/in_progress/fulfilled 등 과거 의미)는 결정 상태를 대체하지 않는다. 신규 submission_status는 captured 또는 submitted 등 제출 단계, review_snapshot은 통과한 정확한 내용/근거, 결정 상태는 D에서 파생한다. 과거 fulfilled를 승인 범위로 간주하지 않는다.
SUB는 submission_id + revision별 불변 Markdown과 metadata다. 수정본은 새 revision·파일로 제출한다. 새 버전은 pending으로 보며 이전 버전 결정은 역사로만 연결한다.
D는 target_type/id/content_revision/content_hash, scope_key, previous_decision_id로 연결한다. 전역 최신 날짜 하나로 다른 버전·범위까지 덮어쓰지 않는다. 동시에 같은 선행 D를 대체하는 분기가 생기면 CONFLICT로 처리하고 관리자가 해소한다.

## 업무
신규 W는 administrator work_start 승인과 연결한다. confirmation_decision_ref, authorized_scopes, request_refs, submission_refs, decision_refs를 갖는다. 관리자가 이미 승인한 같은 R의 상세 품의를 결재해도 W를 중복 생성하지 않는다. 기존 legacy W는 일괄 삭제·재생성하지 않으며, 승인 근거가 미확인인 건의 추가 실행은 재확인한다.
기존 필수 필드 schema_version,id,revision,title,requested_by_actor_id,assigned_to_actor_id,created_at,updated_at,information_as_of,work_status,evidence_status,approval_status,persistence_status,execution_status,priority,due_at,next_action,source_refs,directive_refs,evidence_refs,artifact_refs,submission_refs,decision_refs,related_idea_ids,related_problem_ids,unknowns,completion_criteria와 request_refs/request_change_refs를 유지한다.
work_status: draft/queued/in_progress/submitted/revision_required/blocked/done/cancelled. evidence_status: pending/partial/passed/failed. approval_status: not_requested/pending/approved/revision_required/rejected/revoked. persistence_status: pending_commit/verified/failed/partial. execution_status: not_requested/running/succeeded/failed/uncertain.
승인은 queued와 실행 허용 범위를 만들 수 있지만 실제 작업 시작·완료를 가정하지 않는다. 게시 상태·영수증은 별도다. work revision은 진행 갱신마다 올리고 결과 버전은 별도 artifact_refs로 고정한다.

## 조회판
CURRENT_WORK=회사 수행 업무, ACTIVE=ACT-003 배정 활성 업무, BLOCKED=차단 업무, DECISION_NEEDED=관리자 결정대기다. 별도 records/decision-views/ACT-NNN.json은 요청/품의 pending·held·revision_required·approved·rejected 상태함이다. INBOX는 아직 안내하지 않은 최신 결정 사건 요약이다. 상태함이나 INBOX를 고쳐 결정을 변경하지 않는다.

work_start 결재는 간이 R와 상세 SUB가 같은 authorization_target(R-ID/content_revision/hash) 체인을 공유한다. 대상 버전은 개별 R/SUB로 보존하되 승인 상태가 서로 모순되거나 업무를 중복 생성하지 않게 한다.
