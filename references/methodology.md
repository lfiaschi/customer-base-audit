# Customer-Base Audit Methodology Reference

Based on "The Customer-Base Audit" by Fader, Hardie & Ross (Wharton School Press).

---

## The Data Cube

A firm's transaction database can be conceptualized as a three-dimensional cube with edges representing:

- **Customer** -- who made the purchase
- **Time** -- when it occurred
- **Product** -- what was purchased

Most organizations report from the **product x time** face, aggregating over the customer dimension. A customer-base audit pivots orientation to the **customer x time** face, aggregating over the product dimension. Chapter 8 reintroduces the product dimension to complete the picture.

### Data Requirements

The minimum dataset for Lenses 1-5 is an order-level summary:

| Field | Description |
|---|---|
| Order_ID | Unique transaction identifier |
| Customer_ID | Unique customer identifier |
| Date | Transaction date |
| Spend | Net revenue (after discounts and returns) |
| Profit | Spend minus allocated costs |

For product-dimension analyses, SKU-level line items are also needed.

---

## The Five Lenses Framework

### Lens 1 -- Customer Heterogeneity (Chapter 3)

**View:** A single vertical slice of the customer x time face (one period, typically a year or quarter).

**Purpose:** Uncover the extent to which customers differ in their buying behavior and value.

**Core analyses:**

1. **Distributions** -- Plot frequency distributions of:
   - Total spend per customer (right-skewed; mean > median)
   - Number of transactions per customer (right-skewed; modal value is 1)
   - Average spend per transaction (right-skewed)
   - Total profit per customer (right-skewed)
   - Average margin per customer (relatively symmetric)

2. **Decompositions** -- Apply multiplicative decomposition:
   - `profit = #customers x AOF x AOV x avg_margin`
   - `revenue = #customers x AOF x AOV`
   - `total_spend = #transactions x avg_spend_per_transaction`

3. **Decile analysis** -- Two variants:
   - **Equal-customer deciles:** Each decile contains 10% of customers, sorted by profitability. Reveals concentration (e.g., top 10% = 40% of profit).
   - **Equal-profit deciles:** Each decile accounts for 10% of profit. Reveals how few customers drive each slice of profit (e.g., top decile may contain only 1% of customers).
   - For each decile, report AOF, AOV, and average margin.

**Key insight:** "There is no average customer." The three Ds -- distribution, decomposition, decile -- are the foundational analytical tools.

---

### Lens 2 -- Behavioral Change / Period Comparison (Chapter 4)

**View:** Two adjacent vertical slices of the customer x time face (two periods).

**Purpose:** Identify changes in buyer behavior from one period to the next.

**Core analyses:**

1. **Customer overlap (Venn diagram)** -- Classify customers into three groups:
   - Period 1 only (not active in Period 2)
   - Both periods (active in both)
   - Period 2 only (not active in Period 1)

2. **Additive decomposition of profit** -- Break each period's profit by customer group.

3. **Multiplicative decomposition by group** -- For each group, decompose:
   - `profit = #customers x AOF x AOV x avg_margin`
   - Compare "same-customer" performance (those active in both periods).

4. **Decile switching analysis** -- Cross-tabulate profit decile membership across periods.
   - Use common decile boundaries for both periods.
   - Examine the diagonal (stable), above-diagonal (dropped), below-diagonal (rose).
   - Extended diagonal (+/- 1 decile) typically captures ~49% of both-period customers.

5. **Up/Down analysis** -- For each customer active in both periods, classify whether each component went up or down:
   - Profit direction (up/down)
   - Number of transactions (up/down)
   - Average spend per transaction (up/down)
   - Average margin (up/down)
   - Results in 16 possible groups; summarize customer counts and profit changes.

**Key insight:** Roughly 80% of customers active across a two-year span are active in only one of the two years. Those active in both periods are typically more valuable (higher AOF).

---

### Lens 3 -- Cohort Evolution (Chapter 5)

**View:** A single horizontal slice of the customer x time face (one cohort tracked over time).

**Purpose:** Identify patterns of change -- usually decay -- in buying behavior over time from acquisition.

**Core analyses:**

1. **Revenue decomposition over time:**
   ```
   cohort_revenue = cohort_size x %_cohort_active x avg_spend_per_active_member
   avg_spend_per_active_member = AOF x AOV
   ```
   Plot each component over successive quarters/years.

2. **Activity patterns** -- For each cohort member, record yes/no activity in each subsequent period. Enumerate all 2^n patterns to identify:
   - One-and-done rate (typically 40-70% never make a second purchase)
   - Consistent repeat buyers (active every period, typically 5-10%)
   - Intermittent buyers (inactive in one period but return later)

3. **Repeat-buying rates** -- Percentage of cohort active in one period who are also active in the next. Rates typically increase with cohort age as lighter buyers drop out.

4. **Time to second purchase** -- Cumulative plot of % of cohort making their second-ever purchase over weeks since acquisition. More than half of eventual repeat buyers typically do so within 16 weeks.

5. **Time to nth purchase** -- Extend the analysis to 2nd-to-3rd, 3rd-to-4th, etc. The gap between successive purchases typically decreases (a "depth of repeat" analysis).

6. **Value-to-date (VTD) distribution** -- Cumulative profit from acquisition through the present, analyzed via:
   - VTD distribution (right-skewed)
   - VTD-based decile analysis
   - Decomposition: VTD = sum of (AOF x AOV x avg_margin) across active periods

**Key insight:** Revenue decline is driven primarily by declining % active, not by declining spend among active members. A cohort "shakes out" -- lighter buyers drop away, but surviving members maintain relatively stable behavior.

---

### Lens 4 -- Cohort Comparison (Chapter 6)

**View:** Two or more horizontal slices of the customer x time face (multiple cohorts compared).

**Purpose:** Compare the quality and quantity of customers acquired in different periods.

**Core analyses:**

1. **Left-aligned comparison** -- Plot % active, AOF, AOV, and margin over cohort age (periods since acquisition) for two or more cohorts. This reveals differences in cohort quality.

2. **Calendar-aligned comparison** -- Plot the same metrics by calendar time. This reveals macro effects (e.g., pricing/promotional changes) versus cohort-specific effects.

3. **Time to second purchase comparison** -- Compare cumulative and incremental plots across cohorts to assess differences in early engagement.

4. **Annual buying patterns** -- Compare year-by-year repeat-buying rates across cohorts to detect degradation or improvement.

**Key insight:** Cross-cohort stability is generally preferable. Subtle degradation across cohorts is an early warning sign that may not appear in aggregate metrics until it has accumulated over several years.

---

### Lens 5 -- Customer-Base Health (Chapter 7)

**View:** The entire customer x time face (all cohorts across all periods).

**Purpose:** Provide an overall customer-centric assessment of firm health.

**Core analyses:**

1. **C3 chart (Customer Cohort Chart)** -- Stacked bar chart showing each year's profit decomposed by acquisition cohort. Reveals:
   - What fraction of profit comes from new vs. existing customers
   - How cohort profit "retains" from one year to the next
   - Whether the firm is growing through acquisition, development, or both

2. **Acquisition flow** -- Plot number of customers acquired per period. Monitor trends and seasonality.

3. **Active customer evolution** -- Stacked bar chart showing active customer counts by cohort over time.

4. **Cross-cohort decomposition** -- For each cohort and year, compute:
   - % cohort active
   - Average profit per active customer
   - AOF, AOV, average margin
   Plot these over time for all cohorts on the same axes.

5. **Repeat-buying development** -- Table showing cumulative % of each cohort making their second-ever purchase over years since acquisition (Table 7.3 in the book).

6. **Repeat-buying rates by cohort** -- Table showing annual repeat-buying rates by cohort and overall (Table 7.4 in the book). Rates rise with cohort age, reflecting the shakeout of lighter buyers.

7. **Back-of-envelope forecasting** -- Use observed repeat-buying rates and acquisition trends to project next-period customer counts and revenue.

**Key insight:** Growth is decomposed into acquisition, retention, and development. Average metrics across all customers are weighted averages of cohort-specific metrics, dominated by the newest (and typically least valuable) cohort.

---

### Product Dimension (Chapter 8)

**View:** Reintroduces the product edge of the data cube into the customer x time analysis.

**Purpose:** Understand how customer differences are manifested in product purchasing and how product performance benefits from customer visibility.

**Core analyses:**

1. **Category decomposition:**
   ```
   category_profit = #active_firm_customers
                      x category_penetration
                      x ACOF
                      x ACOV
                      x avg_category_margin
   ```
   Where:
   - `category_penetration` = % of active customers who bought in the category
   - `ACOF` = average *category* order frequency (among category buyers)
   - `ACOV` = average *category* order value

2. **AOV decomposition:**
   ```
   AOV = avg_units_per_transaction x avg_price_per_unit
   ```

3. **Units-per-transaction decomposition:**
   ```
   avg_units_per_transaction = avg_units_per_category x avg_categories_per_transaction
   ```

4. **Category buying breadth** -- By decile: avg number of categories, avg number of unique SKUs.

5. **Co-purchasing analysis** -- For each category, compute % of category buyers who also bought in each other category. Identify the most common additional category.

6. **Sole-category buyers** -- % of customers who only purchased from a single category.

7. **Category penetration evolution** -- Track cumulative % of a cohort that has ever bought in each category over time. Higher-penetration categories grow more slowly; lower-penetration categories show higher growth rates.

8. **Entry categories** -- Which categories appear on customers' first-ever transaction? Compute VTD index for customers whose first transaction included each category.

**Key insight:** Higher-value customers buy more often (higher AOF) and buy more items per transaction (higher avg units). They do not generally buy more categories per transaction, but their higher AOF means they purchase across more categories over time. Some categories serve as "entry points" that predict higher lifetime value.

---

## Decomposition Formulas Summary

### Firm-Level Decomposition

| Formula | Components |
|---|---|
| `revenue = #customers x AOF x AOV` | AOF = avg order frequency; AOV = avg order value |
| `profit = #customers x AOF x AOV x avg_margin` | avg_margin = profit / revenue |
| `AOV = avg_units_per_transaction x avg_price_per_unit` | Units and price decomposition |
| `avg_units_per_transaction = avg_units_per_category x avg_categories_per_transaction` | Breadth vs depth |

### Cohort-Level Decomposition

| Formula | Components |
|---|---|
| `cohort_revenue = cohort_size x %_active x AOF x AOV` | %_active = fraction of cohort making 1+ purchases |
| `cohort_profit = cohort_size x %_active x AOF x AOV x avg_margin` | Full profit decomposition |

### Category-Level Decomposition

| Formula | Components |
|---|---|
| `category_profit = #active_customers x penetration x ACOF x ACOV x avg_cat_margin` | ACOF/ACOV are category-specific |
| `#category_buyers = #active_customers x penetration` | penetration = % active in category |
| `ACOV = avg_units_per_category_order x avg_price_per_unit` | Category-level price/quantity |

### Period Comparison Decomposition

| Formula | Components |
|---|---|
| `total_profit = profit_period1_only + profit_both + profit_period2_only` | Additive by customer group |
| Per group: `profit = #customers x AOF x AOV x avg_margin` | Multiplicative within each group |

---

## Analytical Principles

1. **Three Ds:** Distribution, Decomposition, Decile -- the foundational tools for every lens.
2. **Averages are misleading:** Always examine distributions; the mean is not representative in right-skewed distributions.
3. **Cohorts, not segments:** Cohort membership is fixed, making longitudinal analysis meaningful. Segment membership changes over time.
4. **Audit first, models later:** Descriptive analysis provides the foundation for any predictive modeling.
5. **Multiplicative decompositions** reveal which components drive observed differences.
6. **Additive decompositions** reveal which groups contribute to observed totals.
