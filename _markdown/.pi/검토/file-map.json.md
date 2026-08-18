---
source_path: ".pi/검토/file-map.json"
source_filename: "file-map.json"
source_type: "text"
source_size_bytes: 8718
source_modified_at: "2026-08-17T18:43:40+09:00"
source_sha256: "f95be2f8034cd1f8d9b56c1bd5b535e76a307ffbd3ba228ad74850b4ec1a83d9"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
{
  "summary": {
    "audit_target": "C:\\Users\\JIN\\Desktop\\미라클인베스트\\.pi",
    "audit_date": "2026-08-17",
    "total_files": 303,
    "total_directories": 212,
    "total_bytes": 595318619,
    "markdown_files": 96,
    "core_vault_markdown_files": 67,
    "audit_mode": "sampled",
    "source_mutated": false,
    "github_source_reread": false
  },
  "coverage": {
    "inventory": "all files and directories",
    "hashing": "all files",
    "markdown_structure": "all 96 Markdown files",
    "business_markdown": "all titles, openings, headings, and metadata; stratified deep reading",
    "hermes_journal": "all six daily notes read",
    "docx": "all paragraphs and tables extracted",
    "pdf": "all nine pages rendered and inspected",
    "sensitive_runtime_files": "path and structure only; secret values not read"
  },
  "groups": [
    {
      "current_path": "BusinessVault/",
      "content_type": "business knowledge vault",
      "description": "Premium MultiShop and BELLOON research, plans, decisions, indexes, and execution tracking",
      "file_count": 85,
      "preprocessing_level": "curated structured Markdown plus Obsidian app state",
      "recommended_group": "knowledge-corpus/business/",
      "recommended_action": "regroup",
      "confidence": "high"
    },
    {
      "current_path": "BusinessVault/research/premium-multishop-*.md",
      "content_type": "market and sourcing research",
      "description": "Market demand, competitor, channel, supply landscape, and content monetization research",
      "file_count": 5,
      "preprocessing_level": "human-readable synthesis with sources and caveats",
      "recommended_group": "knowledge-corpus/business/premium-multishop/01-evidence-and-research/",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": "BusinessVault/research/belloon-*.md",
      "content_type": "buyer research and sourcing operations",
      "description": "Company and person candidate reports plus a LinkedIn sourcing operating standard",
      "file_count": 4,
      "preprocessing_level": "structured research snapshots and operating template",
      "recommended_group": "knowledge-corpus/business/belloon/01-evidence-and-research and 05-reference-and-templates",
      "recommended_action": "regroup",
      "confidence": "high"
    },
    {
      "current_path": "BusinessVault/plans/",
      "content_type": "mixed business design collection",
      "description": "Strategies, architectures, reviews, audits, decisions, prompts, contracts, and roadmaps",
      "file_count": 33,
      "preprocessing_level": "structured authored Markdown; multiple lifecycle stages mixed",
      "recommended_group": "project-specific research, decisions, strategy, execution, reference, and history",
      "recommended_action": "regroup",
      "confidence": "high"
    },
    {
      "current_path": "BusinessVault/04-decision-log.md",
      "content_type": "decision register",
      "description": "Chronological decisions, with many distinct decisions under one heading",
      "file_count": 1,
      "preprocessing_level": "append-style summary register",
      "recommended_group": "business/*/02-decisions plus a shared decision index",
      "recommended_action": "split",
      "confidence": "high"
    },
    {
      "current_path": "BusinessVault/ideas and BusinessVault/market",
      "content_type": "ideas and research indexes",
      "description": "Business-specific idea notes and duplicated two-level navigation indexes",
      "file_count": 10,
      "preprocessing_level": "short curated index and summary notes",
      "recommended_group": "each business folder",
      "recommended_action": "regroup",
      "confidence": "high"
    },
    {
      "current_path": "HermesWiki/",
      "content_type": "personal wiki and daily journal",
      "description": "Daily summaries, personal wiki index, change log, and Obsidian app state",
      "file_count": 34,
      "preprocessing_level": "templated daily summaries with YAML frontmatter",
      "recommended_group": "knowledge-corpus/personal/",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": "BusinessVault/.obsidian, BusinessVault/TaskNotes, HermesWiki/.obsidian, HermesWiki/TaskNotes",
      "content_type": "Obsidian and TaskNotes app assets",
      "description": "Plugin bundles, configuration, generated views, and duplicate onboarding note",
      "file_count": 48,
      "preprocessing_level": "generated or installed app state",
      "recommended_group": "app-state-no-index or retained inside each portable vault",
      "recommended_action": "keep",
      "confidence": "high"
    },
    {
      "current_path": ".agents/skills/",
      "content_type": "AI instruction packages",
      "description": "Twenty-one marketing, SEO, content, and platform skills with installation provenance",
      "file_count": 21,
      "preprocessing_level": "installed Markdown instructions",
      "recommended_group": "ai-operating-assets/marketing-skills/",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": ".claude/skills/hermes-vps-setup/",
      "content_type": "installation skill package",
      "description": "Hermes VPS setup instructions, scripts, example configuration, and a nine-page PDF guide",
      "file_count": 17,
      "preprocessing_level": "reusable executable documentation package",
      "recommended_group": "ai-operating-assets/hermes-vps-setup/",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": ".claude/projects and .claude/tasks",
      "content_type": "conversation and task event logs",
      "description": "Eight JSONL conversation histories and seven task state files, useful for provenance but sensitive",
      "file_count": 26,
      "preprocessing_level": "raw application event records",
      "recommended_group": "app-state-no-index/conversation-history/",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": "Claude/",
      "content_type": "generated business artifacts",
      "description": "One PMS benchmark DOCX and one PMS sourcing architecture HTML with thumbnail",
      "file_count": 3,
      "preprocessing_level": "formatted derived reports and visual artifact",
      "recommended_group": "knowledge-corpus/business/premium-multishop/01-evidence-and-research/source-artifacts/",
      "recommended_action": "needs-decision",
      "confidence": "medium"
    },
    {
      "current_path": ".cache/",
      "content_type": "browser runtime cache",
      "description": "Chromium binaries and resources; not text corpus material",
      "file_count": 86,
      "preprocessing_level": "runtime binary",
      "recommended_group": "machine-cache-no-index/browser-runtime/ or outside corpus",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": ".hermes-sync/",
      "content_type": "synchronization runtime and secrets",
      "description": "Syncthing executable, configuration, log, certificates, and key material",
      "file_count": 8,
      "preprocessing_level": "runtime state",
      "recommended_group": "app-state-no-index/sync-state plus external secret storage",
      "recommended_action": "split",
      "confidence": "high"
    },
    {
      "current_path": ".ssh/",
      "content_type": "private credentials and connection state",
      "description": "SSH private key, public key, configuration, and known hosts",
      "file_count": 5,
      "preprocessing_level": "security-sensitive runtime state",
      "recommended_group": "outside shared corpus root",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": "Intel, Favorites, dwhelper",
      "content_type": "operating system residue",
      "description": "Driver logs, Windows favorites metadata, and an empty helper directory",
      "file_count": 8,
      "preprocessing_level": "system log and shell state",
      "recommended_group": "machine-cache-no-index or outside corpus",
      "recommended_action": "move",
      "confidence": "high"
    },
    {
      "current_path": "49 empty top-level agent target directories",
      "content_type": "empty placeholders",
      "description": "Mostly empty skills targets for various coding agents; exact creator needs verification",
      "file_count": 0,
      "preprocessing_level": "empty scaffold",
      "recommended_group": "app-state-no-index/agent-target-placeholders/",
      "recommended_action": "needs-decision",
      "confidence": "medium"
    }
  ]
}
