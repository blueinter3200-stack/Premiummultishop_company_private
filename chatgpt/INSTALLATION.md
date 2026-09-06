# 세 프로젝트 설치 — GOV-20260906-03

이번 판은 단순 경로 변경이 아니라 트리거 발견·추천·요청 보존·명령 이름을 보강한 판이다. 기존 GOV-20260906-02 프로젝트 지침과 첨부를 이번 판으로 교체한다. 실제 프로젝트 설정 편집은 GitHub 반영과 별도다.

## 프로젝트 지침

각 `chatgpt/admin/`, `chatgpt/representative/`, `chatgpt/assistant/PROJECT_INSTRUCTIONS.md` 본문을 해당 프로젝트의 지침으로 사용한다. 지침 파일 자체를 소스에 중복 첨부할 필요는 없다.

## 첨부할 소스

공통: `chatgpt/PROJECT_COMMON.md`, `llm-source/ACTOR_REGISTRY.json`.
관리자: `llm-source/actors/ACT-001/ROLE.md`.
대표님: `llm-source/actors/ACT-002/ROLE.md`.
부사수: `llm-source/actors/ACT-003/ROLE.md`와 `RULES.md`.

PROJECT_COMMON에 명령 목록·용도·추천 조건·실행 경계가 들어 있다. 자기 ROLE에는 허용 명령, 지침에는 축약 목록이 있다. GitHub가 없어도 기능 설명·추천·대화 내 아이디어/문제 정리를 안내하도록 구성한다.
옛 IDEA_CHAT/PROBLEM_CHAT/WORK_CHAT/ADMIN_REFLECT_CHAT 및 중복 구역할 파일은 이번 판과 함께 상충하는 실행 소스로 두지 않는다. 관련 세부 규칙은 workflows로 이관했다. 일반 업무자료까지 전부 삭제하라는 뜻은 아니다.
다른 actor ROLE을 섞지 않는다. 워크플로·업무판·전체 근거를 상시 첨부하지 않고 원격 실행 때 필요한 최신본을 읽는다.

## 사용 전 확인

명령 추천·출력은 GitHub 없이 하는지, 실제 저장은 최신 main과 자기 actor 경로를 쓰는지 확인한다. 대표 순수 아이디어 검토가 업무공유로 넘어가지 않는지, 부사수 품의서 작성이 자체 승인으로 바뀌지 않는지 확인한다.
관리자 /업무점검의 대상별 조회와 /품의서승인의 버전·범위를 확인한다. 명확한 지속 요청은 보존하고 읽기 전용 검토는 쓰지 않는지 확인한다.
문서·구조 검사는 실제 세 프로젝트의 행동·계정 권한·승인 인증·자동 알림을 검증한 것이 아니다. GitHub/Drive/제작 도구의 연결·사용 가능 여부는 별도로 확인한다.
