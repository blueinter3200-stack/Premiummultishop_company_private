# Miracle Company Private

대표님과 관리자가 함께 사용하는 **Miracle Company OS의 비공개 기준 저장소**입니다.

- Repository: `jintonic1010/miracle_company_private`
- GitHub: `https://github.com/jintonic1010/miracle_company_private`
- Visibility: private
- Default branch: `main`

## 목적

이 저장소는 대표님 ChatGPT와 관리자 ChatGPT가 회사 전체 구조, 확정 요구사항, 부서별 역할, 아이디어·문제 기록의 반영 기준을 같은 소스로 읽도록 하기 위한 회사 OS 소스 저장소입니다.

## LLM 권장 읽기 순서

1. `FILE_MAP.json`
2. `COMPANY_OS.md`
3. `PRODUCT_REQUIREMENTS.md`
4. 현재 질문과 관련된 `departments/` 또는 `architecture/` 문서
5. 필요할 때만 `docs/requirement-changelog.md`, `ideas/`, `problems/`, `projects/`

## 핵심 구분

- `COMPANY_OS.md`: 회사 전체 구조와 방향
- `PRODUCT_REQUIREMENTS.md`: 현재 확정된 요구사항
- `docs/requirement-changelog.md`: 확정 요구사항이 의미 있게 바뀐 기록
- `ideas/`: 아직 공식 요구사항이 아닌 아이디어
- `problems/`: 아직 공식 요구사항이 아닌 문제 기록
- `departments/`: 부서별 역할과 데이터 흐름
- `architecture/`: n8n 뼈대와 API 연결 원칙
- `data/db/`: DB 관련 문서·스키마·비민감 샘플만. 실제 운영 DB와 고객 개인정보는 Git에 저장하지 않음
- `archive/`: 과거 자료와 이전 구조에 대한 안내

## 중요 보안 원칙

고객 실명, 전화번호, 주소, 주문 원본 개인정보, API 키, 토큰, 비밀번호, SSH 개인키, `.env`, 운영 DB는 이 저장소에 저장하지 않습니다. 고객·판매·주문 데이터 자체는 ERP/운영 데이터 계층에서 관리합니다.

## 저장/반영 원칙

아이디어와 문제는 저장만으로 회사 공식 방향이 되지 않습니다. 관리자가 별도 반영 결정을 했을 때만 `COMPANY_OS.md`, `PRODUCT_REQUIREMENTS.md`, 부서 문서 등에 반영합니다.
