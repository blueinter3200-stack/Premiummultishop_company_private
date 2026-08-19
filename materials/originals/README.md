# Original Materials

아이디어·문제 저장 또는 업무공유 시 관련 첨부파일의 **원본 보존 영역**입니다.

경로 규칙:

```text
materials/originals/<author-role>/ideas/YYYY-MM-DD/<original-file>
materials/originals/<author-role>/problems/YYYY-MM-DD/<original-file>
materials/originals/<author-role>/work/YYYY-MM-DD/<original-file>
```

`author-role`은 역할 소스에서 결정합니다.

- 대표님: `representative`
- 관리자: `admin`

기본 LLM 읽기 대상이 아닙니다. 원본 확인 요청이나 normalized Markdown 오류 확인이 필요할 때만 사용합니다.

원본이 저장되더라도 LLM은 평소 원본을 다시 열지 않고 대응되는 `materials/normalized/` Markdown을 우선 사용합니다.

API 키, 비밀번호, 토큰, SSH 개인키 등 인증 비밀과 실제 운영 고객 DB는 저장하지 않습니다.
