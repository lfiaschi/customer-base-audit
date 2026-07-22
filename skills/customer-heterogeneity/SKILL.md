---
name: customer-heterogeneity
description: Lens 1 -- Analyze customer heterogeneity via profit decomposition, distributions, and deciles
---

## When to Use

Lens 1 of the customer-base audit. Apply to a single period's customer-level data to understand the range and shape of customer value.

## Required Inputs

Customer-period summary with columns: customer_id, num_transactions, total_spend, total_profit (optional).

## Step 1: Profit Decomposition

The multiplicative identity: **Profit = #Customers x AOF x AOV x Avg Margin**

```python
import polars as pl

n_customers = df["customer_id"].n_unique()
n_transactions = df["num_transactions"].sum()
total_revenue = df["total_spend"].sum()

aof = n_transactions / n_customers  # Average Order Frequency
aov = total_revenue / n_transactions  # Average Order Value

# If profit data exists:
total_profit = df["total_profit"].sum()
avg_margin = total_profit / total_revenue

# CROSS-CHECK (must hold within 1%)
reconstructed = n_customers * aof * aov * avg_margin
assert abs(reconstructed - total_profit) < 0.01 * abs(total_profit), \
    f"Decomposition failed: {reconstructed:.2f} != {total_profit:.2f}"

# Revenue-only cross-check:
assert abs(n_customers * aof * aov - total_revenue) < 0.01 * abs(total_revenue)
```

Present these metrics in a summary table.

## Step 2: Distributions

Compute spend and transaction-count distributions to show heterogeneity.

```python
# Spend distribution with auto-binning
spend = df["total_spend"]
mean_val = spend.mean()
median_val = spend.median()
std_val = spend.std()

# Create bins: use ~10-20 bins, clipping outliers at 3 sigma
upper = min(spend.max(), mean_val + 3 * std_val)
bin_edges = list(range(0, int(upper) + 1, max(1, int(upper / 15))))

binned = df.with_columns(
    pl.col("total_spend").cut(bin_edges).alias("bin")
).group_by("bin").agg(
    pl.len().alias("count")
).sort("bin").with_columns(
    (pl.col("count") / pl.col("count").sum()).alias("pct")
)

# Plotly histogram
import plotly.graph_objects as go
fig = go.Figure(go.Bar(
    x=binned["bin"].cast(pl.Utf8).to_list(),
    y=binned["count"].to_list(),
    text=[f"{p:.1%}" for p in binned["pct"].to_list()],
    textposition="outside",
))
fig.add_annotation(x=0.95, y=0.95, xref="paper", yref="paper",
    text=f"Mean: {mean_val:,.1f}<br>Median: {median_val:,.1f}",
    showarrow=False, bgcolor="rgba(255,255,255,0.8)")
fig.update_layout(template="plotly_white", title="Spend Distribution",
    xaxis_title="Spend", yaxis_title="Count")
```

## Step 3: Decile Analysis

Rank customers by value and group into deciles.

```python
# Equal-customer deciles (each decile = ~10% of customers)
ranked = df.sort("total_spend", descending=True).with_row_index("rank")
ranked = ranked.with_columns(
    ((pl.col("rank") * 10) // len(ranked) + 1).clip(1, 10).alias("decile")
)
decile_summary = ranked.group_by("decile").agg(
    pl.len().alias("n_customers"),
    pl.col("total_spend").sum().alias("decile_revenue"),
    pl.col("total_profit").sum().alias("decile_profit"),  # if profit exists
    pl.col("num_transactions").mean().alias("aof"),
    (pl.col("total_spend") / pl.col("num_transactions")).mean().alias("aov"),
).sort("decile").with_columns(
    (pl.col("n_customers") / pl.col("n_customers").sum()).alias("pct_customers"),
    (pl.col("decile_revenue") / pl.col("decile_revenue").sum()).alias("pct_revenue"),
    (pl.col("decile_profit") / pl.col("decile_profit").sum()).alias("pct_profit"),
)

# Plotly decile chart
fig = go.Figure()
fig.add_trace(go.Bar(x=decile_summary["decile"].to_list(),
    y=decile_summary["pct_profit"].to_list(), name="% of Profit"))
fig.add_trace(go.Scatter(x=decile_summary["decile"].to_list(),
    y=decile_summary["aof"].to_list(), name="AOF", yaxis="y2", mode="lines+markers"))
fig.update_layout(template="plotly_white", title="Decile Analysis",
    xaxis=dict(title="Decile", dtick=1),
    yaxis=dict(title="% of Profit"),
    yaxis2=dict(title="AOF", overlaying="y", side="right"))
```

## Validation Rules

- **Cross-check:** `n_customers * AOF * AOV` must equal `total_revenue` within 1%. With margin: `n_customers * AOF * AOV * avg_margin` must equal `total_profit` within 1%.
- **Pattern:** Top 10% of customers typically account for 30-50% of profit. Flag if outside this range.
- **Pattern:** Spend distribution should be right-skewed (mean > median). Flag if mean <= median.
- **Pattern:** AOF distribution should be heavily concentrated at low values (many one-time buyers).

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- Decomposition formulas
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- What "normal" looks like
- `${CLAUDE_PLUGIN_ROOT}/references/common_pitfalls.md` -- Pitfall #1: ignoring heterogeneity
