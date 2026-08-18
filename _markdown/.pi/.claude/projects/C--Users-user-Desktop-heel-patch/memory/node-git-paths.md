---
source_path: ".pi/.claude/projects/C--Users-user-Desktop-heel-patch/memory/node-git-paths.md"
source_filename: "node-git-paths.md"
source_type: "text"
source_size_bytes: 696
source_modified_at: "2026-06-07T17:09:17+09:00"
source_sha256: "a2927fda7b7c576f0af076d3d5fc22e32508de661008e3d2a51ad5401aa25b9a"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
---
name: node-git-paths
description: "Node.js and Git are installed but not on the tool shell's default PATH"
metadata: 
  node_type: memory
  type: project
  originSessionId: d66b17ae-6839-4343-b82c-03b9b709f1bd
---

Node.js (v24.16.0) and Git (2.54.0) were installed via winget on 2026-06-07. They are NOT on the default PATH of the Bash/PowerShell tool shells, so commands like `node`, `npx`, `git` fail with "command not found" unless PATH is prepended first.

**How to apply:** Before running node/git commands in a tool shell, prepend:
`$env:Path = "C:\Program Files\nodejs;C:\Program Files\Git\cmd;" + $env:Path`

- node/npx: `C:\Program Files\nodejs\`
- git: `C:\Program Files\Git\cmd\`
