# 아이디어 출력·저장 — GOV-20260906-03

명령: `/아이디어출력`, `/아이디어저장`. 관리자·대표님·부사수의 자기 actor 기록에 적용한다.

## 출력 — 로컬, 쓰기 없음

현재 대화의 명확한 대상 또는 가장 최근 활성 아이디어를 제목, 아이디어, 목적/기대효과, 관련 업무, 미정으로 정리한다. GitHub 조회가 없어도 가능하다. 없는 내용을 억지로 넣지 않고 회사의 확정 사실이나 실행 지시로 바꾸지 않는다. 결과에 저장되지 않았음을 구분한다.

## 저장 — 최신 main 확인

COMMON_IO와 NORMALIZATION_STANDARD, `templates/IDEA_RECORD.md`를 따른다. 선행 `/아이디어출력`은 강제하지 않는다. 현재 대화에서 대상이 명확하면 실행하고 이미 제공된 내용을 다시 묻지 않는다. 여러 대상이 실제로 모호하면 임의 선택하여 쓰지 않는다.
`record_id: I-YYYYMMDD-NNN`, `author_id`, 당시 `author_role/author_name`, `created_at`, `status: saved`, `source`, `keywords`를 남긴다. 원 발안자·기록 작성자·정제자는 다르면 별도 actor 필드로 보존한다. AI 자체를 사람 ID로 만들지 않는다.
새 경로는 `records/ideas/<actor_id>/YYYY-MM-DD-<short-slug>.md`다. 기존 role 기반 경로와 원문은 이동하지 않는다. 충돌 파일은 덮어쓰지 않고 suffix를 쓴다.
원문 또는 의미를 보존한 발췌와 정리본을 구분한다. 관련 work/request가 실제 있으면 ID를 연결하고 없는 업무를 생성하지 않는다.

## 첨부·목차

원본: `materials/originals/<actor_id>/ideas/YYYY-MM-DD/<original-file>`.
정제본: `materials/normalized/<actor_id>/ideas/YYYY-MM-DD/<original-file>.md` 및 필요 시 CSV 등 정밀 자료.
제목·표·목록·단위·수치·날짜·조건·요구를 보존한다. 자료 확인·정제는 검증·승인이 아니다.
실제 기록과 `records/PENDING_INDEX.md`의 Ideas를 같은 변경 단위로 저장한다. 목차에는 record_id, actor_id, 당시 role, 날짜, 제목, keywords, 원문 경로, 1~2문장 summary만 둔다.
기록 실패면 목차를 추가하지 않는다. 목차 실패 또는 원본 첨부 실패는 실제 성공 범위를 나눠 보고한다.

## 경계

순수 아이디어는 업무검토 PASS여도 업무공유하지 않는다. 조사 요청이 명확히 함께 있으면 원 아이디어와 조사 업무를 별도 ID로 연결하되 조사 완료는 아이디어 채택이 아니다.
아이디어 저장만으로 llm-source, CURRENT_WORK, work/items, approvals, changelog, 타인 기록을 변경하지 않는다. 동시 요청이 명시한 별도 업무만 별도 검토·권한으로 처리한다.
저장 완료 후 기록 경로·ID와 확인한 커밋을 보고한다.
