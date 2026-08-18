---
source_path: "premium-multishop-revenue-os_export_20260818/premium-multishop-revenue-os/.git/hooks/pre-merge-commit.sample"
source_filename: "pre-merge-commit.sample"
source_type: "text"
source_size_bytes: 416
source_modified_at: "2026-08-18T05:49:26+09:00"
source_sha256: "d3825a70337940ebbd0a5c072984e13245920cdf8898bd225c8d27a6dfc9cb53"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git merge" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message to
# stderr if it wants to stop the merge commit.
#
# To enable this hook, rename this file to "pre-merge-commit".

. git-sh-setup
test -x "$GIT_DIR/hooks/pre-commit" &&
        exec "$GIT_DIR/hooks/pre-commit"
:
