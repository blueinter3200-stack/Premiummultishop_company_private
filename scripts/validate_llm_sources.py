#!/usr/bin/env python3
"""Validate active GOV-20260907-02 sources without executing remote actions."""
import argparse, hashlib, json
from pathlib import Path


def validate(root, staged_only=False):
    def load(p):return json.loads((root/p).read_text(encoding='utf-8'))
    def need(ok,msg):
        if not ok:raise ValueError(msg)
    reg=load('llm-source/ACTOR_REGISTRY.json');fm=load('FILE_MAP.json');tr=load('llm-source/TRIGGER_REGISTRY.json');names=[c['name'] for c in tr['commands']]
    need(len(names)==len(set(names))==17,'17 canonical commands required');need(tr['aliases']=={},'Aliases forbidden')
    retired=set(load('llm-source/RETIRED_COMMANDS.json')['commands']);need(not retired.intersection(names),'Retired command active')
    common=(root/'chatgpt/PROJECT_COMMON.md').read_text(encoding='utf-8');counts={};active={root/'chatgpt/PROJECT_COMMON.md',root/'llm-source/LLM_RUNTIME.md',root/'llm-source/PRODUCT_REQUIREMENTS.md'}
    actors=reg['actors'];need({'ACT-001','ACT-002','ACT-003'}<={a['actor_id'] for a in actors},'Missing actor')
    for a in actors:
        texts=[]
        for p in (a['role_source'],a['project_instructions']):
            text=(root/p).read_text(encoding='utf-8');need(a['actor_id'] in text,'Identity missing');texts.append(text);active.add(root/p)
        allowed=[c for c in tr['commands'] if a['role'] in c['roles']];counts[a['actor_id']]=len(allowed)
        for c in allowed:need(all(c['name'] in t for t in texts),'Local command missing')
    need(counts=={'ACT-001':17,'ACT-002':8,'ACT-003':10},f'Unexpected actor command counts {counts}')
    for c in tr['commands']:
        need(c['name'] in common and c.get('recommend_when'),'Recommendation missing');need(fm['workflow_routes'][c['name']]==c['workflow'],'Workflow route mismatch')
        need((root/c['workflow']).is_file(),'Missing workflow');active.add(root/c['workflow'])
        if c['name'] in {'/업무결정','/업무계획안결의','/업무점검','/결과승인','/기준확정','/아이디어반영','/문제반영'}:need(c['roles']==['admin'],'Admin boundary')
        if c['name'] in {'/업무계획안제출','/업무업데이트'}:need(c['roles']==['admin','assistant'],'Staff boundary')
        if c['name']=='/업무진행현황':need(c['roles']==['admin','representative','assistant'] and c['mode']=='read_map','Status command boundary')
    for p in active:need(not any(r in p.read_text(encoding='utf-8') for r in retired),f'Retired command in active source: {p}')
    need(fm['work_status_map']=='working/WORK_STATUS_MAP.json' and fm['direct_request_workflow']=='llm-source/workflows/DIRECT_REQUEST_WORKFLOW.md','New routes missing')
    need((root/fm['work_status_map']).is_file(),'Status map missing')
    from work_status import load_verified_map
    m=load_verified_map(root);need(m['audience']=='all_registered_company_roles','Wrong map audience')
    need('public_summary' in load('templates/REQUEST.json') and 'related_repositories' in load('templates/WORK.json'),'Template extensions missing')
    manifest=root/f"docs/releases/{fm['release_id']}-manifest.json";need(manifest.is_file(),'Release manifest missing')
    for e in json.loads(manifest.read_text(encoding='utf-8'))['files']:
        need(hashlib.sha256((root/e['path']).read_bytes()).hexdigest()==e['sha256'],f"Manifest mismatch {e['path']}")
    return dict(status='PASS',commands=17,aliases=0,actor_command_counts=counts,status_map_items=len(m['items']),live_project_behavior='not tested')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--staged-only',action='store_true');a=p.parse_args()
    try:print(json.dumps(validate(a.root,a.staged_only),ensure_ascii=False,indent=2))
    except Exception as exc:p.exit(1,f'FAIL: {exc}\n')
