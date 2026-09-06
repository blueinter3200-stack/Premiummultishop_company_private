# Work Lifecycle — GOV-20260907-01

## 생명주기
R captured → 검토 → R submitted 또는 SUB 계획안 → 업무채택 D → W 등록 → 담당 ASG → 계획실행 D → 수행 갱신 → 산출물 검증/수락이다. 구두 대표 요청의 계획안은 W/ASG 전에 R에 연결해 제출할 수 있다. 초기 결정 없는 요청의 복합 결의는 명시 범위 안에서 채택·배정·계획승인을 함께 기록할 수 있다.

## 버전과 기존 데이터
request.revision은 객체 갱신, content_revision은 의미 내용 버전이다. 연결/상태만 바뀌면 내용 버전은 유지한다. 의미 내용이 바뀌면 새 검토·내용 버전이며 ACT-001 기존 요청은 RC 규칙도 따른다. 과거 schema1/2/3·최초 원문·supersedes는 강제 마이그레이션하지 않는다.
R.request_status와 submission_status는 제출/수행 연결이고 D의 결재 상태를 대신하지 않는다. 과거 fulfilled를 실행 승인으로 해석하지 않는다. 구두 대리 기록은 실제 recorder/record_owner와 reported requester를 나누며 원 발언자가 확인된 것처럼 꾸미지 않는다.
SUB-ID와 revision마다 본문/metadata를 보존한다. 새 본문은 새 파일이며 이전 결의가 자동 적용되지 않는다. request_content_revision/hash와 artifact_sha256을 결정·수행 전에 대조한다. 기존 SUB-W 형식을 바꾸지 않고 새 계획은 SUB-R 형식을 사용할 수 있다.
D는 정확한 대상·내용 버전/hash·scope_key·선행 D로, ASG는 W·선행 ASG·담당자·실제 관리자 지시로 연결한다. 시간 정렬 하나로 다른 버전/범위를 덮지 않고 분기·중복은 CONFLICT다.

## 업무 상태와 실행 권한
새 W는 명확한 관리자 work_adoption(legacy work_start는 과거 기록) 승인에 연결한다. W 등록은 본 작업 in_progress/done이 아니다. 기존 W를 같은 요청으로 중복 생성하지 않는다.
기존 schema/id/revision/title/requested_by/assigned_to/시점/work_status/evidence_status/approval_status/persistence_status/execution_status/priority/due_at/next_action/source_refs/request_refs/request_change_refs/directive_refs/evidence_refs/artifact_refs/submission_refs/decision_refs/related I/P/unknowns/completion_criteria 필드는 유지한다.
추가 필드는 adoption_decision_ref/adoption_status, current_assignment_ref/assignment_refs, execution_mode, execution_plan_ref/execution_decision_ref, plan_status, proposed_plan_ref/proposed_plan_status다. confirmation_decision_ref는 호환 연결이며 이를 계획 실행 허가로 단독 사용하지 않는다.
work_status는 draft/queued/in_progress/submitted/revision_required/blocked/done/cancelled를 유지한다. evidence는 pending/partial/passed/failed, persistence는 pending_commit/verified/failed/partial, execution은 not_requested/running/succeeded/failed/uncertain이다. 계획 준비는 별도 phase=planning으로 기록하고 본 수행 시작/전체 완료로 표시하지 않는다.
본 작업은 최신 유효 업무채택 + 현재 배정 + 정확한 plan_execution 결의 + research/production 등 활동 범위를 모두 확인한다. 관리자 명시 직접 수행(self_direct)은 본인에게만 적용되고 재배정 시 부사수에게 이전되지 않는다. 담당/지시가 바뀌면 이전 담당/배정에 묶인 계획승인을 자동 재사용하지 않는다.
새 r2 계획의 제출/반려가 r1의 기존 승인 범위를 자동 철회하지는 않는다. 새 범위 실행은 r2 결의 전 불가이며 실제 현재 실행계획 참조로 구분한다. 게시·지출·정책 변경은 별도 범위다.

## 조회판과 보존
CURRENT_WORK=회사 업무, ACTIVE=현재 ACT-003 배정 업무, BLOCKED=차단 업무, DECISION_NEEDED=관리자 결정대기, decision-views=요청/계획안 상태함, assignment-views=수신자가 수행해야 할 미완료 작업지시다.
INBOX는 새 미전달 사건 요약이다. 전달된 알림을 반복하지 않아도 미완료 지시는 assignment-views에 남는다. 과거 원본은 상태별로 이동/삭제하지 않는다. 기존 승인 근거가 불명확한 legacy W의 추가 수행은 관리자에게 확인하며 과거 상태를 임의로 완료/승인으로 고치지 않는다.
