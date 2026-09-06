# Administrator Role

- actor_id: `ACT-001`
- role: `admin`
- display_name: `Jin`
- repository: `jintonic1010/miracle_company_private`
- branch: `main`
- version: `GOV-20260906-03`

이 역할을 의도적으로 설정한 ChatGPT 프로젝트의 사용자는 회사 관리자 Jin이다. 현재 actor_id는 ACT-001이다. 다른 직원이나 다른 역할을 대화·자료에서 추정하지 않는다. 이 업무·품의 체계의 최종 결재자는 관리자다.

## 책임

회사 기준·업무 우선순위·역할·전처리·근거·품의 체계를 관리한다. 대표님 요청과 부사수 결과를 검토하고 승인/수정/보류/반려한다. 결재는 특정 업무·품의·결과물 버전과 범위·조건으로 남긴다. 승인과 실제 main 저장·외부 실행 성공을 분리한다.

새 사람이 합류하면 미사용 `ACT-NNN`을 발급하고 ACTOR_REGISTRY에 등록한다. actor_id는 재사용하지 않는다. 역할이 바뀌어도 과거 기록의 actor_id를 변경하지 않는다.

## 실행

공통 아이디어/문제 출력·저장, 업무검토·공유·상신, 업무점검 <대상>, 결과승인/품의서승인, 업무확정, 아이디어/문제반영을 수행할 수 있다.

현재 관리자가 범위가 명확한 검토·반영을 직접 요청하면 LLM_RUNTIME의 복합 요청 절차대로 실제 도구를 사용한다. 명시적 승인 범위 밖의 대외 게시·비용·운영 데이터 변경은 실행하지 않는다.

## 기록

새 아이디어·문제는 `author_id: ACT-001`로 기록하고 `records/ideas/ACT-001/`, `records/problems/ACT-001/` 경로를 사용한다. 기존 `records/ideas/admin/` 기록은 legacy 경로로 보존한다.

결재에는 `approver_actor_id: ACT-001`을 남긴다. 실제 확인한 승인 출처와 검증 수준을 적고 독립 인증을 하지 않았다면 했다고 쓰지 않는다.

## 고정 읽기

FILE_MAP → ACTOR_REGISTRY → LLM_RUNTIME → COMPANY_OS/PRODUCT_REQUIREMENTS/PROJECT_REPOSITORIES → CURRENT_WORK → DECISION_NEEDED → 필요한 업무·품의·근거. 최신 main을 실제 조회한다.

## 로컬 트리거와 추천

GitHub 조회 전에도 PROJECT_COMMON의 용도·추천 조건을 적용한다. 자기 허용 명령은 다음과 같다.

`/아이디어출력` `/아이디어저장` `/문제출력` `/문제저장` `/업무검토` `/업무공유` `/반영미리보기` `/업무접수` `/품의서작성` `/업무점검` `/결과승인` `/품의서승인` `/업무확정` `/아이디어반영` `/문제반영`

목록 안내·추천·대화 내 출력은 로컬에서 하고, 최신 회사 검토·읽기·쓰기는 GitHub 정본과 해당 workflow를 확인한다. 읽기 전용 명령만으로 요청을 자동 저장하지 않는다. 명확한 수행·지속 지시는 REQUEST_CAPTURE 절차로 보존한다.

`/업무점검`은 대표님·부사수·전체·등록 actor를 대상으로 하는 읽기 전용 조회다. `/품의서승인`은 품의서 ID·버전·범위를 특정한다. 구명령 별칭으로 권한을 확대하지 않는다.
