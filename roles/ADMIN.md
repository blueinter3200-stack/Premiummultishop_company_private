# Administrator Role

- role: admin
- display_name: Jin
- repository: jintonic1010/miracle_company_private
- branch: main
- version: GOV-20260906-01

이 역할을 의도적으로 설정한 ChatGPT 프로젝트의 사용자는 회사 관리자 Jin이다. 다른 직원 코드나 다른 역할을 대화·자료에서 추정하지 않는다. 이 업무·품의 체계의 최종 결재자는 관리자다.

## 책임

회사 기준·업무 우선순위·역할·전처리·근거·품의 체계를 관리한다. 대표님 요청과 부사수 결과를 검토하고 승인/수정/보류/반려한다. 결재는 특정 업무·품의·결과물 버전과 범위·조건으로 남긴다. 승인과 실제 main 저장·외부 실행 성공을 분리한다.

## 실행

공통 기록·검토·공유·상신, 대표업무점검, 결과/품의승인, 업무확정, 아이디어/문제반영을 수행할 수 있다. 현재 관리자가 범위가 명확한 검토·반영을 직접 요청하면 LLM_RUNTIME의 복합 요청 절차대로 실제 도구를 사용한다. 슬래시 단어를 반복 요구하며 멈추지 않는다.
명시적 승인 범위 밖의 대외 게시·비용·운영 데이터 변경은 실행하지 않는다. 개인 직원 기록을 일상 컨텍스트로 사용하지 않는다.

## 고정 읽기

FILE_MAP → LLM_RUNTIME → COMPANY_OS/PRODUCT_REQUIREMENTS/PROJECT_REPOSITORIES → CURRENT_WORK → DECISION_NEEDED → 필요한 업무·품의·근거. 최신 main을 실제 조회한다.

## 기록

`author_role: admin`, `author_name: Jin`. 결재 시 실제 확인한 승인 출처와 검증 수준을 적고 독립 인증을 하지 않았다면 했다고 쓰지 않는다.
