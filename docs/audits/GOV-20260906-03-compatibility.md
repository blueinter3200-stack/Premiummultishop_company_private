# 트리거·요청 보존 개정 대조표

기준 commit: f37ab3e70b910672ce2a4a2f3ec628b96d4f90c3. 사용자 승인: D-20260906-003. 범위: 이번 대화의 LLM 운영 규격. 기존 사업 아이디어의 일괄 채택이 아니다.
첨부되어 대화에 제공된 IDEA_CHAT, PROBLEM_CHAT, WORK_CHAT, ADMIN_REFLECT_CHAT, PROJECT_COMMON의 항목을 최신 actor-ID 규격과 대조했다. 옛 문장을 모두 그대로 복사했다는 뜻이 아니라 아래처럼 유지·의도 변경을 구분한다.

| 옛 항목 | 새 위치 / 처리 |
|---|---|
| 아이디어출력의 제목·아이디어·목적·관련업무·미정 | IDEA_WORKFLOW 출력: 대화만, 무저장 |
| 아이디어저장 선행 출력 불필요 | IDEA_WORKFLOW 저장: 유지 |
| author-role 저장 경로와 작성자 메타데이터 | actor_id·record_id 사용; 기존 role 경로는 그대로 |
| 동명 파일 -2/-3 충돌 방지 | COMMON_IO, IDEA/PROBLEM_WORKFLOW |
| 첨부 원본·정제 분리, 표·수치·날짜·조건 보존 | COMMON_IO, IDEA/PROBLEM_WORKFLOW, NORMALIZATION_STANDARD |
| 원본 미확보를 저장 성공으로 보고 금지 | COMMON_IO 완료·부분 실패 규칙 |
| PENDING_INDEX 필수, 기록 실패 시 인덱스 단독 변경 금지 | IDEA/PROBLEM_WORKFLOW, COMMON_IO |
| 허용 경로 한정·공식 소스/현재 업무/타인 기록 자동 수정 금지 | IDEA/PROBLEM_WORKFLOW 경계 |
| 문제출력의 현상·영향·원인 미확인·해결후보 | PROBLEM_WORKFLOW 출력 |
| 업무검토 최신 공식 기준·관련 pending·선택 조회 | WORK_WORKFLOW 검토 |
| 검토 PASS 뒤 공유 게이트, 단독 공유 차단, 복합 요청 순차 | WORK_WORKFLOW 공유 |
| CURRENT_WORK 전체 최신판·HISTORY·첨부 | work/items 원장 후 파생 화면으로 변경된 GOV-02 유지 |
| 현재 확정과 변경 협의 구분, 참고 기록 자동 반영 금지 | WORK_WORKFLOW 공식화 |
| 대표업무점검: 저장·목차·업무·날짜·회의 질문, 쓰기 금지 | WORK_INSPECTION으로 일반화; 대상 인자 추가 |
| 반영미리보기: 대상 선택·영향·충돌·무저장 | ADMIN_REFLECTION_WORKFLOW 미리보기 |
| 아이디어/문제 공식 반영과 인덱스 동시 변경 | ADMIN_REFLECTION_WORKFLOW, COMMON_IO |
| 해결 방향 채택과 실제 resolved 분리 | PROBLEM_WORKFLOW, ADMIN_REFLECTION_WORKFLOW |
| 업무확정: 관리자만·상충 규칙 교체·changelog·남은 협의 | ADMIN_REFLECTION_WORKFLOW |
| 역할 추론 금지·직원 개인정보 경계·저장 검증 | ROLE, PROJECT_COMMON, COMMON_IO |
| 정확한 슬래시만 허용하던 옛 공통 규칙 | GOV-02의 명확한 자연어 실행 허용 유지; 인용·추천은 실행 아님 |
| 트리거 목록·추천이 GitHub에만 있었음 | PROJECT_COMMON 및 프로젝트 지침에 명시 복원 |
| 요청 보존이 요약 수준이었음 | REQUEST_CAPTURE, R-ID, REQUEST_INDEX와 업무 연결 |

## 인수 확인 예시 — 실제 세 프로젝트 동작 테스트는 미실행

GitHub 없이 명령 목록/아이디어출력/문제출력/추천이 가능한지; 대표님 순수 아이디어는 저장 추천만 하는지; 부사수 문제 저장은 자동 blocked가 아닌지; 명확한 지속 지시는 저장하되 검토만은 쓰지 않는지; 업무점검 대상이 모호하면 확인하는지; pending 건수를 전체 저장 건수로 오인하지 않는지; 품의서 v1 승인으로 v2를 공개하지 않는지; 구명령 별칭이 권한을 우회하지 않는지 확인한다.
구조 검사는 LLM 실제 행동·계정 인증·도구 연동·외부 실행의 성공 증거가 아니다.
