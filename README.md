# Miracle Company Private

대표님·관리자 Jin·부사수와 향후 등록 actor가 사용하는 회사 기준·요청·전처리·업무·품의·결정 저장소다.
Repository: `jintonic1010/miracle_company_private` / main / GOV-20260906-05.

## 대화와 실행
명령 설명·추천·대화 내 아이디어/문제 정리는 프로젝트 지침·PROJECT_COMMON·자기 ROLE로 한다. GitHub 조회부터 요구하지 않는다.
최신 회사 사실·검토·저장·결정을 실제 수행할 때 FILE_MAP → ACTOR_REGISTRY → 자기 ROLE → LLM_RUNTIME → 회사 기준·관련 workflow·CURRENT_WORK를 확인한다.

## 업무 흐름
업무검토 → 업무요청(간이 제출)/품의서작성(상세 제출) → 관리자 업무결정/품의서결정 → 승인 범위 업무 → 업무업데이트다.
결정값은 승인·수정요청·보류·반려를 명시한다. default 승인은 없다. 대표님·부사수의 요청 기록만으로 W-ID나 착수 권한을 만들지 않는다. 같은 요청을 상세 품의로 보강할 때 중복 업무를 만들지 않는다.
업무 시작(work_start) 승인이 포함되면 관리자 결정에서 W를 생성/연결한다. 일반 결과 수락은 결과승인, 지속 회사 기준은 기준확정이다. 구명령 별칭은 사용하지 않는다.

## 사람과 데이터
ACT-001=Jin, ACT-002=대표님, ACT-003=부사수. actor ID는 재사용하지 않고 role 변경과 과거 원문 귀속을 분리한다. I/P/R/RC/SUB/W/D는 서로 다른 객체다.
기존 role 기반 원문·과거 요청·결정·materials는 보존한다. 상태함으로 원본 파일을 이동하지 않는다. 상태는 최신 유효 결정에서 파생하며 보류→승인/반려는 새 D다.
GitHub는 지식·업무·결정 기록이고 ERP는 운영 데이터 원장, n8n은 연결·자동화 기반이다. 기존 COMPANY_OS의 부서·ERP·채널 방향은 유지한다. 비밀번호·키·토큰·운영 DB·민감 개인정보를 GitHub에 복사하지 않는다.

## 위치
- llm-source/: 회사 기준, 역할, TRIGGER_REGISTRY, 상세 workflows.
- chatgpt/: 고정 공통 소스와 세 프로젝트 지침·설치 안내.
- assistant/10-playbooks/: 반복 업무 방법; assistant/20-directives/: 과거 지시 원문.
- records/ideas·problems·requests/: actor별 입력 원문과 연결.
- records/request-changes/: ACT-001 의미 변경 RC; REQUEST_CHANGE_INDEX는 조회용.
- work/items/: 승인된 개별 수행 업무 원장; working/CURRENT_WORK와 assistant/30-working은 조회판.
- assistant/40-handoff/: 품의 본문·근거·결과물; records/submissions는 버전 metadata.
- approvals/: 관리자 결정 원본. records/DECISION_INDEX.json·decision-views는 상태 조회판.
- records/notifications·notification-receipts·inbox: 새 결정 통지·실제 표시/확인·경량 조회판.
- materials/originals·normalized/: 실제 확보 원본과 의미 보존 정제자료.

## 알림
새 결정 변화만 작성자/요청자·직접 관련 담당자에게 연결한다. 사용자 다음 실제 업무 행동 때 자기 작은 INBOX를 확인하고 동일 알림을 반복하지 않는다. 과거 반려를 소급 방송하지 않는다. 같은 건 재검토에는 관련 과거 이유·현재 차이를 별도로 확인한다.
fetch는 사용자 읽음이 아니다. 실제 표시 뒤 허용된 경우에만 전달 기록을 남기고 읽기 전용/저장 금지에는 영수증도 쓰지 않는다. 영속 전달 기록이 없으면 새 대화에서 다시 보일 수 있다. 이 기능은 실시간 푸시 설치가 아니다.

## 설치와 검증
chatgpt/INSTALLATION.md를 따라 이번에는 세 프로젝트 지침·운영 소스를 교체한다. 일반 업무자료는 삭제하지 않는다. 이후 내부 workflow·알림 주기·업무 데이터 변경은 통상 GitHub만 갱신한다. 역할/명령/로컬 행동 변경에는 관련 고정 소스 교체가 필요하다.
`python scripts/validate_llm_sources.py`, `python -m unittest discover -s tests`로 문서 연결과 코드 동작을 검사한다. `decision_flow.py plan`은 파일 변경 계획만 출력하며 실제 GitHub 쓰기는 연결 도구로 원자적으로 반영하고 재조회해야 한다. `build_chatgpt_package.py`는 정본 바이트로 ZIP을 만든다.
스크립트 테스트는 실제 계정 인증·세 채팅방 행동·자동 메시지·외부 게시·지출의 완료 증거가 아니다.
