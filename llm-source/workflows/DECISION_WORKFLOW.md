# 업무결정·품의서결정 — GOV-20260906-05

## 호출
ACT-001 전용이다. `/업무결정 <승인|수정요청|보류|반려> <R-ID/버전> 이유·조건`, `/품의서결정 <승인|수정요청|보류|반려> <SUB-ID/rN> 이유·조건`으로 사용한다. 결정값 기본값은 없다. `수정 요청` 띄어쓰기만 정규화한다. 구명령·별칭은 실행하지 않는다. 명확한 자연어와 현재 문맥의 단일 대상은 같은 검토를 적용한다.

## 먼저 확인
COMMON_IO, 최신 등록·ROLE·결재 기준·정확한 R/SUB/근거와 review_snapshot, 관련 최신 D를 읽는다. 제출 내용 hash와 결정 대상 버전이 일치해야 한다. 승인/수정요청/보류/반려 모두 대상 버전을 특정한다. 비승인 실제 이유가 없으면 이유만 확인하고 추측하지 않는다. 현재 구체적 이유가 있으면 재질문하지 않는다.
정식 submitted 대상만 결정한다. 업무요청 승인에는 명확한 실행 범위·산출물·완료 기준이 있어야 한다. 담당/기한이 미정이면 null이지만 담당 미정의 업무를 부사수가 임의로 실행하지 않는다. 관리자가 배정할 수 있다.

## D 이벤트
새 결정은 templates/DECISION.json v3를 따른다. target_type=request/submission, target_id, target_revision(content 기준), target_hash, target_ref, scope_key(결재 범위), previous_decision_id, decision, reason 및 실제 source, requested/granted_scopes, approver_actor_id=ACT-001, conditions, decided_at, source_event_id, effect를 가진다.
같은 source_event_id 재시도는 기존 D를 그대로 사용하며 다른 payload면 충돌이다. 같은 대상·버전·범위·결정·이유·조건·범위의 단순 재확인은 새 D/N을 만들지 않는다. 명백한 새로운 이유·조건/결정만 새 사건이다. 알 수 없는 시각·이유는 실제로 확인한 것처럼 채우지 않는다.
현재 상태는 동일 target/content revision/scope_key의 연결 체인에서 계산한다. 새 D는 최신 선행 D를 가리킨다. main의 동시 결정으로 체인이 바뀌면 재검토하며 시간순 정렬 하나로 이기게 하지 않는다. 분기·경로 불일치는 CONFLICT다.

## 전이
pending→approved/revision_required/held/rejected. held→approved/revision_required/rejected 또는 새 이유/조건의 held. 수정본은 같은 SUB/R의 새 내용 버전으로 제출하고 새 pending 결정이다.
반려된 같은 버전의 재개는 관리자 명시적 reopen_reason/근거가 필요하다. 새 버전 재요청이면 과거 반려와 현재 차이를 검토한다. 반려는 자료 삭제·영구 금지가 아니다.
approved→중단/축소/반려는 명시적 기존 승인 변경·철회와 revokes_decision_ids를 기록한다. scope_key가 다른 결정(예: 게시)으로 기존 조사 승인을 덮어쓰지 않는다. 과거 D나 최초 원문은 수정·이동하지 않는다.
비승인은 granted_scopes=[]이다. 업무 전체 착수 scope_key=work_start 결정이 held/rejected/revision_required라면 그 범위는 실행 불가다. 결과물 불수락을 전체 업무 취소로 자동 확대하지 않는다.

## W 생성·연결
신규 W는 승인 granted_scopes에 work_start가 있을 때만 만든다. 요청 R 또는 품의의 request_ref로 기존 W를 먼저 찾는다. 같은 R/승인에 이미 W가 있으면 재사용하고 D를 연결한다. 신규 id는 충돌을 확인한 W-YYYYMMDD-NNN이다.
W에 confirmation_decision_ref, request_refs, submitted_by/assigned_to, authorized_scopes, 완료 조건을 남긴다. 실제 수행이 없으면 queued이지 in_progress/done이 아니다. 생성과 착수 승인이지 외부 실행 완료가 아니다. 품의 승인에 work_start가 없으면 W 생성 없이 해당 버전·범위만 결정한다.
보류/반려에 W를 만들지 않는다. 기존 W 영향은 해당 승인 범위에만 적용하며 필요하면 blocked/revision_required·재결재 필요를 기록한다. 게시·지출·운영 변경은 별도 승인과 실행 요청이다.

## 작성자 통지·저장
수신자는 요청자, 품의서 작성자, 직접 영향을 받는 현재 담당자의 합집합이며 ACT-001 자기 결정 수신은 기본 제외한다. 파일을 대신 기록한 사람이 아니라 실제 요청자/작성자를 확인한다.
D+R/W의 허용 연결+records/DECISION_INDEX.json+상태함+수신자별 N 이벤트+INBOX를 동일 커밋으로 저장한다. 최초 pending 결정과 보류→승인/반려 등 의미 변화마다 새 이벤트를 만들고 과거 사건을 방송용으로 소급 생성하지 않는다. 실패는 부분 저장으로 보고하며 재시도는 같은 event/ID로 복구한다.
INBOX_WORKFLOW대로 새 변화만 안내한다. 영수증은 표시·확인 기록이지 결재 변경이 아니다. 실제 저장 후 D/R/W/인덱스/N/INBOX를 재조회하고 완료를 보고한다.

동일 R의 간이 요청과 상세 품의가 work_start를 결정할 때는 authorization_target(R-ID/내용 버전/hash)로 업무 시작 결정 체인을 공유한다. target은 실제 R/SUB 버전으로 남긴다. 상세 품의에서 승인한 동일 요청을 별도 미승인으로 남기거나 두 업무로 만들지 않는다. 품의가 참조하는 요청 내용이 바뀌었거나 본문 해시가 다르면 재검토한다.
