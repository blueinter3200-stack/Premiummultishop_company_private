# Normalized Materials

첨부 원본을 LLM이 읽기 쉽게 정제한 Markdown 영역입니다.

경로 규칙:

```text
materials/normalized/<author-role>/ideas/YYYY-MM-DD/<original-name>.md
materials/normalized/<author-role>/problems/YYYY-MM-DD/<original-name>.md
materials/normalized/<author-role>/work/YYYY-MM-DD/<original-name>.md
```

정제 원칙:
- 의미 있는 본문, 제목, 표, 목록, 수치, 날짜, 결정·요구사항 구조를 보존
- 바이너리 메타데이터, XML, 앱 캐시, 중복 시스템 잔여물은 제거
- 원본에 없는 사실을 새로 만들지 않음
- 원본 파일 경로, 작성 역할, 정제일을 문서 상단에 기록
- 원본이 길어도 LLM이 업무 맥락을 파악할 수 있도록 구조를 보존하면서 불필요한 포맷 잔여물만 제거

관련 질문·업무검토·저장 기록 확인 때 필요한 정제본만 선택적으로 읽습니다. 폴더 전체를 반복해서 읽지 않습니다.
