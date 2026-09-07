#!/usr/bin/env python3
import json,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
tr=json.loads((root/'llm-source/TRIGGER_REGISTRY.json').read_text())
fm=json.loads((root/'FILE_MAP.json').read_text())
reg=json.loads((root/'llm-source/ACTOR_REGISTRY.json').read_text())
names=[c['name'] for c in tr['commands']]
assert len(names)==len(set(names))==17
assert tr.get('aliases')=={} and '/업무진행현황' in names
assert fm['release_id']=='GOV-20260907-02' and fm['status_map']=='working/WORK_STATUS_MAP.json'
assert {a['actor_id'] for a in reg['actors']} >= {'ACT-001','ACT-002','ACT-003'}
for p in [fm['status_workflow'],fm['direct_admin_workflow'],'working/WORK_STATUS_MAP.json']:
    assert (root/p).is_file(),p
print('PASS: GOV-20260907-02 structure, 17 commands, aliases=0')
