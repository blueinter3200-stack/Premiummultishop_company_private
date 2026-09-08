---
record_id: P-20260908-002
object_type: problem_source_normalized
schema_version: 1
revision: 1
author_id: ACT-003
author_role: assistant
author_name: 부사수
created_at: 2026-09-08
normalized_at: 2026-09-08
source_path: materials/originals/ACT-003/problems/2026-09-08/image-generation-text-folds-contrast-quality-source.md
source_revision: 1
source_locator: conversation user problem statement ending with /문제출력, followed by /문제저장
information_as_of: 2026-09-08
verification_status: source_assertion_only
authority: saved_input_not_approval
access_scope: internal
related_work_ids: []
---

# 이미지 생성 텍스트·주름·명암 품질 문제 원문 정제본

## 원문에서 명시된 현상

- 이미지 생성 시 텍스트 라인이 `부자역스러워`라고 표현될 정도로 어색하게 보인다는 문제 제기.
- 의류에 주름이 자연스럽게 잡히지 않는다는 문제 제기.
- 명암 대비가 충분하지 않다는 문제 제기.

`부자역스러워`는 원문 그대로 보존한다. 문맥상 텍스트 라인이 부자연스럽다는 취지로 해석했지만, 원문 오탈자 여부를 별도로 확인한 것은 아니다.

## 대화 내 구조화된 문제 요소

- 타이포그래피: 줄 구성·배치가 실제 편집디자인처럼 자연스럽지 않은 문제.
- 의류 표현: 접힘·당김·중력에 따른 주름과 원단 변형이 부족한 문제.
- 조명 표현: 하이라이트와 그림자의 차이가 약해 입체감이 떨어지는 문제.

위 항목은 `/문제출력` 단계에서 원문을 구조화한 것이며 독립 검증된 사실이 아니다.

## 원인 가설 — 미확인

- 텍스트 위치뿐 아니라 행간·자간·정렬·줄바꿈·최대 행 폭 같은 편집 조건이 충분히 지정되지 않았을 가능성.
- 원단의 장력·접힘·압축 주름·자연스러운 드레이핑 등 물리적 조건이 충분히 지정되지 않았을 가능성.
- 조명의 방향·강도·그림자 깊이·키라이트와 음영 차이가 충분히 지정되지 않았을 가능성.
- 모델 포즈 또는 동작이 정적이라 의류가 당겨지고 접히는 힘이 부족했을 가능성.

## 해결 방향 후보 — 제안

- 텍스트의 고정 위치, 최대 행 폭, 줄바꿈 위치, 행간, 자간, 정렬 기준을 구체화한다.
- 의류에는 natural draping, tension wrinkles, compression folds, fabric self-shadow 등 실제 원단 변형 조건을 명시한다.
- 방향성 있는 키라이트와 반대편 음영을 지정해 하이라이트·그림자 대비를 강화한다.
- 영상 프레임 생성 시 동작에 따라 주름이 프레임별로 자연스럽게 변화하도록 조건을 추가한다.

## 검증 상태

이 정제본은 현재 대화의 사용자 문제 제기와 `/문제출력` 단계의 구조화를 바탕으로 작성되었다. 어떤 프롬프트 요소가 주원인인지, 특정 생성 모델·도구에서 동일 문제가 재현되는지는 비교 생성이나 별도 테스트로 확인하지 않았다. 따라서 `source_assertion_only` 상태를 유지한다.
