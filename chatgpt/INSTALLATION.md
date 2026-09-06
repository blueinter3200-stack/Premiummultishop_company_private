# 세 ChatGPT 프로젝트 배포

- Release: GOV-20260906-02
- 저장소 파일과 실제 프로젝트 설정은 별개의 배포 대상이다.

각 프로젝트의 지침 칸에 해당 PROJECT_INSTRUCTIONS.md 본문을 붙여넣는다. 공통 첨부는 `chatgpt/PROJECT_COMMON.md`, `llm-source/ACTOR_REGISTRY.json`이다.

역할 첨부:
- 관리자 ACT-001: `llm-source/actors/ACT-001/ROLE.md`
- 대표님 ACT-002: `llm-source/actors/ACT-002/ROLE.md`
- 부사수 ACT-003: `llm-source/actors/ACT-003/ROLE.md` + `llm-source/actors/ACT-003/RULES.md`

기존 구버전 역할/공통 소스가 있으면 최신 묶음으로 교체한다. 한 프로젝트에 서로 다른 actor/role을 동시에 넣지 않는다.

업무판·모든 근거·원본 전체를 프로젝트 첨부에 복사하지 않는다. GitHub 연결 도구로 최신 main을 읽고 필요한 것만 추가한다.

## 설치 검수

각 방에서 `내 actor_id, 역할, 최신 main 기준 현재 업무를 확인해`라고 요청해 actor_id와 role이 맞는지 확인한다.

추가 검수:
1. 대표님 방에서 순수 아이디어를 검토했을 때 `/아이디어저장`을 권장하고 `/업무공유`로 자동 넘기지 않는지.
2. 부사수 방에서 `/아이디어저장`, `/문제저장`이 ACT-003 경로로 저장되는지.
3. 관리자만 최종 결재·공식 반영을 수행하는지.
4. 새 사람 추가 시 새 ACT-NNN을 발급하고 기존 ID를 재사용하지 않는지.

프로젝트 지침 텍스트는 계정별 기술적 권한 분리를 대신하지 않는다. GitHub/Drive/제작 도구 연결은 실제 사용 가능 여부를 별도로 확인한다.
