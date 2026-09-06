#!/usr/bin/env python3
"""Validate active command/source routing. --staged-only skips unchanged RC code checks."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

def validate(root: Path, staged_only: bool=False) -> dict:
    def load(p):return json.loads((root/p).read_text(encoding='utf-8'))
    reg=load('llm-source/ACTOR_REGISTRY.json');actors=reg['actors'];tr=load('llm-source/TRIGGER_REGISTRY.json');fm=load('FILE_MAP.json')
    common=(root/'chatgpt/PROJECT_COMMON.md').read_text(encoding='utf-8')
    need=lambda ok,msg: None if ok else (_ for _ in ()).throw(ValueError(msg))
    ids=[a['actor_id'] for a in actors];need(len(ids)==len(set(ids)),'Duplicate actor')
    need({'ACT-001','ACT-002','ACT-003'}<=set(ids),'Required actors missing')
    commands=tr['commands'];names=[c['name'] for c in commands]
    need(len(names)==len(set(names))==16,'Expected 16 canonical commands')
    need(tr.get('aliases')=={},'Aliases must be absent')
    retired=set(load('llm-source/RETIRED_COMMANDS.json')['commands']);need(not retired.intersection(names),'Retired command is active')
    admin_only={'/업무결정','/품의서결정','/업무점검','/결과승인','/기준확정','/아이디어반영','/문제반영'}
    counts={}
    active=[root/'chatgpt/PROJECT_COMMON.md',root/'llm-source/LLM_RUNTIME.md',root/'llm-source/PRODUCT_REQUIREMENTS.md']
    for a in actors:
        need(fm['role_sources'][a['actor_id']]==a['role_source'],'Role route mismatch')
        for path in [a['role_source'],a['project_instructions']]:
            text=(root/path).read_text(encoding='utf-8');need(a['actor_id'] in text,'Actor identity missing');active.append(root/path)
        allowed=[c for c in commands if a['role'] in c['roles']];counts[a['actor_id']]=len(allowed)
        for c in allowed:
            need(c['name'] in (root/a['role_source']).read_text(encoding='utf-8') and c['name'] in (root/a['project_instructions']).read_text(encoding='utf-8'),'Local command discovery missing')
    for c in commands:
        need(c['name'] in common and c.get('recommend_when'),'Recommendation missing')
        need((root/c['workflow']).is_file() and fm['workflow_routes'][c['name']]==c['workflow'],'Workflow route broken')
        active.append(root/c['workflow'])
        if c['name'] in admin_only:need(c['roles']==['admin'],'Administrator boundary broken')
        if c['name'] in {'/품의서작성','/업무업데이트'}:need(c['roles']==['admin','assistant'],'Staff boundary broken')
        if c['name'] in {'/업무결정','/품의서결정'}:need(c.get('default_outcome') is None and len(c['required_outcomes'])==4,'Decision default or outcomes invalid')
    for p in set(active):need(not any(n in p.read_text(encoding='utf-8') for n in retired),f'Retired active command reference: {p}')
    for p in root.rglob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    need(fm['approval_actor_id']=='ACT-001','Wrong final approver')
    need('request_change_refs' in load('templates/REQUEST.json') and 'request_change_refs' in load('templates/WORK.json'),'RC compatibility missing')
    need(load('templates/REQUEST.json')['source_created_at'] is None,'Invented original timestamp')
    manifest=root/f"docs/releases/{fm['release_id']}-manifest.json"
    if manifest.is_file():
        for e in json.loads(manifest.read_text(encoding='utf-8'))['files']:
            need(hashlib.sha256((root/e['path']).read_bytes()).hexdigest()==e['sha256'],f"Manifest mismatch: {e['path']}")
    legacy='skipped (unchanged files not in staged snapshot)'
    if not staged_only:
        from request_changes import validate_repository
        validate_repository(root);legacy='passed'
    return dict(status='PASS',commands=len(names),aliases=0,actor_command_counts=counts,legacy_rc=legacy,live_project_behavior='not tested')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--staged-only',action='store_true');a=p.parse_args()
    try: print(json.dumps(validate(a.root,a.staged_only),ensure_ascii=False,indent=2))
    except (ValueError,KeyError,OSError,ImportError) as exc:p.exit(1,f'FAIL: {exc}\n')
