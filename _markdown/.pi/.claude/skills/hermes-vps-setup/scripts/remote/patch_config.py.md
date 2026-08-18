---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/remote/patch_config.py"
source_filename: "patch_config.py"
source_type: "text"
source_size_bytes: 1407
source_modified_at: "2026-08-12T14:19:57+09:00"
source_sha256: "ccebe482e292848d8495d3525914713601fbb7f120599f6ebeae4daf706eae87"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env python3
"""Hermes config.yaml 점(dot) 경로 패치. 컨테이너 안(uid 10000)에서 실행.

stdin: {"set": {"stt": {...}, "mcp_servers.composio": {...}}, "setdefault": {...}}
  - set:        항상 덮어씀. 점 경로는 중간 딕셔너리를 만들며 내려감.
  - setdefault: 마지막 키가 이미 있으면 건드리지 않음.

사용: docker exec -i -u 10000 <컨테이너> python3 /opt/data/tmp/patch_config.py < ops.json
주의: yaml 재직렬화라 주석은 사라질 수 있음 — 호출 측에서 백업 필수.
"""
import json
import sys

import yaml

CFG = "/opt/data/config.yaml"

ops = json.load(sys.stdin)
with open(CFG) as f:
    cfg = yaml.safe_load(f) or {}


def put(d, dotted, val, only_if_absent=False):
    keys = dotted.split(".")
    cur = d
    for k in keys[:-1]:
        if not isinstance(cur.get(k), dict):
            cur[k] = {}
        cur = cur[k]
    if only_if_absent and keys[-1] in cur:
        return False
    cur[keys[-1]] = val
    return True


changed = []
for k, v in (ops.get("set") or {}).items():
    if put(cfg, k, v):
        changed.append(k)
for k, v in (ops.get("setdefault") or {}).items():
    if put(cfg, k, v, only_if_absent=True):
        changed.append(k)

with open(CFG, "w") as f:
    yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)
print("패치됨: " + ", ".join(changed) if changed else "변경 없음")
