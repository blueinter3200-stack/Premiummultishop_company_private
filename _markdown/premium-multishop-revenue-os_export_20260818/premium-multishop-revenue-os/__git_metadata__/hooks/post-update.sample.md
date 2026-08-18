---
source_path: "premium-multishop-revenue-os_export_20260818/premium-multishop-revenue-os/.git/hooks/post-update.sample"
source_filename: "post-update.sample"
source_type: "text"
source_size_bytes: 189
source_modified_at: "2026-08-18T05:49:26+09:00"
source_sha256: "81765af2daef323061dcbc5e61fc16481cb74b3bac9ad8a174b186523586f6c5"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

exec git update-server-info
