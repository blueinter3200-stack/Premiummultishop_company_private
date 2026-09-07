#!/usr/bin/env python3
"""Explicit ACT-001 direct request -> review -> adoption -> W -> optional ASG/N -> status-map planner.
No NLP, no network, no authentication. The caller must supply collision-checked IDs and actual user source.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path


def core():
    import decision_flow as c
    return c


def plan_direct(root: Path, event: dict) -> dict:
    c=core(); from work_status import project_status, validate_public_summary
    c.need(event.get('actor_id')=='ACT-001','Administrator only')
    c.need(event.get('command')=='/업무결정' and str(event.get('outcome','')).replace(' ','')=='승인','Explicit 업무결정 승인 required')
    c.need(event.get('write_requested') is True and not any(event.get(x) for x in ('quoted','read_only','save_prohibited')),'Actual write request required')
    source=event.get('source',{}); c.need(source.get('text') and source.get('locator') and event.get('source_event_id'),'Actual administrator source required')
    spec=event.get('direct_request',{}); c.need(spec.get('title') and spec.get('scope') and spec.get('completion_criteria'),'Concrete work title/scope/completion criteria required')
    c.need(isinstance(spec['scope'],list) and isinstance(spec['completion_criteria'],list) and spec['scope'] and spec['completion_criteria'],'Nonempty direct scope/criteria required')
    if spec.get('public_summary'): validate_public_summary(spec['public_summary'])
    # Idempotency: find an existing request created from the exact same source event.
    existing=[]
    for p,r in c.records(root,'records/requests','R-*.json'):
        if r.get('source_event_id')==event['source_event_id']: existing.append((p,r))
    c.need(len(existing)<=1,'Duplicate direct-request source event')
    if existing:
        rp,req=existing[0]; c.need(req.get('source_fingerprint')==c.digest({'text':source['text'],'locator':source['locator']}),'Reused source event with changed source')
        wid=(req.get('related_work_ids') or [None])[0]
        c.need(wid and c.safe(root,f'work/items/{wid}.json').exists(),'Partial direct request persistence')
        return dict(status='already_recorded',base_commit=event['base_commit'],files={},expected_blobs={})
    # If the caller resolved an existing R, it must go through the ordinary decision path instead.
    c.need(not event.get('existing_request_ref'),'Existing request must preserve its original requester and use ordinary decision')
    rid=event.get('request_id'); wid=event.get('work_id'); did=event.get('decision_id')
    c.need(c.valid_id(rid,'R') and c.valid_id(wid,'W') and c.valid_id(did,'D'),'Collision-checked R/D/W IDs required')
    c.need(not any(r.get('request_id')==rid for _,r in c.records(root,'records/requests','R-*.json')),'R-ID collision')
    c.need(not any(w.get('id')==wid for _,w in c.records(root,'work/items','W-*.json')),'W-ID collision')
    c.need(not any(d.get('decision_id')==did for _,d in c.records(root,'approvals','D-*.json')),'D-ID collision')
    captured=event.get('recorded_at'); c.need(captured,'Recording date required')
    proposal={'title':spec['title'],'scope':spec['scope'],'completion_criteria':spec['completion_criteria']}
    request=dict(schema_version=4,object_type='request',request_id=rid,revision=1,content_revision=1,requester_actor_id='ACT-001',recorded_by_actor_id='ACT-001',
        record_owner_actor_id='ACT-001',submitted_by_actor_id='ACT-001',requester_role_at_capture='admin',source_type='direct_conversation',source_verification=None,
        source_locator=source['locator'],original_text=source['text'],source_created_at=event.get('source_created_at'),captured_at=captured,classification='work',scope=[],conditions=event.get('conditions',[]),
        request_status='in_progress',submission_status='submitted',primary_scope='work_adoption',requested_scopes=['work_adoption','planning'],related_work_ids=[wid],related_idea_ids=[],
        related_problem_ids=[],related_decision_ids=[did],submission_refs=[],supersedes=None,unknowns=[],request_change_refs=[],current_requirements=proposal,public_summary=spec.get('public_summary'),
        source_event_id=event['source_event_id'],source_fingerprint=c.digest({'text':source['text'],'locator':source['locator']}))
    review=event.get('review'); c.check_review(review,request,event['base_commit']);request['review_snapshot']=review
    rp=f'records/requests/ACT-001/{rid}.json'
    dec_event=copy.deepcopy(event);dec_event.update(operation='decide',target_ref=rp,target_revision=1,target_hash=c.digest(c.proposal(request)),scope_key='work_adoption',
        granted_scopes=['work_adoption','planning'],previous_decision_id=None,request_context={'request_id':rid,'content_revision':1,'content_hash':c.digest(c.proposal(request))})
    result=c.make_decision(request,dec_event,[d for _,d in c.records(root,'approvals','D-*.json')]);c.need(result['status']=='planned','Unexpected direct decision result');d=result['decision']
    # First create a W without allowing plan execution.
    work=c.work_effect(d,request,{**event,'work_id':wid},c.records(root,'work/items','W-*.json'));c.need(work,'Adopted work required');wp,w=work
    assignment_event=copy.deepcopy(event);assignment_event['assignment']=event.get('assignment')
    files={rp:c.dump(request),f'approvals/{did}.json':c.dump(d),wp:c.dump(w)}
    if event.get('assignment'):
        added=c.wp.assign(root,w,assignment_event,d);files.update(added);files[wp]=c.dump(w)
    # Set public repository refs only when they are registered locators; no implementation verification is invented.
    if spec.get('related_repositories'):
        from work_status import validate_related_repositories
        validate_related_repositories(root,spec['related_repositories']);w['related_repositories']=spec['related_repositories'];files[wp]=c.dump(w)
    actors=c.load(root,'llm-source/ACTOR_REGISTRY.json')['actors']
    files.update(c.render(root,files,actors))
    files['working/WORK_STATUS_MAP.json']=project_status(root,files)
    ip='records/REQUEST_INDEX.md'; prior=c.safe(root,ip).read_text(encoding='utf-8') if c.safe(root,ip).exists() else '# Request Index\n'
    files[ip]=prior+f"\n- {rid} / ACT-001 / direct approved request / {rp}\n"
    expected={p:c.blob(c.safe(root,p).read_bytes()) if c.safe(root,p).exists() else None for p in files}
    return dict(status='planned',base_commit=event['base_commit'],files=files,expected_blobs=expected,
        follow_up='Commit complete R/D/W/optional ASG/N/views/map atomically and re-read. No external repository changes are implied.')
