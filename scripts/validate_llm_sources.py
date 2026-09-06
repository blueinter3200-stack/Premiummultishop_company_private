#!/usr/bin/env python3
"""Validate active sources and changed manifests, without executing any trigger."""
import argparse
import hashlib
import json
from pathlib import Path


def validate(root, staged_only=False):
    def load(path): return json.loads((root/path).read_text(encoding='utf-8'))
    def need(ok, message):
        if not ok: raise ValueError(message)
    reg=load('llm-source/ACTOR_REGISTRY.json'); fm=load('FILE_MAP.json'); tr=load('llm-source/TRIGGER_REGISTRY.json')
    names=[c['name'] for c in tr['commands']]; actors=reg['actors']
    need(len(names)==len(set(names))==16,'16 distinct commands required')
    need(tr['aliases']=={},'No aliases permitted')
    retired=set(load('llm-source/RETIRED_COMMANDS.json')['commands']); need(not retired.intersection(names),'Retired command active')
    common=(root/'chatgpt/PROJECT_COMMON.md').read_text(encoding='utf-8')
    counts={}; active={root/'chatgpt/PROJECT_COMMON.md',root/'llm-source/LLM_RUNTIME.md',root/'llm-source/PRODUCT_REQUIREMENTS.md'}
    need(len({a['actor_id'] for a in actors})==len(actors),'Duplicate actor')
    need({'ACT-001','ACT-002','ACT-003'}<={a['actor_id'] for a in actors},'Missing actor')
    for a in actors:
        need(fm['role_sources'][a['actor_id']]==a['role_source'],'Role route mismatch')
        texts=[]
        for path in (a['role_source'],a['project_instructions']):
            p=root/path; active.add(p); text=p.read_text(encoding='utf-8'); need(a['actor_id'] in text,'Identity missing'); texts.append(text)
        allowed=[c for c in tr['commands'] if a['role'] in c['roles']]; counts[a['actor_id']]=len(allowed)
        for c in allowed: need(all(c['name'] in s for s in texts),'Local discovery missing')
    expected={'ACT-001':16,'ACT-002':7,'ACT-003':9}
    need(all(counts[k]==v for k,v in expected.items()),'Role command counts changed')
    for c in tr['commands']:
        need(c['name'] in common and c.get('recommend_when'),'Recommendation missing')
        need(fm['workflow_routes'][c['name']]==c['workflow'],'Workflow route mismatch')
        p=root/c['workflow']
        if not p.is_file():
            need(staged_only and c['workflow'] in {'llm-source/workflows/IDEA_WORKFLOW.md','llm-source/workflows/PROBLEM_WORKFLOW.md'},'Missing workflow')
        else: active.add(p)
        if c['name'] in {'/업무결정','/업무계획안결의','/업무점검','/결과승인','/기준확정','/아이디어반영','/문제반영'}: need(c['roles']==['admin'],'Admin boundary')
        if c['name'] in {'/업무계획안제출','/업무업데이트'}: need(c['roles']==['admin','assistant'],'Staff boundary')
        if c['name'] in {'/업무결정','/업무계획안결의'}: need(c.get('default_outcome') is None and len(c['required_outcomes'])==4,'Decision outcomes/default')
    for p in active: need(not any(n in p.read_text(encoding='utf-8') for n in retired),f'Retired command in active source: {p}')
    for p in root.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))
    need(fm['approval_actor_id']=='ACT-001','Wrong approver')
    for p in ('templates/REQUEST.json','templates/WORK.json'): need('request_change_refs' in load(p),'RC compatibility lost')
    need(load('templates/REQUEST.json')['source_created_at'] is None,'Invented source date')
    need(load('templates/SUBMISSION.json')['primary_scope']=='plan_execution','Wrong plan scope')
    need((root/fm['assignment_workflow']).is_file(),'Assignment route missing')
    manifest=root/f"docs/releases/{fm['release_id']}-manifest.json"
    need(manifest.is_file(),'Manifest required')
    for e in json.loads(manifest.read_text(encoding='utf-8'))['files']:
        need(hashlib.sha256((root/e['path']).read_bytes()).hexdigest()==e['sha256'],f"Manifest mismatch: {e['path']}")
    rc='not rerun; unchanged RC implementation and histories preserved'
    if not staged_only:
        from request_changes import validate_repository
        validate_repository(root); rc='passed'
    return dict(status='PASS',commands=16,aliases=0,actor_command_counts=counts,legacy_rc=rc,
                workflow_check='changed workflows local; unchanged I/P routes verified remotely' if staged_only else 'all local',live_project_behavior='not tested')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--staged-only',action='store_true');a=p.parse_args()
    try: print(json.dumps(validate(a.root,a.staged_only),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,ImportError) as exc: p.exit(1,f'FAIL: {exc}\n')
