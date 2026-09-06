# Normalization Standard — 전처리 규격

- Version: 1.1 / 2026-09-06
- Authority: official
- Release: GOV-20260906-02

## 원칙

전처리는 원본을 의미 손실 없이 검색·검증·재사용 가능한 형태로 바꾸는 것이다. 조사·추론·추천·승인은 다른 단계다. `이것 어떨까`를 `실행 확정`으로 바꾸지 않는다. 정제본 오류는 새 revision으로 고치며 원본과 변경 이력을 보존한다.

## 공통 필드

가능한 객체에는 `id` 또는 `record_id`, `object_type`, `schema_version`, `revision`, `author_id`, `author_role`, `author_name`, `created_at`, `normalized_at`, `source_id/path/url`, `source_revision 또는 hash`, `source_locator`, `information_as_of`, `verification_status`, `authority`, `access_scope`, `related_work_ids`를 사용한다.

`author_id`는 ACTOR_REGISTRY의 안정적인 actor_id다. role/name은 당시 문맥 보존용이며 actor_id를 대체하지 않는다. 알 수 없는 값은 null 또는 명시적 unknown으로 남긴다.

## 원본 보존과 상태

실제 확보한 파일만 stored라고 표시한다. 링크만 있으면 reference_only, 원본이 없으면 missing, 실제 열어보지 않았으면 not_inspected다. 정제본으로 원본 바이너리를 복원했다고 주장하지 않는다.

## 문서·대화

제목·절·표·목록·단위·수치·날짜·조건·부정·예외·발언 주체를 보존한다. 원문이 `확정`이라고 해도 회사 승인 여부는 별도다. 원문 속 주장(source_assertion), 독립 검증 사실, 해석, 제안, 미확인을 분리한다.

## 표·상품 데이터

원본 열과 표준 열의 매핑, SKU 문자열의 앞자리 0, 통화, 세금 포함 여부, 날짜·시간대를 보존한다. 결측/0/공백/해당 없음을 구분한다. 판매량·조회수·검색량·순위·주문수는 다른 지표다. `베스트`라는 열 이름으로 판매량을 추정하지 않는다.

중복 제거 기준, 제외 행의 원래 위치·사유, 충돌 값을 남긴다. 입력 행 수=유효 행 수+제외/격리 행 수를 검수한다. 분석 가능한 CSV/표를 남기고 Markdown 요약만 보존해 구조·정밀도를 잃지 않는다.

## ID와 경로

actor_id, idea/problem/work/decision ID는 경로·담당자·도구·현재 role이 바뀌어도 유지한다. 동일 사람의 role 변경은 actor_id를 바꾸지 않고 registry의 현재 role을 갱신한다. 다른 사람이 자리를 인수하면 새 actor_id를 발급한다.

기존 role 기반 기록 경로는 이관만을 이유로 이동하지 않는다. 새 기록은 actor_id 경로를 사용하며 PENDING_INDEX/normalized metadata가 ID와 경로를 연결한다.

## 정정과 이관

supersedes, 정정 사유, 영향받는 분석·품의·승인 목록을 연결한다. 동일 입력·변환 버전은 재실행으로 중복 생성하지 않도록 식별한다. 정당한 개인정보 삭제·보안 조치는 보존보다 우선할 수 있다.

## 검수

구조 검수 통과 ≠ 사실 검증 통과 ≠ 관리자 승인. 출처 누락, 원본 없음, 내용 상충, 오래된 정보는 issue로 남기고 사실로 승격하지 않는다. 전처리 작업은 법률·가격·시장 수치의 최신 재검증을 자동 포함하지 않는다.
