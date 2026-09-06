# Work Governance — GOV-20260906-03

## 계층과 정체성

역할·사람·반복 방법·지시·상태·결과·결재를 분리한다. 사람은 ACT-ID, 요청은 R-ID, 아이디어 I-ID, 문제 P-ID, 업무 W-ID, 품의 SUB-ID, 결재 D-ID로 연결한다. 반복 방법은 플레이북, 권한·규칙 변경은 관리자 확정 대상이다.
원본 → 의미 보존 전처리 → 종류 분류 → 필요한 기록·업무 → 실제 근거 조사·초안 → 품의서 작성 → 관리자 결재 → 승인 범위 실행 → 결과 확인이다.

## 로컬 인식과 최신 조회

PROJECT_COMMON과 역할별 프로젝트 지침에 명령·용도·추천 조건을 둔다. 추천·목록 안내·대화 내 출력에는 GitHub를 먼저 요구하지 않는다. 최신 회사 사실을 답하거나 검토·저장·결재를 실제로 할 때는 최신 main의 공식 기준·관련 업무를 확인한다.
LLM_RUNTIME과 TRIGGER_REGISTRY는 실행 진입점이고 상세 절차는 workflows에 둔다. 추천은 실행·동의·승인이 아니다.

## 검토와 분류

/업무검토는 읽기 전용이며 FILE_MAP, ACTOR_REGISTRY, 자기 ROLE, LLM_RUNTIME, COMPANY_OS, PRODUCT_REQUIREMENTS, PROJECT_REPOSITORIES, CURRENT_WORK, PENDING_INDEX와 필요한 REQUEST_INDEX를 확인한다. 직접 관련된 부서·원장·기록·정제본만 읽는다. 코드 구현이 중요한 경우에만 구현 저장소를 확인한다.
공식 기준 충돌, 중복·모순, 미반영 경고, 제외·보류·폐기, 미검증 수치, 민감성, 주체·범위·다음 행동·접근 가능한 근거를 검토한다.
classification은 idea/problem/work/mixed/policy_change, 결과는 PASS/REVISION/HOLD이며 권장 다음 행동과 이유를 남긴다. PASS는 자동 업무공유가 아니다. 순수 idea/problem에 업무공유를 요청하면 `ROUTING_MISMATCH`로 차단한다.
대표님의 탐색·가설은 아이디어다. 명시적 조사·기획 요청은 원 아이디어와 조사 업무를 별도 ID로 연결한다. 조사 완료는 채택이 아니다.

## 요청·공유·원장

명확한 업무·지속 지시는 REQUEST_CAPTURE에 따라 원문과 요청 actor·기록 actor를 보존한다. 새 요청 정본은 records/requests/<actor_id>/, 기존 assistant/20-directives 원문은 보존한다. directive가 필요하면 R-ID 참조를 둔다. 아이디어 저장만 요청한 경우 업무를 만들지 않는다.
정식 /업무공유는 유효한 검토를 통과한 실제 업무만 갱신한다. 단독 공유에 유효한 PASS가 없으면 쓰지 않고 검토를 안내한다. 현재 요청이 검토+공유를 명시하면 순차 처리한다. 핵심 내용·근거·main 변경 시 재검토한다.
상태 원본은 work/items이며 CURRENT_WORK·ACTIVE·BLOCKED·DECISION_NEEDED는 파생 조회판이다. 변경 때 revision과 관련 HISTORY를 함께 남기고 화면만으로 승인·상태를 바꾸지 않는다. 미정 담당·기한은 null이다.
문제 저장 자체로 업무를 blocked로 바꾸지 않는다. 확인된 실제 영향과 권한이 있을 때 별도 원장 변경·P-ID 연결을 한다.

## 품의서·권한

/품의서작성은 근거·기획·스토리보드·결과물 버전·위험·미확인·요청 승인 범위를 정리해 관리자 승인대기 저장이다. 본문만 요청은 미저장이다. 최종 결재는 관리자 ACT-001만 /품의서승인 또는 /결과승인으로 한다. 일반 결과 수락으로 COMPANY_OS·PRODUCT_REQUIREMENTS를 바꾸지 않는다.
대표님 지시와 Jin 지시가 충돌하면 원문을 보존하고 영향을 받는 범위를 결정대기로 둔다. 최종 조정자는 관리자다. 부사수는 충돌 없는 허용 조사·초안만 계속한다.

## 기록·공식 반영

새 아이디어·문제는 record_id와 author_id 및 당시 role/name을 남기고 actor_id 경로에 저장한다. 기존 role 기반 6개 아이디어 원문·경로·상태는 그대로 두고 목차/정제 메타데이터로 소유자를 해석한다.
공식 채택을 지시한 기록만 관리자 절차로 reflected 처리한다. 문제 resolved는 실제 해결 증거가 필요하다. 참고·정제·점검만으로 pending에서 제거하지 않는다.
COMMON_IO, APPROVAL_GOVERNANCE, TOOL_EXECUTION에 따라 기록·목차·조회판을 같은 단위로 저장한다. 실패 시 인덱스만 먼저 고치지 않는다. 승인과 main 저장·제작·게시 성공을 각각 확인한다.
