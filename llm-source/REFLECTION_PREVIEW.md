# Reflection Preview

- Repository: `jintonic1010/miracle_company_private`
- Branch: `main`
- Trigger: `/반영미리보기`
- Allowed roles: `representative`, `admin`
- Mode: read-only

## 목적

저장된 아이디어·문제를 실제 회사 기준에 반영하기 전에, **반영하면 무엇이 어떻게 달라질지**를 미리 확인한다.

이 기능은 제안의 영향 분석이지 승인·반영·확정 기능이 아니다.

## Exact Trigger Gate

현재 사용자 메시지에 정확한 `/반영미리보기` 문자열이 있을 때만 실행한다.

- 비슷한 표현이나 의도를 트리거로 추론하지 않는다.
- 이전 메시지의 트리거를 승계하지 않는다.
- 이 트리거는 GitHub에 어떤 파일도 쓰거나 수정하지 않는다.
- `/아이디어반영`, `/문제반영`, `/업무확정`으로 자동 전환하지 않는다.

## 대상 선택

우선순위:

1. 현재 메시지가 특정 저장 기록 제목·경로를 명시하면 그 기록
2. 같은 대화에서 방금 저장 완료한 아이디어·문제가 하나로 명확하면 그 기록
3. 그 외에는 `records/PENDING_INDEX.md`를 읽고 현재 대화와 직접 관련된 후보만 선별

대상이 둘 이상으로 남으면 임의로 하나를 확정하지 말고 후보별로 짧게 구분해 보여준다.

대표님 역할에서는 다른 작성자의 기록을 임의로 탐색하지 않는다. 기본 대상은 `author_role: representative`인 기록이다.

## 읽기 범위

대상 기록을 정한 뒤 최신 `main`에서 필요한 것만 읽는다.

- 대상 `records/ideas/**` 또는 `records/problems/**`
- `llm-source/COMPANY_OS.md`
- `llm-source/PRODUCT_REQUIREMENTS.md`
- `llm-source/PROJECT_REPOSITORIES.md`
- `working/CURRENT_WORK.md`
- 대상과 직접 관련된 `llm-source/departments/*`
- 대상 기록이 연결한 `materials/normalized/**` 중 판단에 필요한 것만
- 실제 구현 상태가 영향 판단의 핵심일 때만 `PROJECT_REPOSITORIES.md`에서 대상 저장소를 찾아 최신 `main` 확인

관계없는 아이디어·문제 전체를 읽지 않는다.

## 분석 항목

반영 전에 다음을 구분한다.

### 현재 확정 기준
- 지금 `llm-source/`에 실제로 존재하는 기준

### 반영 시 예상 변경
- 추가될 요구사항
- 교체될 기존 기준
- 삭제·완화가 필요한 기존 기준
- `CURRENT_WORK`에 미칠 영향
- 관련 프로젝트/부서 문서 영향

### 충돌 / 결정 필요
- 기존 공식 기준과 충돌
- 아직 확인되지 않은 사실
- 비용·권한·법률·개인정보·운영 위험
- 대표 판단만으로 확정하면 안 되는 관리자 결정사항

### 예상 변경 파일

실제 쓰지는 않고, 반영된다면 변경 가능성이 있는 파일만 제시한다.

예:

```text
예상 변경 파일
- llm-source/PRODUCT_REQUIREMENTS.md — 신규 요구사항 추가 예상
- llm-source/departments/ERP_LOGISTICS.md — 운영 기준 보완 예상
- working/CURRENT_WORK.md — 진행업무 정합성 재정리 필요
- docs/requirement-changelog.md — 기존 확정 기준 변경 시 기록 필요
```

## 출력 형식

```text
반영 미리보기

대상
- ...

현재 확정 기준
- ...

반영 시 예상 변경
- ...

영향 범위
- ...

충돌 / 확인 필요
- ...

예상 변경 파일
- ...

상태
- 미리보기만 완료 / 실제 반영되지 않음
```

불필요한 항목은 생략할 수 있다.

## 권한 경계

대표님은 이 미리보기 결과를 바탕으로 의견을 추가하거나 업무검토·업무공유를 할 수 있다.

그러나 다음은 관리자만 가능하다.

- `/아이디어반영`
- `/문제반영`
- `/업무확정`
- 공식 `llm-source/` 변경
- 기존 확정 요구사항 교체·삭제

대표님의 `/반영미리보기` 결과가 `반영 가능`해 보여도 자동 반영하지 않는다.

## Final Rule

`/반영미리보기` = 영향 분석 전용 read-only 기능이다.

**예상 변경을 설명할 수는 있지만 실제 결정을 만들거나 회사 기준을 바꿀 수는 없다.**
