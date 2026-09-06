# Miracle Company Private

대표님·관리자 Jin·부사수와 향후 등록 actor가 사용하는 회사 기준·요청·전처리·업무·계획·결정 저장소다.
Repository: jintonic1010/miracle_company_private / main / GOV-20260907-01.

## 대화와 실행
명령 설명·추천·대화 내 아이디어/문제 정리는 프로젝트 지침·PROJECT_COMMON·자기 ROLE로 한다. 최신 회사 사실·검토·저장·결정·실행은 FILE_MAP→ACTOR_REGISTRY→자기 ROLE→LLM_RUNTIME→회사 기준·관련 workflow·CURRENT_WORK를 확인한다.

## 업무 흐름
대표님 업무검토→업무요청→관리자 업무결정→담당 지정/작업지시→부사수 업무계획안제출→관리자 업무계획안결의→승인 범위 업무업데이트다.
대표님이 부사수에게 직접 구두 요청했다면 원문 출처·실제 기록자를 분리해 보존하고 검토 후 업무계획안을 바로 제출할 수 있다. 선행 업무요청/관리자 업무채택은 필수가 아니지만 본 작업은 관리자 결의 전 실행하지 않는다.
업무 채택, 부사수 배정, 계획 실행 승인, 결과 수락, 회사 기준 변경은 구분한다. 관리자 직접 수행이나 담당 미정도 가능하며 부사수에게 무조건 지시하지 않는다. 승인 뒤 나중 배정/재배정은 새 ASG 사건이다. 업무결정/업무계획안결의는 승인·수정요청·보류·반려를 명시하고 기본 승인이 없다. 옛 별칭은 실행하지 않는다.

## 사람과 데이터
ACT-001=Jin, ACT-002=대표님, ACT-003=부사수. actor ID 재사용 금지, role 변경과 과거 귀속 분리를 유지한다. I/P/R/RC/SUB/W/ASG/D는 서로 다른 객체다. 상태함은 조회판이지 원본을 옮기는 폴더가 아니다.
기존 role 원문·과거 요청/결정·materials는 보존한다. GitHub는 지식/업무/결정 기록이며 ERP 운영 원장을 대체하지 않는다. n8n 연결 기반·기존 COMPANY_OS 부서/ERP/채널 방향은 변경하지 않는다. 비밀·민감 개인정보·운영 DB를 GitHub에 복사하지 않는다.

## 주요 위치
llm-source: 회사 기준·역할·명령·상세 workflow. chatgpt: 고정 공통 소스·프로젝트 지침·설치 안내.
assistant/10-playbooks: 반복 방법. assistant/20-directives: 과거 지시 원문. work/assignments: 새 불변 관리자 배정 사건.
records/ideas·problems·requests: actor별 입력/출처. records/request-changes: 관리자 RC. records/submissions: 계획 버전 metadata. assistant/40-handoff: 계획 본문/근거/결과.
work/items: 개별 W 원장. working/CURRENT_WORK·assistant/30-working: 파생 화면. approvals: 불변 D.
records/decision-views: 상태함. records/assignment-views: 현재 담당 미완료 작업지시. records/notifications·notification-receipts·inbox: 새 사건·실제 전달/확인·경량 조회판.
materials/originals·normalized: 실제 확보 원본과 의미 보존 정제 자료.

## 알림과 조회 범위
신규/재배정은 수신자에게 최초 안내 대상으로 남기고, 계획/업무 결정 변화도 관련 대상에게 한 번씩 연결한다. 알림 전달 후에도 미완료 지시는 작업지시 조회판에 남는다. 부사수는 대표님의 전체 미배정 요청을 보지 않고 자기 기록/계획과 승인된 작업지시 요약만 선택한다.
INBOX는 다음 실제 회사 업무 행동에서 확인한다. 잡담·매 메시지·시간 경과만의 폴링은 하지 않는다. fetch는 사람 읽음이 아니다. 읽기 전용에서는 영수증도 쓰지 않으며 영속 기록 없는 새 대화의 재표시 가능성을 숨기지 않는다. 실제 계정 ACL·실시간 푸시는 별도다.

## 설치·검증
chatgpt/INSTALLATION.md대로 이번 지침/운영 소스를 교체하되 일반 업무자료는 삭제하지 않는다. 이후 내부 workflow·데이터·조회 간격 변경은 통상 원격 기준만 갱신하고 역할/명령/로컬 행동 변경 때만 고정 소스를 교체한다.
scripts/decision_flow.py plan은 관련 파일 변경 계획만 출력한다. work_plans.py는 배정/계획 게이트를 보조한다. 실제 쓰기는 연결 GitHub 도구로 원자 반영·재조회한다. build_chatgpt_package.py는 정본 바이트로 ZIP을 만든다.
문서 연결은 scripts/validate_llm_sources.py, 현재 결정/계획 테스트는 tests/test_decision_flow.py와 tests/test_work_plans.py다. 과거 정책의 테스트 사본은 archive/test-snapshots에 보존한다. 테스트 통과는 실제 세 채팅방 설치·사용자 확인·푸시·독립 인증·외부 실행 증거가 아니다.
