---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/remote/env_set.py"
source_filename: "env_set.py"
source_type: "text"
source_size_bytes: 1011
source_modified_at: "2026-08-12T14:19:57+09:00"
source_sha256: "698cbc1be93140690fff17bf242dcff30919d1340a75b0fce97742b52d070ff4"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env python3
"""VPS의 .env 파일에 키를 안전하게 설정. 값은 stdin으로만 받는다(argv/ps 노출 방지).

사용: printf '%s' "$VALUE" | python3 env_set.py <envfile> <KEY>
"""
import os
import sys

path, key = sys.argv[1], sys.argv[2]
val = sys.stdin.read().strip()
if not val:
    print(f"{key}: 값이 비어 있어 건너뜀")
    sys.exit(0)

lines = []
if os.path.exists(path):
    with open(path) as f:
        lines = f.read().splitlines()

replaced = False
for i, line in enumerate(lines):
    if line.split("=", 1)[0].strip() == key:
        lines[i] = f"{key}={val}"
        replaced = True
        break
if not replaced:
    lines.append(f"{key}={val}")

with open(path, "w") as f:
    f.write("\n".join(lines) + "\n")
os.chmod(path, 0o600)
try:
    os.chown(path, 10000, 10000)  # 호스트 root로 실행됨 — Hermes(uid 10000)가 못 읽으면 설정 전체가 무효
except (PermissionError, OSError):
    pass
print(f"{key} {'갱신' if replaced else '추가'}됨")
