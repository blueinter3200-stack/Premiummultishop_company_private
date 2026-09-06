# 문제 출력·저장 — GOV-20260906-03

명령: `/문제출력`, `/문제저장`. 세 역할 모두 자기 actor_id로 사용한다.

## 출력 — 로컬, 쓰기 없음

현재 대화에서 가장 최근의 명확한 문제를 제목, 문제, 현재 상황/영향, 원인 또는 확인 필요, 해결 방향 후보, 관련 업무로 정리한다. 원인 가설은 사실과 나눈다. GitHub를 읽지 않아도 정리할 수 있고 자동 저장하지 않는다.

## 저장

COMMON_IO와 NORMALIZATION_STANDARD, `templates/PROBLEM_RECORD.md`를 따른다. 선행 출력은 필수가 아니다. 현재 명확한 문제의 원문·정리본을 보존한다.
`record_id: P-YYYYMMDD-NNN`, `author_id`, 당시 role/name, created_at, `status: saved`, source, keywords를 남긴다. 발견자·요청자·기록자·정제자가 다르면 구분한다.
새 경로: `records/problems/<actor_id>/YYYY-MM-DD-<short-slug>.md`. 기존 기록과 ID를 덮어쓰지 않는다. 충돌 시 suffix, 재시도 시 동일 요청의 저장 결과를 확인한다.
관련 업무가 실제 있으면 `related_work_id` 또는 `related_work_ids`, 발견 단계, 확인된 영향, 미확인 원인, 필요한 확인을 남긴다. 없는 업무 ID·원인·담당·마감을 만들지 않는다.

## 첨부·목차

원본: `materials/originals/<actor_id>/problems/YYYY-MM-DD/<original-file>`.
정제본: `materials/normalized/<actor_id>/problems/YYYY-MM-DD/<original-file>.md` 및 필요한 정밀 자료.
실제 확보 여부·출처·버전을 표시하고 원본에 없는 사실을 만들지 않는다. 문제 기록과 PENDING_INDEX의 Problems를 함께 갱신한다. 기록 실패 시 인덱스만 쓰지 않는다. 일부 실패는 부분 저장으로 보고한다.

## 업무·해결과 분리

문제 저장 자체로 work를 blocked, 문제를 resolved, 해결책을 공식 정책으로 만들지 않는다. 실제 업무를 막는 영향이 확인되고 배정 업무의 상태 갱신이 허용·요청된 경우만 별도 WORK_WORKFLOW 절차로 원장과 조회판을 갱신한다. 근거 problem_id를 연결한다.
`/문제반영`은 관리자 전용이다. 해결 방향 채택은 reflected이며 실제 해결 증거가 있어야 resolved다. 부사수·대표님이 스스로 해결 완료나 공식 반영을 확정하지 않는다.
허용 쓰기는 자기 문제 기록·관련 첨부·pending index다. 저장만으로 회사 공식 소스·changelog·타인 기록·업무 상태를 바꾸지 않는다. 완료 시 ID·경로·검증 커밋을 보고한다.
