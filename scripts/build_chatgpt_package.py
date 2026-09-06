#!/usr/bin/env python3
"""Package exact canonical sources per actor; no ChatGPT settings or network writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def build(root, output, source_commit):
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('Verified source commit required')
    fm=json.loads((root/'FILE_MAP.json').read_text(encoding='utf-8'))
    reg=json.loads((root/'llm-source/ACTOR_REGISTRY.json').read_text(encoding='utf-8'))
    release=fm['release_id']; files={}; entries=[]; instructions=[]
    folders={'ACT-001':'01_ADMIN','ACT-002':'02_REPRESENTATIVE','ACT-003':'03_ASSISTANT'}
    for actor in reg['actors']:
        if actor.get('status')!='active': continue
        aid=actor['actor_id']; folder=folders.get(aid,f"{aid}_{actor['role'].upper()}")
        pairs=[('chatgpt/PROJECT_COMMON.md',f'{folder}/UPLOAD_SOURCES/PROJECT_COMMON.md'),
               ('llm-source/ACTOR_REGISTRY.json',f'{folder}/UPLOAD_SOURCES/ACTOR_REGISTRY.json'),
               (actor['role_source'],f'{folder}/UPLOAD_SOURCES/ROLE.md'),
               (actor['project_instructions'],f"PROJECT_INSTRUCTIONS/{aid}_{actor['role'].upper()}_INSTRUCTIONS.md")]
        rules=str(Path(actor['role_source']).with_name('RULES.md'))
        if (root/rules).is_file(): pairs.append((rules,f'{folder}/UPLOAD_SOURCES/RULES.md'))
        for source,dest in pairs:
            data=(root/source).read_bytes(); files[dest]=data
            entries.append(dict(package_path=dest,github_path=source,git_blob_sha=git_blob(data),sha256=hashlib.sha256(data).hexdigest()))
        instructions.append(f"# {actor['display_name']} ({aid}) 프로젝트 지침\n\n"+(root/actor['project_instructions']).read_text(encoding='utf-8'))
    manifest=dict(release_id=release,repository=fm['repository'],source_commit=source_commit,files=entries,
                  note='Exact byte snapshot. Project installation, live behavior and push delivery are not performed by this builder.')
    files['SOURCE_MANIFEST.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    files['README_먼저읽기.md']=(f'# {release} 설치 묶음\n\n소스 커밋: {source_commit}\n\n'
        '자기 폴더 UPLOAD_SOURCES 안 파일만 해당 프로젝트 소스에 올린다. PROJECT_INSTRUCTIONS의 자기 파일 본문은 지침 칸에 붙여넣는다. 지침 파일·manifest는 소스에 중복 첨부하지 않는다. 다른 actor ROLE을 섞지 않는다.\n\n'
        '업무계획안제출·업무계획안결의, 관리자 업무 채택/배정, 대표님 구두 요청의 계획안 직접 제출, 배정별 최초 알림과 지속 작업지시 목록을 반영했다. 기존 품의서 명령을 별칭으로 실행하지 않는다.\n\n'
        '세 프로젝트 운영 지침·소스를 이번 판으로 교체한다. 일반 업무자료를 지우라는 뜻은 아니다. 세부 workflow·업무 데이터·조회 주기는 GitHub 최신 main에서 읽으므로 통상 로컬 교체가 필요 없다. 역할·명령·로컬 행동·진입 경로 변경은 교체가 필요하다.\n\n'
        '알림은 다음 관련 업무 행동에서 조회한다. 실제 표시 뒤 허용된 쓰기에서만 전달 영수증을 저장하며 읽기 전용/저장 금지는 예외다. 영속 영수증 없이 전역 정확히 한 번 표시를 보장하지 않는다. 전달 후에도 미완료 작업지시는 목록에 남는다. 실제 프로젝트 설정·실시간 푸시·계정 ACL 설치는 별도다.\n').encode()
    output.mkdir(parents=True,exist_ok=True); target=output/f'miracle_chatgpt_sources_{release}.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,9,7,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; info.external_attr=0o100644<<16
            z.writestr(info,data)
    with zipfile.ZipFile(target) as z:
        if z.testzip(): raise ValueError('ZIP integrity failed')
        for e in entries:
            if z.read(e['package_path'])!=(root/e['github_path']).read_bytes(): raise ValueError('Source/package mismatch')
    combined=output/f'miracle_project_instructions_{release}.md'
    combined.write_text('\n\n---\n\n'.join(instructions),encoding='utf-8')
    (output/f'{release}-package-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    checksum=hashlib.sha256(target.read_bytes()).hexdigest()
    (output/f'{target.name}.sha256').write_text(checksum+'  '+target.name+'\n',encoding='utf-8')
    return dict(zip=str(target),instructions=str(combined),sha256=checksum,source_copies=len(entries),source_commit=source_commit)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]); p.add_argument('--output',type=Path,required=True)
    p.add_argument('--source-commit',required=True); a=p.parse_args()
    print(json.dumps(build(a.root,a.output,a.source_commit),ensure_ascii=False,indent=2))
