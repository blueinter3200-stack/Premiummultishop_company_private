# 사용자 요청 보존·업무요청 — GOV-20260906-05

## 원문 보존과 제출 분리
명확한 회사 수행·배정·지속 지시는 한 번의 발언으로 R-ID와 원문/요청자/기록자를 보존한다. 이것은 captured이고 검토 전이면 formal submission이 아니다. 새로운 조사·제작·개발을 바로 시작하거나 W-ID를 만들지 않는다. 질문·탐색·가정·검토만·저장 금지·출력/업무검토/업무점검/반영미리보기는 자동 저장하지 않는다.
관리자의 직접 실행 승인도 범위 확인·검토·결정 기록을 건너뛰지 않는다. 다만 한 메시지가 검토·제출·승인·반영까지 명확히 포함하면 내부적으로 순차 처리하고 같은 확인을 반복하지 않는다.

## 업무요청: 검토가 먼저
세 역할이 사용한다. 현재 대상의 유효한 업무검토 PASS와 classification=work/mixed가 있어야 관리자 결정대기 submitted로 저장한다. 검토 결과가 없으면 제출 준비로 검토부터 수행하며, REVISION/HOLD 또는 순수 아이디어/문제는 formal submission하지 않고 적합한 정리를 안내한다. 사용자가 검토만 원하면 저장하지 않는다.
검토 대상 내용 hash/revision과 실제 제출 내용이 같아야 한다. main이 바뀌어도 관련 기준·결정·근거가 동일한지 확인할 수 있으면 PASS를 재사용할 수 있고, 확인 불가/영향 변경이면 재검토한다. review_snapshot의 관련 SHA와 최신 조회 SHA를 함께 보존한다.
기존 R-ID가 있으면 같은 원문을 유지한 채 proposal/current_requirements와 제출 메타데이터만 갱신한다. 새로운 독립 요청만 새 R-ID다. 재시도·같은 제안의 상세화는 중복 R/W를 만들지 않는다.

## 데이터와 저장
경로 records/requests/<requester_actor_id>/<R-ID>.json. templates/REQUEST.json을 따른다. original_text와 실제 원문 위치, source_created_at(null 가능), captured_at, 요청자·기록자 actor, scope/conditions, proposal, content_revision, submission_status, review_snapshot, 관련 I/P/W/D/SUB와 RC 참조를 구분한다. 전해 들은 요청은 reported_request이지 직접 관리자 승인 아니다.
REQUEST_INDEX와 해당 요청/품의 조회 metadata를 같은 커밋으로 저장한다. W-ID는 관리자 work_start 결정까지 null/빈 목록이다. 신규 대기 건은 수행 ACTIVE가 아닌 결정대기 조회판에 보인다. 기존 지시 원문은 assistant/20-directives에 보존하고 새 directive는 R 참조를 쓴다.
아이디어·문제 저장은 I/P를 정본으로 삼아 R을 불필요하게 중복 생성하지 않는다. 아이디어와 조사 요청이 함께 있으면 I와 R을 연결하되 W는 승인 후 연결한다.

## 변경·재개
최초 원문과 원본 경로를 후속 요구로 교체하지 않는다. revision은 객체 갱신, content_revision은 의미 내용 갱신이다. 수정본 제출은 새 검토·내용 버전이고 이전 결재를 물려받지 않는다. 보류 조건 해소·반려 후 재추진 근거는 실제 출처와 함께 남긴다. 과거 반려를 삭제하거나 영구 금지로 해석하지 않는다.
ACT-001 기존 요청의 의미 있는 변경은 REQUEST_CHANGE_WORKFLOW의 RC와 전후·이유·근거·영향 W/D를 연결한다. 기존 revision/supersedes와 schema1/2 읽기를 보존한다. content_revision은 메타데이터이며 실제 의미 delta는 RC의 current_requirements 등 허용 필드로 기록한다. 이유 미확인은 null/unknown이다. 상태/표현만 수정은 RC를 만들지 않는다. ACT-002/003은 기존 revision 방식이며 관리자 RC 의무가 없다.

## 후속 확인
업무 재개 시 관련 활성 요청과 실제 최신 결정만 읽고 이미 제공된 요구를 다시 묻지 않는다. COMMON_IO대로 저장·연결·인덱스를 한 단위로 반영하고 재조회한다. 실패하면 실제 저장 범위와 미저장 부분을 보고한다. 다른 방을 자동 통보했다거나 GitHub에 없는 요구를 기억했다고 말하지 않는다.
