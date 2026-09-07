# GOV-20260907-02 Governance Overlay

- Authority: official additive requirements for the current release.
- Basis commit: `f94b3bbc7a85cf78425979f488d4b0661f4af43a`.
- This overlay supersedes conflicting GOV-20260907-01 workflow wording while preserving older historical records.

## GOV-050 — 회사 전체 업무진행현황
`/업무진행현황`은 ACT-001/002/003 공통 읽기 전용이며 대상 생략 시 회사 전체다. 일반 호출은 `working/WORK_STATUS_MAP.json`만 읽는다.

## GOV-051 — 현황 맵 거래 단위 갱신
업무요청·업무결정·배정/재배정·업무계획안 제출/결의·업무업데이트·완료·관련 요청 변경 저장 시 정본과 WORK_STATUS_MAP을 같은 변경 집합으로 갱신한다. 맵 갱신 실패는 전체 성공으로 보고하지 않는다.

## GOV-052 — 공용 요약과 비공개 원문 분리
공용 맵은 전체 업무의 ID·제목/제한 제목·요청자·담당·단계·결정상태·계획상태·업무상태·최근 공용요약·다음 행동·관련 저장소·확인시점을 표시할 수 있다. 다른 사람의 비공개 요청 원문·상세 결재 메모·개인자료 읽기 권한은 추가하지 않는다.

## GOV-053 — 관리자 직접 지시 복합 처리
ACT-001이 기존 R-ID 없이 구체적인 새 업무와 승인/담당 지시를 함께 주면 ACT-001 요청 원문 보존→최신 업무검토→업무결정→W→명시된 담당 ASG/N→WORK_STATUS_MAP을 한 처리로 연결한다. 기존 R가 대상이면 새 요청으로 바꾸지 않는다.

## GOV-054 — 다중 구현 저장소 연결
업무는 `related_repositories`로 등록 저장소의 repository/branch/purpose를 연결할 수 있다. 실제 확인한 full commit/PR/run/check/checked_at/evidence만 `implementation_snapshots`에 기록한다. 커밋/PR은 운영 배포나 업무 완료 증거가 아니다.

## GOV-055 — 제한 조회
일반 `/업무진행현황`은 원문 전수 조회·개인 INBOX 읽음 처리·외부 저장소 실시간 확인·맵 재생성을 하지 않는다. 상세/최신 구현 확인을 명시한 경우에만 추가 조회한다.
