# 업무결정·업무계획안결의 — GOV-20260907-01

## 명령과 대상
ACT-001 전용이다. /업무결정 <승인|수정요청|보류|반려> <R-ID/내용버전> [이유·범위·담당], /업무계획안결의 <동일 결과값> <SUB-ID/rN> [이유·범위·담당]를 사용한다. 결과 기본값은 없다. 결정값 “수정 요청” 띄어쓰기만 정규화하며 구명령/별칭은 실행하지 않는다.
현재 문맥의 대상/버전이 하나로 확정되면 불필요한 재질문 없이 실제 최신본을 확인한다. 비승인 이유가 없으면 이유만 확인하며 그럴듯한 이유를 만들지 않는다. 근거가 이미 있으면 재질문하지 않는다.

## 준비
COMMON_IO, 최신 ROLE/등록·APPROVAL_GOVERNANCE·정확한 R/SUB/본문/근거/검토와 현재 D를 읽는다. submitted인 대상만 결정한다. 계획이 연결한 R의 내용 버전/hash와 본문 SHA-256이 실제 일치해야 한다. review_snapshot은 최신 관련 기준/결정과 대조한다.
계획 제출 전 W가 없어도 R에 연결되어 있으면 결정할 수 있다. 대표님 구두 요청의 출처는 보고된 것으로 표시하고 직접 대표 승인으로 바꾸지 않는다. 업무 채택에는 실제 목적·범위·완료 기준이 필요하며 담당/기한 미정은 null이다.

## 결재 범위와 업무 연결
업무요청은 primary_scope=work_adoption, 일반 채택은 work_adoption/planning을 허용한다. W를 등록할 수 있으나 부사수의 본 실행은 별도 계획실행 결의 전 불가다. 관리자 본인의 명시 직접 수행은 실제 범위·self_direct를 기록하고 불필요한 자기 계획 결재를 강요하지 않는다.
계획안은 primary_scope=plan_execution이며 정확한 계획 버전/담당/배정과 research/production 등 실제 활동 범위를 승인한다. 이미 채택된 R의 W를 재사용한다. 신규·아직 결정 없는 구두 요청의 계획에 work_adoption·담당·plan_execution을 함께 명시하면 한 동작에서 W·ASG·계획승인을 연결한다. 기존 held/rejected 요청은 업무결정으로 먼저 해소하고 계획 결의로 무음 우회하지 않는다.
담당 부사수·관리자 직접·미정을 구분한다. ACT-003 배정은 WORK_ASSIGNMENT_WORKFLOW의 ASG와 최초 알림을 만든다. 승인된 W에 나중 배정은 같은 W의 새 ASG다. plan_execution 결의는 execution_assignee_actor_id와 assignment_ref를 고정한다. 아직 작성되지 않은 계획까지 “계획 잘하고 해”로 사전 승인하지 않는다.
비승인에는 granted_scopes=[]이며 W/ASG를 새로 만들지 않는다. 새 r2의 반려가 기존 승인된 r1이나 다른 scope를 자동 철회하지 않는다. 게시·지출·운영 변경·정책 변경은 정확한 별도 범위/후속 실행 요청이 필요하다.

## 불변 D·전이
D-ID에는 target_type/request 또는 submission, target_id/revision/hash/ref, scope_key, previous_decision_id, decision, 실제 이유/원문/locator, requested/granted_scopes, 조건, 시점, source_event_id, 원래 R의 authorization_target을 보존한다. 실제 사용자 발언 시점 미확인은 추정하지 않는다.
같은 source_event_id 재시도·동일 대상/버전/범위/결과/이유/조건 재확인은 새 사건을 만들지 않는다. 다른 payload로 같은 event 키를 쓰면 충돌이다. 정확한 선행 D와 target/content/scope로 체인을 계산하며 날짜순 하나로 충돌을 덮지 않는다.
pending→각 결정, held→approved/revision_required/rejected 또는 의미 있는 held 변경은 새 D다. 반려 후 같은 버전 재개에는 명시적 reopen_reason/근거, 새 버전은 과거 이유·현재 차이 검토가 필요하다. 기존 approved의 중단/축소/반려는 실제 철회/재결재·이유·revokes_decision_ids를 남긴다.
기존 work_start 체인은 역사적 원문으로 보존한다. 새 business adoption과 plan_execution은 서로 다른 범위이며 새 결의가 옛 기록을 일괄 변환하지 않는다. 같은 R로 W를 두 개 만들거나 아직 발생하지 않은 수행을 in_progress/done으로 표시하지 않는다.

## 통지·저장·실행
초기 대표 업무요청 결정은 요청자에게, 부사수 신규 배정은 승인된 작업지시 요약으로 전달한다. 대표 원문을 부사수에게 자동 공개하지 않는다. 부사수가 직접 대리 기록한 요청 또는 자기 계획의 결정은 실제 작성/요청 관계에 따라 알린다. 이미 배정된 업무의 후속 보류/승인은 직접 영향 있는 담당자도 알린다.
D/W/필요 ASG/연결/결정 인덱스/상태함/N/INBOX를 같은 커밋으로 저장하고 모든 변경 파일을 재조회한다. 기록·알림 일부 실패를 전체 성공이라고 하지 않는다. 동일 ID로 복구하며 옛 결정을 소급 방송하지 않는다.
관리자 결정 저장은 채팅방 푸시/실제 표시/사용자 확인/본 작업/외부 공개 성공이 아니다. 계획 본 수행 직전 최신 업무채택·현재 배정·계획 결의·내용 hash·허용 활동을 다시 확인한다.
