# 관리자 요청 변경이력 — GOV-20260906-04

정본: 개별 RC JSON. R-ID는 무엇을 요청했는지, RC-ID는 이후 무엇이 왜 바뀌었는지, W-ID는 수행 업무, D-ID는 결재다. 기존 REQUEST_CAPTURE의 하위 절차이며 새 슬래시 명령이나 새 권한은 아니다.

## 적용·판정

필수 조건은 기존 request.requester_actor_id=ACT-001, 현재 변경 지시자=ACT-001, 명확한 회사 요청 변경, 의미 있는 차이, 저장 금지/읽기 전용이 아님이다. 실제 최신 registry·ROLE과 계정 권한을 확인한다. 대표님·부사수의 요청에는 이 무거운 RC 의무를 강제하지 않고 기존 revision 절차를 유지한다. 해당 actor의 관리자 기록 열람·쓰기·결재 권한은 확대하지 않는다.
목적, 범위, 필수 조건, 결과물 요구, 대상 시스템/사용자/담당, 실무에 영향을 주는 우선순위, 완료·승인 조건, 지속 지시, 취소·일부 철회·대체·의미 있는 추가 요구는 RC 대상이다.
오탈자·띄어쓰기·표현·포맷·링크 표시만의 변경, 동일 내용 재확인, 단순 질문·아이디어 탐색은 RC가 아니다. /아이디어출력·/문제출력·/업무검토·/업무점검·/반영미리보기 및 검토만/저장하지 마 예외를 유지한다. 단어 하나나 JSON 값 차이만으로 의미 변경이라고 단정하지 않는다. 판정 근거를 materiality_basis에 남긴다.

## 원문·revision·스키마

최초 original_text, R-ID, 작성자, source_created_at, captured_at 및 기존 supersedes 관계를 후속 요구로 덮어쓰지 않는다. 새 요청의 대체 관계가 있으면 기존 관계를 지우지 말고 별도 요청/event에 연결한다.
revision은 request 객체 갱신 횟수다. RC는 의미 있는 변경 사건으로 모든 revision에 RC가 필요한 것은 아니다. 실제 의미 변경을 적용하는 revision에는 request_change_refs로 RC 경로를 연결한다.
REQUEST template v2는 request_change_refs와 current_requirements만 추가한다. v1은 그대로 읽고 없는 선택 필드는 빈 목록/객체로 취급한다. 과거 파일의 schema_version·원문·revision을 일괄 바꾸지 않는다. 기존 v1을 건별 수정해도 기존 필드 의미를 유지하며 선택 필드를 추가할 수 있다.
현재 요구는 scope/conditions 등 기존 의미 필드 또는 current_requirements로 표현한다. current_requirements는 원문 대체물이 아니다. 취소·대체 의도도 이 필드와 change_type에 남길 수 있다. RC 작성만으로 request_status나 W/D 상태를 변경하지 않는다. 이미 fulfilled인 이력은 그때의 범위에 한정되며 새 변경의 수행 완료 증거가 아니다.

## RC 데이터

경로: `records/request-changes/ACT-001/<R-ID>/RC-YYYYMMDD-NNN.json`. 서식: `templates/REQUEST_CHANGE.json`.
request_change_id, request_id, changed_by_actor_id, changed_at, captured_at, change_type, change_summary, changed_fields의 before/after와 존재 여부, change_reason/reason_source, source_type/locator/excerpt, source_event_id, 전/후 revision, 영향 W/D/I/P·요구사항 참조, unknowns를 남긴다.
request_snapshot_before/after와 각각의 canonical JSON SHA-256으로 최초 원문 및 갱신 상태를 복원·검증한다. before_present=false와 before=null은 다르다. 이전 RC 경로를 previous_request_change_ref로 연결한다. source_event는 판정·변경 입력의 보존본이고 event_fingerprint는 그 중복/오염 점검용이며 사람 인증이 아니다.
changed_at은 실제 확인 가능한 변경 발언 시점이다. 없으면 null과 unknowns를 쓰고 captured_at과 구분한다. captured_at은 실제 기록일이다. Git blob SHA와 canonical JSON SHA-256을 섞지 않는다.

## 이유·근거

관리자의 실제 이유 발언은 reason_source=explicit_user_statement, 원문 reason_excerpt와 source_excerpt/locator에 연결한다. normalized change_reason은 원문 취지를 보존한다.
실제로 확인한 대화·회사 자료의 이유는 source_evidence로 표시하고 reason_evidence_refs에 파일/URL과 정확한 위치를 남긴다. 추정은 근거가 아니다.
이유가 불명확하면 change_reason=null, reason_source=unknown, unknowns에 변경 이유 미확인을 남긴다. 이유를 채우려고 관리자에게 이미 답한 내용을 재질문하거나 AI가 그럴듯한 이유를 만들지 않는다.

## 실제 저장 절차

1. COMMON_IO대로 최신 main SHA와 대상 request, REQUEST_INDEX, 관련 RC/목차, W/D를 실제 읽는다. 기존 R-ID가 특정되지 않으면 임의의 과거 요청에 붙이지 않는다. 독립적인 새 요청은 새 R-ID다.
2. 현재 발언을 원문·현재 유효 범위와 비교한다. 위 적용 조건, 저장 예외, materiality_basis와 변경 전/후 필드를 확인한다. 조건 불충족이면 RC를 생성하지 않는다.
3. 기존 RC 파일과 REQUEST_CHANGE_INDEX에서 전역 RC-ID 충돌 및 source_event_id 중복을 확인한다. 동일 작업 재시도는 원래 event ID를 재사용한다. 플랫폼 메시지 ID가 없으면 기록 작업의 식별자임을 밝힌 별도 키와 실제 원문 위치를 남긴다. 같은 문장으로 새로 한 독립 지시는 별개다.
4. RC와 request 전/후 snapshot, revision+1, request_change_refs를 준비한다. original_text와 supersedes는 동일해야 한다. 변경 이유가 없으면 null이다. 이미 저장된 RC 본문을 수정·삭제하지 않는다. RC 기록 오류 정정도 새 사건/정정 근거로 연결한다.
5. REQUEST_CHANGE_INDEX와 필요한 REQUEST_INDEX 연결을 준비한다. RC 목차가 정본을 대신하지 않는다. 관련 W에 request_refs/request_change_refs를 추가할 수 있으나 실제 영향이 없는 업무나 미확인 ID를 만들지 않는다. 관련 W 갱신은 권한·범위를 확인하고 revision을 증가시키며 필요한 조회판을 함께 처리한다.
6. affected_decision_ids는 영향 관계다. 이미 승인된 범위가 달라지면 approval_recheck_required를 표시하고 변경 요청→검토→새 D-ID→허용된 공식 반영 순서로 한다. 과거 D 파일을 수정하거나 RC만으로 approved/done/official로 만들지 않는다. impact_execution_status=not_verified에서 실제 수행·검증 근거는 W/D/실행 영수증으로 확인한다.
7. RC/request/index/허용된 W 연결을 하나의 논리적 변경 집합·동일 커밋으로 반영한다. 최신 parent와 force=false를 사용하며 동시 변경이면 대상·중복·전/후 해시를 다시 비교한다. 공유 계정이나 프로젝트 지침은 인증 장치가 아니다.
8. commit/main ref와 저장한 모든 RC/request/index/W 파일을 실제 재조회한다. ID·원문·revision·before/after·이유·참조·해시를 비교한다. 전/후 snapshot 및 source_event로 변경 내용과 이유를 재구성한다.
9. 일부만 성공하면 성공 경로·실패 경로를 각각 보고한다. 일부 RC만 존재하면 동일 event ID/RC-ID를 유지한 채 원문·전/후 해시로 복구 대상을 확인한다. 현재 상태와 맞지 않으면 중단·재검토하며 새 RC로 중복 처리하거나 인덱스만 성공으로 간주하지 않는다.

## 검증·보조 도구

`python scripts/request_changes.py plan <읽은 저장소> <event.json>`은 변경 집합과 expected_blobs/base_commit을 출력할 뿐 파일·GitHub를 쓰지 않는다. helper의 write_requested/material_change는 확인된 사용자 의도와 의미 판정을 입력하는 값이지 자동 NLP 판정이나 관리자 인증이 아니다.
이 계획의 files 전체와 기대 blob을 확인한 뒤 연결된 GitHub 도구로 COMMON_IO 저장을 수행한다. `verify <재조회한 저장소> <bundle.json>`은 불일치 경로가 하나라도 있으면 실패한다. `validate <저장소>`는 실제 RC 구조·원문·request/index 역참조를 점검한다.
취소·철회·대체도 변경 이력으로 기록하되 그에 따른 업무 취소·결재 정정은 기존 권한 절차로 별도 처리한다. 새 정책을 실제 채팅방에서 자동 실행하는 서버·알림·인증 기능을 이 스크립트가 설치하는 것은 아니다.
