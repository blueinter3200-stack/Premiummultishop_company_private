# Tool Execution — 실제 실행·저장 통제

- Version: 1.0 / 2026-09-06

## 실행 전

실제 연결 가능 도구, 읽기/쓰기 범위, 사용자 명시 요청, 관리자 승인 대상·버전·조건을 확인한다. 비밀키나 고객 개인정보를 GitHub에 넣지 않는다. 승인된 데이터 정리·내부 초안과 외부 공개·비용 집행·운영 데이터 수정은 분리한다.

## 제작 도구

Higgsfield 등은 교체 가능한 adapter다. 도구명만 언급됐다고 연결·계정·모델·사용권이 확인된 것은 아니다. 실제 job_id, 요청시각, 입력 파일 ID/버전, 모델·설정·프롬프트 버전, 출력 파일 ID/버전, 비용 확인값, 검수 결과를 기록한다. 미지원 필드를 만들어 채우지 않는다.
작업 접수 응답과 영상 제작 완료는 다르다. 생성 성공 후에도 실제 상품 재현·문구·이미지 권리·음원·개인정보를 검수한다. 게시 승인은 별도 확인한다.

## GitHub

최신 base commit/blob 확인, 관련 파일 집합만 수정, 가능한 한 원자적 커밋, force=false, 결과 ref·파일 재조회. 동시 변경은 최신 원본에 재적용하고 다른 사람 작업을 덮어쓰지 않는다. 브랜치 보호·계정 권한을 우회하지 않는다.
상태판·원장·pending index는 함께 반영한다. 실패 시 partial/failed를 남기고 실제 실패 범위를 보고한다. 커밋 성공만으로 외부 실행 성공을 주장하지 않는다.

## 재시도

조회 실패와 실행 실패를 구분한다. 외부 공개·결제·메시지 전송의 결과가 불확실하면 상태를 먼저 조회한다. 중복 실행을 피할 idempotency key 또는 외부 job ID가 있으면 사용한다. 없는 기능을 구현됐다고 쓰지 않는다.

## 결과 영수증

operation, work_id, decision_ref, request/version hash, started_at, completed_at, tool, external_id, destination, observed_result, verification_method, result_status, error를 기록한다. 민감 요청값은 마스킹한다. 자동 알림·다른 채팅방 통보는 실제 전송 확인이 있어야만 완료다.
