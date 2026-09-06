# 업무검토·업무공유 — GOV-20260906-03

세 역할의 허용 범위 안에서 적용한다. 요청 접수는 REQUEST_CAPTURE, 품의서는 SUBMISSION_WORKFLOW를 따른다.

## 업무검토 — 읽기 전용

`/업무검토`는 최신 FILE_MAP, ACTOR_REGISTRY, 자기 ROLE, LLM_RUNTIME, COMPANY_OS, PRODUCT_REQUIREMENTS, PROJECT_REPOSITORIES, CURRENT_WORK, PENDING_INDEX를 확인한다. 관련 부서·원장·정제본만 추가한다. 미반영 기록은 목차로 골라 읽고, 이미 반영된 내용은 현재 공식 기준을 우선한다. 코드 구현 주장이 중요할 때만 해당 구현 저장소의 최신 main을 직접 확인한다.
회사 방향 충돌, 기존 기준 변경, 중복·모순, 관련 아이디어·위험, 보류·폐기된 내용, 확정/협의 혼합, 근거 없는 수치, 민감 데이터, 주체·범위·현재 상태·다음 행동, 첨부 확보·정제 가능성을 검토한다.

출력: `classification`, `review_result: PASS/REVISION/HOLD`, 현재 확정 기준, 진행/협의, 관련 기록·근거, `recommended_next_action`과 이유. 관련 항목이 없으면 짧게 표시한다.
idea → 아이디어저장, problem → 문제저장, work → 업무공유/업무접수, mixed → 별도 ID 연결, policy_change → 관리자 확정 전 변경안이다. PASS가 업무공유 허가는 아니다.
검토만 수행하면 요청 기록·업무 원장·인덱스를 쓰지 않는다. 검토 뒤 저장을 명시하면 적합한 별도 경로로 처리한다.

## 업무공유 — 쓰기

현재 대화에서 최근 유효한 검토가 PASS이고 실제 수행 업무로 분류된 항목만 공유한다. 순수 idea/problem이면 ROUTING_MISMATCH로 저장을 막고 올바른 저장을 안내한다.
검토 없이 `/업무공유`만 있으면 쓰지 않고 `/업무검토`를 안내한다. 현재 메시지에 검토+공유가 함께 있거나 자연어로 둘 다 명확히 요청하면 검토를 먼저 하고 통과 범위만 공유한다.
범위·핵심 내용·근거·main이 달라졌으면 재검토한다. 오래된 PASS를 다른 업무나 수정본에 재사용하지 않는다.
기존 `work/items/<work_id>.json`을 먼저 읽고 revision을 올려 추가·수정·보류·완료·다음 행동을 반영한다. 이름만 바뀌었다고 새 업무를 만들지 않는다. 완료/취소도 원장을 삭제하지 않는다. 현재 담당이 미정이면 null로 둔다.
CURRENT_WORK, ACTIVE/BLOCKED/DECISION_NEEDED를 원장 기반으로 함께 갱신하고 HISTORY에 주요 차이·작성 actor만 남긴다. 타인의 업무나 승인을 임의 변경하지 않는다.

## 첨부·공식화

새 업무 첨부는 `materials/originals/<actor_id>/work/YYYY-MM-DD/`와 `materials/normalized/<actor_id>/work/YYYY-MM-DD/`로 나누고 source/work ID로 연결한다. COMMON_IO 검수와 실패 보고를 적용한다.
공유는 COMPANY_OS·PRODUCT_REQUIREMENTS·부서 공식 요구사항·요구사항 changelog를 변경하지 않는다. 기존 공식 기준 변경안은 기존 확정/변경 협의로 구분하고 관리자 `/업무확정` 때만 교체한다.
참고한 아이디어·문제는 자동 reflected/resolved 처리하거나 pending에서 제거하지 않는다. 아이디어를 조사한 업무 완료와 원 아이디어 채택은 별개다.
