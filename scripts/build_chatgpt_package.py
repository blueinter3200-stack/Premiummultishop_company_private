#!/usr/bin/env python3
"""Build project upload packs from local canonical sources; never edits project settings."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def build(root, output, source_commit):
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise ValueError("An actually verified source commit is required")
    release = json.loads((root/"FILE_MAP.json").read_text())["release_id"]
    registry = json.loads((root/"llm-source/ACTOR_REGISTRY.json").read_text())
    folders = {"ACT-001":"01_ADMIN", "ACT-002":"02_REPRESENTATIVE", "ACT-003":"03_ASSISTANT"}
    labels = {"ACT-001":"ADMIN", "ACT-002":"REPRESENTATIVE", "ACT-003":"ASSISTANT"}
    files, entries, instructions = {}, [], []
    for actor in registry["actors"]:
        aid = actor["actor_id"]
        pairs = [("chatgpt/PROJECT_COMMON.md",f"{folders[aid]}/UPLOAD_SOURCES/PROJECT_COMMON.md"),
                 ("llm-source/ACTOR_REGISTRY.json",f"{folders[aid]}/UPLOAD_SOURCES/ACTOR_REGISTRY.json"),
                 (actor["role_source"],f"{folders[aid]}/UPLOAD_SOURCES/ROLE.md"),
                 (actor["project_instructions"],f"PROJECT_INSTRUCTIONS/{aid}_{labels[aid]}_INSTRUCTIONS.md")]
        if aid == "ACT-003":
            pairs.append(("llm-source/actors/ACT-003/RULES.md", f"{folders[aid]}/UPLOAD_SOURCES/RULES.md"))
        for source, dest in pairs:
            data=(root/source).read_bytes(); files[dest]=data
            entries.append({"package_path":dest,"github_path":source,"git_blob_sha":git_blob(data),
                            "sha256":hashlib.sha256(data).hexdigest()})
        instructions.append(f"# {actor['display_name']} ({aid}) 프로젝트 지침\n\n"+(root/actor["project_instructions"]).read_text())
    manifest={"release_id":release,"repository":"jintonic1010/miracle_company_private",
              "source_commit":source_commit,"files":entries,
              "note":"Byte snapshot; actual ChatGPT settings and live LLM execution are separate."}
    files["SOURCE_MANIFEST.json"]=(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n").encode()
    files["README_먼저읽기.md"]=(
        f"# {release} 설치 묶음\n\n자기 프로젝트의 UPLOAD_SOURCES 파일만 첨부하고 PROJECT_INSTRUCTIONS 본문은 지침 칸에 붙여넣는다.\n"
        "관리자 ROLE과 지침에 RC 변경추적이 추가되었다. 공통 PROJECT_COMMON과 대표님/부사수 ROLE·지침·RULES는 GOV-03 내용 그대로다.\n"
        "ACTOR_REGISTRY의 RC 식별자/경로 메타데이터만 갱신되며 대표님/부사수 권한과 의무는 늘지 않는다.\n"
        "실제 프로젝트 설정은 자동 교체되지 않는다. 원격 작업은 최신 main을 다시 확인한다.\n").encode()
    output.mkdir(parents=True,exist_ok=True)
    target=output/f"miracle_chatgpt_sources_{release}.zip"
    with zipfile.ZipFile(target,"w",zipfile.ZIP_DEFLATED) as archive:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,9,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16;archive.writestr(info,data)
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:raise ValueError("Invalid ZIP")
        for entry in entries:
            if archive.read(entry["package_path"]) != (root/entry["github_path"]).read_bytes():
                raise ValueError("Package/source mismatch")
    (output/f"miracle_project_instructions_{release}.md").write_text("\n\n---\n\n".join(instructions),encoding="utf-8")
    (output/f"{release}-package-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    checksum=hashlib.sha256(target.read_bytes()).hexdigest()
    (output/f"{target.name}.sha256").write_text(f"{checksum}  {target.name}\n")
    return {"zip":str(target),"sha256":checksum,"source_copies":len(entries),"source_commit":source_commit}


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--source-commit",required=True)
    a=p.parse_args()
    print(json.dumps(build(a.root,a.output,a.source_commit),ensure_ascii=False,indent=2))
