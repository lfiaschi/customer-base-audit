# Customer-Base Audit Skill Plugin

A Claude Code skill plugin implementing the customer-base audit framework from *The Customer-Base Audit* by Fader, Hardie & Ross.

## What It Does

Runs a structured five-lens audit of transaction data to assess customer base health, heterogeneity, retention dynamics, cohort quality, and product-level patterns.

## Installation

In Claude Code:

```
/plugin marketplace add lfiaschi/customer-base-audit
/plugin install customer-base-audit@customer-base-audit
```

## How to Use

Invoke `customer-base-audit:full-audit` with a path to transaction data (CSV, Parquet, or Excel). Claude will orchestrate the full analysis pipeline: data preparation, parallel lens analysis, cross-validation, and synthesis into a final report.

Individual lenses can also be invoked directly: `customer-base-audit:data-prep`, `customer-base-audit:customer-heterogeneity`, `customer-base-audit:period-comparison`, `customer-base-audit:cohort-evolution`, `customer-base-audit:cohort-comparison`, `customer-base-audit:customer-base-health`, `customer-base-audit:product-dimension`, `customer-base-audit:review`.

## Directory Structure

- `skills/` -- 9 SKILL.md files with methodology, inline Polars/Plotly code snippets, and validation rules
- `references/` -- 4 reference docs (methodology, expected patterns, common pitfalls, executive questions)

## Runtime Dependencies

Claude installs these as needed: `polars`, `plotly`.
