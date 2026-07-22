---
name: full-audit
description: "Complete customer-base audit orchestrator -- runs all lenses with parallel sub-agents and review"
---

## When to Use

Invoke this skill to run a complete customer-base audit from raw data to final report. This is the top-level orchestrator that coordinates all other CBA skills.

## Required Inputs

- Path to transaction data file (CSV, Parquet, or Excel)
- Output directory for results (default: `./audit_output/`)

## Orchestration Stages

### Stage 1: Data Preparation (BLOCKING)

Invoke `customer-base-audit:data-prep` and wait for completion. All subsequent stages depend on prepared data. If quality gates fail with errors, stop the entire audit and report to the user.

Outputs: `prepared_data.parquet`, `customer_summary.parquet`, period labels, cohort assignments.

### Stage 2: Lens Analysis (PARALLEL)

Launch sub-agents in parallel, one for each lens:

1. **customer-base-audit:customer-heterogeneity** -- Lens 1: single-period snapshot of customer value distribution
2. **customer-base-audit:period-comparison** -- Lens 2: two-period comparison (retained/lost/new dynamics)
3. **customer-base-audit:cohort-evolution** -- Lens 3: single cohort tracked over time
4. **customer-base-audit:cohort-comparison** -- Lens 4: two cohorts compared side-by-side (left-aligned)
5. **customer-base-audit:customer-base-health** -- Lens 5: C3 chart, acquisition flow, repeat rates
6. **customer-base-audit:product-dimension** -- Product dimension (only if category column exists in data)

Each sub-agent works independently on the shared prepared data. Wait for all to complete.

### Stage 3: Review (BLOCKING)

Invoke `customer-base-audit:review` to validate cross-lens consistency, verify arithmetic identities, scan for pitfalls, and check completeness. If critical inconsistencies are found, flag them prominently in the final report.

### Stage 4: Synthesis

Write the final audit report directly in markdown. Structure:

```markdown
# Customer-Base Audit: [Company Name]

## Executive Summary
Answer the key questions from ${CLAUDE_PLUGIN_ROOT}/references/executive_questions.md:
- How many active customers? Is it growing or shrinking?
- How concentrated is value? (top decile share)
- Is customer quality improving or declining? (cohort comparison)
- Where is profit coming from? (C3 chart interpretation)
- What is the product dimension story? (if applicable)

## Validation Summary
**Status: PASSED/FAILED**
[Include any cross-check failures, pattern flags, or pitfall warnings]

## Lens 1: Customer Heterogeneity
[Decomposition table, distribution charts, decile analysis, key findings]

## Lens 2: Period Comparison
[Segment analysis, migration matrix, up-down analysis, key findings]

## Lens 3: Cohort Evolution
[Activity decay, buying patterns, time-to-nth, key findings]

## Lens 4: Cohort Comparison
[Left-aligned charts, 2nd purchase CDF comparison, key findings]

## Lens 5: Customer Base Health
[C3 chart, acquisition flow, repeat rates, key findings]

## Product Dimension
[Category decomposition, co-purchasing, sole buyers, entry categories]

## Recommended Actions
[3-5 actionable recommendations based on findings]
```

## Smart Defaults

When the user does not specify parameters:
- **Granularity:** quarterly if data spans >= 2 years, monthly otherwise
- **Analysis period (Lens 1):** most recent complete period
- **Comparison periods (Lens 2):** two most recent complete periods
- **Tracked cohort (Lens 3):** oldest cohort with >= 4 periods of history
- **Compared cohorts (Lens 4):** same-season cohorts 1 year apart
- **Value metric:** use profit if available, otherwise revenue

## Output

All results saved to the output directory:
- `audit_report.md` -- final synthesis report
- `validation_report.md` -- cross-lens validation results
- Charts saved as HTML files (Plotly interactive)

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- audit methodology and definitions
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- expected patterns and benchmarks
- `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md` -- known pitfalls to avoid
- `${CLAUDE_PLUGIN_ROOT}/references/executive_questions.md` -- key questions the audit should answer
