#!/usr/bin/env python3
"""Rebuild a redacted company status projection at write time; read only it at query time.
No network, authentication, decisions or repository writes are performed by render().
Only explicit public_summary text is copied from requests/decisions/progress records.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
from typing import Any

MAP_PATH = 'working/WORK_STATUS_MAP.json'
SCHEMA = 1
SUMMARY_KEYS = {'title', 'latest_update', 'next_action', 'blocker_summary'}
REPO_KEYS = {'repository', 'branch', 'purpose'}
SNAPSHOT_KEYS = {'repository', 'branch', 'commit', 'checked_at', 'status', 'evidence_refs', 'deployment_status'}
SOURCE_GROUPS = (
    ('records/requests', 'R-*.json'), ('work/items', 'W-*.json'),
    ('records/submissions', 'SUB-*.json'), ('approvals', 'D-*.json'),
    ('work/assignments', 'ASG-*.json'),
)

def need(ok: Any, message: str) -> None:
    if not ok: raise ValueError(message)

def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(value: Any) -> str: return hashlib.sha256(canonical(value)).hexdigest()

def safe(root: Path, name: str) -> Path:
    path = (root / name).resolve(); need(not Path(name).is_absolute() and '..' not in Path(name).parts and path.is_relative_to(root.resolve()), 'Unsafe path'); return path

def collect(root: Path, overlay: dict[str, str] | None = None) -> dict[str, dict]:
    overlay = overlay or {}; result = {}
    for folder, pattern in SOURCE_GROUPS:
        for path in sorted((root / folder).rglob(pattern)):
            rel = path.relative_to(root).as_posix(); result[rel] = json.loads(overlay.get(rel, path.read_text(encoding='utf-8')))
        for rel, text in overlay.items():
            if rel.startswith(folder + '/') and Path(rel).match(pattern): safe(root, rel); result[rel] = json.loads(text)
    return result

def public_text(obj: dict) -> dict:
    value = obj.get('public_summary', {})
    if not isinstance(value, dict): return {}
    return {key: text for key, text in value.items() if key in SUMMARY_KEYS and isinstance(text, str) and len(text) <= 500}

def validate_summary(value: Any) -> None:
    need(isinstance(value, dict) and set(value) <= SUMMARY_KEYS, 'Only allowlisted public summary fields')
    for text in value.values(): need(isinstance(text, str) and len(text) <= 500, 'Public summary must be bounded text')

def allowed_repositories(root: Path) -> set[str]:
    file = root / 'llm-source/PROJECT_REPOSITORIES.md'
    if not file.is_file(): return set()
    return set(re.findall(r'`([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)`', file.read_text(encoding='utf-8')))

def validate_repositories(root: Path, links: Any) -> None:
    need(isinstance(links, list), 'Repository links must be a list'); seen=set()
    for link in links:
        need(isinstance(link, dict) and set(link) <= REPO_KEYS, 'Invalid repository link fields'); repo=link.get('repository')
        need(repo in allowed_repositories(root) and repo not in seen, 'Repository must be registered and unique'); seen.add(repo)
        need(isinstance(link.get('branch'), str) and bool(re.fullmatch(r'[A-Za-z0-9._/-]{1,200}', link['branch'])) and '..' not in link['branch'], 'Explicit safe target branch required')
        need(isinstance(link.get('purpose'), str), 'Repository purpose required')

def validate_snapshots(root: Path, snapshots: Any, links: list[dict]) -> None:
    need(isinstance(snapshots, list), 'Implementation snapshots must be a list'); allowed={(r['repository'],r['branch']) for r in links}; seen=set()
    for snap in snapshots:
        need(isinstance(snap, dict) and set(snap) <= SNAPSHOT_KEYS, 'Invalid snapshot fields'); key=snap.get('repository'),snap.get('branch')
        need(key in allowed and key not in seen, 'Snapshot outside registered work repositories'); seen.add(key)
        need(snap.get('status') in {'unverified','reported','verified','inaccessible'}, 'Snapshot status required')
        if snap['status']=='verified':
            need(re.fullmatch(r'[0-9a-f]{40}', str(snap.get('commit',''))), 'Verified commit must be a full SHA'); need(snap.get('checked_at') and snap.get('evidence_refs'), 'Verification time and evidence required')
        need(snap.get('deployment_status','unverified') in {'unverified','verified','failed','not_deployed'}, 'Invalid deployment state')
        need(snap.get('deployment_status')!='verified' or bool(snap.get('evidence_refs')), 'Deployment requires evidence separate from commit')
        for ref in snap.get('evidence_refs',[]):
            need(isinstance(ref,dict) and set(ref)<= {'path','commit','pr_number','run_id','check_name'}, 'Use structured evidence, not raw URLs or credentials'); need(bool(ref),'Empty implementation evidence')
            if 'path' in ref: need(not str(ref['path']).startswith('/') and '..' not in Path(ref['path']).parts, 'Unsafe evidence path')

def proposal(obj: dict) -> dict: return obj.get('current_requirements') or obj.get('proposal') or {key:obj.get(key) for key in ('original_text','scope','conditions','current_requirements')}
def revision(obj: dict) -> int: return obj.get('content_revision', obj.get('revision',1))

def current_decision(decisions: list[dict], kind: str, oid: str, rev: int, scopes: tuple[str,...]) -> dict | None:
    import decision_flow as flow
    for scope in scopes:
        chosen=flow.latest(decisions,(kind,oid,rev,scope))
        if chosen is not None:return chosen
    return None

def linked_decision(data: dict[str,dict], ref: str|None, decisions: list[dict]) -> dict|None:
    import decision_flow as flow
    item=data.get(ref or '')
    if item and item.get('target_type') and item.get('scope_key'): return flow.latest(decisions,flow.chain_key(item))
    return None

def max_date(items: list[dict]) -> str|None:
    values=[obj[key] for obj in items for key in ('updated_at','decided_at','assigned_at','submitted_at','captured_at','created_at') if isinstance(obj.get(key),str)]
    return max(values) if values else None

def build(root: Path, overlay: dict[str,str]|None=None) -> dict:
    data=collect(root,overlay); requests={p:o for p,o in data.items() if p.startswith('records/requests/')}; works={p:o for p,o in data.items() if p.startswith('work/items/')}; submissions={p:o for p,o in data.items() if p.startswith('records/submissions/')}; decisions=[o for p,o in data.items() if p.startswith('approvals/') and o.get('target_type') in {'request','submission'}]; rows=[]; linked_requests=set()
    def row_for(rp,req,wp,work):
        req,work=req or {},work or {}; rid,wid=req.get('request_id'),work.get('id'); chosen=current_decision(decisions,'request',rid,revision(req),('work_adoption','work_start')) if rid else None
        if chosen is None and work:
            candidate=linked_decision(data,work.get('adoption_decision_ref') or work.get('confirmation_decision_ref'),decisions); context=(candidate or {}).get('authorization_target',{})
            if candidate and context.get('request_id')==rid and context.get('content_revision')==revision(req) and context.get('content_hash')==digest(proposal(req)): chosen=candidate
        if chosen and chosen.get('target_type')=='request' and chosen.get('target_hash')!=digest(proposal(req)): chosen=None; work=dict(work,adoption_decision_ref=work.get('adoption_decision_ref') or 'needs_redecision')
        state=(chosen or {}).get('decision') or ('needs_redecision' if work.get('adoption_decision_ref') else ('legacy_unverified' if work else 'pending'))
        pool=[(p,s) for p,s in submissions.items() if (rp and s.get('request_ref')==rp) or (wid and s.get('work_id')==wid)]; latest_plans={}
        for p,s in pool:
            old=latest_plans.get(s['submission_id'])
            if not old or s['revision']>old[1]['revision']: latest_plans[s['submission_id']]=(p,s)
        plan_rows=[]
        for p,s in sorted(latest_plans.values()):
            d=current_decision(decisions,'submission',s['submission_id'],s['revision'],('plan_execution','work_start')); bound=(not req or (s.get('request_content_revision')==revision(req) and s.get('request_content_hash')==digest(proposal(req))))
            plan_rows.append({'plan_id':s['submission_id'],'revision':s['revision'],'status':(d or {}).get('decision','pending') if bound else 'needs_review','decision_id':(d or {}).get('decision_id')})
        summary=public_text(req)|public_text(work); title=summary.get('title') or (work.get('title') if work.get('visibility')!='restricted' else None) or '업무요청 (원문 비공개)'; work_state=work.get('work_status','not_created')
        stage=('completed' if work_state=='done' else 'cancelled' if work_state=='cancelled' else 'request_'+state if state in {'held','rejected','revision_required','pending','needs_redecision'} else 'in_progress' if work_state=='in_progress' else 'blocked' if work_state=='blocked' else 'execution_ready' if work.get('plan_status')=='approved' or work.get('execution_mode')=='self_direct' else 'plan_decision_pending' if plan_rows and any(p['status']=='pending' for p in plan_rows) else 'plan_required' if work.get('assigned_to_actor_id') else 'unassigned' if work else 'request_pending')
        row=dict(entry_id=wid or rid,request_id=rid,work_id=wid,title=title,requested_by_actor_id=req.get('requester_actor_id') or work.get('requested_by_actor_id'),assigned_to_actor_id=work.get('assigned_to_actor_id'),request_decision=state,decision_id=(chosen or {}).get('decision_id'),assignment_status='assigned' if work.get('assigned_to_actor_id') else 'unassigned',assignment_id=Path(work['current_assignment_ref']).stem if work.get('current_assignment_ref') else None,plans=plan_rows,effective_plan_ref=Path(work['execution_plan_ref']).name if work.get('execution_plan_ref') else None,effective_plan_status=work.get('plan_status','not_submitted'),work_status=work_state,current_stage=stage,latest_update=summary.get('latest_update'),next_action=summary.get('next_action'),blocker_summary=summary.get('blocker_summary'),information_as_of=work.get('information_as_of') or req.get('source_created_at'),updated_at=max_date([req,work]+[s for _,s in pool]+([chosen] if chosen else [])),related_repositories=[],implementation_snapshots=[])
        links=work.get('related_repositories',proposal(req).get('related_repositories',[]))
        if links: validate_repositories(root,links); row['related_repositories']=[{k:r[k] for k in REPO_KEYS if k in r} for r in links]
        snaps=work.get('implementation_snapshots',[])
        if snaps: validate_snapshots(root,snaps,links); row['implementation_snapshots']=[{k:s[k] for k in SNAPSHOT_KEYS if k in s} for s in snaps]
        row['recorded_state_only']=True; return row
    for path,work in sorted(works.items()):
        refs=[p for p in work.get('request_refs',[]) if p in requests]; adoption=data.get(work.get('adoption_decision_ref') or work.get('confirmation_decision_ref') or '',{}); rp=adoption.get('request_ref') if adoption.get('request_ref') in refs else (refs[0] if refs else None)
        if rp: linked_requests.add(rp)
        rows.append(row_for(rp,requests.get(rp),path,work))
    for rp,req in sorted(requests.items()):
        if rp in linked_requests:continue
        has_plan=any(s.get('request_ref')==rp for s in submissions.values())
        if req.get('submission_status')=='submitted' or has_plan: rows.append(row_for(rp,req,None,None))
    need(len({r['entry_id'] for r in rows})==len(rows),'Duplicate map entry ID')
    out=dict(schema_version=SCHEMA,authority='derived_company_status_not_authorization',audience='all_registered_company_roles',default_scope='company_all',freshness='recorded_snapshot_not_live_external_verification',records_latest_at=max_date(list(data.values())),source_fingerprint=digest(data),counts=dict(total=len(rows),by_stage=dict(sorted(collections.Counter(r['current_stage'] for r in rows).items()))),items=rows); out['map_revision']=digest(out); return out

def render(root:Path,overlay:dict[str,str]|None=None)->dict[str,str]:
    value=build(root,overlay); header={k:v for k,v in value.items() if k!='items'}; text=json.dumps(header,ensure_ascii=False,separators=(',',':'))[:-1]; text+=',"items":[\n'+',\n'.join(json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in value['items'])+'\n]}\n'; return {MAP_PATH:text}

def query(root:Path,actor_id:str,filter_text:str|None=None)->dict:
    need(bool(re.fullmatch(r'ACT-\d{3,}',actor_id)),'Registered actor context required'); value=json.loads((root/MAP_PATH).read_text(encoding='utf-8')); need(value.get('schema_version')==SCHEMA and value.get('audience')=='all_registered_company_roles','Unsupported status map'); expected=value.get('map_revision'); need(expected==digest({k:v for k,v in value.items() if k!='map_revision'}),'Status map integrity failure')
    if filter_text:
        term=filter_text.casefold(); value=dict(value,items=[r for r in value['items'] if term in canonical(r).decode().casefold()])
    return value

def finalize(root:Path,bundle:dict)->dict:
    result=dict(bundle,files=dict(bundle.get('files',{})),expected_blobs=dict(bundle.get('expected_blobs',{})))
    if not result['files']:return result
    if any(p.startswith(folder+'/') and Path(p).match(pattern) for p in result['files'] for folder,pattern in SOURCE_GROUPS):
        result['files'].update(render(root,result['files'])); target=root/MAP_PATH; result['expected_blobs'][MAP_PATH]=hashlib.sha1(b'blob '+str(target.stat().st_size).encode()+b'\0'+target.read_bytes()).hexdigest() if target.is_file() else None
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('action',choices=['build','check','query','finalize']); parser.add_argument('root',type=Path); parser.add_argument('--input',type=Path); parser.add_argument('--actor',default='ACT-001'); parser.add_argument('--filter'); args=parser.parse_args()
    try:
        if args.action=='query': print(json.dumps(query(args.root,args.actor,args.filter),ensure_ascii=False,indent=2))
        elif args.action=='finalize': need(args.input,'--input bundle required'); print(json.dumps(finalize(args.root,json.loads(args.input.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2))
        elif args.action=='check': need((args.root/MAP_PATH).read_text(encoding='utf-8')==render(args.root)[MAP_PATH],'Map is stale or incomplete'); print('PASS: projection equals canonical local sources')
        else: print(render(args.root)[MAP_PATH],end='')
    except (ValueError,KeyError,OSError,TypeError) as exc: parser.exit(1,f'FAIL: {exc}\n')
