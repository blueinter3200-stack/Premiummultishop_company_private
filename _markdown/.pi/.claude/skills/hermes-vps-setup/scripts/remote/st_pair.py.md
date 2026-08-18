---
source_path: ".pi/.claude/skills/hermes-vps-setup/scripts/remote/st_pair.py"
source_filename: "st_pair.py"
source_type: "text"
source_size_bytes: 2596
source_modified_at: "2026-08-12T14:19:57+09:00"
source_sha256: "46c1cbb64d9b6283f7311414f15bad456e84d3dfe3aa26cde2ca63abd42036a9"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/usr/bin/env python3
"""서버 Syncthing에 로컬 기기 등록 + wiki 폴더 공유. 컨테이너 안(uid 10000)에서 실행.

사용: docker exec -u 10000 <컨테이너> python3 /opt/data/tmp/st_pair.py <LOCAL_DEVICE_ID> [기기이름]
출력 마지막 줄: SERVER_ID=<서버 기기 ID>  (로컬 쪽 페어링에 사용)
"""
import json
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

HOME = "/opt/data/.config/syncthing"
local_id = sys.argv[1].strip()
name = sys.argv[2] if len(sys.argv) > 2 else "my-computer"

root = ET.parse(HOME + "/config.xml").getroot()
apikey = root.find("gui/apikey").text
addr = (root.findtext("gui/address") or "127.0.0.1:8384").strip()
base = "http://" + addr


def req(method, path, body=None):
    r = urllib.request.Request(
        base + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"X-API-Key": apikey, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(r, timeout=10) as resp:
        d = resp.read()
        return json.loads(d) if d else None


# Syncthing이 워치독으로 막 기동된 직후일 수 있음 — 최대 30초 대기
my_id = None
for attempt in range(6):
    try:
        my_id = req("GET", "/rest/system/status")["myID"]
        break
    except Exception:
        if attempt == 5:
            print("서버 Syncthing이 응답하지 않습니다 — 03단계 완료 후 잠시 뒤 재시도하세요.", file=sys.stderr)
            raise
        time.sleep(5)

devices = req("GET", "/rest/config/devices")
if not any(d["deviceID"] == local_id for d in devices):
    req("POST", "/rest/config/devices", {"deviceID": local_id, "name": name})
    print(f"기기 등록: {name} ({local_id[:7]}…)")
else:
    print("기기 이미 등록됨")

folders = req("GET", "/rest/config/folders")
folder = next((f for f in folders if f["id"] == "wiki"), None)
if folder is None:
    req("POST", "/rest/config/folders", {
        "id": "wiki",
        "label": "hermes-wiki",
        "path": "/opt/data/wiki",
        "type": "sendreceive",
        "devices": [{"deviceID": my_id}, {"deviceID": local_id}],
        "rescanIntervalS": 60,
        "fsWatcherEnabled": True,
    })
    print("wiki 폴더 공유 생성")
elif not any(d["deviceID"] == local_id for d in folder["devices"]):
    folder["devices"].append({"deviceID": local_id})
    req("PUT", "/rest/config/folders/wiki", folder)
    print("wiki 폴더에 기기 추가")
else:
    print("wiki 폴더 공유 이미 설정됨")

print("SERVER_ID=" + my_id)
