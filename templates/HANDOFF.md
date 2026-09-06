---
object_type: submission_template
schema_version: 3
---
# 품의 / 진행 보고 제목

- request_id / content_revision / content_hash:
- work_id: 승인 전이면 null. 가짜 W-ID 생성 금지.
- submission_id / revision:
- submitted_by_actor_id:
- work_revision: 실제 W가 있을 때만.
- report_type: progress 또는 submission 또는 verified_final
- requested_scopes / primary_scope:
- status: draft 또는 submitted
- review_snapshot: 제출 전 검토 대상·버전·근거·결과

## 결론과 관리자 결정 요청
어떤 요청/품의서 버전의 어느 범위를 결정받을 것인지. 업무 시작·계획·결과수락·게시·지출은 구분한다.

## 요청 출처
실제 원문, requested_by_actor_id, R-ID/directive/자료 경로. 접수자가 요청자를 대신하지 않음.

## 관련 아이디어 / 문제
related_idea_ids, related_problem_ids. 아이디어·문제 기록과 현재 업무를 혼동하지 않음.

## 내부 근거
파일 ID/링크, 버전·시트·행/범위, 정보 기준일, 확인한 내용, 상품/SKU.

## 외부 근거·벤치마크
실제 링크, 확인일, 실제 확인 범위·영상 구간, 관찰, 참고 요소. 미접근·미시청은 구분.

## 적용 기준과 주요 판단 이유
근거 → 선택 기준 → 대안 비교 → 적용 이유. 가정은 별도 표시.

## 기획·스토리보드·결과물
각 파일/영상의 실제 링크·ID·revision/hash.

## 검수 결과
상품 재현·문구 사실성·권리·개인정보·수치·승인 범위. 실제 도구 job/결과 확인.

## 미확인·리스크·차단 조건
불확실한 주장으로 결론을 확정하지 않음. 관련 과거 보류/반려 사유·현재 차이·해소 근거.

## 요청 승인
업무 시작 / 조사 / 제작 / 결과수락 / 게시 / 지출 / 정책변경 중 실제 필요한 범위와 조건. 승인 전 필요한 본 조사도 해당 범위로 먼저 요청한다.

## 실제 저장·실행 결과
GitHub 경로·커밋, 생성/게시 영수증. 실행하지 않은 항목은 미실행. 품의서 제출과 관리자 결정, 알림 생성·표시·사용자 확인은 각각 구분한다.
