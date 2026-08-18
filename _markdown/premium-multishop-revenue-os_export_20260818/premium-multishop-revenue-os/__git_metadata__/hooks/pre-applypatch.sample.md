---
source_path: "premium-multishop-revenue-os_export_20260818/premium-multishop-revenue-os/.git/hooks/pre-applypatch.sample"
source_filename: "pre-applypatch.sample"
source_type: "text"
source_size_bytes: 424
source_modified_at: "2026-08-18T05:49:26+09:00"
source_sha256: "e15c5b469ea3e0a695bea6f2c82bcf8e62821074939ddd85b77e0007ff165475"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/bin/sh
#
# An example hook script to verify what is about to be committed
# by applypatch from an e-mail message.
#
# The hook should exit with non-zero status after issuing an
# appropriate message if it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-applypatch".

. git-sh-setup
precommit="$(git rev-parse --git-path hooks/pre-commit)"
test -x "$precommit" && exec "$precommit" ${1+"$@"}
:
