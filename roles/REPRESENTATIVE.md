# Representative Role

- role: `representative`
- display_name: `대표님`
- repository: `jintonic1010/miracle_company_private`
- branch: `main`

이 역할 소스가 ChatGPT 프로젝트에 들어 있으면 현재 사용자는 미라클 회사 대표님이다.

## 권한
- 아이디어 출력/저장
- 문제 출력/저장
- 업무검토
- 업무공유

## 업무공유 규칙
- `/업무검토`는 읽기 전용이다.
- 같은 대화의 최신 `/업무검토`가 `PASS / 공유 가능`인 경우에만 `/업무공유`를 실행한다.
- 검토 후 핵심 내용이 바뀌면 다시 검토한다.
- 업무공유는 `working/CURRENT_WORK.md`를 최신화하지만 공식 요구사항을 확정하지 않는다.

## 회사 기록 작성자 메타데이터
- `author_role: representative`
- `author_name: 대표님`

## 제한
공식 회사 기준을 변경하는 관리자 전용 `/아이디어반영`, `/문제반영`, `/업무확정`은 실행하지 않는다.

역할을 대화 내용이나 말투로 추론하지 않는다.
