#!/usr/bin/env python3
"""Plan/validate RC records. No network, writes, semantic classifier or authentication.

A caller supplies an evidence-backed materiality assessment and a fresh main snapshot.
The plan must be committed atomically using COMMON_IO, then verified against read-back.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
from typing import Any

ADMIN = "ACT-001"
READ_ONLY = {"/아이디어출력", "/문제출력", "/업무검토", "/업무점검", "/반영미리보기", "/대표업무점검"}
TYPES = {"modify", "add_scope", "remove_scope", "replace", "cancel", "condition_change", "other"}
MUTABLE = {"purpose", "scope", "conditions", "deliverable_requirements", "target_systems",
           "target_actor_ids", "priority", "completion_criteria", "approval_conditions",
           "standing_instructions", "current_requirements"}
IMPACT = {"affected_work_ids": "W", "affected_decision_ids": "D",
          "affected_idea_ids": "I", "affected_problem_ids": "P"}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def valid_id(value: Any, prefix: str) -> bool:
    return isinstance(value, str) and re.fullmatch(re.escape(prefix) + r"-\d{8}-\d{3,}", value) is not None


def rc_path(rid: str, rcid: str) -> str:
    require(valid_id(rid, "R") and valid_id(rcid, "RC"), "Invalid R/RC ID")
    return f"records/request-changes/{ADMIN}/{rid}/{rcid}.json"


def safe_path(root: Path, path: str) -> Path:
    relative = Path(path)
    require(not relative.is_absolute() and ".." not in relative.parts, "Unsafe path")
    resolved = (root / relative).resolve()
    require(resolved.is_relative_to(root.resolve()), "Path escapes repository")
    return resolved


def load(root: Path, path: str) -> Any:
    return json.loads(safe_path(root, path).read_text(encoding="utf-8"))


def build_change(before: dict, event: dict, existing: list[dict] | None = None) -> dict:
    """Pure RC constructor; returns no changes for read-only, other actors or nonmaterial edits."""
    existing = existing or []
    command = str(event.get("command", "")).split(" ", 1)[0]
    if (event.get("read_only") or event.get("save_prohibited") or event.get("is_quoted")
            or command in READ_ONLY or not event.get("write_requested", False)):
        return {"status": "no_write"}
    if before.get("requester_actor_id") != ADMIN:
        return {"status": "rc_not_required_for_actor"}
    require(event.get("current_actor_id") == ADMIN, "Only ACT-001 may change ACT-001 requests")
    require(type(event.get("material_change")) is bool, "Explicit materiality assessment required")
    if not event["material_change"]:
        return {"status": "nonmaterial_no_rc"}
    require(bool(event.get("materiality_basis")), "Materiality basis required; do not infer from a keyword alone")
    rid, rcid = event.get("request_id"), event.get("request_change_id")
    path = rc_path(rid, rcid)
    require(rid == before.get("request_id"), "Wrong request")
    require(event.get("change_type") in TYPES, "Invalid change type")
    for key in ("source_event_id", "source_type", "source_locator", "source_excerpt", "change_summary", "captured_at"):
        require(isinstance(event.get(key), str) and bool(event[key].strip()), f"Missing {key}")
    require("changed_at" in event, "changed_at must be supplied or explicitly null")
    fingerprint = digest(event)
    for prior in existing:
        if prior.get("request_id") == rid and prior.get("source_event_id") == event["source_event_id"]:
            require(prior.get("event_fingerprint") == fingerprint, "Reused event key with changed payload")
            return {"status": "already_recorded", "request_change_id": prior["request_change_id"]}
        require(prior.get("request_change_id") != rcid, "RC ID collision")
    require(type(before.get("revision")) is int and before["revision"] > 0, "Invalid request revision")
    require(before["revision"] == event.get("before_revision"), "Stale request revision")
    require(digest(before) == event.get("before_sha256"), "Stale request content")
    changes = event.get("changes")
    require(isinstance(changes, dict) and bool(changes), "Changes object required")
    require(set(changes) <= MUTABLE, "Cannot patch original text, identity, state, supersedes or approval metadata")
    unknowns = list(event.get("unknowns", []))
    reason_source = event.get("reason_source")
    reason = event.get("change_reason")
    require(reason_source in {"explicit_user_statement", "source_evidence", "unknown"}, "Invalid reason source")
    if reason_source == "unknown":
        require(reason is None, "An unknown reason must be null")
        if "변경 이유 미확인" not in unknowns:
            unknowns.append("변경 이유 미확인")
    else:
        require(isinstance(reason, str) and bool(reason.strip()), "Known reason must be nonempty")
        if reason_source == "explicit_user_statement":
            excerpt = event.get("reason_excerpt")
            require(isinstance(excerpt, str) and bool(excerpt.strip()) and excerpt in event["source_excerpt"],
                    "Explicit reason needs an exact source excerpt")
        else:
            refs = event.get("reason_evidence_refs")
            require(isinstance(refs, list) and bool(refs), "Evidence-backed reason requires references")
            require(all(isinstance(r, dict) and (r.get("path") or r.get("url")) and r.get("locator") for r in refs),
                    "Reason evidence needs a path/URL and locator")
    if event["changed_at"] is None and "변경 발언 시각 미확인" not in unknowns:
        unknowns.append("변경 발언 시각 미확인")
    after = copy.deepcopy(before)
    fields = []
    for key, value in changes.items():
        # Missing and explicit null are not the same state.
        if key not in before or canonical(before[key]) != canonical(value):
            fields.append({"field": key, "before_present": key in before,
                           "before": copy.deepcopy(before.get(key)), "after_present": True,
                           "after": copy.deepcopy(value)})
            after[key] = copy.deepcopy(value)
    if not fields:
        return {"status": "unchanged_no_rc"}
    refs = before.get("request_change_refs", [])
    require(isinstance(refs, list) and len(refs) == len(set(refs)), "Invalid existing RC references")
    after["revision"] += 1
    after["request_change_refs"] = refs + [path]
    rc = {
        "schema_version": 1, "object_type": "request_change", "request_change_id": rcid,
        "request_id": rid, "requester_actor_id": ADMIN, "changed_by_actor_id": ADMIN,
        "changed_at": event["changed_at"], "captured_at": event["captured_at"],
        "change_type": event["change_type"], "change_summary": event["change_summary"],
        "materiality_basis": event["materiality_basis"], "changed_fields": fields,
        "change_reason": reason, "reason_source": reason_source,
        "reason_excerpt": event.get("reason_excerpt"), "reason_evidence_refs": event.get("reason_evidence_refs", []),
        "source_type": event["source_type"], "source_locator": event["source_locator"],
        "source_excerpt": event["source_excerpt"], "source_event_id": event["source_event_id"],
        "event_fingerprint": fingerprint, "source_event": copy.deepcopy(event),
        "request_revision_before": before["revision"], "request_revision_after": after["revision"],
        "request_snapshot_before": copy.deepcopy(before), "request_snapshot_after": after,
        "before_sha256": digest(before), "after_sha256": digest(after),
        "previous_request_change_ref": refs[-1] if refs else None,
        "affected_requirement_refs": event.get("affected_requirement_refs", []), "unknowns": unknowns,
        "authority": "change_history_not_approval_or_completion", "impact_execution_status": "not_verified",
    }
    for key, prefix in IMPACT.items():
        values = event.get(key, [])
        require(isinstance(values, list) and len(values) == len(set(values))
                and all(valid_id(v, prefix) for v in values), f"Invalid {key}")
        rc[key] = values
    rc["approval_recheck_required"] = bool(rc["affected_decision_ids"])
    validate_change(rc)
    return {"status": "planned", "request": after, "request_change": rc, "rc_path": path}


def validate_change(rc: dict) -> None:
    require(rc.get("schema_version") == 1 and rc.get("object_type") == "request_change", "Invalid RC schema")
    path = rc_path(rc.get("request_id"), rc.get("request_change_id"))
    require(rc.get("requester_actor_id") == rc.get("changed_by_actor_id") == ADMIN, "RC actor boundary")
    before, after = rc["request_snapshot_before"], rc["request_snapshot_after"]
    require(before.get("requester_actor_id") == ADMIN and before.get("request_id") == rc["request_id"], "Snapshot identity")
    require(rc["request_revision_before"] == before["revision"] and rc["request_revision_after"] == before["revision"] + 1, "Revision edge")
    require(digest(before) == rc["before_sha256"] and digest(after) == rc["after_sha256"], "Snapshot hash mismatch")
    rebuilt = copy.deepcopy(before)
    seen = set()
    for f in rc["changed_fields"]:
        key = f["field"]
        require(key in MUTABLE and key not in seen, "Forbidden or duplicate changed field")
        seen.add(key)
        require(f["before_present"] == (key in before) and f["before"] == before.get(key), "Before value mismatch")
        require(f["after_present"] is True and (not f["before_present"] or canonical(f["before"]) != canonical(f["after"])), "Empty delta")
        rebuilt[key] = copy.deepcopy(f["after"])
    require(bool(seen), "RC cannot be an empty change")
    rebuilt["revision"] += 1
    rebuilt["request_change_refs"] = before.get("request_change_refs", []) + [path]
    require(canonical(rebuilt) == canonical(after), "Untracked change in after snapshot")
    refs = before.get("request_change_refs", [])
    require(rc.get("previous_request_change_ref") == (refs[-1] if refs else None), "Wrong RC predecessor")
    event = rc["source_event"]
    require(digest(event) == rc["event_fingerprint"], "Event fingerprint mismatch")
    require(event.get("current_actor_id") == ADMIN and event.get("material_change") is True
            and event.get("write_requested") is True, "Missing explicit administrator change")
    require(not any(event.get(k) for k in ("read_only", "save_prohibited", "is_quoted"))
            and str(event.get("command", "")).split(" ", 1)[0] not in READ_ONLY, "Read-only event")
    for key in ("change_type", "change_summary", "change_reason", "reason_source", "source_type", "source_locator", "source_excerpt", "source_event_id", "changed_at", "captured_at"):
        require(rc.get(key) == event.get(key), f"Source event mismatch: {key}")
    require(rc["reason_source"] in {"explicit_user_statement", "source_evidence", "unknown"}, "Invalid reason source")
    if rc["reason_source"] == "unknown":
        require(rc["change_reason"] is None and "변경 이유 미확인" in rc["unknowns"], "Invented unknown reason")
    elif rc["reason_source"] == "explicit_user_statement":
        require(bool(rc.get("reason_excerpt")) and rc["reason_excerpt"] in rc["source_excerpt"], "Missing reason excerpt")
    else:
        require(bool(rc.get("reason_evidence_refs")), "Missing reason evidence")
    require(event.get("before_revision") == before["revision"] and event.get("before_sha256") == digest(before), "Event base mismatch")
    expected_changes = {k:v for k,v in event.get("changes", {}).items() if k not in before or canonical(before[k]) != canonical(v)}
    require(expected_changes == {f["field"]: f["after"] for f in rc["changed_fields"]}, "Delta does not match source event")
    for key, prefix in IMPACT.items():
        require(rc.get(key) == event.get(key, []) and all(valid_id(v,prefix) for v in rc[key]), "Impact mismatch")
    require(rc.get("approval_recheck_required") == bool(rc["affected_decision_ids"]), "Decision recheck mismatch")
    require(rc.get("impact_execution_status") == "not_verified", "RC is not implementation verification")
    require(rc.get("authority") == "change_history_not_approval_or_completion", "RC is not approval")


def plan(root: Path, event: dict) -> dict:
    require(re.fullmatch(r"[0-9a-f]{40}", str(event.get("base_commit", ""))) is not None, "Fresh base_commit required")
    rid = event.get("request_id")
    require(valid_id(rid, "R"), "Invalid request ID")
    owner = event.get("requester_actor_id", ADMIN)
    require(re.fullmatch(r"ACT-\d{3,}", str(owner)) is not None, "Invalid requester")
    request_path = f"records/requests/{owner}/{rid}.json"
    before = load(root, request_path)
    if owner == ADMIN and event.get("current_actor_id") == ADMIN:
        actors = load(root, "llm-source/ACTOR_REGISTRY.json")["actors"]
        require(any(a["actor_id"] == ADMIN and a["role"] == "admin" and a["status"] == "active" for a in actors), "Inactive admin")
    existing = [json.loads(p.read_text(encoding="utf-8")) for p in (root/"records/request-changes").rglob("RC-*.json")]
    result = build_change(before, event, existing)
    if result["status"] == "already_recorded":
        validate_repository(root)  # Partial writes are not an idempotent success.
    if result["status"] != "planned":
        return {**result, "files": {}, "base_commit": event["base_commit"]}
    change, path = result["request_change"], result["rc_path"]
    for old_ref in before.get("request_change_refs", []):
        validate_change(load(root, old_ref))
    files = {path: text(change), request_path: text(result["request"])}
    index = "records/REQUEST_CHANGE_INDEX.md"
    index_text = safe_path(root, index).read_text(encoding="utf-8") if safe_path(root,index).exists() else "# Request Change Index\n\n개별 RC JSON이 정본이다.\n"
    require(change["request_change_id"] not in index_text, "Index collision requires recovery, not duplicate append")
    files[index] = index_text.rstrip() + f"\n\n- {change['request_change_id']} | {rid} | ACT-001 | revision {before['revision']} → {result['request']['revision']} | `{path}`\n"
    rindex = "records/REQUEST_INDEX.md"
    rtext = safe_path(root, rindex).read_text(encoding="utf-8")
    if index not in rtext:
        files[rindex] = rtext.rstrip() + f"\n\n관리자 요청 변경이력: `{index}` (개별 RC JSON 참조).\n"
    for wid in change["affected_work_ids"]:
        wp = f"work/items/{wid}.json"
        work = load(root, wp)
        require(work.get("id") == wid, "Wrong affected work")
        for field, value in (("request_refs", request_path), ("request_change_refs", path)):
            refs = work.setdefault(field, [])
            if value not in refs:
                refs.append(value)
        require(type(work.get("revision")) is int, "Invalid work revision")
        work["revision"] += 1
        files[wp] = text(work)  # Link-only update. Never approves/completes work.
    for did in change["affected_decision_ids"]:
        require(load(root, f"approvals/{did}.json").get("decision_id") == did, "Unknown affected decision")
    expected = {p: blob(safe_path(root,p).read_bytes()) if safe_path(root,p).is_file() else None for p in files}
    return {"status": "planned", "base_commit": event["base_commit"], "files": files,
            "expected_blobs": expected, "request_change_id": change["request_change_id"],
            "note": "Commit ALL files in one non-force Git update; re-read before claiming success."}


def verify_readback(root: Path, bundle: dict) -> list[str]:
    failures = []
    for path, expected in bundle.get("files", {}).items():
        p = safe_path(root, path)
        if not p.is_file() or p.read_bytes() != expected.encode():
            failures.append(path)
    return failures


def validate_repository(root: Path) -> int:
    seen = set()
    for path in (root/"records/request-changes").rglob("RC-*.json"):
        rc = json.loads(path.read_text(encoding="utf-8"))
        validate_change(rc)
        require(path.relative_to(root).as_posix() == rc_path(rc["request_id"],rc["request_change_id"]), "RC path mismatch")
        require(rc["request_change_id"] not in seen, "Duplicate RC ID")
        seen.add(rc["request_change_id"])
        current = load(root, f"records/requests/ACT-001/{rc['request_id']}.json")
        require(path.relative_to(root).as_posix() in current.get("request_change_refs",[]), "Missing request back-reference")
        require(current["revision"] >= rc["request_revision_after"], "Request behind RC")
        require(current["original_text"] == rc["request_snapshot_before"]["original_text"], "Original text changed")
        if current["revision"] == rc["request_revision_after"]:
            require(digest(current) == rc["after_sha256"], "Current revision differs from RC snapshot")
        for previous_ref in rc["request_snapshot_before"].get("request_change_refs", []):
            previous = load(root, previous_ref)
            require(previous["request_id"] == rc["request_id"] and previous["request_revision_after"] <= rc["request_revision_before"], "Invalid predecessor chain")
        require(rc["request_change_id"] in (root/"records/REQUEST_CHANGE_INDEX.md").read_text(), "Missing RC index entry")
    return len(seen)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["plan", "validate", "verify"])
    parser.add_argument("root", type=Path)
    parser.add_argument("input", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            print(text({"validated_rc_count": validate_repository(args.root)}))
        else:
            require(args.input is not None, "Input JSON required")
            data = json.loads(args.input.read_text(encoding="utf-8"))
            if args.command == "plan":
                print(text(plan(args.root,data)))
            else:
                failures = verify_readback(args.root,data)
                print(text({"verified": not failures, "failed_paths": failures}))
                raise SystemExit(1 if failures else 0)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
