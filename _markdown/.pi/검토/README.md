---
source_path: ".pi/검토/README.md"
source_filename: "README.md"
source_type: "text"
source_size_bytes: 4099
source_modified_at: "2026-08-17T18:38:52+09:00"
source_sha256: "786e9f5ac4b786f4df0035b5aabd8f69f84bdc9e7b512a805fe2f6bbe6b0caff"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
# 외부 텍스트 코퍼스 감사 보고서

## 목적

현재 작업 폴더 `C:\Users\JIN\Desktop\미라클인베스트\.pi`를 애플리케이션 코드가 아니라 **문서 컬렉션과 AI 활용용 지식 자산**으로 보아 구조, 실제 내용, 전처리 흔적, 중복, 누락, 분류 기준을 감사했다. 원본은 수정하지 않았고 결과만 `검토/`에 작성했다.

## 무엇을 확인했나

- `검토/`를 제외한 파일 303개, 하위 디렉터리 212개, 총 595,318,619바이트
- 최상위 디렉터리 59개 중 실제 파일이 있는 디렉터리 10개, 비어 있는 디렉터리 49개
- Markdown 96개 전체의 경로·크기·줄 수·제목·헤딩·메타데이터 패턴
- 핵심 지식 영역인 `BusinessVault/`와 `HermesWiki/`의 모든 Markdown 그룹
- `BusinessVault/`의 계획·조사·결정·아이디어·시장 인덱스 실제 본문 표본
- `HermesWiki/`의 일일기록 6개 전체와 인덱스·변경 로그
- `.agents/`의 설치된 스킬 21개와 로컬 설치 잠금 파일
- `.claude/`의 대화 기록·작업 기록·설치 스킬 구조. 자격증명·개인키 값은 읽거나 기록하지 않음
- DOCX 1개는 전체 텍스트와 표를 추출해 확인
- PDF 1개는 9페이지 전부 렌더링해 확인
- 정확한 파일 해시 중복, 문서 유사군, 빈 파일, UTF-8 상태, 위키링크 해석 가능성, 누락 참조

## 전체 자료 요약

현재 폴더는 하나의 전처리 코퍼스가 아니다. 다음 네 종류가 한 루트에 섞여 있다.

1. `BusinessVault/`: Premium MultiShop과 BELLOON의 사업 조사·전략·결정·실행 자료
2. `HermesWiki/`: 일상·업무 흐름을 날짜별로 요약한 개인 위키
3. `.agents/`, `.claude/skills/`, `Claude/`: AI 스킬·설치 가이드·생성 산출물
4. `.cache/`, `.hermes-sync/`, `.ssh/`, `Intel/` 등: 코퍼스가 아닌 프로그램·동기화·보안·로그 파일

사람이 읽는 두 볼트의 Markdown은 67개, 약 545KB다. 전체 568MB가량 중 대부분은 브라우저 실행 파일, Obsidian 플러그인, 동기화 실행 파일이다.

## 읽기 순서

1. [CORPUS_OVERVIEW.md](CORPUS_OVERVIEW.md)
2. [FOLDER_CONTENT_MAP.md](FOLDER_CONTENT_MAP.md)
3. [SPLIT_AND_GROUPING_PROPOSAL.md](SPLIT_AND_GROUPING_PROPOSAL.md)
4. [PROPOSED_FOLDER_STRUCTURE.md](PROPOSED_FOLDER_STRUCTURE.md)
5. [CURRENT_TO_PROPOSED_MAPPING.md](CURRENT_TO_PROPOSED_MAPPING.md)
6. [CURRENT_STRUCTURE_AUDIT.md](CURRENT_STRUCTURE_AUDIT.md)
7. [PREPROCESSING_ANALYSIS.md](PREPROCESSING_ANALYSIS.md)
8. [DATA_QUALITY_FINDINGS.md](DATA_QUALITY_FINDINGS.md)
9. [file-map.json](file-map.json)

## 텍스트 전체 읽기 여부

**표본 확인**이다.

- 모든 파일은 인벤토리·크기·해시 수준으로 확인했다.
- Markdown 96개는 모두 구조적으로 검사했다.
- `BusinessVault/`의 사람이 읽는 Markdown 59개는 전부 제목, 도입부, 헤딩, 메타데이터를 확인했다.
- 폴더 인덱스, `04-decision-log.md`, 모든 `HermesWiki/journal/` 파일, 각 계획·조사 계열의 대표 문서는 더 깊게 읽었다.
- DOCX는 전체 문단·표를 추출했고 PDF는 9페이지 전체를 보았다.
- 대화 원문 JSONL, 자격증명, 개인키, 대형 프로그램 파일은 코퍼스 본문으로 읽지 않고 구조·레코드 유형·파일 서명 수준으로만 분류했다.

## 중요한 한계

- 로컬 자료만 사용했으며 GitHub의 대응 원문은 조회하지 않았다.
- 원자료 웹페이지나 현재 없는 `/opt/data/...` 파일과 내용 정확성을 대조하지 않았다.
- 일부 사업 문서의 작성 주체와 자동 생성 범위는 작업 기록으로 일부 확인되지만 모든 문서의 정확한 생성 경로는 `Needs verification`이다.
- DOCX 렌더러가 LibreOffice 부재로 실행되지 않아 문서 레이아웃은 확인하지 못했다. 본문과 표는 전체 추출했다.
- 이 감사의 수치 기준은 보고서 생성 전 원본 상태이며 `검토/`는 집계에서 제외했다.

Runtime verification: not applicable to corpus-structure audit

