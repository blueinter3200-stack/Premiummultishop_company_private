# Administrator Role

- role: `admin`
- display_name: `Jin`
- repository: `jintonic1010/miracle_company_private`
- branch: `main`

이 역할 소스가 ChatGPT 프로젝트에 들어 있으면 현재 사용자는 미라클 회사 관리자다.

## 권한
- 아이디어 출력/저장
- 문제 출력/저장
- 업무검토
- 업무공유
- 아이디어반영
- 문제반영
- 업무확정

## 업무공유 규칙
- `/업무검토`는 최신 `main`의 공식 기준과 현재 업무를 비교하는 읽기 전용 단계다.
- 같은 대화의 최신 `/업무검토`가 `PASS / 공유 가능`인 경우에만 `/업무공유`를 실행한다.
- 검토 후 핵심 내용이 바뀌면 다시 검토한다.
- `/업무공유`는 CURRENT_WORK를 최신화할 뿐 공식 요구사항 확정이 아니다.

## 관리자 전용 확정
- `/아이디어반영`
- `/문제반영`
- `/업무확정`

`/업무확정`만 CURRENT_WORK의 선택된 내용을 공식 `llm-source/` 요구사항으로 승격할 수 있다.

## 회사 기록 작성자 메타데이터
- `author_role: admin`
- `author_name: Jin`

관리자는 공식 회사 기준과 확정 요구사항을 관리한다. 역할을 대화 내용이나 말투로 추론하지 않는다.
