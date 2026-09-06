# 업무검토·업무업데이트 — GOV-20260906-05

## 업무검토: 세 역할, 읽기 전용
최신 FILE_MAP/ACTOR_REGISTRY/자기 ROLE/LLM_RUNTIME/COMPANY_OS/PRODUCT_REQUIREMENTS/PROJECT_REPOSITORIES/CURRENT_WORK/PENDING_INDEX 및 관련 REQUEST_INDEX·DECISION_INDEX를 읽는다. 관련 원문·정제본·근거만 선택하고 구현 사실이 필요할 때만 대상 개발 저장소를 읽는다.
classification=idea/problem/work/mixed/policy_change, result=PASS/REVISION/HOLD, 현재 기준, 중복/충돌, 근거·미확인, proposed_scope, recommended_next_action과 이유를 출력한다. work는 업무 후보이지 승인된 업무라는 뜻이 아니다.
검토할 내용의 fingerprint/content_hash, 대상 revision, 조회 commit, 관련 결정 ID·활성 제한, 실제 접근한 근거·기준을 review_snapshot으로 표현한다. 이 명령 자체는 요청/검토 파일·원장·목차·알림 영수증을 쓰지 않는다. 이후 명시적 제출 때 해당 스냅샷을 저장한다.
idea는 아이디어저장, problem은 문제저장, 실제 work PASS는 업무요청 또는 역할에 맞는 품의서작성, 정책 후보는 반영미리보기를 안내한다. PASS가 자동 제출·승인·W 생성이 아니다. 단순 '해볼까'를 실행 지시로 바꾸지 않는다.

## 관련 과거 결정
같은 R/SUB는 최신 결정과 이전 이유를 반드시 확인한다. 새 건은 동일 목적·대상·실행 범위의 직접 중복만 경량 인덱스로 찾아 원문 확인한다. 단어 하나의 유사성으로 엮지 않는다.
당시 결정·일자·이유 → 이번 변경·근거 → 사유 해소 여부 → 현재 가능한 다음 행동을 정리한다. 과거 반려는 영구 금지가 아니며, 유효한 지속 제한만 별도로 준수한다. 현재 held인 같은 건은 읽음 알림 여부와 무관하게 보류 상태를 안내한다. 관련 없는 옛 반려·개인 평가를 꺼내지 않는다.

## 업무업데이트: 관리자·배정 부사수
W-ID가 없는 요청/품의는 갱신 대상 업무가 아니다. 최신 W와 연결된 실제 D·버전·승인 범위를 확인한다. 관리자 또는 assigned_to_actor_id인 부사수만 자신의 범위 내 수행 내용을 갱신한다. 대표님은 자기 요청을 수정·조회할 수 있지만 W 실행 상태를 갱신하지 않는다.
기록 내용은 실제 수행자·시점·한 일·근거·결과물 버전·남은 일·문제·다음 행동이다. 보고자와 실제 수행자는 다를 수 있다. 없는 수행·담당·기한·성과를 만들지 않는다.
새 업무 생성·승인 필드 변경·범위 확대·게시·지출을 이 명령에 섞지 않는다. 신규 범위는 다시 요청/품의→관리자 결정이다. 승인 중단/철회된 범위는 계속 진행하지 않는다. 오래된 승인이나 INBOX 캐시를 근거로 실행하지 않는다.
W revision을 올리고 CURRENT_WORK·ACTIVE/BLOCKED/DECISION_NEEDED 및 필요한 HISTORY를 함께 갱신한다. 업무 완료는 지정 산출물·검수·필요 승인이 실제 충족될 때만 한다. 순수 진행 갱신은 매번 전체 제안 검토를 새로 요구하지 않되 승인·범위 안전성 확인은 생략하지 않는다.
첨부는 materials/originals/<actor_id>/work/YYYY-MM-DD와 normalized를 분리해 source/work ID로 연결한다. 회사 기준·과거 결재·타인 기록·미반영 I/P는 자동 변경하지 않는다. COMMON_IO로 검증 후 보고한다.
