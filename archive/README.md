# Archive / Legacy Import Note

## 2026-08-18 import

이 저장소에는 과거 `_markdown/` 아래에 약 488개 원본을 Markdown으로 변환한 대규모 import가 들어왔습니다.

해당 import에는 다음이 혼합되어 있었습니다.

- BusinessVault 사업 자료
- HermesWiki 일지
- Claude 원시 대화/상태
- 브라우저/Chromium 캐시와 바이너리 메타데이터
- Intel 설치 로그
- Obsidian 플러그인 파일
- nested `.git` 메타데이터
- SSH/인증/환경 관련 민감 가능 자료
- 중복 변환 자료

현재 회사 OS 정본에서는 이 dump를 기본 읽기 범위에서 제거합니다. 필요 자료는 이후 프로젝트별로 안전하게 선별해 `projects/` 또는 별도 참조 저장소로 가져옵니다.

Git history는 보존되어 있으므로 이 정리만으로 과거 commit이 사라지지는 않습니다. 민감정보가 과거 이력에 포함된 경우 history rewrite와 자격증명/키 회전은 별도 보안 작업입니다.
