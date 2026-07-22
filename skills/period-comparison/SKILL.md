---
name: period-comparison
description: Lens 2 -- Compare two periods to understand customer dynamics (retained, lost, new)
---

## When to Use

Lens 2 of the customer-base audit. Compare two consecutive periods to understand customer retention, acquisition, and value shifts.

## Required Inputs

Two customer-period summaries (e.g., Year 1 and Year 2) with columns: customer_id, num_transactions, total_spend, total_profit (optional).

## Step 1: Customer Overlap Segmentation

```python
import polars as pl

p1_custs = set(df_p1["customer_id"].to_list())
p2_custs = set(df_p2["customer_id"].to_list())

retained = p1_custs & p2_custs
lost = p1_custs - p2_custs
new = p2_custs - p1_custs

# Verify segment sizes
assert len(retained) + len(lost) == len(p1_custs)
assert len(retained) + len(new) == len(p2_custs)

print(f"P1: {len(p1_custs):,} customers")
print(f"P2: {len(p2_custs):,} customers")
print(f"Retained: {len(retained):,} ({len(retained)/len(p1_custs):.1%} retention rate)")
print(f"Lost: {len(lost):,}")
print(f"New: {len(new):,}")
```

## Step 2: Decomposition per Segment

Apply the multiplicative decomposition to each segment (retained-in-P1, retained-in-P2, lost, new):

```python
def decompose_segment(df, label):
    n = df["customer_id"].n_unique()
    txns = df["num_transactions"].sum()
    rev = df["total_spend"].sum()
    aof = txns / n if n > 0 else 0
    aov = rev / txns if txns > 0 else 0
    return {"segment": label, "n_customers": n, "aof": aof, "aov": aov, "total_revenue": rev}

df_retained_p1 = df_p1.filter(pl.col("customer_id").is_in(list(retained)))
df_retained_p2 = df_p2.filter(pl.col("customer_id").is_in(list(retained)))
df_lost = df_p1.filter(pl.col("customer_id").is_in(list(lost)))
df_new = df_p2.filter(pl.col("customer_id").is_in(list(new)))

segments = pl.DataFrame([
    decompose_segment(df_retained_p1, "Retained (P1)"),
    decompose_segment(df_retained_p2, "Retained (P2)"),
    decompose_segment(df_lost, "Lost"),
    decompose_segment(df_new, "New"),
])
```

## Step 3: Decile Migration

Track how customers move between value tiers across periods.

```python
# Assign deciles in each period independently
def assign_deciles(df, value_col="total_spend"):
    return df.sort(value_col, descending=True).with_row_index("rank").with_columns(
        ((pl.col("rank") * 10) // len(df) + 1).clip(1, 10).alias("decile")
    ).select("customer_id", "decile")

d1 = assign_deciles(df_p1).rename({"decile": "decile_p1"})
d2 = assign_deciles(df_p2).rename({"decile": "decile_p2"})

migration = d1.join(d2, on="customer_id").group_by("decile_p1", "decile_p2").agg(
    pl.len().alias("n_customers")
)

# Plotly heatmap
import plotly.graph_objects as go
pivot = migration.pivot(on="decile_p2", index="decile_p1", values="n_customers").fill_null(0).sort("decile_p1")
value_cols = [c for c in pivot.columns if c != "decile_p1"]
fig = go.Figure(go.Heatmap(
    z=pivot.select(value_cols).to_numpy(),
    x=value_cols, y=pivot["decile_p1"].to_list(),
    colorscale="Blues", text=pivot.select(value_cols).to_numpy(), texttemplate="%{text}",
))
fig.update_layout(template="plotly_white", title="Decile Migration Matrix",
    xaxis_title="P2 Decile", yaxis_title="P1 Decile", yaxis=dict(autorange="reversed"))
```

## Step 4: Up-Down Analysis

For retained customers, classify changes in spend, frequency, and profit:

```python
both = df_p1.join(df_p2, on="customer_id", suffix="_p2")
both = both.with_columns(
    (pl.col("total_spend_p2") > pl.col("total_spend")).alias("spend_up"),
    (pl.col("num_transactions_p2") > pl.col("num_transactions")).alias("freq_up"),
)
up_down = both.group_by("spend_up", "freq_up").agg(
    pl.len().alias("n_customers"),
    pl.col("total_spend_p2").sum().alias("p2_revenue"),
)
```

## Validation Rules

- **Cross-check:** Retained + Lost = P1 total customers. Retained + New = P2 total customers.
- **Cross-check:** Sum of segment revenues must equal period totals.
- **Pattern:** Retention rate for established businesses is typically 40-70%. Flag if outside this range.
- **Pattern:** Most migration should cluster near the diagonal (customers staying in similar deciles).

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- Period comparison framework
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- Typical retention rates
