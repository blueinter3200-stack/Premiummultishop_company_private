# 아이디어 출력·저장 — GOV-20260906-05

세 역할은 자기 actor 기록에 사용한다. 아이디어출력은 현재 대화의 명확한 대상/활성 아이디어를 제목·아이디어·목적/기대효과·관련 업무·미정으로 정리하며 GitHub 조회나 쓰기가 없다. 없는 내용을 보충하거나 회사 확정 사실로 바꾸지 않는다.
아이디어저장은 COMMON_IO와 NORMALIZATION_STANDARD, templates/IDEA_RECORD.md를 따른다. 선행 출력은 필수가 아니다. 명확한 대상은 다시 묻지 않지만 모호한 여러 건을 임의로 선택하지 않는다.
I-YYYYMMDD-NNN,author_id,당시 role/name,created_at,status=saved,source,keywords를 남긴다. 발안자·기록자·정제자가 다르면 별도 actor를 기록한다. AI 자체를 사람 ID로 만들지 않는다.
records/ideas/<actor_id>/YYYY-MM-DD-<slug>.md에 저장하고 기존 role 경로·원문은 이동하지 않는다. 충돌 시 suffix, 동일 실행 재시도는 기존 ID를 확인한다. 원문과 의미 보존 정리본을 구분한다. 관련 R/W는 실제 존재할 때만 연결한다.
첨부 원본은 materials/originals/<actor_id>/ideas/YYYY-MM-DD, 정제본은 materials/normalized/<actor_id>/ideas/YYYY-MM-DD다. 표·단위·날짜·조건·요구를 보존하고 필요하면 CSV 등 정밀 자료를 둔다. 원본 미확보를 stored라고 하지 않는다.
기록과 PENDING_INDEX의 Ideas를 같은 단위로 저장한다. 목차에는 ID/actor/role/날짜/제목/keywords/경로/짧은 요약을 둔다. 기록 실패면 목차만 추가하지 않고 첨부/목차 일부 실패는 부분 저장으로 보고한다.
검토 PASS인 아이디어도 실제 업무가 아니다. 조사 요청이 명확하면 I와 R을 별개로 연결하며 W는 관리자 결정 후다. 아이디어 저장만으로 work/items,CURRENT_WORK,approvals,회사 기준,changelog,타인 기록을 바꾸지 않는다. 공식 채택은 관리자 아이디어반영이다. ID·경로·검증 커밋을 보고한다.
