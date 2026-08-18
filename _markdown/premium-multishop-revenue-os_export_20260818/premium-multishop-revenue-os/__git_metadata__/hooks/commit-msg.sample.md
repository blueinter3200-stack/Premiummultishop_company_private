---
source_path: "premium-multishop-revenue-os_export_20260818/premium-multishop-revenue-os/.git/hooks/commit-msg.sample"
source_filename: "commit-msg.sample"
source_type: "text"
source_size_bytes: 896
source_modified_at: "2026-08-18T05:49:26+09:00"
source_sha256: "1f74d5e9292979b573ebd59741d46cb93ff391acdd083d340b94370753d92437"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/bin/sh
#
# An example hook script to check the commit log message.
# Called by "git commit" with one argument, the name of the file
# that has the commit message.  The hook should exit with non-zero
# status after issuing an appropriate message if it wants to stop the
# commit.  The hook is allowed to edit the commit message file.
#
# To enable this hook, rename this file to "commit-msg".

# Uncomment the below to add a Signed-off-by line to the message.
# Doing this in a hook is a bad idea in general, but the prepare-commit-msg
# hook is more suited to it.
#
# SOB=$(git var GIT_AUTHOR_IDENT | sed -n 's/^\(.*>\).*$/Signed-off-by: \1/p')
# grep -qs "^$SOB" "$1" || echo "$SOB" >> "$1"

# This example catches duplicate Signed-off-by lines.

test "" = "$(grep '^Signed-off-by: ' "$1" |
	 sort | uniq -c | sed -e '/^[ 	]*1[ 	]/d')" || {
	echo >&2 Duplicate Signed-off-by lines.
	exit 1
}
