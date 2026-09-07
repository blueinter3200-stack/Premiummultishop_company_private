#!/usr/bin/env python3
"""Public company work-status projection and read-only query. No network or GitHub writes."""
from __future__ import annotations
import hashlib,json,re
from pathlib import Path

AUTH='derived_company_status_not_authorization'
PUBLIC_KEYS={'entry_id','request_id','work_id','title','requester_actor_id','assigned_to_actor_id','current_stage','request_decision_status','assignment_status','plan_status','work_status','latest_update','next_action','blockers','related_repositories','implementation_snapshots','updated_at','recorded_state_only','source_refs'}
SUMMARY_KEYS={'title','latest_update','next_action','blockers'}


def core():
 import decision_flow as c;return c

def canonical(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def digest(o):return hashlib.sha256(canonical(o)).hexdigest()

def validate_public_summary(s):
 c=core();c.need(isinstance(s,dict) and set(s)<=SUMMARY_KEYS,'Public summary allowlist only')
 for k,v in s.items():c.need(v is None or isinstance(v,(str,list)),'Invalid public summary')
 c.need(not any(x in json.dumps(s,ensure_ascii=False).lower() for x in ('password','token','private_notes','credential')),'Private data in public summary')

def registry_repos(root):
 text=(root/'llm-source/PROJECT_REPOSITORIES.md').read_text(encoding='utf-8');return set(re.findall(r'`([\w.-]+/[\w.-]+)` / ',text))
def validate_related_repositories(root,repos):
 c=core();known=registry_repos(root);c.need(isinstance(repos,list),'Repository list required')
 for r in repos:c.need(r.get('repository') in known and r.get('branch') and r.get('purpose'),'Only registered repository refs')
def validate_implementation_patch(root,w,patch,event):
 c=core();repos=patch.get('related_repositories',w.get('related_repositories',[]));validate_related_repositories(root,repos);allowed={x['repository'] for x in repos}
 for s in patch.get('implementation_snapshots',w.get('implementation_snapshots',[])):
  c.need(s.get('repository') in allowed and s.get('branch') and s.get('verified_at') and s.get('evidence_ref'),'Implementation evidence required')
  c.need(bool(s.get('commit_sha') or s.get('pr_ref') or s.get('ref')),'Commit/PR/ref required')
  c.need(s.get('verified_at')==event.get('external_verified_at'),'Do not invent/advance external verification time')

def group(root,overlay,folder,pattern):
 c=core();d=dict(c.records(root,folder,pattern))
 for p,s in overlay.items():
  if p.startswith(folder+'/') and Path(p).match(pattern):d[p]=json.loads(s)
 return list(d.items())

def public_title(req):
 s=req.get('public_summary');
 if isinstance(s,dict) and isinstance(s.get('title'),str) and s['title'].strip():return s['title'].strip()
 return '업무요청 (원문 비공개)'
def decision_status(ds,obj):
 c=core();kind,oid,rev=c.subject(obj);scope=obj.get('primary_scope','work_adoption')
 try:d=c.latest(ds,(kind,oid,rev,scope))
 except Exception:return 'conflict'
 return (d or {}).get('decision','pending')
def stage(req_status,w):
 if not w:return {'pending':'approval_pending','held':'held','revision_required':'revision_required','rejected':'rejected','approved':'adopted','conflict':'conflict'}.get(req_status,'approval_pending')
 if w.get('work_status') in {'done','cancelled'}:return 'completed' if w['work_status']=='done' else 'cancelled'
 if w.get('work_status')=='blocked':return 'blocked'
 ps=w.get('plan_status')
 if ps in {'submitted','pending'}:return 'plan_pending'
 if ps in {'revision_required','held','rejected'}:return ps
 if ps=='approved' and w.get('work_status')=='in_progress':return 'in_progress'
 if ps=='approved':return 'adopted'
 if w.get('assigned_to_actor_id'):return 'planning'
 return 'adopted'
def item_for(req_path,req,w,req_status):
 s=req.get('public_summary') or {};out={'entry_id':(w or {}).get('id') or req['request_id'],'request_id':req['request_id'],'work_id':(w or {}).get('id'),'title':public_title(req),'requester_actor_id':req.get('requester_actor_id'),'assigned_to_actor_id':(w or {}).get('assigned_to_actor_id'),'current_stage':stage(req_status,w),'request_decision_status':req_status,'assignment_status':'assigned' if (w or {}).get('assigned_to_actor_id') else 'unassigned','plan_status':(w or {}).get('plan_status'),'work_status':(w or {}).get('work_status'),'latest_update':((w or {}).get('public_progress_summary') or {}).get('latest_update',s.get('latest_update')),'next_action':((w or {}).get('public_progress_summary') or {}).get('next_action',(w or {}).get('next_action',s.get('next_action'))),'blockers':((w or {}).get('public_progress_summary') or {}).get('blockers',s.get('blockers')),'related_repositories':(w or {}).get('related_repositories',[]),'implementation_snapshots':(w or {}).get('implementation_snapshots',[]),'updated_at':(w or {}).get('updated_at',req.get('captured_at')),'source_refs':[req_path]+(([f"work/items/{w['id']}.json"] if w else []))}
 return {k:v for k,v in out.items() if k in PUBLIC_KEYS and v is not None}
def legacy_items(root,overlay,seen):
 # Older W without a stable request link remain visible without fabricating missing states.
 items=[]
 for p,w in group(root,overlay,'work/items','W-*.json'):
  if w['id'] in seen:continue
  items.append({'entry_id':w['id'],'work_id':w['id'],'title':w.get('title') or '기존 업무','assigned_to_actor_id':w.get('assigned_to_actor_id'),'current_stage':'legacy_recheck','work_status':w.get('work_status','recorded_legacy'),'next_action':w.get('next_action'),'updated_at':w.get('information_as_of') or w.get('updated_at'),'recorded_state_only':True,'related_repositories':w.get('related_repositories',[]),'implementation_snapshots':w.get('implementation_snapshots',[]),'source_refs':[p]})
 return items
def project_status(root,overlay):
 c=core();ds=[d for _,d in group(root,overlay,'approvals','D-*.json') if d.get('target_type')];works=group(root,overlay,'work/items','W-*.json');requests=group(root,overlay,'records/requests','R-*.json');items=[];seen=set()
 for rp,r in requests:
  if r.get('submission_status') not in {'submitted','captured'}:continue
  matched=[w for _,w in works if rp in w.get('request_refs',[])];c.need(len(matched)<=1,'Duplicate W for request');w=matched[0] if matched else None
  if w:seen.add(w['id'])
  items.append(item_for(rp,r,w,decision_status(ds,r)))
 items.extend(legacy_items(root,overlay,seen));items.sort(key=lambda x:(str(x.get('updated_at','')),x['entry_id']),reverse=True)
 counts={}
 for x in items:counts[x['current_stage']]=counts.get(x['current_stage'],0)+1
 sources=[]
 for x in items:sources.extend(x.get('source_refs',[]))
 sources=sorted(set(sources));source_hashes={p:hashlib.sha256((overlay.get(p) or c.safe(root,p).read_text(encoding='utf-8')).encode()).hexdigest() for p in sources if p in overlay or c.safe(root,p).exists()}
 body={'schema_version':1,'authority':AUTH,'audience':'all_registered_company_roles','default_scope':'company_all','freshness':'recorded_snapshot_not_live_external_verification','records_latest_at':max([str(x.get('updated_at','')) for x in items] or ['']),'counts':{'total':len(items),'by_stage':counts},'items':items,'source_refs':sources,'source_hashes':source_hashes}
 body['map_checksum']=digest(body);return json.dumps(body,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
def load_verified_map(root):
 p=root/'working/WORK_STATUS_MAP.json';c=core();c.need(p.exists(),'WORK_STATUS_MAP missing');m=json.loads(p.read_text(encoding='utf-8'));c.need(m.get('schema_version')==1 and m.get('authority')==AUTH and m.get('audience')=='all_registered_company_roles','Unsupported status map')
 check=copy_no_checksum={k:v for k,v in m.items() if k!='map_checksum'};c.need(m.get('map_checksum')==digest(copy_no_checksum),'Status map checksum mismatch')
 return m
def query_bundle(root,event):
 c=core();c.need(event.get('command')=='/업무진행현황','Wrong map query');c.need(event.get('actor_id') in {'ACT-001','ACT-002','ACT-003'},'Registered company roles only');c.need(not event.get('write_requested') and not event.get('mark_notifications'),'Read-only map query')
 m=load_verified_map(root);flt=str(event.get('filter','')).strip().lower();items=m['items']
 if flt:
  def hit(x):return flt in json.dumps({k:x.get(k) for k in ('entry_id','request_id','work_id','title','assigned_to_actor_id','current_stage','work_status','related_repositories')},ensure_ascii=False).lower()
  items=[x for x in items if hit(x)]
 return {'status':'read_only','base_commit':event.get('base_commit'),'map_ref':'working/WORK_STATUS_MAP.json','records_latest_at':m['records_latest_at'],'counts':m['counts'],'items':items,'files':{},'expected_blobs':{}}
