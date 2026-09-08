---
record_id: P-20260908-001
object_type: problem_source_normalized
schema_version: 1
revision: 1
author_id: ACT-002
author_role: representative
author_name: 대표님
created_at: 2026-09-08
normalized_at: 2026-09-08
source_path: materials/originals/ACT-002/problems/2026-09-08/meta-pixel-security-incident-suspected-source.md
source_revision: 1
source_locator: conversation message ending with /문제저장
information_as_of: 2026-09-08
verification_status: source_assertion_only
authority: saved_input_not_approval
access_scope: internal
related_work_ids: []
---

# Meta 픽셀 보안 이슈 원문 정제본

## 원본에서 명시된 대상

- Meta 데이터 세트: `CĐ-HN`
- 데이터 세트 ID: `647894930506901`
- 화면상 소유자명: `Z799`
- 소유자 ID: `386312022711352`
- 생성 관련 표시: `Kareen Gomeez / 2023-04-22`
- 광고계정 관련 표시: `455684045006286`, `121104165361159`
- 정상 주력 후보로 제시된 자산: `241213cafe24 / 449337224670661`
- 회사와 관련 없어 보인다고 제시된 해외 도메인: 9개

## 원문 주장

- 위 조합이 정상적인 프리미엄멀티샵 픽셀 구조와 맞지 않는다는 판단.
- 외부 자산 연결 정황은 확인된 것으로 제시됨.
- 계정 침해 또는 과거 외부 대행사 연결 잔재 가능성 때문에 보안 감사가 필요하다는 판단.
- 단순 외부 픽셀/데이터 세트 연결만으로는 해당 외부인이 회사 결제수단으로 광고를 집행할 수 있다고 단정할 수 없다는 구분.
- 실제 광고비 집행 가능 여부는 광고계정 사람·파트너 권한 확인이 필요하다는 판단.

## 사실과 분리해야 하는 미확인

- 실제 계정 탈취 여부.
- 실제 무단 광고비 지출 여부.
- 두 광고계정 ID 중 회사 주력 광고계정이 무엇인지.
- Z799 또는 Kareen Gomeez가 광고계정 캠페인 생성·수정·결제 권한을 가진 적이 있는지.
- 해외 도메인 9개가 해당 데이터 세트에 연결된 정확한 원인.
- Meta 내부 로그상 최초 연결 주체·시점·권한.

## 제안된 대응

1. 연결·권한·활동·결제·캠페인 증거 보존.
2. 사람·파트너 권한, 개인계정 비밀번호, 로그인 세션, 2단계 인증 점검.
3. 회사 광고계정 ID를 확정한 뒤 `CĐ-HN` 연결 해제 판단.
4. 2023-04-22 이후 캠페인·결제수단·관리자·파트너 변경 이력 감사.
5. Meta Business Security Review 접수 및 연결/권한/무단지출/외부공유 감사 요청.
6. 침해와 무단 광고비가 실제 확인된 경우에만 환불/광고 크레딧 검토 요청.
7. Meta 로그 보존, 케이스 ID, 서면 조사 결과 요청.

## 검증 상태

이 정제본은 대표님이 현재 대화에 제공한 원문을 구조화한 것이다. 저장 과정에서 Meta 계정 화면, 거래내역, 캠페인 로그, Facebook Help Center 링크 또는 Meta 내부 로그를 독립적으로 재검증하지 않았다. 따라서 `source_assertion_only` 상태를 유지한다.
