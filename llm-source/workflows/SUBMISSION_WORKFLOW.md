# 품의서작성 — GOV-20260906-05

관리자·부사수가 사용한다. 대표님은 가벼운 업무요청을 사용하고, 부사수는 해당 R-ID에 상세 실행계획을 보강한다. 두 경로는 같은 요청을 향하며 별도 업무를 중복 생성하지 않는다.

## 선행 검토
최신 공통 규칙·대상 R/W·EVIDENCE_STANDARD·APPROVAL_GOVERNANCE와 관련 과거 결정을 읽는다. 유효한 검토가 없으면 작성 준비 검토를 먼저 하고 PASS인 실제 후보만 제출한다. HOLD/핵심 근거 부족은 draft 또는 조사 범위 요청으로 표시한다. '품의서'라는 이름으로 미검증 결론을 검증 완료로 승격하지 않는다.
원문 기록·현재 확보 자료 정리와 본 조사/제작은 다르다. 승인 전 본 조사가 필요하면 그 조사 자체를 요청한다. 현재 W가 없다고 가짜 업무를 생성하지 않는다.

## 내용
R-ID와 원문·요청자/발안자/작성자/수행자, 실제 확인한 내부 파일 ID·시트·범위·버전, 외부 링크·실제 본 구간, 목적·방법·대안·판단 이유, 기획·스토리보드·산출물 버전, 비용·일정(미정은 null), 미확인·위험·요청 승인 범위를 적는다.
쇼츠는 실제 상품 데이터와 관련 실제 사례의 참고 요소를 연결한다. 관련 사례 3~5개는 목표일 뿐 미시청 자료로 숫자를 채우지 않는다. Hook/장면/자막/CTA 분석은 직접 확인 범위로 한정한다. 게시 카피·최종 검증 보고의 핵심 사실이 미검증이면 출력/게시를 보류한다.

## ID·버전·상태
신규 SUB-ID는 SUB-<R-ID>-NNN이며 W 이전에 만들 수 있다. 이미 존재하는 SUB-W 형식은 변경하지 않는다. 내용 수정은 revision을 올려 `assistant/40-handoff/to-jin/<SUB-ID>-rN.md`로 새 파일을 만든다. 원본 r1을 r2로 덮어쓰지 않는다.
기계 조회 metadata는 `records/submissions/<SUB-ID>-rN.json`이며 submission_id,revision,request_ref,work_id(null 가능),submitted_by_actor_id,artifact_path,artifact_sha256,content_hash,review_snapshot,requested_scopes,submission_status를 가진다. Markdown이 품의 본문 정본이며 metadata는 중복 본문이 아닌 연결 정보다.
'본문만/저장하지 마'는 대화 초안만 제공하고 미저장이다. 정식 작성 요청은 위 준비 검토 후 submitted/결정대기로 저장하며 알림을 실제 보냈다고 하지 않는다. 새 버전은 pending으로 시작한다. 대상 r1의 승인·반려를 새 r2로 덮어씌우지 않는다.

## 결정과 실무
관리자 품의서결정의 granted_scopes에 work_start가 명시돼야 W 생성/연결을 겸한다. 기존 W가 있으면 같은 업무를 갱신하고 새 W를 만들지 않는다. 단순 기획 수락이 게시·지출까지 허용하지 않는다. 새 게시안 반려가 기존 조사 업무를 자동 취소하지 않는다.
COMMON_IO로 R/SUB 연결·metadata·결정대기를 같이 저장하고 ID/버전/경로·확인 커밋을 보고한다. 작성자는 자기 승인이나 관리자 결재를 만들지 않는다.

metadata에는 request_content_revision과 request_content_hash를 저장한다. 결정 전 현재 R와 대조하며 품의 본문의 artifact_sha256도 실제 바이트로 다시 확인한다.
