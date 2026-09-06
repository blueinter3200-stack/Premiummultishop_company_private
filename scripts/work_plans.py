#!/usr/bin/env python3
"""Work adoption, assignment and execution-plan gates. Pure local planning only.
The caller must authenticate separately, fetch a fresh snapshot, and persist/read back
one complete bundle. A source string or a boolean is not proof of identity or work.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re

ADMIN = 'ACT-001'
ASSISTANT = 'ACT-003'


def core():
    # Lazy import avoids a module-import cycle with the decision planner.
    import decision_flow
    return decision_flow


def active_actor(root, actor):
    c = core()
    found = next((a for a in c.load(root, 'llm-source/ACTOR_REGISTRY.json')['actors']
                  if a['actor_id'] == actor and a['status'] == 'active'), None)
    c.need(found is not None, 'Inactive/unknown actor')
    return found


def assignment_tip(assignments, work_id):
    c = core()
    items = [a for a in assignments if a['work_id'] == work_id]
    if not items:
        return None
    ids = {a['assignment_id']: a for a in items}
    c.need(len(ids) == len(items), 'Duplicate assignment ID')
    parents = [a['previous_assignment_id'] for a in items if a.get('previous_assignment_id')]
    c.need(len(parents) == len(set(parents)) and set(parents) <= set(ids), 'Assignment conflict')
    tips = [a for a in items if a['assignment_id'] not in parents]
    c.need(len(tips) == 1, 'Ambiguous assignment chain')
    seen = set(); cur = tips[0]
    while cur:
        c.need(cur['assignment_id'] not in seen, 'Assignment cycle')
        seen.add(cur['assignment_id']); cur = ids.get(cur.get('previous_assignment_id'))
    c.need(len(seen) == len(items), 'Disconnected assignment history')
    return tips[0]


def owns_request(actor, request):
    return actor == ADMIN or actor in {request.get('record_owner_actor_id'),
                                      request.get('recorded_by_actor_id'), request.get('requester_actor_id')}


def check_request_access(root, actor, request, assignment_ref=None):
    c = core()
    if owns_request(actor, request):
        return
    c.need(assignment_ref, 'Do not read or submit another actor request without an assignment')
    assignment = c.load(root, assignment_ref)
    tip = assignment_tip([a for _, a in c.records(root, 'work/assignments', 'ASG-*.json')], assignment['work_id'])
    c.need(tip and tip['assignment_id'] == assignment['assignment_id'] and tip.get('assigned_to_actor_id') == actor,
           'Only the current assignee may use this assignment')
    c.need(assignment['request_context']['request_id'] == request['request_id'], 'Wrong assignment request')
    # The LLM-facing assignment supplies only the approved brief and a binding hash;
    # it does not grant unrestricted browsing of representative requests.


def reported_request(root, actor, request):
    c = core(); obj = copy.deepcopy(request)
    c.need(actor == ASSISTANT, 'Oral representative request capture is an assistant operation')
    c.need(obj.get('requester_actor_id') == 'ACT-002' and obj.get('recorded_by_actor_id') == actor,
           'Preserve reported requester and actual recorder separately')
    c.need(obj.get('source_type') == 'reported_oral_request'
           and obj.get('source_verification') == 'reported_not_independently_verified',
           'Oral report is not a verified direct statement')
    c.need(obj.get('original_text') and obj.get('source_locator') and obj.get('captured_at'), 'Oral source required')
    c.need(c.valid_id(obj.get('request_id'), 'R'), 'Invalid R-ID')
    c.need(not obj.get('related_work_ids') and not obj.get('related_decision_ids'), 'Capture cannot invent work/approval')
    c.need(not any(x.get('request_id') == obj['request_id'] for _, x in c.records(root, 'records/requests', 'R-*.json')),
           'R-ID already exists: use the known original, not a duplicate proxy request')
    obj.update(record_owner_actor_id=actor, submitted_by_actor_id=actor,
               submission_status='captured', request_status='captured',
               primary_scope='work_adoption', schema_version=4)
    path = f"records/requests/{actor}/{obj['request_id']}.json"
    return path, obj


def work_effect(d, request, event, existing):
    c = core(); rp = d['request_ref']
    found = [(p, w) for p, w in existing if rp in w.get('request_refs', [])]
    c.need(len(found) <= 1, 'Duplicate work for the same request')
    granted = set(d['granted_scopes']) if d['decision'] == 'approved' else set()
    adopts = bool(granted & {'work_adoption', 'work_start'})
    executes = d['scope_key'] == 'plan_execution' and 'plan_execution' in granted
    if not found and not adopts:
        return None
    if not found:
        wid = event.get('work_id'); c.need(c.valid_id(wid, 'W'), 'New adopted work needs W-ID')
        c.need(all(w.get('id') != wid for _, w in existing), 'W-ID collision')
        path = f'work/items/{wid}.json'
        w = dict(schema_version=4, id=wid, revision=1, title=request.get('title') or c.proposal(request).get('title'),
                 requested_by_actor_id=request['requester_actor_id'], assigned_to_actor_id=None,
                 created_at=d['decided_at'], work_status='queued', evidence_status='pending',
                 approval_status='pending', persistence_status='pending_commit', execution_status='not_requested',
                 priority=event.get('priority'), due_at=event.get('due_at'), source_refs=[], request_refs=[rp],
                 request_change_refs=[], directive_refs=[], evidence_refs=[], artifact_refs=[], submission_refs=[],
                 decision_refs=[], related_idea_ids=[], related_problem_ids=[], unknowns=[],
                 completion_criteria=c.proposal(request).get('completion_criteria', []), assignment_refs=[],
                 execution_mode='plan_required', execution_plan_ref=None, execution_decision_ref=None,
                 current_assignment_ref=None, plan_status='not_submitted', authorized_scopes=[])
    else:
        path, old = found[0]; w = copy.deepcopy(old); w['revision'] += 1
        if adopts and old['work_status'] in {'done', 'cancelled'}:
            c.need(event.get('reopen_work') and event.get('reopen_reason'), 'Reopening completed work must be explicit')
            w['work_status'] = 'queued'
    c.need(w.get('title') and w.get('completion_criteria'), 'Actual work scope/completion criteria required')
    ref = f"approvals/{d['decision_id']}.json"
    if adopts and (not found or d['target_type']=='request'):
        w['adoption_decision_ref'] = ref
        w['confirmation_decision_ref'] = ref  # legacy reader compatibility, not the execution-plan approval
        w['adoption_status'] = 'approved'
        w['execution_mode'] = 'plan_required'
        w['authorized_scopes'] = ['planning']
        w['next_action'] = '담당 지정 및 업무계획안 작성·결의 대기'
        w['approval_status'] = 'approved'
        if event.get('execution_mode') == 'self_direct':
            c.need(event.get('self_execution_authorized') is True
                   and event.get('assigned_to_actor_id', w.get('assigned_to_actor_id')) == ADMIN,
                   'Only explicit administrator self-execution can skip a separate plan')
            w['assigned_to_actor_id'] = ADMIN
            w['execution_mode'] = 'self_direct'; w['authorized_scopes'] = sorted(granted)
            w['next_action'] = '관리자 직접 수행: 명시 승인 범위만 진행'
    if executes:
        c.need(d['target_type'] == 'submission', 'A plan decision must target a specific plan')
        w['execution_plan_ref'] = d['target_ref']; w['execution_decision_ref'] = ref
        w['authorized_scopes'] = sorted(granted | {'planning'})
        w['plan_status'] = 'approved'; w['next_action'] = '담당·배정·최신 계획 버전·실행 범위를 확인 후 수행'
        if w['work_status'] == 'blocked': w['work_status'] = 'queued'
    elif d['scope_key'] == 'plan_execution':
        # A rejected new r2 is not an implicit revocation of an approved r1.
        w['proposed_plan_status'] = d['decision']
        if not w.get('execution_plan_ref'):
            w['plan_status'] = d['decision']; w['next_action'] = '계획안 결의 사유 확인: ' + d['decision']
        if w.get('execution_plan_ref') == d['target_ref']:
            w['plan_status'] = d['decision']; w['work_status'] = 'blocked'
    if d['scope_key'] in {'work_adoption', 'work_start'} and d['decision'] != 'approved':
        w['adoption_status'] = d['decision']
        if w['work_status'] not in {'done', 'cancelled'}: w['work_status'] = 'blocked'
    w['effective_decision_ref'] = ref
    w['updated_at'] = w['information_as_of'] = d['decided_at']
    w['decision_refs'] = list(dict.fromkeys(w.get('decision_refs', []) + [ref]))
    d['work_id'] = w['id']
    return path, w


def current_adoption(root, w, overlay_decision=None):
    c = core()
    ds = [d for _, d in c.records(root, 'approvals', 'D-*.json')]
    if overlay_decision: ds.append(overlay_decision)
    ref = w.get('adoption_decision_ref') or w.get('confirmation_decision_ref')
    c.need(ref, 'Work has no administrator adoption decision')
    d = overlay_decision if overlay_decision and ref == f"approvals/{overlay_decision['decision_id']}.json" else c.load(root, ref)
    tip = c.latest(ds, c.chain_key(d))
    c.need(tip and tip['decision'] == 'approved' and set(tip['granted_scopes']) & {'work_adoption', 'work_start'},
           'Work adoption is not currently authorized')
    req = c.load(root, tip['request_ref']); ctx = tip['authorization_target']
    c.need(ctx['content_revision'] == c.revision(req) and ctx['content_hash'] == c.digest(c.proposal(req)),
           'Request requirements changed; redecision required')
    return tip


def assign(root, w, event, adoption=None):
    """Return immutable assignment/notification overlays; caller owns the W revision."""
    c = core(); c.need(event.get('actor_id') == ADMIN, 'Only administrator may assign work')
    spec = event.get('assignment')
    if spec is None:
        return {}
    source = spec.get('source') or event.get('source', {})
    c.need(source.get('text') and source.get('locator') and spec.get('source_event_id'), 'Assignment source required')
    recipient = spec.get('assigned_to_actor_id')
    if recipient is not None:
        a = active_actor(root, recipient)
        c.need(a['role'] in {'admin', 'assistant'}, 'This role is not an authorized work assignee')
    known = [a for _, a in c.records(root, 'work/assignments', 'ASG-*.json')]
    fp = c.digest(spec)
    for a in known:
        if a.get('source_event_id') == spec['source_event_id']:
            c.need(a.get('event_fingerprint') == fp, 'Reused assignment event with changed payload')
            c.need(w.get('current_assignment_ref') == f"work/assignments/{a['assignment_id']}.json", 'Partial assignment persistence')
            for aid in a.get('notification_recipients', []):
                c.need(c.safe(root, f"records/notifications/{aid}/N-{a['assignment_id']}-{aid}.json").exists(), 'Partial assignment notification')
            return {}
    prior = assignment_tip(known, w['id'])
    c.need((prior or {}).get('assignment_id') == spec.get('previous_assignment_id'), 'Stale assignment predecessor')
    current_adoption(root, w, adoption)
    aid = spec.get('assignment_id'); c.need(c.valid_id(aid, 'ASG'), 'Invalid assignment ID')
    c.need(all(x['assignment_id'] != aid for x in known), 'Assignment ID collision')
    instruction = spec.get('instruction_text')
    c.need(instruction and instruction in source['text'], 'Use the actual administrator instruction, not an invented order')
    brief = spec.get('approved_brief')
    c.need(isinstance(brief, dict) and brief.get('title') and brief.get('scope'), 'Assignee-safe approved brief required')
    c.need(not any(k in brief for k in ('private_notes', 'raw_request', 'credentials')), 'Do not expose private raw material')
    assigned_at = spec.get('assigned_at'); c.need(assigned_at, 'Assignment recording time required')
    old_actor = (prior or {}).get('assigned_to_actor_id', w.get('assigned_to_actor_id'))
    recipients = {recipient, old_actor} - {None, ADMIN}
    ctx = current_adoption(root, w, adoption)['authorization_target']
    assignment = dict(schema_version=1, object_type='work_assignment', assignment_id=aid, work_id=w['id'],
        assigned_by_actor_id=ADMIN, assigned_to_actor_id=recipient, previous_assignee_actor_id=old_actor,
        previous_assignment_id=(prior or {}).get('assignment_id'), assigned_at=assigned_at,
        instruction_text=instruction, approved_brief=brief, request_context=ctx,
        authorization_decision_ref=w.get('adoption_decision_ref') or w['confirmation_decision_ref'],
        source=source, source_event_id=spec['source_event_id'], event_fingerprint=fp,
        notification_recipients=sorted(recipients), authority='assignment_not_plan_execution_approval')
    ap = f'work/assignments/{aid}.json'
    w['assigned_to_actor_id'] = recipient; w['current_assignment_ref'] = ap
    w['assignment_refs'] = list(dict.fromkeys(w.get('assignment_refs', []) + [ap]))
    # Changing a person or work instruction invalidates reliance on the old person's plan.
    if recipient != ADMIN or w.get('execution_mode') != 'self_direct':
        w['execution_mode'] = 'plan_required'; w['plan_status'] = 'not_submitted'
        w['execution_plan_ref'] = None; w['execution_decision_ref'] = None
        w['authorized_scopes'] = ['planning']
    w['next_action'] = '담당 미정' if recipient is None else ('업무계획안 제출' if recipient != ADMIN else '관리자 직접 수행 범위 확인')
    overlay = {ap: c.dump(assignment)}
    for to in sorted(recipients):
        nid = f'N-{aid}-{to}'; new = to == recipient
        n = dict(schema_version=2, notification_id=nid, event_type='assignment' if new else 'assignment_released',
            recipient_actor_id=to, assignment_id=aid, assignment_ref=ap, target_type='assignment', target_id=w['id'],
            target_revision=1, title=brief['title'], assigned_at=assigned_at, decided_at=assigned_at,
            instruction_text=instruction if new else '이 업무의 배정이 변경되어 기존 담당 배정이 종료되었습니다.',
            approved_brief=brief if new else None, authority='derived_assignment_notification_not_execution_approval')
        overlay[f'records/notifications/{to}/{nid}.json'] = c.dump(n)
    return overlay


def assignment_notifications(actor, notes, receipts, assignments):
    delivered = {r['notification_id'] for r in receipts if r.get('recipient_actor_id') == actor and r.get('delivered_at')}
    selected = []
    for n in notes:
        if n.get('event_type') not in {'assignment', 'assignment_released'} or n.get('recipient_actor_id') != actor or n['notification_id'] in delivered:
            continue
        tip = assignment_tip(assignments, n['target_id'])
        if tip and tip['assignment_id'] == n['assignment_id']:
            selected.append(n)
    return selected


def assignment_views(root, overlay, actors):
    c = core()
    def group(folder, pattern):
        result = dict(c.records(root, folder, pattern))
        for p, s in overlay.items():
            if p.startswith(folder + '/') and Path(p).match(pattern): result[p] = json.loads(s)
        return list(result.values())
    assignments = group('work/assignments', 'ASG-*.json'); works = group('work/items', 'W-*.json')
    result = {}
    for actor in actors:
        items = []
        for w in works:
            tip = assignment_tip(assignments, w['id'])
            if not tip or tip.get('assigned_to_actor_id') != actor['actor_id'] or w['work_status'] in {'done', 'cancelled'}:
                continue
            items.append(dict(work_id=w['id'], assignment_id=tip['assignment_id'], assignment_ref=f"work/assignments/{tip['assignment_id']}.json",
                title=tip['approved_brief']['title'], instruction_text=tip['instruction_text'],
                approved_brief=tip['approved_brief'], plan_status=w.get('plan_status'), work_status=w['work_status'],
                next_action=w.get('next_action')))
        result[f"records/assignment-views/{actor['actor_id']}.json"] = c.dump(dict(schema_version=1, actor_id=actor['actor_id'],
            authority='derived_active_assignment_view_not_notification', items=items))
    return result


def check_execution(root, w, event):
    c = core(); adoption = current_adoption(root, w)
    who = event['actor_id']
    c.need(w.get('assigned_to_actor_id') is not None, 'Unassigned work cannot be performed')
    phase = event.get('phase', 'execution')
    c.need(phase in {'planning', 'execution'}, 'Unknown work phase')
    if phase == 'planning':
        c.need(event.get('patch', {}).get('work_status') not in {'done', 'in_progress'}, 'Planning update cannot claim full execution/completion')
        return
    if w.get('execution_mode') == 'self_direct':
        c.need(w.get('assigned_to_actor_id') == who == ADMIN, 'Self-execution is not delegated authority')
        return
    # Legacy work remains readable but needs an explicit valid plan for new execution.
    dp = w.get('execution_decision_ref'); sp = w.get('execution_plan_ref')
    c.need(dp and sp and w.get('plan_status') == 'approved', 'Plan approval required before actual execution')
    d = c.load(root, dp); s = c.load(root, sp)
    ds = [x for _, x in c.records(root, 'approvals', 'D-*.json')]; tip = c.latest(ds, c.chain_key(d))
    c.need(tip and tip['decision'] == 'approved' and 'plan_execution' in tip['granted_scopes'], 'Plan execution approval is no longer current')
    c.need(d['target_ref'] == sp and d['target_revision'] == s['revision'] and d['target_hash'] == c.digest(c.proposal(s)), 'Approved plan version changed')
    c.need(hashlib.sha256(c.safe(root, s['artifact_path']).read_bytes()).hexdigest() == s['artifact_sha256'], 'Approved plan body changed')
    c.need(d.get('execution_assignee_actor_id') == w['assigned_to_actor_id']
           and d.get('assignment_ref') == w.get('current_assignment_ref'), 'Plan approval belongs to another assignment')
    req = c.load(root, d['request_ref'])
    c.need(s['request_content_revision'] == c.revision(req) and s['request_content_hash'] == c.digest(c.proposal(req)), 'Plan parent requirements changed')
    scope = event.get('execution_scope')
    c.need(scope in tip['granted_scopes'] and scope not in {'work_adoption', 'planning', 'plan_execution', 'work_start'}, 'Name the actually authorized activity scope')
