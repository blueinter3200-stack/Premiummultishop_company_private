# Pending Idea / Problem Index

- Repository: `https://github.com/jintonic1010/miracle_company_private`
- Branch: `main`
- Purpose: `/업무검토`에서 미반영 아이디어·문제를 전부 읽지 않고 관련 기록만 찾기 위한 경량 인덱스

이 파일에는 **아직 공식 반영되지 않은 아이디어와 문제만** 짧게 색인합니다.

## 읽기 규칙

`/업무검토`는 이 파일을 항상 확인합니다.

1. 현재 업무와 관련된 제목·요약·키워드·경로만 찾습니다.
2. 관련된 기록 파일만 `records/ideas/**` 또는 `records/problems/**`에서 읽습니다.
3. 기록이 연결한 `materials/normalized/**`도 판단에 필요할 때만 읽습니다.
4. 관계없는 아이디어·문제 원문 전체를 훑지 않습니다.
5. `materials/originals/**`는 normalized가 불완전하거나 사용자가 원본 확인을 요청한 경우에만 읽습니다.

## 유지 규칙

- `/아이디어저장` 성공 시 Ideas에 1행 추가
- `/문제저장` 성공 시 Problems에 1행 추가
- 관리자 `/아이디어반영` 성공 시 해당 항목 제거
- 관리자 `/문제반영` 성공 시 해당 항목 제거
- 파일이 실제로 저장/반영되지 않았으면 인덱스만 먼저 바꾸지 않음

권장 항목 형식:

```text
- 제목 | author_role | YYYY-MM-DD | keywords: a, b, c | path: `records/...`
  - summary: 한두 문장
```

## Ideas

- PMS Sourcing OS — Evidence-to-Revenue Buying Desk | admin | 2026-08-20 | keywords: Premium MultiShop, PMS Sourcing OS, sourcing, buying, CM1, CM2, Cafe24, READY, RARE, CARE | path: `records/ideas/admin/2026-08-20-pms-sourcing-os.md`
  - summary: 상품 URL을 출발점으로 동일 SKU·공급처·증거·CM1/CM2·대표 승인·AI 상세페이지·Cafe24 임시등록·CARE 학습을 연결하는 Premium MultiShop 전용 바잉 OS 아이디어. 자동결제·자동발주·자동공개 등 고위험 실행은 금지하고 승인 중심으로 운영한다.

- 업무 설명 시 약어·전문용어 쉬운 풀이 원칙 | representative | 2026-08-31 | keywords: 업무설명, 전문용어, 영문약어, 이니셜, 쉬운풀이 | path: `records/ideas/representative/2026-08-31-explain-acronyms-and-technical-terms.md`
  - summary: 모든 업무 내용을 안내할 때 영문 약어·이니셜·전문용어를 단독으로 쓰지 않고 한국어 뜻과 쉬운 설명을 함께 제공해 대표님의 이해와 의사결정을 돕는 아이디어.

## Problems

현재 미반영 문제 없음.
