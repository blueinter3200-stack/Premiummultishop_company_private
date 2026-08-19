# Work Governance

- Repository: `https://github.com/jintonic1010/miracle_company_private`
- Branch: `main`
- Authority: official work-sharing governance
- Updated: 2026-08-19

## 목적

회사에서 진행·협의 중인 업무는 자유롭게 대화하되, `working/CURRENT_WORK.md`에 공유하기 전 **현재 확정된 회사 기준과 충돌하지 않는지 한 번 검토**한다.

진행업무와 공식 요구사항을 섞지 않기 위해 다음 3단계를 구분한다.

```text
자유로운 업무 대화
      ↓
/업무검토
      ↓
공유 가능 여부 판단
      ↓ PASS일 때만
/업무공유
      ↓
working/CURRENT_WORK.md 최신화
      ↓
관리자 결정 시
/업무확정
      ↓
llm-source/ 공식 기준으로 승격
```

## /업무검토의 기준

업무검토는 GitHub에 쓰지 않는 읽기 전용 단계다.

검토 시 최신 `main`에서 다음을 확인한다.

1. `FILE_MAP.json`
2. `llm-source/COMPANY_OS.md`
3. `llm-source/PRODUCT_REQUIREMENTS.md`
4. `working/CURRENT_WORK.md`
5. 현재 논의와 직접 관련된 `llm-source/departments/` 문서만 선택적으로
6. 현재 대화에서 특정 반영 아이디어/문제 또는 정제자료를 명시적으로 참조한 경우에만 해당 자료

저장된 아이디어·문제 전체나 원본 첨부파일을 습관적으로 전부 읽지 않는다.

## 업무검토 체크

- 현재 공식 회사 방향과 충돌하는가
- 기존 확정 요구사항을 변경하려는 내용인가
- 기존 CURRENT_WORK와 중복·모순되는가
- 확정사항과 협의사항이 섞였는가
- 이미 폐기·보류된 내용을 되살리는가
- 주체, 범위, 조건 또는 다음 단계가 너무 모호해 공유 후 오해할 위험이 있는가
- 실제 확인되지 않은 추정치를 확정 사실처럼 쓰는가
- 고객정보·운영 DB·인증정보 등 GitHub 금지 데이터가 포함되는가
- 첨부자료가 있다면 원본 보존과 LLM용 Markdown 정제가 가능한가

모든 항목을 형식적으로 채우게 만들 필요는 없다. **현재 진행상황을 다른 LLM/사람이 오해 없이 이어받을 수 있는지**가 핵심이다.

## 검토 결과

검토 결과는 셋 중 하나다.

- `PASS / 공유 가능`: 현재 내용으로 업무공유 가능
- `REVISION / 수정 필요`: 충돌·모호함을 고친 뒤 다시 검토
- `HOLD / 보류`: 현재는 공유하면 안 됨

`PASS`는 회사 공식 요구사항 확정을 의미하지 않는다. 진행업무판에 공유할 수 있다는 뜻이다.

## /업무공유 게이트

`/업무공유`는 같은 대화에서 가장 최근 `/업무검토`가 `PASS / 공유 가능`일 때만 실행한다.

검토 후 핵심 내용이 실질적으로 바뀌었다면 기존 PASS를 재사용하지 않고 `/업무검토`를 다시 실행한다.

업무공유 시:

1. 기존 `working/CURRENT_WORK.md`를 읽는다.
2. 현재 대화에서 검토 통과한 내용을 반영한다.
3. 새 내용 추가뿐 아니라 기존 내용의 수정·삭제·보류·완료도 반영한다.
4. 파일 전체를 다시 정리해 **현재 시점의 단일 최신판**으로 만든다.
5. 주요 변경 요약만 `working/HISTORY.md`에 짧게 추가한다.
6. 첨부자료가 있으면 가능한 경우 원본과 normalized Markdown을 분리 저장한다.

## 업무 첨부자료

업무공유에 첨부파일이 있는 경우:

```text
materials/originals/<author-role>/work/YYYY-MM-DD/<original-file>
materials/normalized/<author-role>/work/YYYY-MM-DD/<original-file>.md
```

- 원본은 보존용이며 기본 LLM 읽기 금지
- normalized Markdown은 필요한 본문·표·수치·날짜·결정·요구사항을 보존한 LLM용 정제본
- CURRENT_WORK에는 필요한 경우 normalized 경로만 연결
- 원본에 없는 사실을 추가하지 않는다

## /업무확정

관리자 전용이다.

CURRENT_WORK에 이미 공유된 항목 중 관리자가 명시적으로 확정한 내용만:

- `llm-source/COMPANY_OS.md`
- `llm-source/PRODUCT_REQUIREMENTS.md`
- 직접 관련된 `llm-source/departments/` 문서

에 반영한다.

기존 공식 요구사항을 추가·교체·삭제하거나 의미 있게 바꾸면 `docs/requirement-changelog.md`도 갱신한다.

확정 후 `CURRENT_WORK.md`는 다시 전체 최신판으로 정리해서 이미 확정된 내용과 아직 남은 협의사항이 섞이지 않게 한다.

## 기존 확정사항 수정

기존 공식 기준을 바꾸고 싶을 때도 바로 공식 문서를 고치지 않는다.

```text
변경안 논의
 → /업무검토
 → PASS
 → /업무공유
 → CURRENT_WORK에 "기존 확정 / 변경 협의안"으로 기록
 → 관리자 /업무확정
 → 공식 기준 교체 + changelog
 → CURRENT_WORK 재정리
```

따라서 LLM은 변경 확정 전에는 다음처럼 구분해 답한다.

- `현재 확정 기준`: 기존 공식 소스
- `현재 협의/진행 중`: CURRENT_WORK의 변경안
