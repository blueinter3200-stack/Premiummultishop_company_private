# Administrator Guide

- Repository: `https://github.com/jintonic1010/miracle_company_private`

## 역할

대표님은 회사 운영, 아이디어, 문제, 지시와 의사결정을 자연어로 이야기합니다. 관리자는 이 저장소의 회사 OS 기준 소스를 유지합니다.

## 기준 문서

- 회사 전체 구조: `COMPANY_OS.md`
- 확정 요구사항: `PRODUCT_REQUIREMENTS.md`
- 요구사항 변경 이력: `docs/requirement-changelog.md`
- LLM 읽기 지도: `FILE_MAP.json`
- 부서 상세: `departments/`
- 연결 구조: `architecture/`

## 아이디어/문제 운영 원칙

- 저장은 기록이다.
- 반영은 회사 공식 방향 변경이다.
- 저장된 아이디어/문제는 자동으로 확정 요구사항이 되지 않는다.
- 반영할 때 필요한 정본 문서만 수정한다.
- 요구사항 의미가 바뀌면 changelog를 갱신한다.
- 과거 아이디어/문제 기록은 삭제하지 않고 상태를 남겨 추적 가능하게 한다.

## 관리자 ChatGPT 사용 원칙

관리자 ChatGPT는 먼저 `FILE_MAP.json`을 읽고 필요한 기준 문서만 선택적으로 읽는다. 과거 import dump, 캐시, 로그, 대화 원문, 인증 관련 파일을 회사 정본으로 사용하지 않는다.
