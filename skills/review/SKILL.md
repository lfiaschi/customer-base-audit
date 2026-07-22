---
name: review
description: "Cross-lens validation: consistency checks, arithmetic verification, pitfall scanning"
---

## When to Use

Invoked automatically by customer-base-audit:full-audit after all lens analyses complete. Can also be invoked standalone to validate a partial audit.

## Required Inputs

- Analysis outputs (DataFrames, summary tables, charts) from completed lens skills
- The prepared orders and customer-period data from customer-base-audit:data-prep

## Step 1: Cross-Lens Consistency

Verify that numbers agree across lenses:

- **Lens 1 vs Lens 5:** Total profit in Lens 1 (customer-heterogeneity) must match the sum of cohort profits in the C3 chart (Lens 5) for the same period. Customer counts must reconcile.
- **Lens 1 vs Lens 2:** Total revenue in Lens 1 must equal P2 total revenue in Lens 2 (if same period).
- **Lens 5 cohort sizes:** Sum of all cohort sizes must equal total unique customers.
- **Product dimension:** Sum of category revenues must equal total revenue within 1%.

```python
# Example cross-check
lens1_total = ...  # from Lens 1 decomposition
c3_period_total = c3.filter(pl.col("period") == target_period)["value"].sum()
diff_pct = abs(lens1_total - c3_period_total) / abs(lens1_total)
assert diff_pct < 0.01, f"Lens 1 vs Lens 5 mismatch: {diff_pct:.2%}"
```

## Step 2: Arithmetic Cross-Checks

For **every** decomposition table produced across all lenses, verify:

- **Revenue identity:** `n_customers * AOF * AOV = total_revenue` within 1%
- **Profit identity:** `n_customers * AOF * AOV * avg_margin = total_profit` within 1%
- **Category identity:** `n_active * penetration * ACOF * ACOV = category_revenue` within 1%

```python
# Generic cross-check
def cross_check(n, aof, aov, total, label, margin=None, profit=None):
    reconstructed = n * aof * aov
    assert abs(reconstructed - total) < 0.01 * abs(total), \
        f"{label} revenue check failed: {reconstructed:,.2f} vs {total:,.2f}"
    if margin is not None and profit is not None:
        reconstructed_profit = reconstructed * margin
        assert abs(reconstructed_profit - profit) < 0.01 * abs(profit), \
            f"{label} profit check failed: {reconstructed_profit:,.2f} vs {profit:,.2f}"
```

## Step 3: Pattern Deviation Checks

Review outputs against expected patterns. Flag deviations for human review:

**Checklist:**
- [ ] Spend distributions are right-skewed (mean > median). Flag if mean <= median.
- [ ] One-and-done rate is 30-70%. Flag if < 20% or > 85%.
- [ ] Repeat-buying rates increase with cohort age. Flag if >50% of consecutive periods show decreases > 2%.
- [ ] Top 10% of customers account for 30-50% of profit. Flag if outside this range.
- [ ] Retention rate for established businesses is 40-70%. Flag if outside this range.
- [ ] Cohort activity decays over time. Flag if activity increases > 5% between consecutive periods.
- [ ] Sole-category buyer rate is 50-80%. Flag if outside this range.

## Step 4: Pitfall Scanning

Read `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md` and check each pitfall against the analysis outputs:

- **Double-counting:** Was line-item vs order-level data handled correctly?
- **Survivorship bias:** Were "lost" customers included in period comparisons?
- **Seasonal distortion:** Were compared cohorts from the same season?
- **Missing data periods:** Could gaps in data create false churn signals?
- **Cohort definition:** Is cohort = first purchase period, not first period in dataset?

## Step 5: Completeness Check

Verify all expected outputs exist:

| Lens | Expected Outputs |
|------|-----------------|
| Data Prep | prepared_data.parquet, customer_summary.parquet |
| Lens 1 | Decomposition table, spend distribution, decile summary |
| Lens 2 | Segment table, migration matrix, up-down analysis |
| Lens 3 | Activity decay chart, buying patterns, time-to-nth |
| Lens 4 | Left-aligned comparison charts, 2nd purchase CDF |
| Lens 5 | C3 chart, acquisition flow, repeat rates |
| Product | Category decomposition, co-purchasing matrix (if category data exists) |

If product-dimension was skipped (no category column), note as expected.

## Output

Write a `validation_report.md` with sections:
1. **Status:** PASSED or FAILED
2. **Cross-Check Results:** List any failures
3. **Pattern Flags:** List any deviations with expected ranges
4. **Pitfall Warnings:** Any detected pitfalls
5. **Completeness:** Missing outputs

## References
- `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md`
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md`
