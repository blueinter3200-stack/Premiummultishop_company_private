# 세 ChatGPT 프로젝트 배포

- Release: GOV-20260906-01
- 저장소 파일과 실제 프로젝트 설정은 별개의 배포 대상이다.

각 프로젝트의 지침 칸에 해당 PROJECT_INSTRUCTIONS.md 본문을 붙여넣는다. 공통 첨부는 `chatgpt/PROJECT_COMMON.md`, 역할 첨부는 관리자 `roles/ADMIN.md`, 대표 `roles/REPRESENTATIVE.md`, 부사수 `assistant/00-role/ROLE.md` 중 자기 것 하나다. 부사수는 RULES.md를 추가할 수 있다.

기존 ADMIN_ROLE/REPRESENTATIVE_ROLE/WORK_CHAT/PROJECT_COMMON 첨부가 구기준이면 최신 묶음으로 교체한다. 한 프로젝트에 서로 다른 역할을 동시에 넣지 않는다. 특히 일반 직원 개인화용 소스와 관리자/대표/부사수 회사 운영 소스를 혼합하지 않는다.

업무판·모든 근거·원본 전체를 프로젝트 첨부에 복사하지 않는다. GitHub 연결 도구로 최신 main을 읽고 필요한 것만 추가한다. 공통 규칙은 GitHub 정본으로 유지하며 역할별 첨부는 진입 안내와 권한 역할을 고정한다.

## 설치 검수

각 방에서 '내 역할과 최신 main 기준 현재 업무를 확인해'를 실행해 실제 역할·저장소·읽은 커밋을 확인한다. 관리자만 결재하고 부사수는 상신할 수 있는지 테스트한다. 프로젝트의 지침 텍스트는 계정별 기술적 권한 분리를 대신하지 않는다. GitHub/Drive/제작 도구 연결은 실제 사용 가능 여부를 별도로 확인한다.

## 이번 배포의 한계

저장소의 지침·규격을 작성하는 것은 실제 세 프로젝트 설정을 편집한 것과 다르다. 자동 알림·역할별 API 권한·승인 서명 검증·Higgsfield 연동은 별도 구현·검증 대상이다. 이 파일을 생성했다는 이유로 구현 완료라 보고하지 않는다.

OpenAI 프로젝트 지침 위치 참고(2026-09-06 확인): https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt
