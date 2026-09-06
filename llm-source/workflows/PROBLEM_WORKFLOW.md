# 문제 출력·저장 — GOV-20260906-05

세 역할이 자기 actor로 사용한다. 문제출력은 현재 명확한 문제를 제목·상황/영향·원인 가설/확인 필요·해결 후보·관련 업무로 정리한다. GitHub 조회 없이 가능하며 저장하지 않는다. 가설은 사실과 분리한다.
문제저장은 COMMON_IO와 NORMALIZATION_STANDARD, templates/PROBLEM_RECORD.md를 따른다. 선행 출력은 강제하지 않는다. P-YYYYMMDD-NNN,author_id,당시 role/name,created_at,status=saved,source,keywords와 원문/정리본을 보존한다. 발견자·요청자·기록자·정제자가 다르면 구분한다.
records/problems/<actor_id>/YYYY-MM-DD-<slug>.md를 쓰고 과거 경로/ID는 보존한다. 충돌 시 suffix, 재시도 시 기존 결과를 확인한다. 실제 관련 W가 있으면 related_work_id,발견 단계,확인된 영향,미확인 원인,다음 확인을 연결한다. 없는 담당·기한·원인·W를 만들지 않는다.
원본은 materials/originals/<actor_id>/problems/YYYY-MM-DD,정제본은 materials/normalized/<actor_id>/problems/YYYY-MM-DD다. 출처·확보 여부·버전을 표시한다. PENDING_INDEX의 Problems와 함께 저장하고 부분 실패를 구분한다.
문제 저장 자체로 W를 blocked,문제를 resolved,해결안을 회사 정책으로 바꾸지 않는다. 실제 업무 영향과 승인된 갱신 권한이 있을 때 업무업데이트로 원장·조회판을 별도 변경한다. 해결 방향 채택은 관리자 문제반영이며 실제 해결까지 증거가 있어야 resolved다.
허용 쓰기는 자기 문제·첨부·pending이다. 타인 기록·회사 기준·결정·업무 상태를 저장 명령에 끼워 바꾸지 않는다. ID·경로·검증 커밋을 보고한다.
