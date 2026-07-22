---
name: cohort-comparison
description: Lens 4 -- Compare two acquisition cohorts side-by-side using left-aligned analysis
---

## When to Use

Lens 4 of the customer-base audit. Compare two acquisition cohorts at the same "age" (periods since acquisition) to see if customer quality is improving or declining.

## Required Inputs

Orders DataFrame with columns: customer_id, date, period, spend, profit (optional), cohort.

## Cohort Selection

Choose two cohorts to compare, ideally:
- Same season, 1 year apart (e.g., Q1-2019 vs Q1-2020) to control for seasonality
- Both with enough history to compare at least 4 periods

## Step 1: Left-Aligned Cohort Activity

```python
import polars as pl

def compute_cohort_activity(orders, cohort_label):
    """Compute activity metrics by age (periods since acquisition)."""
    cohort_data = orders.filter(pl.col("cohort") == cohort_label)
    cohort_size = cohort_data["customer_id"].n_unique()
    periods = sorted(cohort_data["period"].unique().to_list())

    activity = cohort_data.group_by("period").agg(
        pl.col("customer_id").n_unique().alias("n_active"),
        pl.col("spend").sum().alias("total_revenue"),
        pl.len().alias("n_transactions"),
    ).sort("period")

    # Add age column (0 = acquisition period)
    activity = activity.with_columns(
        pl.arange(0, pl.len()).alias("age"),
        (pl.col("n_active") / cohort_size).alias("pct_active"),
        (pl.col("n_transactions") / pl.col("n_active")).alias("aof"),
        (pl.col("total_revenue") / pl.col("n_transactions")).alias("aov"),
        (pl.col("total_revenue") / pl.col("n_active")).alias("spend_per_active"),
    )
    return activity, cohort_size

c1, size1 = compute_cohort_activity(orders, "COHORT_A")  # e.g., "2019-Q1"
c2, size2 = compute_cohort_activity(orders, "COHORT_B")  # e.g., "2020-Q1"

# Left-align by age
comparison = c1.select("age", "pct_active", "aof", "aov", "spend_per_active").join(
    c2.select("age", "pct_active", "aof", "aov", "spend_per_active"),
    on="age", suffix="_c2"
)
```

## Step 2: Side-by-Side Visualization

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(rows=2, cols=2, subplot_titles=["% Active", "AOF", "AOV", "Spend/Active"])
ages = comparison["age"].to_list()

for i, (metric, title) in enumerate([
    ("pct_active", "% Active"), ("aof", "AOF"), ("aov", "AOV"), ("spend_per_active", "Spend/Active")
]):
    row, col = divmod(i, 2)
    fig.add_trace(go.Scatter(x=ages, y=comparison[metric].to_list(),
        name=f"Cohort A", mode="lines+markers"), row=row+1, col=col+1)
    fig.add_trace(go.Scatter(x=ages, y=comparison[f"{metric}_c2"].to_list(),
        name=f"Cohort B", mode="lines+markers"), row=row+1, col=col+1)

fig.update_layout(template="plotly_white", title="Cohort Comparison (Left-Aligned)", height=600)
```

## Step 3: Second Purchase CDF Comparison

```python
def second_purchase_cdf(orders, cohort_label):
    cohort_data = orders.filter(pl.col("cohort") == cohort_label).sort("customer_id", "date")
    ranked = cohort_data.with_columns(
        pl.col("date").rank("ordinal").over("customer_id").alias("purchase_num")
    )
    first = ranked.filter(pl.col("purchase_num") == 1).select("customer_id", pl.col("date").alias("first_date"))
    second = ranked.filter(pl.col("purchase_num") == 2).select("customer_id", pl.col("date").alias("second_date"))
    cohort_size = cohort_data["customer_id"].n_unique()

    days = first.join(second, on="customer_id").with_columns(
        (pl.col("second_date") - pl.col("first_date")).dt.total_days().alias("days")
    )
    max_d = int(days["days"].quantile(0.95))
    cdf = [{"days": d, "pct": days.filter(pl.col("days") <= d).height / cohort_size}
           for d in range(0, max_d + 1, max(1, max_d // 50))]
    return pl.DataFrame(cdf)

cdf_a = second_purchase_cdf(orders, "COHORT_A")
cdf_b = second_purchase_cdf(orders, "COHORT_B")
```

## Validation Rules

- **Cross-check:** At age 0, both cohorts should show 100% activity (by definition).
- **Pattern:** Newer cohorts with lower retention at same age may signal declining customer quality.
- **Pattern:** If AOV increases but activity decreases, the cohort may be losing casual buyers (not necessarily bad).

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- Left-aligned cohort analysis
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- Typical cohort trajectories
