---
name: product-dimension
description: Lens 6 -- Analyze product/category dimension of customer behavior
---

## When to Use

Product dimension analysis for the customer-base audit. Applies when the data includes a product category column. Decomposes revenue/profit by category and analyzes cross-purchasing patterns.

## Required Inputs

Orders DataFrame with columns: customer_id, date, period, spend, profit (optional), category.

## Step 1: Category Penetration

```python
import polars as pl

n_active = orders["customer_id"].n_unique()

cat_penetration = orders.group_by("category").agg(
    pl.col("customer_id").n_unique().alias("n_buyers"),
    pl.col("spend").sum().alias("total_revenue"),
).with_columns(
    (pl.col("n_buyers") / n_active).alias("penetration"),
).sort("total_revenue", descending=True)
```

## Step 2: Category Decomposition

**Formula:** Category Profit = N_active x Penetration x ACOF x ACOV x Avg Margin

```python
# Per-customer-category aggregation
cust_cat = orders.group_by("customer_id", "category").agg(
    pl.len().alias("cat_transactions"),
    pl.col("spend").sum().alias("cat_spend"),
    pl.col("profit").sum().alias("cat_profit"),  # if profit exists
)

cat_decomp = cust_cat.group_by("category").agg(
    pl.col("customer_id").n_unique().alias("n_buyers"),
    pl.col("cat_transactions").sum().alias("total_transactions"),
    pl.col("cat_spend").sum().alias("total_revenue"),
    pl.col("cat_profit").sum().alias("total_profit"),  # if profit exists
).with_columns(
    (pl.col("n_buyers") / n_active).alias("penetration"),
    (pl.col("total_transactions") / pl.col("n_buyers")).alias("acof"),
    (pl.col("total_revenue") / pl.col("total_transactions")).alias("acov"),
    (pl.col("total_profit") / pl.col("total_revenue")).alias("avg_margin"),  # if profit exists
).sort("total_revenue", descending=True)

# Plotly horizontal bar chart
import plotly.graph_objects as go
fig = go.Figure(go.Bar(
    y=cat_decomp["category"].to_list(),
    x=cat_decomp["total_revenue"].to_list(),
    orientation="h",
))
fig.update_layout(template="plotly_white", title="Category Revenue Decomposition",
    xaxis_title="Revenue", yaxis=dict(autorange="reversed"))
```

## Step 3: Co-Purchasing Matrix

Which categories are bought together by the same customers?

```python
# Get unique categories per customer
cust_cats = orders.group_by("customer_id").agg(
    pl.col("category").unique().alias("categories")
)

# Explode and self-join to get all category pairs
pairs = cust_cats.explode("categories").rename({"categories": "cat_a"})
pairs2 = pairs.rename({"cat_a": "cat_b"})
co = pairs.join(pairs2, on="customer_id").filter(pl.col("cat_a") != pl.col("cat_b"))

matrix = co.group_by("cat_a", "cat_b").agg(
    pl.col("customer_id").n_unique().alias("n_both")
)

# Add overlap rate (n_both / n_buyers_of_cat_a)
cat_sizes = orders.group_by("category").agg(
    pl.col("customer_id").n_unique().alias("n_cat_buyers")
)
matrix = matrix.join(cat_sizes.rename({"category": "cat_a", "n_cat_buyers": "n_a"}), on="cat_a")
matrix = matrix.with_columns(
    (pl.col("n_both") / pl.col("n_a")).alias("overlap_rate")
)

# Plotly heatmap
cats = sorted(orders["category"].unique().to_list())
pivot = matrix.pivot(on="cat_b", index="cat_a", values="overlap_rate").fill_null(0)
```

## Step 4: Sole-Category Buyers

Customers who only ever purchase from one category:

```python
cats_per_cust = orders.group_by("customer_id").agg(
    pl.col("category").n_unique().alias("n_categories")
)
sole_buyers = cats_per_cust.filter(pl.col("n_categories") == 1)
sole_rate = sole_buyers.height / n_active
print(f"Sole-category buyers: {sole_buyers.height:,} ({sole_rate:.1%})")

# Which category do sole buyers belong to?
sole_cats = orders.filter(
    pl.col("customer_id").is_in(sole_buyers["customer_id"])
).group_by("category").agg(
    pl.col("customer_id").n_unique().alias("n_sole_buyers")
).sort("n_sole_buyers", descending=True)
```

## Step 5: Entry Category Analysis

What category do customers first purchase from?

```python
first_orders = orders.sort("customer_id", "date").group_by("customer_id").first()
entry = first_orders.group_by("category").agg(
    pl.len().alias("n_entries")
).sort("n_entries", descending=True).with_columns(
    (pl.col("n_entries") / pl.col("n_entries").sum()).alias("pct")
)
```

## Validation Rules

- **Cross-check:** Sum of category revenues must equal total revenue within 1%.
- **Cross-check:** `n_active x penetration x ACOF x ACOV` must equal category revenue within 1%.
- **Pattern:** Sole-category buyer rate is typically 50-80%. Very low rates may indicate data issues (miscategorization).
- **Pattern:** Entry categories with high penetration but low repeat rates may signal one-time promotional purchases.

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md` -- Category decomposition formula
- `${CLAUDE_PLUGIN_ROOT}/references/expected_patterns.md` -- Typical category patterns
