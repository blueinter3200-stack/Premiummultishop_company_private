---
source_path: "premium-multishop-revenue-os_export_20260818/premium-multishop-revenue-os/.git/hooks/applypatch-msg.sample"
source_filename: "applypatch-msg.sample"
source_type: "text"
source_size_bytes: 478
source_modified_at: "2026-08-18T05:49:26+09:00"
source_sha256: "0223497a0b8b033aa58a3a521b8629869386cf7ab0e2f101963d328aa62193f7"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/bin/sh
#
# An example hook script to check the commit log message taken by
# applypatch from an e-mail message.
#
# The hook should exit with non-zero status after issuing an
# appropriate message if it wants to stop the commit.  The hook is
# allowed to edit the commit message file.
#
# To enable this hook, rename this file to "applypatch-msg".

. git-sh-setup
commitmsg="$(git rev-parse --git-path hooks/commit-msg)"
test -x "$commitmsg" && exec "$commitmsg" ${1+"$@"}
:
