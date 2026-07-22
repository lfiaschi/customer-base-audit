---
name: cohort-evolution
description: Lens 3 -- Track a single cohort's behavior over time (activity, frequency, value decay)
---

## When to Use

Lens 3 of the customer-base audit. Track how a single acquisition cohort evolves over multiple periods. Focuses on retention/activity decay, buying patterns, and time-to-nth-purchase.

## Required Inputs

Orders DataFrame with columns: customer_id, date, period, spend, profit (optional), cohort.

## Step 1: Cohort Activity Over Time

```python
import polars as pl

cohort_label = "TARGET_COHORT"  # e.g., "2020-Q1"
cohort_data = orders.filter(pl.col("cohort") == cohort_label)
cohort_size = cohort_data["customer_id"].n_unique()

activity = cohort_data.group_by("period").agg(
    pl.col("customer_id").n_unique().alias("n_active"),
    pl.col("spend").sum().alias("total_revenue"),
    pl.col("spend").mean().alias("avg_spend"),
    pl.len().alias("n_transactions"),
).sort("period").with_columns(
    (pl.col("n_active") / cohort_size).alias("pct_active"),
    (pl.col("n_transactions") / pl.col("n_active")).alias("aof"),
    (pl.col("total_revenue") / pl.col("n_transactions")).alias("aov"),
)

# Plotly line chart
import plotly.graph_objects as go
fig = go.Figure(go.Scatter(
    x=activity["period"].to_list(), y=activity["pct_active"].to_list(),
    mode="lines+markers", name="% Active"
))
fig.update_layout(template="plotly_white", title=f"Cohort {cohort_label} Activity Decay",
    xaxis_title="Period", yaxis_title="% Active", yaxis=dict(tickformat=".0%"))
```

## Step 2: Annual Buying Patterns

For cohorts observed over multiple years, create binary purchase patterns:

```python
# Create customer x period matrix of Y/N
cust_periods = cohort_data.group_by("customer_id", "period").agg(
    pl.len().alias("n_orders")
)
periods = sorted(cust_periods["period"].unique().to_list())

# Pivot to wide format
wide = cust_periods.pivot(on="period", index="customer_id", values="n_orders").fill_null(0)
# Convert to binary patterns (Y/N strings)
for p in periods:
    if p in wide.columns:
        wide = wide.with_columns(
            pl.when(pl.col(p) > 0).then(pl.lit("Y")).otherwise(pl.lit("N")).alias(p)
        )

# Count pattern frequencies
pattern_col = pl.concat_str([pl.col(p) for p in periods if p in wide.columns], separator="")
patterns = wide.with_columns(pattern_col.alias("pattern")).group_by("pattern").agg(
    pl.len().alias("count")
).sort("count", descending=True).with_columns(
    (pl.col("count") / pl.col("count").sum()).alias("pct")
)
```

## Step 3: Time to Nth Purchase

```python
# Rank each customer's orders chronologically
ranked = cohort_data.sort("customer_id", "date").with_columns(
    pl.col("date").rank("ordinal").over("customer_id").alias("purchase_num")
)

first = ranked.filter(pl.col("purchase_num") == 1).select("customer_id", pl.col("date").alias("first_date"))

for n in [2, 3, 5]:
    nth = ranked.filter(pl.col("purchase_num") == n).select("customer_id", pl.col("date").alias("nth_date"))
    time_to_nth = first.join(nth, on="customer_id").with_columns(
        (pl.col("nth_date") - pl.col("first_date")).dt.total_days().alias("days_to_nth")
    )
    median_days = time_to_nth["days_to_nth"].median()
    pct_reached = len(time_to_nth) / cohort_size
    print(f"Purchase #{n}: {pct_reached:.1%} reached, median {median_days:.0f} days")
```

## Step 4: Second Purchase Cumulative Distribution

```python
second = ranked.filter(pl.col("purchase_num") == 2).select("customer_id", pl.col("date").alias("second_date"))
days_to_second = first.join(second, on="customer_id").with_columns(
    (pl.col("second_date") - pl.col("first_date")).dt.total_days().alias("days")
)

# Build CDF
max_days = int(days_to_second["days"].max())
cdf = []
for d in range(0, max_days + 1, max(1, max_days // 50)):
    pct = days_to_second.filter(pl.col("days") <= d).height / cohort_size
    cdf.append({"days": d, "pct_reached_2nd": pct})
cdf_df = pl.DataFrame(cdf)
```

## Validation Rules

- **Pattern:** One-and-done rate (customers with exactly 1 purchase / cohort size) is typically 40-70%. Flag if < 20% or > 85%.
- **Pattern:** Activity rate should generally decline over time (cohort decay). Flag if activity increases by > 5% in consecutive periods.
- **Pattern:** Time-to-2nd-purchase CDF should flatten -- most repeat buyers repurchase quickly.

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- Cohort analysis framework
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- Typical decay curves
- `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md` -- Pitfall #8: ignoring one-and-done buyers
