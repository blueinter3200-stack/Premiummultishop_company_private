#!/usr/bin/env python3
"""Compose a new ACT-001 request, reviewed decision and optional assignment locally.
No remote writes. The original checkout is never modified; one atomic bundle is returned.
A trusted caller still supplies real intent, reviewed scope and source attribution.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import tempfile


def plan_direct(root: Path, event: dict, planner) -> dict:
    import decision_flow as f
    f.need(event.get('actor_id') == f.ADMIN, 'Only ACT-001 can create-and-approve a direct instruction')
    f.need(event.get('command') == '/업무결정' and event.get('outcome') == '승인', 'Direct instruction requires explicit approval')
    f.need(event.get('intent') == 'direct_work_instruction', 'A discussion/example is not a direct instruction')
    f.need(not any(event.get(k) for k in ('quoted', 'read_only', 'save_prohibited')), 'Direct instruction cannot bypass no-write')
    req = copy.deepcopy(event.get('request', {}))
    for key in ('requester_actor_id', 'record_owner_actor_id', 'recorded_by_actor_id'):
        f.need(req.get(key) == f.ADMIN, 'A new administrator request must preserve ACT-001 ownership')
    source = event.get('source', {})
    f.need(source.get('text') and source.get('locator'), 'Actual direct instruction source required')
    f.need(req.get('original_text') == source['text'] and req.get('source_type') == 'direct_conversation', 'No invented request source')
    f.need(req.get('source_locator') == source['locator'], 'Request and decision source must agree')
    f.need(req.get('primary_scope') == 'work_adoption', 'New direct requests use work_adoption')
    f.need(req.get('revision') == 1 and req.get('content_revision') == 1, 'Direct operation creates a new request only')
    f.need(not req.get('related_work_ids') and not req.get('related_decision_ids'), 'Do not fabricate existing links')
    f.need(f.valid_id(req.get('request_id'), 'R'), 'Invalid request ID')
    key = event.get('source_event_id')
    f.need(key, 'Stable operation event ID required')
    fp = f.digest({k: v for k, v in event.items() if k not in {'base_commit', 'review'}})
    receipt_path = f"records/direct-operations/{f.digest(key)}.json"
    old_receipt = root / receipt_path
    if old_receipt.is_file():
        prior = f.load(root, receipt_path)
        f.need(prior.get('event_fingerprint') == fp, 'Direct event key reused with changed payload')
        for path in prior['required_record_paths']:
            f.need(f.safe(root, path).is_file(), 'Partial direct operation persistence; repair same IDs')
        f.need(f.load(root, prior['request_ref'])['original_text'] == req['original_text'], 'Original request changed')
        import work_status
        f.need((root / work_status.MAP_PATH).read_text(encoding='utf-8') == work_status.render(root)[work_status.MAP_PATH], 'Partial or stale status map')
        return dict(status='already_recorded', files={}, expected_blobs={}, base_commit=event['base_commit'], operation_receipt=receipt_path)
    f.need(not any(r.get('request_id') == req['request_id'] for _, r in f.records(root, 'records/requests', 'R-*.json')),
           'Existing request must be reused by the normal decision workflow, not recaptured')
    f.check_review(event.get('review', {}), req, event['base_commit'])
    f.need(f.proposal(req).get('title') and f.proposal(req).get('completion_criteria'), 'Clear work title and completion criteria required')
    if event.get('execution_mode') != 'self_direct':
        f.need(set(event.get('granted_scopes', [])) <= {'work_adoption', 'planning'}, 'Assignment is not approval of an unwritten execution plan')
    req_path = f"records/requests/{f.ADMIN}/{req['request_id']}.json"
    combined = {}
    with tempfile.TemporaryDirectory(prefix='miracle-direct-') as name:
        stage = Path(name)
        for folder in ('llm-source', 'records', 'approvals', 'work', 'assistant', 'working'):
            if (root / folder).is_dir():
                shutil.copytree(root / folder, stage / folder, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        first = planner(stage, dict(operation='submit_request', command='/업무요청', actor_id=f.ADMIN,
                                   write_requested=True, base_commit=event['base_commit'], request=req, review=event['review']))
        for path, text in first['files'].items():
            target = f.safe(stage, path); target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text, encoding='utf-8')
        combined.update(first['files'])
        second_event = copy.deepcopy(event)
        second_event.update(operation='decide', target_ref=req_path, target_revision=1,
                            target_hash=f.digest(f.proposal(req)), scope_key='work_adoption', previous_decision_id=None)
        for k in ('request', 'intent'):
            second_event.pop(k, None)
        second = planner(stage, second_event)
        combined.update(second['files'])
    required = [p for p in combined if p.startswith(('records/requests/', 'approvals/', 'work/items/', 'work/assignments/', 'records/notifications/')) and p.endswith('.json')]
    combined[receipt_path] = f.dump(dict(schema_version=1, source_event_id=key, event_fingerprint=fp,
                                        request_ref=req_path, decision_id=event['decision_id'], work_id=event['work_id'],
                                        required_record_paths=sorted(required), authority='operation_link_not_execution_receipt'))
    expected = {p: f.blob(f.safe(root, p).read_bytes()) if f.safe(root, p).is_file() else None for p in combined}
    return dict(status='planned', base_commit=event['base_commit'], files=combined, expected_blobs=expected,
                follow_up='Commit the complete request/decision/work/assignment/notification/map bundle, then verify. No remote writes performed.')
