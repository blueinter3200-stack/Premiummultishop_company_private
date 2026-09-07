# 회사 전체 업무진행현황·공용 맵 — GOV-20260907-02

## `/업무진행현황`: 세 역할 공통, 읽기 전용
기본 범위는 회사 전체다. `/업무진행현황 ERP`, `/업무진행현황 ACT-003`, `/업무진행현황 W-...`, `/업무진행현황 보류`처럼 필터할 수 있다. 필터는 결과만 좁히며 원문 접근 권한을 늘리지 않는다.

일반 호출은 **최신 main의 `working/WORK_STATUS_MAP.json` 하나만** 읽는다. 개인 INBOX/assignment view, FILE_MAP, REQUEST_INDEX, DECISION_INDEX, CURRENT_WORK, R/D/ASG/SUB/W 원문, miracle_n8n/miracle_erp 같은 외부 저장소를 자동으로 함께 읽지 않는다. 이 제한된 맵 조회는 일반 원격 진입 절차의 명시적 예외다.
맵이 없거나 schema/authority/checksum이 미지원·손상이면 `업무현황 맵 미적용/점검 필요`라고 알리고 기억·과거 대화 또는 자동 전체 원문 조회로 대체하지 않는다.

## 표시
전체 건수와 `approval_pending/revision_required/held/rejected/adopted/planning/plan_pending/in_progress/blocked/completed/cancelled/legacy_recheck` 등 기록된 단계를 분리한다. 각 항목은 가능한 범위에서 entry_id, R/W-ID, 공개 제목, 요청자/담당자 ID, current_stage, request_decision_status, assignment_status, plan_status, work_status, public latest_update, next_action, blockers, related_repositories, 마지막 external verified_at을 보여준다.
맵에 없는 진척률·날짜·완료를 계산해 만들지 않는다. 완료/반려/보류도 history 성격으로 남기며 기본 전체 조회에는 중요/활성 상태를 먼저 요약할 수 있다.
공용 맵에는 raw request text, 상세 결재 사유 중 비공개 내용, credentials/PII/private_notes를 넣지 않는다. 승인 전 R에 검증된 `public_summary.title`이 없으면 `업무요청 (원문 비공개)`처럼 ID/단계만 보인다.

## 상세·최신 확인
사용자가 특정 W/R의 원인·결재 근거·계획안 내용·실제 최신 코드 상태를 명시적으로 물으면 일반 원격 진입으로 전환한다. 역할 권한에 맞는 관련 정본만 읽고, 구현 최신 확인이면 해당 W의 등록 `related_repositories`만 실제 조회한다. 이 조회 결과를 맵에 저장하려면 별도의 허용 쓰기(예: 업무업데이트)가 필요하다. 읽기만으로 verified_at을 갱신하지 않는다.

## 맵은 파생물
`WORK_STATUS_MAP`은 승인·업무·결정 정본이 아니다. 업무 승인/실행 직전에는 정확한 R/D/ASG/SUB/W와 승인 범위를 확인한다. 맵을 직접 고쳐 업무를 승인/완료시키지 않는다.

## 쓰기 시 동시 갱신
업무요청 제출, 관리자 업무결정, 배정/재배정, 업무계획안 제출/결의, 업무업데이트/완료, ACT-001 관련 요청 의미 변경을 저장할 때 `scripts/work_status.py` projection을 정본 변경과 같은 변경 집합에서 갱신한다. 생성 대상에는 필요한 `public_summary`를 사용자/검증된 입력에서만 넣는다.
정본 저장 성공 + 맵 갱신 실패는 부분 실패다. 맵만 성공도 부분 실패다. 새 저장 직후 맵 schema/checksum과 대상 entry를 재검증한다.

## 여러 저장소
W의 `related_repositories`는 등록 저장소의 repo/branch/purpose를 가진다. `implementation_snapshots`는 실제 확인한 repo, branch, commit_sha 또는 PR/ref, verified_at, evidence_ref, 상태 요약을 가진다. 프로젝트 레지스트리에 없거나 권한 없는 저장소를 임의 연결하지 않는다.
업무 업데이트 시 실제 외부 구현을 확인했다면 해당 snapshot만 갱신한다. 외부 확인을 안 했으면 이전 snapshot/시점을 유지한다. 회사 업무 승인·맵 갱신은 외부 repo 변경/배포 승인이 아니고, commit/PR merged도 실제 배포·운영 완료의 증거가 아니다.

## 무결성
맵 schema_version, authority, records_latest_at, source_refs/checksum을 검증한다. 같은 entry_id 중복, 요청/W 연결 충돌, 허용되지 않은 public 필드, 미래/조작 verified_at은 거부한다. 기존 legacy 업무는 가짜 최신 상태로 이관하지 않고 legacy_recheck/recorded_state_only로 표시할 수 있다.
