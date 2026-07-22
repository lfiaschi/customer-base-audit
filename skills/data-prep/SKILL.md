---
name: data-prep
description: Load, validate, and aggregate transaction data for customer-base audit
---

## When to Use

First step of any customer-base audit. Invoke when the user provides raw transaction data (CSV, Parquet, Excel).

## Required Inputs

A data file with at minimum: customer identifier, transaction date, transaction amount.
Optional: profit/margin, product category, order ID, units.

## Step 1: Load Data

```python
import polars as pl
from pathlib import Path

path = Path("DATA_FILE")  # user provides this
if path.suffix == ".parquet":
    df = pl.read_parquet(path)
elif path.suffix == ".csv":
    df = pl.read_csv(path, try_parse_dates=True)
elif path.suffix in (".xlsx", ".xls"):
    df = pl.read_excel(path)
```

## Step 2: Identify Columns

Map the user's column names to canonical roles. Look for these patterns:

| Role | Common names |
|------|-------------|
| customer_id | customer_id, cust_id, user_id, buyer_id, client_id |
| date | date, order_date, transaction_date, purchase_date |
| spend | spend, revenue, amount, sales, value, total_spend |
| profit | profit, total_profit, margin_dollars, gross_profit |
| category | category, product_category, product, sku, item |
| order_id | order_id, transaction_id, invoice_id |

**Required:** customer_id, date, spend. If ambiguous, ask the user.

Rename columns to canonical names before proceeding:
```python
df = df.rename({"user_column": "customer_id", "user_date": "date", ...})
```

## Step 3: Quality Gates

Run these checks. **STOP on errors. Warn on warnings.**

```python
# Nulls in required columns (ERROR)
for col in ["customer_id", "date", "spend"]:
    null_count = df[col].null_count()
    if null_count > 0:
        print(f"ERROR: {null_count} nulls in '{col}'")

# Negative spend (WARNING)
neg_spend = df.filter(pl.col("spend") < 0).height
if neg_spend > 0:
    print(f"WARNING: {neg_spend} rows with negative spend (returns?)")

# Date range (WARNING if < 90 days)
span = (df["date"].max() - df["date"].min()).days
if span < 90:
    print(f"WARNING: Only {span} days of data. Most analyses need >= 1 year.")

# Duplicate order IDs (WARNING -- may indicate line-item data)
if "order_id" in df.columns:
    n_unique = df["order_id"].n_unique()
    if n_unique < df.height:
        print(f"WARNING: {df.height - n_unique} duplicate order_ids (line-item data?)")
```

## Step 4: Aggregate to Orders

If data has duplicate order_ids (line-item level), collapse to one row per order:

```python
orders = df.group_by("order_id").agg(
    pl.col("customer_id").first(),
    pl.col("date").first(),
    pl.col("spend").sum(),
    pl.col("profit").sum(),  # if profit column exists
    pl.col("category").first(),  # if category column exists
)
```

If no order_id column, each row is already an order.

## Step 5: Create Period Labels

Auto-detect granularity: **quarterly** if data spans >= 2 years, **monthly** otherwise.

```python
span_years = (df["date"].max() - df["date"].min()).days / 365
granularity = "quarterly" if span_years >= 2 else "monthly"

if granularity == "quarterly":
    orders = orders.with_columns(
        (pl.col("date").dt.year().cast(pl.Utf8) + "-Q" + pl.col("date").dt.quarter().cast(pl.Utf8)).alias("period")
    )
elif granularity == "monthly":
    orders = orders.with_columns(
        pl.col("date").dt.strftime("%Y-%m").alias("period")
    )
```

## Step 6: Aggregate to Customer-Period Summaries

```python
cust_periods = orders.group_by("customer_id", "period").agg(
    pl.len().alias("num_transactions"),
    pl.col("spend").sum().alias("total_spend"),
    pl.col("profit").sum().alias("total_profit"),  # if profit exists
)
```

## Step 7: Assign Cohorts

Each customer's cohort = the period of their first purchase:

```python
cohorts = orders.group_by("customer_id").agg(
    pl.col("period").sort().first().alias("cohort")
)
orders = orders.join(cohorts, on="customer_id")
```

## Step 8: Save Outputs

```python
orders.write_parquet("output/prepared_data.parquet")
cust_periods.write_parquet("output/customer_summary.parquet")
```

## References
- `${CLAUDE_PLUGIN_ROOT}/references/methodology.md`
