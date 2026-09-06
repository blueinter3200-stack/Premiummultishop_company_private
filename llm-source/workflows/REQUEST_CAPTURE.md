# 사용자 요청 보존·업무요청 — GOV-20260907-01

## 원문 보존과 제출
명확한 회사 수행·배정·지속 요청은 한 번의 발언으로 R-ID·원문·출처·요청자·기록자를 보존한다. captured는 검토 전 원문이고 submitted 업무요청 또는 실행 승인이 아니다. 질문·잡담·가정·탐색·검토만·본문만·저장 금지 및 출력/업무검토/업무점검/반영미리보기는 자동 저장하지 않는다.
관리자의 명확한 복합 요청은 검토·제출·범위 결정·저장을 한 번에 순차 수행할 수 있으나 일반 대화를 승인으로 만들지 않는다.

## 업무요청은 검토 후
세 역할이 사용할 수 있다. 실제 work/mixed 후보의 유효한 검토 PASS 후 관리자 결정대기 submitted로 저장한다. 준비 검토가 없으면 그 제출 동작에 포함해 먼저 검토한다. 순수 idea/problem이나 HOLD/REVISION은 억지 제출하지 않는다.
내용 fingerprint/content_revision과 실제 검토 근거·최신 관련 D를 연결한다. 관련 기준/내용/결정 변화가 있으면 재검토한다. 조회만 했던 검토 snapshot은 명시적 제출 때 저장한다.
대표님 요청은 관리자에게 올라가며 부사수에게 바로 배정하거나 전체 요청 원문을 공개하지 않는다. 부사수도 새로운 업무/기존 범위 밖의 요구를 자기 업무요청으로 제출할 수 있다. 기존 W 수행은 업무업데이트로 구분한다.

## 대표님 구두 요청의 대리 기록
부사수가 직접 전달받은 구두 요청을 제출할 수 있다. requester_actor_id=ACT-002, recorded_by_actor_id/submitted_by_actor_id/record_owner_actor_id=ACT-003, source_type=reported_oral_request, source_verification=reported_not_independently_verified로 구분한다. original_text는 실제 부사수의 전달 설명 또는 제공된 명시 발췌이며 확인하지 않은 대표의 정확한 발언을 꾸미지 않는다.
새 대리 원본은 records/requests/ACT-003/<R-ID>.json에 두어 직접 대표 기록을 사칭하거나 덮어쓰지 않는다. 직접 자기 기록은 기존 requester 경로를 유지하고 record_owner는 기본 requester다. 요청 발안자와 파일 소유자의 차이를 인덱스·결정·보고에 보존한다.
구두 요청이 충분히 구체적이면 검토 후 /업무계획안제출에서 R captured와 SUB를 한 변경 집합으로 바로 만들 수 있다. 별도 업무요청·관리자 업무채택 선행을 강제하지 않는다. 본 작업은 아직 불가다.
권한 범위에서 실제 같은 기존 R이 확인되면 그 R에 연결한다. 접근할 수 없는 다른 대표 요청을 임의로 읽어 연결하거나 동일 source_event를 새 R로 중복 저장하지 않는다. 기존 관련 ID만 알면 출처/관련성 미확인을 구분해 관리자 검토 대상으로 남긴다.

## 데이터·저장
templates/REQUEST.json v4를 사용하되 과거 v1/2/3를 재작성하지 않는다. R-ID, 원문 locator/source_created_at(null 가능)/captured_at, 당시 role, 현재 scope/conditions/current_requirements, content_revision, review_snapshot, 관련 I/P/W/D/SUB/RC를 보존한다.
W-ID는 관리자 업무채택까지 빈 목록이다. REQUEST_INDEX 및 필요한 actor 결정대기 조회를 같은 커밋으로 갱신한다. 기록 실패 시 인덱스만 쓰지 않는다. 원본 첨부·정제는 COMMON_IO/NORMALIZATION_STANDARD에 따른다. 큰 영상·비밀은 GitHub에 복사하지 않는다.
아이디어/문제는 I/P를 정본으로 두고 R을 불필요하게 중복 생성하지 않는다. 기존 assistant/20-directives 원문은 보존하고 새 작업지시는 WORK_ASSIGNMENT_WORKFLOW의 ASG로 관리한다.

## 변경과 재개
원문·원본 경로는 불변이다. revision은 객체 갱신, content_revision은 의미 내용 갱신이며 새 내용은 새 검토/결정 대상이다. ACT-001의 의미 있는 기존 요구 변경은 REQUEST_CHANGE_WORKFLOW의 RC로 전후·실제 이유·근거·영향 W/D를 남긴다. 기존 revision/supersedes와 과거 schema 읽기를 유지한다. 이유 미확인은 null/unknown이다. 단순 상태/표현 수정은 RC가 아니며 ACT-002/003에 관리자 RC 의무를 적용하지 않는다.
보류 조건 해소·반려 후 재추진은 과거 이유·이번 차이를 실제 근거로 검토하고 관리자 결정을 받는다. 실패 시 부분 저장을 구분하고 커밋/원문/인덱스 재조회 후 완료를 보고한다.
