# GOV-20260906-04 구현·검증 기록

## 요청·기준

관리자 ACT-001의 첨부 작업 지시 1~25절을 근거로 기존 요청 변경추적을 확장했다. 원본은 records/requests/ACT-001/R-20260906-002.source.md, 요청 R-20260906-002, 업무 W-20260906-004, 결재 D-20260906-004에 연결한다.
시작 시 원격 main을 다시 확인했다. 기준 commit: d708129d0419ca61d79517344091f0b89d096932 / GOV-20260906-03. 기존 사용자 worktree가 없는 별도 로컬 검증 공간을 사용하고 GitHub API의 기존 tree를 기준으로 관련 파일만 적용한다. 이전 커밋으로 reset/force push하지 않는다.

## 무엇을·왜

최초 요청 원문과 request revision만으로는 의미 있는 변경 이유·영향을 독립적으로 찾기 어려워 RC-YYYYMMDD-NNN을 추가했다. 요청 객체의 revision은 그대로 두고 RC에 변경 전/후·이유·실제 근거·관련 W/D/I/P와 snapshot/hash를 남긴다. 한 파일에 역할·업무를 다시 합치거나 회사 OS를 재설계하지 않았다.

## 설계 판단

- REQUEST_CAPTURE의 기존 예외를 보존하고 상세한 건별 RC 절차만 REQUEST_CHANGE_WORKFLOW로 분리했다. 기존 15개 명령은 추가·변경하지 않았다.
- REQUEST template v2는 선택 필드 추가이며 실제 v1 요청은 바꾸지 않았다. 관리자 요청이 처음부터 새로 들어온 이번 작업에는 새 R-ID를 발급했고, 과거 R-20260906-001에 가상의 변경을 소급 생성하지 않았다.
- 코드 helper는 evidence-backed materiality 판정을 입력받는 계획·검증 도구다. 자연어 의미 판정·사용자 인증·GitHub 자동 쓰기를 구현한 것으로 주장하지 않는다.
- 기록자/변경자는 ACT-001 범위이며 대표님·부사수의 역할·지침·의무·접근권한은 그대로다. ACTOR_REGISTRY는 새 RC 식별자·경로 메타데이터만 확장한다.
- 이유를 모르면 null/unknown. original_text·R-ID·supersedes·기존 결재 및 자료는 덮어쓰지 않는다. RC는 승인·완료·공식 확정이 아니며 새 변경의 수행은 W/D/실행 영수증으로 검증한다.
- 기존 validator의 03 manifest 고정을 현재 FILE_MAP release에 연결했다. 과거 manifest 자체를 새 해시로 덮어쓰지 않는다. 패키지 builder는 기존 3/3/4 업로드 파일 구조를 유지한다.

## 실제 로컬 검증

`python -m unittest discover -s tests -v`: 16개 테스트 통과. A–H, 원문·supersedes 불변, 명시 이유/unknown, 읽기 전용·저장 금지, 타 actor 제외, 재시도/ID 충돌, stale revision/hash, 누락/null 구분, 취소·대체 의도, 조작 검출, 원자적 변경 집합·부분 read-back 실패를 포함한다.
테스트 자료는 tests 안의 synthetic fixture이며 회사의 실제 RC·아이디어·업무·승인 데이터로 저장하지 않았다. 실제 기존 v1 R-20260906-001은 읽기 및 바이트 보존을 확인했다.
기존 명령 registry, PROJECT_COMMON, ACT-002/003 역할/지침/RULES, COMMON_IO는 바이트 동일성을 검증했다. actor 3개와 역할 매핑·15개 명령 route가 그대로인지 비교했다.
변경/신규 JSON과 로컬 검증에 사용한 기존 JSON, 연결 경로, 새 template, 배포 source manifest를 검사한다. GitHub 전체의 무관한 과거 JSON 본문을 전수 재수집·재검증한 작업은 아니다. 기존 기록 보존은 최종 Git diff와 blob 대조로 검증한다.

## 저장·배포 검증 경계

본 문서는 로컬 검증 및 구현 판단 기록이다. main 저장 성공과 실제 패키지 SHA/소스 커밋은 성공 후 별도 docs/releases/GOV-20260906-04.json에 기록한다. 미래 commit을 미리 안다고 쓰지 않는다.
실제 ChatGPT 프로젝트 설정 교체, 실사용 LLM의 의미 변경 분류, 독립 계정 인증, 자동 알림, 외부 게시·지출·Higgsfield/Drive 실행은 수행하지 않았다. 관리자 프로젝트 교체 후 실제 대화 테스트가 남는다.

## 영향 파일

- `FILE_MAP.json`
- `README.md`
- `approvals/D-20260906-004.json`
- `chatgpt/INSTALLATION.md`
- `chatgpt/admin/PROJECT_INSTRUCTIONS.md`
- `docs/requirement-changelog.md`
- `llm-source/ACTOR_REGISTRY.json`
- `llm-source/LLM_RUNTIME.md`
- `llm-source/actors/ACT-001/ROLE.md`
- `llm-source/workflows/REQUEST_CAPTURE.md`
- `llm-source/workflows/REQUEST_CHANGE_WORKFLOW.md`
- `records/REQUEST_CHANGE_INDEX.md`
- `records/REQUEST_INDEX.md`
- `records/requests/ACT-001/R-20260906-002.json`
- `records/requests/ACT-001/R-20260906-002.source.md`
- `scripts/build_chatgpt_package.py`
- `scripts/request_changes.py`
- `scripts/validate_llm_sources.py`
- `templates/REQUEST.json`
- `templates/REQUEST_CHANGE.json`
- `templates/WORK.json`
- `tests/test_request_changes.py`
- `work/items/W-20260906-004.json`
- `working/CURRENT_WORK.md`
