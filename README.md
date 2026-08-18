# Miracle Company Private

대표님과 Jin이 함께 관리할 회사 내부 AI·사업 자산 저장소입니다.

## Current Safety Status

> **현재 이 저장소는 GitHub에서 `public`으로 확인되었습니다.**
> 비공개(`private`) 전환이 확인되기 전에는 대표님 Claude 프로젝트 자료, 사업 아이디어, 대화 기록, 고객정보, 내부 문서 등 비공개 자료를 업로드하지 마세요.

## Intended Use

비공개 전환 후 다음 자료를 프로젝트별로 분리해 관리할 예정입니다.

- 대표님 Claude 프로젝트별 지침, 메모리, 컨텍스트 및 생성 문서
- 프로젝트별 원본 자료와 정제된 AI 소스
- 특정 프로젝트에 속하지 않는 사업 아이디어
- 대표님과 Jin만 공유해야 하는 내부 기획 자산

## Planned Structure

```text
projects/
  <project-name>/
    raw/
    normalized/
    analysis/
    history/

business-ideas/
```

실제 폴더 구조는 원본 자료 전수 확보 후 재분석하여 확정합니다.

## Access Boundary

- 대표님: 접근 가능
- Jin: 접근 가능
- 일반 개발자: 접근하지 않음
- 실제 개발 프로젝트는 이 저장소와 분리된 별도 회사 프로젝트 저장소에서 관리

## Data Protection

다음 자료는 저장소가 비공개이더라도 별도 검토 없이 올리지 않습니다.

- 고객 실명, 전화번호, 주소 등 원본 개인정보
- API 키, 비밀번호, 인증 토큰 및 `.env`
- 운영 DB, 캐시, 인덱스 및 기타 런타임 민감 데이터

---

**다음 조치:** GitHub 저장소 가시성을 `private`으로 전환한 뒤 실제 대표님 AI 자산 반입을 시작합니다.
