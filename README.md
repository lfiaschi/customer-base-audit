# Customer-Base Audit Plugin for Claude Code

A Claude Code plugin implementing the customer-base audit framework from *The Customer-Base Audit* by Peter Fader, Bruce Hardie & Michael Ross (Wharton School Press). Point it at raw transaction data and it produces a full, validated audit report with interactive charts.

## The Framework

A firm's transaction history is a three-dimensional **data cube**: customers × time × products. Standard reporting looks at the product × time face ("how did SKU X sell last quarter?") and averages away the customer. A customer-base audit pivots to the **customer × time** face and asks a different question: *how healthy is the base of customers generating this revenue?*

The audit examines that face through five lenses, each a different slice of the cube:

1. **Customer heterogeneity** — one period, all customers. How differently do customers behave, and how concentrated is value? (There is no "average customer": the top decile often drives ~40%+ of profit.)
2. **Period comparison** — two adjacent periods. Who was retained, lost, or newly acquired, and how did the behavior of retained customers shift?
3. **Cohort evolution** — one acquisition cohort tracked over time. How does activity, frequency, and value decay from the moment of acquisition? (40–70% of a typical cohort never buys twice.)
4. **Cohort comparison** — multiple cohorts side by side, left-aligned by cohort age. Is the quality of newly acquired customers improving or quietly degrading?
5. **Customer-base health** — the whole face at once, via the C3 chart (each period's profit stacked by acquisition cohort). Is growth coming from acquisition, retention, or development?

A sixth analysis reintroduces the **product dimension**: which categories acquire customers, which develop them, and how buying breadth relates to value.

## Skills

| Skill | What it does |
|---|---|
| `customer-base-audit:full-audit` | Top-level orchestrator: runs data prep, all lenses in parallel sub-agents, cross-lens review, and synthesizes the final audit report. Start here. |
| `customer-base-audit:data-prep` | Loads CSV/Parquet/Excel, maps columns, runs quality gates, aggregates to orders and customer-period summaries, assigns acquisition cohorts. |
| `customer-base-audit:customer-heterogeneity` | Lens 1: spend/frequency/profit distributions, multiplicative profit decomposition, equal-customer and equal-profit decile analysis. |
| `customer-base-audit:period-comparison` | Lens 2: retained/lost/new customer segmentation, profit decomposition by group, decile migration matrix, up/down analysis. |
| `customer-base-audit:cohort-evolution` | Lens 3: revenue decay decomposition, activity patterns (one-and-done rate), repeat-buying rates, time-to-nth-purchase, value-to-date. |
| `customer-base-audit:cohort-comparison` | Lens 4: left-aligned and calendar-aligned cohort curves, second-purchase CDF comparison, cohort quality trends. |
| `customer-base-audit:customer-base-health` | Lens 5: C3 chart, acquisition flow, active-customer evolution, repeat-buying development, back-of-envelope forecast. |
| `customer-base-audit:product-dimension` | Product lens: category profit decomposition, co-purchasing, sole-category buyers, entry categories of high-value customers. |
| `customer-base-audit:review` | Cross-lens validation: arithmetic identity checks, consistency across lenses, scan against known pitfalls before the report ships. |

## Installation

In Claude Code:

```
/plugin marketplace add lfiaschi/customer-base-audit
/plugin install customer-base-audit@customer-base-audit
```

## How to Use

Invoke `customer-base-audit:full-audit` with a path to transaction data (CSV, Parquet, or Excel). Minimum columns: customer ID, transaction date, spend; profit, product category, and order ID unlock the deeper analyses. Claude orchestrates the full pipeline — data preparation, parallel lens analysis, cross-validation — and writes `audit_report.md` plus interactive Plotly charts to an output directory.

Each lens skill can also be invoked directly for a targeted analysis (see table above).

## Directory Structure

- `skills/` — 9 skills with methodology, inline Polars/Plotly code, and validation rules
- `references/` — methodology deep-dive, expected patterns and benchmarks, common pitfalls, executive questions the audit answers

## Runtime Dependencies

Claude installs these as needed: `polars`, `plotly`.

## License

Apache 2.0 — see [LICENSE](LICENSE).
