---
source_path: ".pi/BusinessVault/.obsidian/plugins/dataview/styles.css"
source_filename: "styles.css"
source_type: "text"
source_size_bytes: 2965
source_modified_at: "2026-08-12T16:19:10+09:00"
source_sha256: "3306dd9032e00f989ba7233a37fd255bc4d3f4340cee661762e952f3f6aa1de9"
conversion_status: "converted"
conversion_notes: "Decoded locally as utf-8-sig."
---
.block-language-dataview {
    overflow-y: auto;
}

/*****************/
/** Table Views **/
/*****************/

/* List View Default Styling; rendered internally as a table. */
.table-view-table {
    width: 100%;
}

.table-view-table > thead > tr, .table-view-table > tbody > tr {
    margin-top: 1em;
    margin-bottom: 1em;
    text-align: left;
}

.table-view-table > tbody > tr:hover {
    background-color: var(--table-row-background-hover);
}

.table-view-table > thead > tr > th {
    font-weight: 700;
    font-size: larger;
    border-top: none;
    border-left: none;
    border-right: none;
    border-bottom: solid;

    max-width: 100%;
}

.table-view-table > tbody > tr > td {
    text-align: left;
    border: none;
    font-weight: 400;
    max-width: 100%;
}

.table-view-table ul, .table-view-table ol {
    margin-block-start: 0.2em !important;
    margin-block-end: 0.2em !important;
}

/** Rendered value styling for any view. */
.dataview-result-list-root-ul {
    padding: 0em !important;
    margin: 0em !important;
}

.dataview-result-list-ul {
    margin-block-start: 0.2em !important;
    margin-block-end: 0.2em !important;
}

/** Generic grouping styling. */
.dataview.result-group {
    padding-left: 8px;
}

/*******************/
/** Inline Fields **/
/*******************/

.dataview.inline-field-key {
    padding-left: 8px;
    padding-right: 8px;
    font-family: var(--font-monospace);
    background-color: var(--background-primary-alt);
    color: var(--nav-item-color-selected);
}

.dataview.inline-field-value {
    padding-left: 8px;
    padding-right: 8px;
    font-family: var(--font-monospace);
    background-color: var(--background-secondary-alt);
    color: var(--nav-item-color-selected);
}

.dataview.inline-field-standalone-value {
    padding-left: 8px;
    padding-right: 8px;
    font-family: var(--font-monospace);
    background-color: var(--background-secondary-alt);
    color: var(--nav-item-color-selected);
}

/***************/
/** Task View **/
/***************/

.dataview.task-list-item, .dataview.task-list-basic-item {
    margin-top: 3px;
    margin-bottom: 3px;
    transition: 0.4s;
}

.dataview.task-list-item:hover, .dataview.task-list-basic-item:hover {
    background-color: var(--text-selection);
    box-shadow: -40px 0 0 var(--text-selection);
    cursor: pointer;
}

/*****************/
/** Error Views **/
/*****************/

div.dataview-error-box {
    width: 100%;
    min-height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 4px dashed var(--background-secondary);
}

.dataview-error-message {
    color: var(--text-muted);
    text-align: center;
}

/*************************/
/** Additional Metadata **/
/*************************/

.dataview.small-text {
    font-size: smaller;
    color: var(--text-muted);
    margin-left: 3px;
}

.dataview.small-text::before {
	content: "(";
}

.dataview.small-text::after {
	content: ")";
}
