---
name: executive-report
description: "Turn completed audit outputs into an executive-ready document (Word/PDF) organized by insight, not by lens -- Pyramid Principle, SCQA, action titles, embedded exhibits"
---

## When to Use

Final stage of a full customer-base audit, after all lenses and the review have completed. Also invoke standalone when the user asks to make existing audit results "executive-ready", "board-ready", or "presentable".

## Why This Skill Exists

The lens-by-lens structure of `audit_report.md` is the right way to *do* the analysis, but the wrong way to *present* it. Executives don't care which lens produced a number — they care what the numbers mean for the business and what to do about it. This skill reorganizes the audit's findings into a consulting-grade document using the Minto Pyramid Principle: answer first, insight-titled sections, one exhibit per claim.

## Required Inputs

- Completed audit outputs: `lens*_findings.md`, `lens*_metrics.json`, `validation_report.md`, chart HTML files
- Output directory (same as the audit's)

## Step 1: Design the Storyline (before writing anything)

Work top-down:

1. **Governing thought** — one sentence that answers "what should the executive take away and do?" It must be a claim about the business, not a description of the analysis. Test: would a CEO who reads only this sentence know the priority?
2. **SCQA opening** — Situation (what's working), Complication (what changed/threatens), Question (the decision at hand), Answer (the governing thought). This becomes the first paragraph of the executive summary.
3. **Three key messages** — MECE supports for the governing thought, drawn from the audit findings. Group by *business meaning* (e.g., "where profit comes from", "what broke", "what's working"), never by lens. Each message gets its own section with an insight-stating title.
4. **The titles test** — read your section titles in order, alone. If they don't tell the complete story to someone who reads nothing else, rewrite them. "Lens 3: Cohort Evolution" fails; "Cohort revenue declines only because fewer customers stay active" passes.

Every number in the storyline must come from the validated `lens*_metrics.json` files — never re-derive figures by hand, and never from memory of the findings prose. (This also applies to any tables: generate them from the metrics JSON.)

## Step 2: Select and Title the Exhibits

- **6–8 exhibits maximum.** The audit produces 20+ charts; the executive document is not a gallery. Pick the one chart that *proves* each claim in the storyline. Everything else stays in the HTML chart set, referenced from the appendix.
- **Action titles**: every exhibit is labeled "EXHIBIT N" plus a sentence stating the insight ("New-customer intake fell by two-thirds year-over-year"), not the content ("Acquisition flow by quarter").
- **"So what" line** under each exhibit: one italic sentence connecting the chart to a decision. If you can't write it, the exhibit doesn't belong.
- **Verify title-chart fit**: the chart must directly show what the title claims — no extrapolation the reader can't see in the picture.

Render charts to static PNGs with the bundled script (extracts figure specs from the saved Plotly HTML files, no recomputation needed — and recolors every chart to the report's single hue):

```bash
uv run ${CLAUDE_PLUGIN_ROOT}/scripts/export_chart_pngs.py <audit-output-dir>
```

## Step 3: Assemble the Document

**Preferred: Word document.** If a `docx` skill is available in the environment, invoke it and follow its document-creation workflow (docx-js). Otherwise fall back to a styled HTML file printed to PDF via headless Chrome (`--headless --print-to-pdf --no-pdf-header-footer`).

Structure (in this order — detail always *after* the answer):

1. **Cover** — a title that states the governing thought (not "Customer-Base Audit Report"), the data basis in one line, validation status, date.
2. **Executive summary (one page)** — SCQA paragraph, a 4-KPI band with the numbers that carry the story, the three key messages each with a bolded claim and 2–3 supporting sentences, and a highlighted recommendation box. An executive who stops here has the whole story.
3. **One section per key message** — insight-stating H1, short narrative paragraphs, 2 exhibits each with action title and so-what.
4. **Recommendations** — a table: action, what-and-why (tied to specific findings), horizon. Add a "measuring success" line with concrete targets.
5. **Appendix** — method, data limitations and caveats (imputed values, partial periods, censoring — never bury these, but never lead with them either), and a pointer to `audit_report.md` / `validation_report.md` / the full chart set for detail.

**Color discipline — exactly three colors in the whole document:**

- **Ink** (near-black) for all text, headings, and KPI values; **gray** for secondary text (captions, so-whats, labels, reference lines); **one accent hue** for everything that needs emphasis (exhibit labels, the recommendation box, cover kicker).
- Charts use the *same* accent hue as the document: single series in the accent, multi-series in sequential light-to-dark shades of it (the bundled export script applies this automatically), dashed reference lines in gray, heatmaps in a monochrome scale. Never let the analysis charts' working palettes (viridis, categorical rainbows, per-panel hues) reach the executive document.
- Nothing is colored for decoration. A second hue is permitted only when it encodes meaning the story depends on — at most once, and it must be named in the exhibit's so-what. If everything is highlighted, nothing is.

Other formatting principles: generous whitespace, page numbers, running header. No dense tables in the body — those live in the appendix or the lens findings.

## Step 4: Verify Visually

Convert the document to images and *look at it* (docx: `soffice --headless --convert-to pdf` then `pdftoppm`, or read the PDF directly). Check:

- Every exhibit renders, is legible at page width, and sits with its own title and so-what (never orphaned across a page break)
- Captions and titles claim only what the chart shows
- The titles test still passes in the final artifact
- Numbers in the document match `lens*_metrics.json`

Fix and re-render until clean. Output files: `executive_report.docx` (or `.pdf`) in the audit output directory.

## Quality Checklist

- [ ] Governing thought is a business claim with an implied action
- [ ] Titles alone tell the full story (titles test)
- [ ] Three key messages are MECE and lens-agnostic
- [ ] ≤8 exhibits, each with action title + so-what
- [ ] All numbers traced to validated metrics JSON
- [ ] Recommendations tied 1:1 to findings, with horizons and success metrics
- [ ] Three colors total: ink, gray, one accent — charts share the accent hue
- [ ] Caveats present in appendix (and inline only where a number would mislead without them)
- [ ] Final artifact visually verified page by page

## References
- `${CLAUDE_PLUGIN_ROOT}/references/executive_questions.md` -- the questions the summary must answer
- `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md` -- caveats that must survive into the appendix
