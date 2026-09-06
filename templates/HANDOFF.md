---
object_type: work_plan_or_progress_template
schema_version: 4
---
# 업무계획안 / 진행 보고 제목

- request_id / content_revision / content_hash:
- requester_actor_id / recorded_by_actor_id / source_verification:
- work_id: 채택 전이면 null. 가짜 W-ID 생성 금지.
- assignment_ref / proposed_assignee_actor_id:
- submission_id / revision:
- submitted_by_actor_id:
- work_revision: 실제 W가 있을 때만.
- report_type: progress 또는 submission 또는 verified_final
- requested_scopes / primary_scope: 계획 결의는 plan_execution, 업무 채택 필요 여부 별도.
- status: draft 또는 submitted
- review_snapshot: 제출 전 검토 대상·버전·근거·결과

## 결론과 관리자 결의 요청
어떤 요청/계획안 버전의 어느 범위를 결정받을 것인지. 업무 채택·담당 배정·계획 실행·결과수락·게시·지출은 구분한다.

## 요청 출처
실제 원문, 요청자/기록자/전달자, R-ID/directive/자료 경로. 구두 대표 요청은 reported_oral_request이고 미독립검증 여부를 표시한다. 직접 발언·관리자 승인으로 사칭하지 않는다.

## 작업지시와 수행 범위
배정받은 ASG의 승인된 요약·담당·목적·기대 산출물·제한을 연결한다. 사전 계획안은 배정/W 없음과 제안 담당을 구분한다. 본 작업은 아직 미실행이다.

## 관련 아이디어 / 문제
related_idea_ids, related_problem_ids. 아이디어·문제 기록과 현재 업무를 혼동하지 않음.

## 내부 근거
파일 ID/링크, 버전·시트·행/범위, 정보 기준일, 확인한 내용, 상품/SKU.

## 외부 근거·벤치마크
실제 링크, 확인일, 실제 확인 범위·영상 구간, 관찰, 참고 요소. 미접근·미시청은 구분.

## 적용 기준과 주요 판단 이유
근거 → 선택 기준 → 대안 비교 → 적용 이유. 가정은 별도 표시.

## 실행 방법·기획·스토리보드·결과물
단계별 방법·예상 산출물·비용/일정(미정은 null) 및 각 파일/영상의 실제 링크·ID·revision/hash.

## 검수 결과
상품 재현·문구 사실성·권리·개인정보·수치·승인 범위. 실제 도구 job/결과 확인.

## 미확인·리스크·차단 조건
불확실한 주장으로 결론을 확정하지 않음. 관련 과거 보류/반려 사유·현재 차이·해소 근거.

## 요청 승인
업무 채택 / 계획 실행 / 조사 / 제작 / 결과수락 / 게시 / 지출 / 정책변경 중 실제 필요한 범위와 조건. 승인 전 필요한 본 조사도 해당 범위를 먼저 계획으로 제출한다.

## 실제 저장·실행 결과
GitHub 경로·커밋, 생성/게시 영수증. 실행하지 않은 항목은 미실행. 계획 제출과 관리자 결의, 배정·알림 생성·표시·사용자 확인은 각각 구분한다.
