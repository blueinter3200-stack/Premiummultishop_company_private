# 관리자 새 업무 직접 지시 — GOV-20260907-02

현재 관리자 ACT-001의 구체적인 새 수행 지시 + 명시적 승인·배정 의도가 한 문장에 있으면 R 생성·검토·업무결정·W·선택적 ASG·수신자 N·공용 현황 맵을 한 변경 집합으로 연결한다. 별도 /업무요청 재입력을 요구하지 않는다. /업무결정 승인과 업무 내용을 같이 준 경우도 동일하다.

## 필수 경계
질문·인용·예시·호감, 단독 “승인”에서 대상을 특정하지 못한 경우, 읽기 전용/저장 금지에는 만들지 않는다. 새 요청이면 요청자/원문 기록자/소유자 ACT-001을 보존한다. 기존 대표님·부사수 R가 대상이면 그 원 요청자·R를 그대로 일반 업무결정에 사용하고 관리자 이름으로 중복 재등록하지 않는다.
최신 회사 기준·활성 업무·직접 중복·과거 제한을 실제 검토한다. 목적·범위·완료 기준이 불명확하면 부족한 사항만 확인하고 완료 기준·기한을 AI가 창작하지 않는다. 원문 보존 필요는 captured 단계로 분리하며 불합격한 검토를 통과한 것처럼 승인하지 않는다.

## 처리
scripts/decision_flow.py plan의 operation=direct_admin, command=/업무결정, outcome=승인, intent=direct_work_instruction을 사용한다. 실제 source.text/locator와 같은 request.original_text/source_locator, 요청자의 등록 정보, review_snapshot, 충돌 없는 R/D/W, 필요 ASG와 실제 instruction_text를 제공한다.
scripts/direct_requests.py는 임시 로컬 snapshot에서 submit_request 다음 decide를 순차 계획하고 한 bundle로 합친다. 원본 checkout·원격 저장소를 직접 쓰지 않는다. source_event_id와 fingerprint로 재시도를 구별하고 같은 사건은 같은 R/D/W/ASG를 사용한다. partial persistence는 기존 ID 복구 대상이다.
담당을 말하지 않으면 null이다. 부사수 지정은 work_adoption/planning과 별도 ASG·최초 알림이며 아직 존재하지 않는 계획의 실행 승인이 아니다. 관리자가 직접 하겠다고 명시한 경우만 ACT-001 self_direct와 정확한 직접 수행 범위를 사용한다. 이후 부사수에게 옮기는 것은 새 배정/계획 허가 확인이 필요하다.

## 반영
COMMON_IO와 WORK_STATUS_WORKFLOW를 적용한다. 최종 bundle의 expected_blobs·최신 main을 재확인하여 R/D/W/ASG/N/현황 맵을 같은 커밋으로 반영하고 내용을 재조회한다. 여러 저장소의 코드 쓰기는 별도 승인 범위이며 이 명령의 자동 부수효과가 아니다.
