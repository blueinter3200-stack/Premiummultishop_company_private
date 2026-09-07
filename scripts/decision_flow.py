#!/usr/bin/env python3
"""Pure planners for work decisions and execution plans. No network, writes, autonomous NLP, authentication or push.
A trusted caller must read current main, assess intent/evidence, commit the entire plan
with optimistic concurrency, then re-read every returned path. Flags are not identity proof.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import work_plans as wp
import work_status as status_map
from typing import Any

ADMIN = 'ACT-001'
OUTCOMES = {'승인':'approved','수정요청':'revision_required','보류':'held','반려':'rejected'}
SCOPES = {'work_start','research','production','deliverable','publication','expenditure','policy_change','work_adoption','planning','plan_execution'}
RETIRED = {'/업무확정','/품의서승인','/업무공유','/업무접수','/대표업무점검','/대표업무검토','/품의상신','/품의승인','/품의서작성','/품의서결정','/품의서결의'}
READ_ONLY = {'/아이디어출력','/문제출력','/업무검토','/업무점검','/반영미리보기','/업무진행현황'}

def need(ok: Any, message: str) -> None:
    if not ok: raise ValueError(message)

def canonical(x: Any) -> bytes:
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def digest(x: Any) -> str: return hashlib.sha256(canonical(x)).hexdigest()

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def dump(x: Any) -> str: return json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n'

def safe(root: Path, path: str) -> Path:
    p=(root/path).resolve()
    need(not Path(path).is_absolute() and '..' not in Path(path).parts and p.is_relative_to(root.resolve()),'Unsafe path')
    return p

def load(root: Path, path: str) -> Any: return json.loads(safe(root,path).read_text(encoding='utf-8'))

def records(root: Path, folder: str, pattern: str) -> list[tuple[str,dict]]:
    return [(p.relative_to(root).as_posix(),json.loads(p.read_text(encoding='utf-8'))) for p in sorted((root/folder).rglob(pattern))]

def valid_id(value: str, prefix: str) -> bool:
    return bool(re.fullmatch(re.escape(prefix)+r'-\d{8}-\d{3,}',str(value)))

def proposal(obj: dict) -> dict:
    return obj.get('current_requirements') or obj.get('proposal') or {k:obj.get(k) for k in ('original_text','scope','conditions','current_requirements')}

def revision(obj: dict) -> int: return obj.get('content_revision',obj.get('revision',1))

def subject(obj: dict) -> tuple[str,str,int]:
    return ('submission',obj['submission_id'],obj['revision']) if 'submission_id' in obj else ('request',obj['request_id'],revision(obj))

def chain_key(d: dict) -> tuple:
    if d.get('scope_key')=='work_start' and d.get('authorization_target'):
        a=d['authorization_target'];return 'request',a['request_id'],a['content_revision'],'work_start'
    return d['target_type'],d['target_id'],d['target_revision'],d['scope_key']

def latest(decisions: list[dict], key: tuple) -> dict|None:
    ds=[d for d in decisions if d.get('target_type') and chain_key(d)==key]
    if not ds: return None
    by_id={d['decision_id']:d for d in ds}
    need(len(by_id)==len(ds),'Duplicate decision ID')
    predecessor_ids={d['previous_decision_id'] for d in ds if d.get('previous_decision_id')}
    need(predecessor_ids<=set(by_id),'Missing decision predecessor')
    children={i:0 for i in by_id}
    for d in ds:
        if d.get('previous_decision_id'): children[d['previous_decision_id']]+=1
    need(all(n<=1 for n in children.values()),'CONFLICT: decision chain branches')
    tips=[d for d in ds if d['decision_id'] not in predecessor_ids]
    roots=[d for d in ds if not d.get('previous_decision_id')]
    need(len(tips)==len(roots)==1,'CONFLICT: ambiguous or cyclic decision chain')
    seen=set();cur=tips[0]
    while cur:
        need(cur['decision_id'] not in seen,'Cyclic decision chain');seen.add(cur['decision_id'])
        cur=by_id.get(cur.get('previous_decision_id'))
    need(len(seen)==len(ds),'Disconnected decision chain')
    return tips[0]

def check_review(review: dict, obj: dict, head: str) -> None:
    need(review.get('result')=='PASS' and review.get('classification') in {'work','mixed'},'Review PASS for work candidate required')
    need(review.get('subject_hash')==digest(proposal(obj)),'Review content is stale')
    need(review.get('basis_commit')==head,'Revalidate review against current main')
    need(review.get('reviewed_by_actor_id') and isinstance(review.get('evidence_refs'),list),'Review provenance required')

def make_decision(obj: dict, event: dict, decisions: list[dict]) -> dict:
    need(event.get('actor_id')==ADMIN,'Administrator only')
    need(obj.get('submission_status')=='submitted','Only reviewed submitted objects can be decided')
    kind,oid,rev=subject(obj)
    expected='/업무결정' if kind=='request' else '/업무계획안결의'
    need(event.get('command')==expected,'Wrong command for decision target')
    val=str(event.get('outcome','')).replace(' ','')
    need(val in OUTCOMES,'Explicit valid outcome required; no default approval')
    outcome=OUTCOMES[val]
    need(event.get('target_revision')==rev and event.get('target_hash')==digest(proposal(obj)),'Stale target version/hash')
    scope=event.get('scope_key')
    need(scope in SCOPES and scope==obj.get('primary_scope','work_start'),'Wrong decision scope')
    check_review(event.get('review',{}),obj,event['base_commit'])
    reason=event.get('reason')
    need(outcome=='approved' or (isinstance(reason,str) and bool(reason.strip())),'Nonapproval requires actual reason')
    source=event.get('source',{})
    need(source.get('text') and source.get('locator'),'Decision source required')
    if reason:
        excerpt=event.get('reason_excerpt',reason)
        need(excerpt and excerpt in source['text'],'Actual reason excerpt must occur in decision source')
    need(event.get('source_event_id') and event.get('decided_at'),'Event key and recording date required')
    scopes=event.get('granted_scopes',[])
    need(isinstance(scopes,list) and len(scopes)==len(set(scopes)) and set(scopes)<=SCOPES,'Invalid granted scopes')
    need(outcome=='approved' or not scopes,'Nonapproval grants no execution')
    details=event.get('scope_details',{})
    if 'expenditure' in scopes:
        v=details.get('expenditure',{});need(all(k in v for k in ('amount','currency','payee','period')),'Explicit expenditure details required')
    if 'publication' in scopes:
        v=details.get('publication',{});need(all(v.get(k) for k in ('account','artifact_version','schedule')),'Explicit publication details required')
    if outcome=='approved':
        need(bool(scopes) and set(scopes)<=set(obj.get('requested_scopes',[])),'Approval must stay within requested scope')
        if kind=='request':
            need(bool(set(scopes)&{'work_adoption','work_start'}),'Work adoption must be explicit')
            if event.get('execution_mode')!='self_direct':
                need(set(scopes)<={'work_adoption','work_start','planning'},'Request approval is not plan execution approval')
        if 'plan_execution' in scopes: need(kind=='submission','Execution plan required')
    ctx=event.get('request_context') or {'request_id':obj.get('request_id'),'content_revision':revision(obj),'content_hash':digest(proposal(obj))}
    need(ctx.get('request_id'),'Request authorization context required')
    key=('request',ctx['request_id'],ctx['content_revision'],scope) if scope=='work_start' else (kind,oid,rev,scope)
    prior=latest(decisions,key)
    if kind=='submission' and outcome=='approved' and 'work_adoption' in scopes:
        for adoption_scope in ('work_adoption','work_start'):
            parent=latest(decisions,('request',ctx['request_id'],ctx['content_revision'],adoption_scope))
            need(not parent or parent['decision']=='approved','Existing held/rejected request needs an explicit 업무결정 first')
    fp=digest({k:v for k,v in event.items() if k not in {'base_commit','review'}})
    for d in decisions:
        if d.get('source_event_id')==event['source_event_id']:
            need(d.get('event_fingerprint')==fp,'Reused event key with changed payload')
            return {'status':'already_recorded','decision':d}
    need((prior or {}).get('decision_id')==event.get('previous_decision_id'),'Stale predecessor')
    semantic={'decision':outcome,'reason':reason,'granted_scopes':scopes,'conditions':event.get('conditions',[]),'scope_details':details,'assignment':event.get('assignment'),'execution_mode':event.get('execution_mode')}
    if prior and (prior['target_type'],prior['target_id'],prior['target_revision'],prior['target_hash'])==(kind,oid,rev,digest(proposal(obj))) and all(prior.get(k)==v for k,v in semantic.items()):
        return {'status':'unchanged','decision':prior}
    if prior and prior['decision']=='rejected': need(event.get('reopen_reason'),'Explicit reopening evidence/reason required')
    revokes=[]
    if prior and prior['decision']=='approved':
        need(event.get('revoke_previous') is True and event.get('change_reason'),'Changing approved scope requires explicit redecision/revocation')
        revokes=[prior['decision_id']]
    did=event.get('decision_id');need(valid_id(did,'D'),'Invalid D-ID')
    need(all(d['decision_id']!=did for d in decisions),'D-ID collision')
    d=dict(schema_version=3,object_type='decision',decision_id=did,target_type=kind,target_id=oid,
           target_revision=rev,target_hash=digest(proposal(obj)),target_ref=event['target_ref'],scope_key=scope,
           previous_decision_id=(prior or {}).get('decision_id'),previous_state=(prior or {}).get('decision','pending'),
           requested_scopes=obj.get('requested_scopes',[]),**semantic,reason_source='explicit_user_statement' if reason else 'not_stated',
           approver_actor_id=ADMIN,approver_role='admin',approval_source=source,
           principal_verification='project_role_based_not_independently_authenticated',decided_at=event['decided_at'],
           source_event_id=event['source_event_id'],event_fingerprint=fp,review_snapshot=event['review'],
           revokes_decision_ids=revokes,reopen_reason=event.get('reopen_reason'),change_reason=event.get('change_reason'),
           request_ref=obj.get('request_ref') or event['target_ref'],authorization_target=ctx,work_id=None,
           authority='scoped_decision_not_execution_receipt')
    return {'status':'planned','decision':d}

def work_effect(d: dict, request: dict, event: dict, existing: list[tuple[str,dict]]) -> tuple[str,dict]|None:
    return wp.work_effect(d,request,event,existing)


def make_notifications(d: dict, target: dict, requester: str, assignee: str|None) -> list[tuple[str,dict]]:
    recipients={requester,target.get('submitted_by_actor_id')} - {None,ADMIN}
    if assignee and ('submission_id' in target or not d.get('assignment')): recipients.add(assignee)
    recipients.discard(ADMIN)
    result=[]
    for aid in sorted(recipients):
        nid=f"N-{d['decision_id']}-{aid}"; path=f'records/notifications/{aid}/{nid}.json'
        result.append((path,dict(schema_version=1,notification_id=nid,recipient_actor_id=aid,decision_id=d['decision_id'],
          decision_ref=f"approvals/{d['decision_id']}.json",target_type=d['target_type'],target_id=d['target_id'],
          target_revision=d['target_revision'],scope_key=d['scope_key'],title=target.get('title') or proposal(target).get('title'),
          previous_state=d['previous_state'],decision=d['decision'],reason=d['reason'],granted_scopes=d['granted_scopes'],authorization_target=d.get('authorization_target'),
          decided_at=d['decided_at'],authority='derived_notification_not_approval')))
    return result

def inbox(actor: str, notifications: list[dict], receipts: list[dict], decisions: list[dict], page_size: int=20, assignments: list[dict]|None=None) -> dict:
    need(page_size>0,'Invalid page size')
    delivered={r['notification_id'] for r in receipts if r.get('recipient_actor_id')==actor and r.get('delivered_at')}
    selected=wp.assignment_notifications(actor,notifications,receipts,assignments or [])
    for n in notifications:
        if n.get('event_type') in {'assignment','assignment_released'}: continue
        if n.get('recipient_actor_id')!=actor or n['notification_id'] in delivered: continue
        tip=latest(decisions,chain_key(n))
        if tip and tip['decision_id']==n['decision_id']: selected.append(n)
    selected.sort(key=lambda n:(n['decided_at'],n.get('decision_id',n['notification_id'])),reverse=True)
    out=dict(schema_version=1,actor_id=actor,authority='derived_view',unread_count=len(selected),items=selected[:page_size],
             more_count=max(0,len(selected)-page_size),next_page=2 if len(selected)>page_size else None)
    out['inbox_revision']=digest(out);return out

def render(root: Path, overlay: dict[str,str], actors: list[dict]) -> dict[str,str]:
    def group(folder,pattern):
        data=dict(records(root,folder,pattern))
        for p,s in overlay.items():
            if p.startswith(folder+'/') and Path(p).match(pattern): data[p]=json.loads(s)
        return list(data.items())
    ds=[d for _,d in group('approvals','D-*.json') if d.get('target_type') in {'request','submission'}]
    notes=[n for _,n in group('records/notifications','N-*.json')]
    receipts=[n for _,n in group('records/notification-receipts','N-*.json')]
    targets=group('records/requests','R-*.json')+group('records/submissions','SUB-*.json')
    assignments=[a for _,a in group('work/assignments','ASG-*.json')]
    all_works=group('work/items','W-*.json')
    summary=[];all_targets={}
    for p,t in targets:
        kind,oid,rev=subject(t);old=all_targets.get((kind,oid))
        if old is None or rev>old[1]: all_targets[(kind,oid)]=(p,rev,t)
    for (kind,oid),(p,rev,t) in all_targets.items():
        adopted=[w for _,w in all_works if p in w.get('request_refs',[]) and w.get('adoption_decision_ref')]
        if t.get('submission_status')!='submitted' and not adopted:continue
        scope=t.get('primary_scope','work_start');tip=latest(ds,(kind,oid,rev,scope))
        if kind=='submission' and scope=='work_start':
            matches=[d for d in ds if (d['target_type'],d['target_id'],d['target_revision'],d['scope_key'])==(kind,oid,rev,scope)]
            tip=latest(ds,chain_key(matches[-1])) if matches else None
        if kind=='request' and not tip and len(adopted)==1:
            ref=adopted[0]['adoption_decision_ref']
            linked=next((d for d in ds if f"approvals/{d['decision_id']}.json"==ref),None)
            if linked:tip=latest(ds,chain_key(linked))
        summary.append(dict(target_type=kind,target_id=oid,target_revision=rev,path=p,scope_key=scope,
           author_actor_id=t.get('submitted_by_actor_id') or t.get('requester_actor_id'),
           requester_actor_id=t.get('requester_actor_id'),title=t.get('title') or proposal(t).get('title'),
           status=(tip or {}).get('decision','pending'),decision_id=(tip or {}).get('decision_id'),
           reason=(tip or {}).get('reason'),decision_ref=f"approvals/{tip['decision_id']}.json" if tip else None))
    files={}
    index=dict(schema_version=1,authority='derived_index',items=summary,decision_events=[
        {k:d.get(k) for k in ('decision_id','target_type','target_id','target_revision','scope_key','decision','reason','decided_at','previous_decision_id','target_ref')}
        for d in ds],legacy_note='Older decisions without target_type remain in approvals; inspect original records when relevant.')
    files['records/DECISION_INDEX.json']=dump(index)
    for a in actors:
        aid=a['actor_id'];view=[x for x in summary if aid==ADMIN or aid in {x.get('author_actor_id'),x.get('requester_actor_id')}]
        files[f'records/decision-views/{aid}.json']=dump(dict(schema_version=1,actor_id=aid,authority='derived_view',items=view))
        current_notes=[n for n in notes if (n.get('target_type'),n.get('target_id')) not in all_targets or n.get('target_revision')==all_targets[(n['target_type'],n['target_id'])][1]]
        current=inbox(aid,current_notes,receipts,ds,assignments=assignments)
        full=inbox(aid,current_notes,receipts,ds,page_size=max(1,len(notes)+1),assignments=assignments)['items']
        pages=[full[i:i+20] for i in range(0,len(full),20)]
        if len(pages)>1:
            current['next_page']=f'records/inbox/pages/{aid}/2.json'
            for num,items in enumerate(pages[1:],2):
                files[f'records/inbox/pages/{aid}/{num}.json']=dump(dict(actor_id=aid,page=num,items=items,
                    next_page=f'records/inbox/pages/{aid}/{num+1}.json' if num<len(pages) else None))
        current['inbox_revision']=digest({k:v for k,v in current.items() if k!='inbox_revision'})
        files[f'records/inbox/{aid}.json']=dump(current)

    if any(p.startswith('work/items/') for p in overlay):
        works=group('work/items','W-*.json')
        def table(items):
            def cell(v):return str(v if v is not None else '미정').replace('|','/').replace('\n',' ')
            text='| ID | 업무 | 상태 | 담당 | 다음 행동 | 기준일 |\n|---|---|---|---|---|---|\n'
            return text+'\n'.join('| '+' | '.join(cell(w.get(k)) for k in ('id','title','work_status','assigned_to_actor_id','next_action','information_as_of'))+' |' for _,w in items)+'\n'
        files['working/CURRENT_WORK.md']='# Current Work\n\nwork/items가 상태 원본이며 승인·구현 증거는 연결된 원문에서 확인한다.\n\n'+table(works)
        files['assistant/30-working/ACTIVE.md']='# Assistant Active\n\n'+table([(p,w) for p,w in works if w.get('assigned_to_actor_id')=='ACT-003' and w.get('work_status') not in {'done','cancelled'}])
        files['assistant/30-working/BLOCKED.md']='# Blocked Work\n\n'+table([(p,w) for p,w in works if w.get('work_status')=='blocked'])
    pending=[x for x in summary if x['status'] in {'pending','held','revision_required'}]
    marker='<!-- GOV05 DECISION VIEW -->'
    dp='assistant/30-working/DECISION_NEEDED.md'
    prior=safe(root,dp).read_text(encoding='utf-8').split(marker)[0] if safe(root,dp).exists() else '# Decision Needed\n'
    files[dp]=prior.rstrip()+'\n\n'+marker+'\n'+''.join(f"- {x['target_id']} r{x['target_revision']} / {x['status']} / {x['path']}\n" for x in pending)
    files.update(wp.assignment_views(root,overlay,actors))
    files['working/WORK_STATUS_MAP.json']=status_map.project_status(root,overlay)
    return files

def plan(root: Path, event: dict) -> dict:
    need(re.fullmatch(r'[0-9a-f]{40}',str(event.get('base_commit',''))),'Fresh main commit required')
    command=event.get('command','').split(' ',1)[0]
    need(command not in RETIRED,'RETIRED_COMMAND; no alias execution')
    if command=='/업무진행현황':
        return status_map.query_bundle(root,event)
    if command in READ_ONLY or any(event.get(k) for k in ('read_only','save_prohibited','quoted')):
        return dict(status='no_write',files={},expected_blobs={},base_commit=event['base_commit'])
    need(event.get('write_requested') is True,'Explicit scoped operation required')
    actors=load(root,'llm-source/ACTOR_REGISTRY.json')['actors'];actor=next((a for a in actors if a['actor_id']==event.get('actor_id') and a['status']=='active'),None)
    need(actor is not None,'Unregistered actor')
    role=actor['role'];files={};operation=event.get('operation')
    if operation=='direct_admin_request':
        from direct_requests import plan_direct
        return plan_direct(root,event)
    if operation=='decide':
        need(role=='admin' and actor['actor_id']==ADMIN,'Administrator only')
        obj=load(root,event['target_ref']);decisions=[d for _,d in records(root,'approvals','D-*.json')]
        req=load(root,obj['request_ref']) if obj.get('request_ref') else obj
        if 'submission_id' in obj:
            need(obj.get('request_content_revision')==revision(req) and obj.get('request_content_hash')==digest(proposal(req)),'Submission parent request changed; review again')
            actual=safe(root,obj['artifact_path']).read_bytes()
            need(hashlib.sha256(actual).hexdigest()==obj['artifact_sha256'],'Submission body/version mismatch')
        event=copy.deepcopy(event);event['request_context']={'request_id':req['request_id'],'content_revision':revision(req),'content_hash':digest(proposal(req))}
        result=make_decision(obj,event,decisions)
        if result['status']!='planned':
            d=result['decision']
            for aid in d.get('recipient_actor_ids',[]):
                need(safe(root,f"records/notifications/{aid}/N-{d['decision_id']}-{aid}.json").is_file(),'Partial notification persistence: repair same D/N, do not duplicate')
            if set(d.get('granted_scopes',[])) & {'work_start','work_adoption'}:
                need(d.get('work_id') and safe(root,f"work/items/{d['work_id']}.json").is_file(),'Partial work persistence: repair same W-ID')
            for q,expected in render(root,{},actors).items():
                need(safe(root,q).is_file() and safe(root,q).read_text(encoding='utf-8')==expected,'Derived views incomplete; rebuild without another decision')
            return dict(status=result['status'],files={},expected_blobs={},base_commit=event['base_commit'])
        d=result['decision']
        if 'submission_id' in obj:d['artifact_refs']=[{'path':obj['artifact_path'],'sha256':obj['artifact_sha256'],'revision':obj['revision']}]
        request=load(root,d['request_ref']);work=work_effect(d,request,event,records(root,'work/items','W-*.json'))
        if work:
            files.update(wp.assign(root,work[1],event,d))
            if d['decision']=='approved' and 'plan_execution' in d['granted_scopes']:
                w=work[1]
                need(w.get('assigned_to_actor_id') is not None,'Plan execution needs an explicitly assigned performer')
                need(w['assigned_to_actor_id']==obj.get('proposed_assignee_actor_id',obj.get('submitted_by_actor_id')),'Plan performer differs from assigned performer')
                d['execution_assignee_actor_id']=w['assigned_to_actor_id'];d['assignment_ref']=w.get('current_assignment_ref')
                w['plan_status']='approved';w['execution_plan_ref']=event['target_ref'];w['execution_decision_ref']=f"approvals/{d['decision_id']}.json"
                w['authorized_scopes']=d['granted_scopes'];w['next_action']='최신 승인 계획·배정 확인 후 허용 범위 수행'
            files[work[0]]=dump(work[1])
        files[f"approvals/{d['decision_id']}.json"]=dump(d)
        assignee=work[1].get('assigned_to_actor_id') if work else None
        if not work and obj.get('work_id'):
            w=load(root,f"work/items/{obj['work_id']}.json");assignee=w.get('assigned_to_actor_id');d['work_id']=w['id'];files[f"approvals/{d['decision_id']}.json"]=dump(d)
        notes=make_notifications(d,obj,request['requester_actor_id'],assignee)
        d['recipient_actor_ids']=[n['recipient_actor_id'] for _,n in notes]
        files[f"approvals/{d['decision_id']}.json"]=dump(d)
        for p,n in notes:
            need(not safe(root,p).exists(),'Notification ID collision');files[p]=dump(n)
    elif operation=='assign_work':
        need(role=='admin' and actor['actor_id']==ADMIN,'Administrator assignment only')
        need(command=='','Use explicit natural-language assignment, not an implicit decision outcome')
        path=event['work_ref'];w=copy.deepcopy(load(root,path))
        need(event.get('expected_revision')==w['revision'],'Stale assignment work revision')
        added=wp.assign(root,w,event)
        if not added:return dict(status='already_recorded',files={},expected_blobs={},base_commit=event['base_commit'])
        w['revision']+=1;w['updated_at']=event['assignment']['assigned_at'];files.update(added);files[path]=dump(w)
    elif operation=='submit_request':
        need(command=='/업무요청','Wrong submission command')
        obj=copy.deepcopy(event['request'])
        if obj.get('requester_actor_id')!=actor['actor_id']:
            _,obj=wp.reported_request(root,actor['actor_id'],obj)
        obj.setdefault('record_owner_actor_id',actor['actor_id'])
        need(obj['record_owner_actor_id']==actor['actor_id'],'Request record ownership')
        need(valid_id(obj.get('request_id'),'R'),'Invalid R-ID');need(obj.get('original_text'),'Original text required')
        check_review(event.get('review',{}),obj,event['base_commit'])
        obj['submission_status']='submitted';obj['review_snapshot']=event['review']
        path=f"records/requests/{actor['actor_id']}/{obj['request_id']}.json"
        if safe(root,path).exists():
            old=load(root,path);need(old['original_text']==obj['original_text'],'Original request text is immutable')
            need(obj.get('revision')==old['revision']+1,'Request revision conflict')
            need(proposal(old)==proposal(obj) or revision(obj)==revision(old)+1,'Changed content needs a new content revision')
        old_links=old.get('related_work_ids',[]) if safe(root,path).exists() else []
        need(set(obj.get('related_work_ids',[]))<=set(old_links),'Submission cannot activate a new work')
        if safe(root,path).exists() and actor['actor_id']==ADMIN and proposal(old)!=proposal(obj):
            need(len(obj.get('request_change_refs',[]))>len(old.get('request_change_refs',[])),'Material admin changes require RC workflow first')
        files[path]=dump(obj)
    elif operation=='submit_submission':
        need(command=='/업무계획안제출' and role in {'admin','assistant'},'Submission role boundary')
        obj=copy.deepcopy(event['submission']);need(obj.get('submitted_by_actor_id')==actor['actor_id'],'Submission author mismatch')
        need(re.fullmatch(r'SUB-[RW]-\d{8}-\d{3,}-\d{3,}',str(obj.get('submission_id'))),'Invalid SUB-ID')
        need(type(obj.get('revision')) is int and obj['revision']>0,'Submission revision required')
        check_review(event.get('review',{}),obj,event['base_commit'])
        if event.get('reported_request'):
            rp,request=wp.reported_request(root,actor['actor_id'],event['reported_request'])
            need(obj['request_ref']==rp,'Plan must reference the captured oral request')
            files[rp]=dump(request)
            ip='records/REQUEST_INDEX.md';prior=safe(root,ip).read_text(encoding='utf-8') if safe(root,ip).exists() else '# Request Index\n'
            files[ip]=prior+f"\n- {request['request_id']} / reported requester ACT-002 / recorder {actor['actor_id']} / captured with plan / {rp}\n"
        else:request=load(root,obj['request_ref'])
        need(request.get('request_id'),'Actual request required')
        wp.check_request_access(root,actor['actor_id'],request,obj.get('assignment_ref'))
        obj['plan_type']='execution_plan';obj['proposed_assignee_actor_id']=obj.get('proposed_assignee_actor_id',actor['actor_id'])
        need(obj.get('primary_scope')=='plan_execution','New plans use a separate plan_execution decision scope')
        if obj.get('work_id'):
            assigned=load(root,f"work/items/{obj['work_id']}.json")
            need(role=='admin' or assigned.get('assigned_to_actor_id')==actor['actor_id'],'Not your assigned work')
            need(obj.get('assignment_ref')==assigned.get('current_assignment_ref'),'Plan assignment is stale')
        artifact=event.get('artifact_text');need(isinstance(artifact,str) and bool(artifact),'Actual submission body required')
        sp=f"records/submissions/{obj['submission_id']}-r{obj['revision']}.json"
        ap=f"assistant/40-handoff/to-jin/{obj['submission_id']}-r{obj['revision']}.md"
        need(not safe(root,sp).exists() and not safe(root,ap).exists(),'Submission revision already exists; do not overwrite')
        if obj.get('work_id'):need(safe(root,f"work/items/{obj['work_id']}.json").is_file(),'Do not invent W-ID before approval')
        obj.update(submission_status='submitted',review_snapshot=event['review'],artifact_path=ap,artifact_sha256=hashlib.sha256(artifact.encode()).hexdigest(),request_content_revision=revision(request),request_content_hash=digest(proposal(request)))
        files[sp]=dump(obj);files[ap]=artifact
        if obj.get('work_id'):
            wp_path=f"work/items/{obj['work_id']}.json";assigned=copy.deepcopy(load(root,wp_path))
            assigned['revision']+=1;assigned['proposed_plan_ref']=sp;assigned['proposed_plan_status']='submitted'
            assigned['submission_refs']=list(dict.fromkeys(assigned.get('submission_refs',[])+[sp]))
            if not assigned.get('execution_plan_ref'):
                assigned['plan_status']='submitted';assigned['next_action']='업무계획안 관리자 결의 대기'
            files[wp_path]=dump(assigned)
    elif operation=='update_work':
        need(command=='/업무업데이트' and role in {'admin','assistant'},'Work-update role boundary')
        path=event['work_ref'];w=load(root,path)
        need(role=='admin' or w.get('assigned_to_actor_id')==actor['actor_id'],'Only assigned assistant may update')
        wp.check_execution(root,w,event)
        need(event.get('expected_revision')==w['revision'],'Stale work revision')
        allowed={'work_status','next_action','evidence_refs','artifact_refs','unknowns','public_progress_summary','related_repositories','implementation_snapshots'}
        patch=event.get('patch',{});need(set(patch)<=allowed,'Cannot expand scope or modify approval')
        need(patch.get('work_status')!='done' or event.get('completion_verified') is True,'Completion evidence required')
        need(event.get('progress_source') and event.get('performed_by_actor_id'),'Actual performer/source required')
        if 'public_progress_summary' in patch: status_map.validate_public_summary(patch['public_progress_summary'])
        if 'related_repositories' in patch or 'implementation_snapshots' in patch:
            status_map.validate_implementation_patch(root,w,patch,event)
        w=copy.deepcopy(w);w.update(patch);w['revision']+=1;w['updated_at']=event['recorded_at']
        w.setdefault('progress_events',[]).append({k:event.get(k) for k in ('actor_id','performed_by_actor_id','progress_source','recorded_at')})
        files[path]=dump(w)
    elif operation=='mark_notifications':
        need(event.get('displayed') is True and event.get('presentation_ref'),'Fetch is not delivery; actual presentation required')
        need(event.get('delivered_at'),'Delivery timestamp required')
        for nid in event.get('notification_ids',[]):
            need(re.fullmatch(r'N-(?:D|ASG)-\d{8}-\d{3,}-ACT-\d{3,}',nid),'Invalid N-ID')
            np=f"records/notifications/{actor['actor_id']}/{nid}.json";n=load(root,np)
            need(n['recipient_actor_id']==actor['actor_id'],'Receipt ownership')
            rp=f"records/notification-receipts/{actor['actor_id']}/{nid}.json"
            receipt=load(root,rp) if safe(root,rp).exists() else dict(schema_version=1,notification_id=nid,recipient_actor_id=actor['actor_id'])
            receipt.setdefault('delivered_at',event['delivered_at']);receipt.setdefault('presentation_ref',event['presentation_ref'])
            if event.get('acknowledged'):
                need(event.get('ack_source'),'Human acknowledgement evidence required');receipt['acknowledged_at']=event['delivered_at'];receipt['ack_source']=event['ack_source']
            files[rp]=dump(receipt)
    else: raise ValueError('Unsupported operation')
    files.update(render(root,files,actors))
    if operation=='submit_request':
        p='records/REQUEST_INDEX.md';old=safe(root,p).read_text(encoding='utf-8') if safe(root,p).exists() else '# Request Index\n'
        files[p]=old+f"\n- {obj['request_id']} / {actor['actor_id']} / submitted r{revision(obj)} / {path}\n"
    expected={p:blob(safe(root,p).read_bytes()) if safe(root,p).exists() else None for p in files}
    return dict(status='planned',base_commit=event['base_commit'],files=files,expected_blobs=expected,
                follow_up='Commit all paths together after expected-blob checks; re-read and verify. No network writes were performed.')

def verify(root: Path, bundle: dict) -> None:
    for p,s in bundle['files'].items():need(safe(root,p).read_bytes()==s.encode(),f'Read-back mismatch: {p}')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['plan','verify']);parser.add_argument('root',type=Path);parser.add_argument('input',type=Path);a=parser.parse_args()
    try:
        data=json.loads(a.input.read_text(encoding='utf-8'))
        if a.action=='plan': print(dump(plan(a.root,data)),end='')
        else: verify(a.root,data);print('PASS: exact file read-back; not user acknowledgement or tool execution')
    except (ValueError,KeyError,OSError,TypeError) as exc:parser.exit(1,f'FAIL: {exc}\n')
