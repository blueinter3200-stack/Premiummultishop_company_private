#!/usr/bin/env python3
"""Validate source routing and role boundaries; does not execute any company trigger."""
import json
import hashlib
from pathlib import Path
import sys

def validate(root: Path) -> int:
    def load(path): return json.loads((root/path).read_text(encoding="utf-8"))
    actors=load("llm-source/ACTOR_REGISTRY.json")["actors"]
    triggers=load("llm-source/TRIGGER_REGISTRY.json")
    fmap=load("FILE_MAP.json")
    common=(root/"chatgpt/PROJECT_COMMON.md").read_text(encoding="utf-8")
    ids=[a["actor_id"] for a in actors]
    assert len(ids)==len(set(ids))==3 and set(ids)=={"ACT-001","ACT-002","ACT-003"}
    names=[c["name"] for c in triggers["commands"]]
    assert len(names)==len(set(names))==15
    admin_only={"/업무점검","/결과승인","/품의서승인","/업무확정","/아이디어반영","/문제반영"}
    for c in triggers["commands"]:
        assert c["name"] in common
        assert (root/c["workflow"]).is_file(),c["workflow"]
        assert fmap["workflow_routes"][c["name"]]==c["workflow"]
        if c["name"] in admin_only: assert c["roles"]==["admin"]
        if c["mode"]=="local": assert c["name"] in {"/아이디어출력","/문제출력"}
        for a in actors:
            if a["role"] in c["roles"]:
                assert c["name"] in (root/a["project_instructions"]).read_text(encoding="utf-8")
                assert c["name"] in (root/a["role_source"]).read_text(encoding="utf-8")
    for a in actors:
        assert fmap["role_sources"][a["actor_id"]]==a["role_source"]
        assert a["actor_id"] in (root/a["role_source"]).read_text(encoding="utf-8")
    for alias,v in triggers["aliases"].items():
        assert alias not in names and v["command"] in names
    for p in root.rglob("*.json"): json.loads(p.read_text(encoding="utf-8"))
    assert "request_refs" in load("templates/WORK.json")
    assert load("templates/REQUEST.json")["source_created_at"] is None
    assert fmap["approval_actor_id"]=="ACT-001"
    assert "검토만" in common and "저장하지 마" in common
    assert "미저장" in common and "추천과 실행은 별개" in common
    manifest=root/f"docs/releases/{fmap['release_id']}-manifest.json"
    assert manifest.is_file(), "Current release manifest missing"
    if manifest.exists():
        for entry in json.loads(manifest.read_text(encoding="utf-8"))["files"]:
            data=(root/entry["path"]).read_bytes()
            if "canonical_json_sha256" in entry:
                data=json.dumps(json.loads(data),ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
                expected=entry["canonical_json_sha256"]
            else: expected=entry["sha256"]
            assert hashlib.sha256(data).hexdigest()==expected,entry["path"]
    if "request_change_workflow" in fmap:
        from request_changes import validate_repository
        assert (root/fmap["request_change_workflow"]).is_file()
        assert (root/fmap["request_change_index"]).is_file()
        assert load(fmap["request_change_template"])["object_type"]=="request_change"
        assert "request_change_refs" in load("templates/REQUEST.json")
        assert "request_change_refs" in load("templates/WORK.json")
        validate_repository(root)
    print("PASS: RC structure, manifest, JSON, 15 commands, 3 roles, aliases, workflow paths, local discovery and request templates. Live LLM/tool tests not run.")
    return 0
if __name__=="__main__":
    try: sys.exit(validate(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]))
    except (AssertionError,KeyError,OSError,ValueError) as exc:
        print("FAIL:",repr(exc),file=sys.stderr);sys.exit(1)
