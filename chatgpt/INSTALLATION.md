# 세 프로젝트 설치 — GOV-20260906-04

이번 판은 GOV-20260906-03의 호환 확장이다. 관리자 ACT-001 ROLE·프로젝트 지침에만 의미 있는 요청 변경의 RC 추적 원칙을 추가한다. PROJECT_COMMON과 대표님/부사수 ROLE·지침·RULES는 그대로 유지한다. ACTOR_REGISTRY는 RC 식별자·경로 메타데이터만 추가하므로 권한 확대가 아니다. 실제 프로젝트 설정 편집은 GitHub 반영과 별도다.

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

## RC 배포 확인

관리자 지침과 ROLE, 최신 registry를 교체한다. 대표님·부사수는 기존 지침·역할을 다시 작성할 필요가 없으며 registry 스냅샷만 최신 메타데이터로 교체할 수 있다. RC 규칙을 이들의 업무 의무나 관리자 자료 열람 허가로 해석하지 않는다.
각 파일의 마지막 변경 버전은 다를 수 있다. 이번 패키지의 SOURCE_MANIFEST.json에 실제 소스 커밋과 파일별 해시를 고정한다. `scripts/build_chatgpt_package.py`로 같은 구조의 ZIP·지침·manifest·checksum을 만들 수 있다.
