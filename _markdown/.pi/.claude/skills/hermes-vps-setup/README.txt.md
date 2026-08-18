---
source_path: ".pi/.claude/skills/hermes-vps-setup/README.txt"
source_filename: "README.txt"
source_type: "text"
source_size_bytes: 1389
source_modified_at: "2026-08-12T14:19:56+09:00"
source_sha256: "953f2992b6b8b42c94ff99427ab6f04cb3c2f924055171bee0e5e179cd4e0a15"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
Hermes VPS 셋업 스킬
====================

Hostinger VPS의 Hermes 에이전트를 자동으로 셋업합니다.
(SSH 연결 → 음성인식/외부앱연동/이미지생성 설정 → 세컨브레인 위키
 → 내 컴퓨터의 Obsidian과 양방향 동기화)

준비물
------
- Hostinger VPS에 앱 카탈로그로 Hermes agent가 설치·실행 중일 것
- 내 컴퓨터(맥 또는 윈도우)에 Claude Code가 설치돼 있을 것

사용법 (3단계)
--------------
1. 이 폴더를 통째로 아래 위치에 두세요.

   맥:      ~/.claude/skills/hermes-vps-setup
   윈도우:  C:\Users\<내이름>\.claude\skills\hermes-vps-setup

2. setup.env.example 파일을 같은 자리에 setup.env 라는 이름으로 복사하고,
   메모장/텍스트편집기로 열어 값을 채우세요.
   - VPS_IP 는 필수. API 키들은 선택(나중에 채워도 됨).
   - ⚠️ API 키는 Claude 채팅창에 절대 붙여넣지 마세요. 이 파일에만 적으세요.
     (전송이 끝나면 파일에서 자동으로 지워집니다)

3. Claude Code를 열고 이렇게 말하세요:

   "헤르메스 셋업해줘"

이후는 Claude가 순서대로 진행하며, 사람 손이 필요한 순간
(Hostinger 패널에 공개키 등록, 컨테이너 재시작 동의)에만 요청합니다.
중간에 실패해도 같은 말로 다시 시작하면 이어서 진행됩니다.
