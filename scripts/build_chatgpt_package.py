#!/usr/bin/env python3
"""Build role-separated upload sources from exact canonical bytes. No ChatGPT settings writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

def git_blob(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def build(root,output,source_commit):
    if not re.fullmatch(r'[0-9a-f]{40}',source_commit):raise ValueError('Verified source commit required')
    fm=json.loads((root/'FILE_MAP.json').read_text(encoding='utf-8'));reg=json.loads((root/'llm-source/ACTOR_REGISTRY.json').read_text(encoding='utf-8'))
    release=fm['release_id'];folders={'ACT-001':'01_ADMIN','ACT-002':'02_REPRESENTATIVE','ACT-003':'03_ASSISTANT'}
    labels={'admin':'ADMIN','representative':'REPRESENTATIVE','assistant':'ASSISTANT'}
    files={};entries=[];instructions=[]
    for actor in reg['actors']:
        if actor.get('status')!='active':continue
        aid=actor['actor_id'];folder=folders.get(aid,f"{aid}_{actor['role'].upper()}")
        pairs=[('chatgpt/PROJECT_COMMON.md',f'{folder}/UPLOAD_SOURCES/PROJECT_COMMON.md'),('llm-source/ACTOR_REGISTRY.json',f'{folder}/UPLOAD_SOURCES/ACTOR_REGISTRY.json'),(actor['role_source'],f'{folder}/UPLOAD_SOURCES/ROLE.md'),(actor['project_instructions'],f"PROJECT_INSTRUCTIONS/{aid}_{labels.get(actor['role'],actor['role'].upper())}_INSTRUCTIONS.md")]
        rules=str(Path(actor['role_source']).with_name('RULES.md'))
        if (root/rules).is_file():pairs.append((rules,f'{folder}/UPLOAD_SOURCES/RULES.md'))
        for source,dest in pairs:
            data=(root/source).read_bytes();files[dest]=data
            entries.append(dict(package_path=dest,github_path=source,git_blob_sha=git_blob(data),sha256=hashlib.sha256(data).hexdigest()))
        instructions.append(f"# {actor['display_name']} ({aid}) 프로젝트 지침\n\n"+(root/actor['project_instructions']).read_text(encoding='utf-8'))
    manifest=dict(release_id=release,repository=fm['repository'],source_commit=source_commit,files=entries,note='Exact bytes; GitHub sources are not automatically installed into ChatGPT projects.')
    files['SOURCE_MANIFEST.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
    files['README_먼저읽기.md']=(f'# {release} 설치 묶음\n\n확인한 소스 커밋: {source_commit}\n\n'
        '자기 폴더 UPLOAD_SOURCES의 파일만 소스에 올리고, PROJECT_INSTRUCTIONS의 자기 파일 본문은 지침 칸에 붙여넣는다. 지침 파일과 manifest는 소스에 중복 업로드하지 않는다. 다른 사람 ROLE은 섞지 않는다.\n\n'
        '이번 판은 16개 정식 명령, 검토→요청/품의→관리자 결정→업무 흐름과 선택적 결정 알림을 반영한다. 구명령 별칭은 없다. 세 방의 기존 운영 지침/소스를 교체하되 일반 업무자료는 삭제하지 않는다.\n\n'
        '일반 업무·데이터·세부 workflow·알림 조회 간격 변경은 GitHub에서 읽으므로 보통 프로젝트 교체가 필요 없다. 역할·명령·로컬 행동 또는 진입 경로 변경에는 관련 고정 소스를 교체한다.\n\n'
        '알림은 다음 관련 업무 행동에서 선택 조회한다. 실시간 푸시가 아니며 조회만으로 사용자 읽음으로 처리하지 않는다. 읽기 전용에서는 표시 영수증도 쓰지 않는다. 실제 프로젝트 설정과 실사용 테스트는 별도다.\n').encode()
    output.mkdir(parents=True,exist_ok=True);target=output/f'miracle_chatgpt_sources_{release}.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,9,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
    with zipfile.ZipFile(target) as z:
        if z.testzip():raise ValueError('ZIP integrity failure')
        for e in entries:
            if z.read(e['package_path'])!=(root/e['github_path']).read_bytes():raise ValueError('Source/package mismatch')
    combined=output/f'miracle_project_instructions_{release}.md';combined.write_text('\n\n---\n\n'.join(instructions),encoding='utf-8')
    (output/f'{release}-package-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    checksum=hashlib.sha256(target.read_bytes()).hexdigest();(output/f'{target.name}.sha256').write_text(checksum+'  '+target.name+'\n',encoding='utf-8')
    return dict(zip=str(target),instructions=str(combined),sha256=checksum,source_copies=len(entries),source_commit=source_commit)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args()
    print(json.dumps(build(a.root,a.output,a.source_commit),ensure_ascii=False,indent=2))
