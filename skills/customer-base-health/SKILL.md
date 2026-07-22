---
name: customer-base-health
description: Lens 5 -- Assess overall customer base health via C3 chart, acquisition flow, and repeat rates
---

## When to Use

Lens 5 of the customer-base audit. Provides the "big picture" view of how the customer base is evolving: are profits coming from loyal returning customers or from constant re-acquisition?

## Required Inputs

Orders DataFrame with columns: customer_id, date, period, spend, profit (optional), cohort.

## Step 1: C3 Chart (Cohort Revenue/Profit Contribution Over Time)

The C3 chart is the signature visualization of the customer-base audit. It shows a stacked bar chart where each bar is a period and each segment is a cohort's contribution.

```python
import polars as pl
import plotly.graph_objects as go

c3 = orders.group_by("cohort", "period").agg(
    pl.col("spend").sum().alias("value"),  # or "profit" if available
    pl.col("customer_id").n_unique().alias("n_active"),
).sort("cohort", "period")

# Plotly stacked bar
fig = go.Figure()
for cohort in sorted(c3["cohort"].unique().to_list()):
    cd = c3.filter(pl.col("cohort") == cohort)
    fig.add_trace(go.Bar(
        x=cd["period"].to_list(),
        y=cd["value"].to_list(),
        name=f"Cohort {cohort}",
    ))
fig.update_layout(barmode="stack", template="plotly_white",
    title="C3: Cohort Contribution Over Time",
    xaxis_title="Period", yaxis_title="Revenue/Profit")
```

## Step 2: Acquisition Flow

Track cohort sizes over time to understand acquisition trends:

```python
acquisition = orders.group_by("cohort").agg(
    pl.col("customer_id").n_unique().alias("cohort_size"),
).sort("cohort")

fig = go.Figure(go.Bar(
    x=acquisition["cohort"].to_list(),
    y=acquisition["cohort_size"].to_list(),
))
fig.update_layout(template="plotly_white", title="Acquisition Flow: New Customers per Cohort",
    xaxis_title="Cohort", yaxis_title="New Customers")
```

## Step 3: Repeat Buying Rates

For each cohort, compute the fraction of period-t customers who also appear in period t+1:

```python
periods = sorted(orders["period"].unique().to_list())
cohorts_list = sorted(orders["cohort"].unique().to_list())

rates = []
for cohort in cohorts_list:
    cohort_orders = orders.filter(pl.col("cohort") == cohort)
    for i in range(len(periods) - 1):
        p1_custs = set(cohort_orders.filter(pl.col("period") == periods[i])["customer_id"].to_list())
        p2_custs = set(cohort_orders.filter(pl.col("period") == periods[i+1])["customer_id"].to_list())
        if p1_custs:
            rates.append({
                "cohort": cohort,
                "from_period": periods[i],
                "repeat_rate": len(p1_custs & p2_custs) / len(p1_custs),
            })
rates_df = pl.DataFrame(rates)
```

## Step 4: Cohort Decomposition Grid

Apply the profit decomposition per cohort per period:

```python
decomp_grid = orders.group_by("cohort", "period").agg(
    pl.col("customer_id").n_unique().alias("n_active"),
    pl.len().alias("n_transactions"),
    pl.col("spend").sum().alias("total_revenue"),
).with_columns(
    (pl.col("n_transactions") / pl.col("n_active")).alias("aof"),
    (pl.col("total_revenue") / pl.col("n_transactions")).alias("aov"),
).sort("cohort", "period")
```

## Validation Rules

- **Cross-check:** Sum of all cohort values in the C3 chart for a given period must equal the period total from Lens 1.
- **Pattern:** Repeat-buying rates should generally increase with cohort age as lighter buyers drop out. If more than half the consecutive periods show decreases > 2%, flag for review.
- **Pattern:** A healthy business shows growing cohort contributions stacking up in the C3 chart. If recent cohorts contribute disproportionately little, acquisition quality may be declining.
- **Pattern:** If the C3 chart shows the business is "running on the treadmill" (constant re-acquisition with little retained revenue), flag this prominently.

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- C3 chart and customer base health
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- What healthy vs unhealthy looks like
- `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md` -- Pitfall #10: ignoring cohort mix effects
