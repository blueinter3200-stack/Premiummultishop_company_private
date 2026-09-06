# Records — 아이디어·문제 기록

## ID

- actor: `ACT-NNN`
- idea: `I-YYYYMMDD-NNN`
- problem: `P-YYYYMMDD-NNN`

새 기록은 `record_id`, `author_id`, `author_role`, `author_name`을 함께 가진다.

## 새 기록 경로

```text
records/ideas/<actor_id>/YYYY-MM-DD-<short-slug>.md
records/problems/<actor_id>/YYYY-MM-DD-<short-slug>.md
```

관련 첨부:
```text
materials/originals/<actor_id>/ideas/YYYY-MM-DD/<file>
materials/normalized/<actor_id>/ideas/YYYY-MM-DD/<file>.md
materials/originals/<actor_id>/problems/YYYY-MM-DD/<file>
materials/normalized/<actor_id>/problems/YYYY-MM-DD/<file>.md
```

## 기존 기록

2026-09-06 이전의 `records/ideas/admin/`, `records/ideas/representative/` 등 role 기반 경로는 참조 안정성을 위해 이동하지 않는다. 소유자는 `records/PENDING_INDEX.md`, `materials/normalized/records/*.json`, `llm-source/ACTOR_REGISTRY.json`으로 연결한다.

## 새 사람

새 사람이 들어오면 관리자가 새 ACT-NNN을 발급한다. 역할이 바뀌어도 actor_id는 유지하고, 다른 사람이 자리를 인수하면 새 actor_id를 발급한다. 실제 첫 기록이 생길 때 actor_id 폴더를 생성하면 된다.

아이디어/문제 저장은 공식 회사 정책 반영이나 업무 시작을 의미하지 않는다.
