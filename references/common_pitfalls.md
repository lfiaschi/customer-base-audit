# Common Pitfalls Reference

14 common pitfalls to avoid when conducting a customer-base audit, based on "The Customer-Base Audit" by Fader, Hardie & Ross.

---

## 1. Aggregation Masking

**Description:** Relying on averages and totals to summarize customer behavior. Averages hide the massive heterogeneity that exists in any customer base. "The average customer" does not exist, yet most reporting systems implicitly assume it does.

**Why it matters:** The mean spend of $183 sounds reasonable until you learn the median is $113 and 69% of customers fall below the mean. Decisions based on the average customer will be wrong for the vast majority of actual customers. Aggregate metrics (e.g., overall repeat-buying rate, overall AOF) are weighted averages of cohort-specific numbers, pulled toward the newest cohort's behavior.

**How to avoid it:**
- Always examine distributions, not just averages.
- Perform decile analyses to reveal the concentration of value.
- Apply multiplicative decompositions to understand what drives observed totals.
- When reporting averages, always report the median alongside them and note what percentage of the base falls below the mean.

---

## 2. Survivor Bias

**Description:** Only analyzing customers who are currently active, ignoring those who have stopped purchasing. This makes the customer base look healthier than it is by excluding the large population of lapsed or one-and-done customers.

**Why it matters:** If you only look at active customers, you miss the fact that 45-70% of acquired customers never return. You also cannot assess the rate of attrition or the true economics of customer acquisition. The surviving cohort members are higher quality by construction -- they self-selected by continuing to buy.

**How to avoid it:**
- Always start analyses from the full cohort (all customers acquired in a period), not just those currently active.
- Report % active as a key metric, using cohort size as the denominator.
- Compute VTD (value to date) across the entire cohort, not just active members.
- Distinguish clearly between "average profit per active customer" and "average profit per cohort member."

---

## 3. Calendar vs. Cohort Confusion

**Description:** Analyzing customer behavior by calendar period (e.g., "2019 customers") without distinguishing between customers acquired at different times. Treating all customers in a period as a homogeneous group obscures cohort-specific dynamics.

**Why it matters:** Customers acquired in 2016 who are still active in 2019 behave very differently from those acquired in 2019. Mixing them together produces misleading averages. For example, the overall AOF of $1.9 masks the fact that active members of older cohorts have an AOF well above 2, while the newest cohort's AOF is below 1.5 in their acquisition year.

**How to avoid it:**
- Always decompose metrics by acquisition cohort.
- Use cohort-based analyses (Lenses 3-5) as the foundational approach.
- When using calendar-period metrics (Lenses 1-2), be explicit about the mix of cohorts.
- Use C3 charts to visualize how cohorts contribute to each period's totals.

---

## 4. Ignoring One-and-Done Customers

**Description:** Dismissing or excluding single-purchase customers from analysis because they "are not real customers" or "did not engage." In many businesses, these customers represent 40-70% of the acquired base.

**Why it matters:** One-and-done customers are part of the acquisition cost structure. They define the baseline from which repeat-purchase rates and cohort economics are calculated. Understanding their composition, entry categories, and the speed at which they can be identified as likely one-and-doners is critical for acquisition strategy.

**How to avoid it:**
- Include one-and-done customers in all cohort-level analyses.
- Track time-to-second-purchase curves to understand when one-and-done status becomes likely.
- Analyze entry categories and first-transaction behavior to identify predictors of future value.
- Compute "conditional" metrics alongside "unconditional" ones (e.g., VTD per cohort member vs. VTD per active member).

---

## 5. Revenue Focus vs. Profit Focus

**Description:** Conducting the entire audit using revenue rather than profit. While revenue is easier to measure, it can paint a misleading picture when products and customers have very different margins.

**Why it matters:** A customer who buys heavily discounted products may generate high revenue but negative profit. Revenue deciles and profit deciles tell different stories. One UK supermarket discovered a customer who generated over 120,000 GBP in losses over three years by exploiting loss-leader promotions.

**How to avoid it:**
- Transition to profit-based analysis as soon as cost data is available.
- Start with spend minus direct product costs; refine over time.
- At minimum, perform parallel revenue and profit decompositions to identify discrepancies.
- If profit data is unavailable, conduct the audit with revenue but flag this as a known limitation.

---

## 6. Static vs. Dynamic Analysis

**Description:** Performing only Lens 1 analyses (single-period snapshots) without examining how behavior changes over time. A snapshot tells you what the customer base looks like today but nothing about its trajectory.

**Why it matters:** Two businesses can have identical Lens 1 profiles but very different health trajectories. One may be acquiring higher-quality customers over time while the other is degrading. Period comparisons (Lens 2) and cohort analyses (Lenses 3-5) reveal the dynamics that snapshots cannot.

**How to avoid it:**
- Always complement Lens 1 with at least one longitudinal analysis (Lens 2, 3, or 5).
- Track cohort behavior over time to identify trends in quality and retention.
- Compare Lens 1 distributions across years; note that near-identical distributions can mask very different underlying dynamics.

---

## 7. Confusing Correlation with Causation in Category Analysis

**Description:** Observing that customers who buy in category X have higher lifetime value and concluding that promoting category X will increase customer value. The causation may run the other way: high-value customers explore more categories.

**Why it matters:** Madrigal's higher-value customers buy across more categories over time, but this is primarily because they make more transactions (higher AOF), giving them more opportunities to explore different categories. Their average number of categories per transaction is only slightly higher than lower-value customers. Pushing a customer into a new category may not change their underlying buying rate.

**How to avoid it:**
- Distinguish between categories that predict value (diagnostic) and categories that drive value (causal).
- Examine whether cross-category buying happens within transactions or across transactions.
- Use entry-category analysis to identify categories associated with higher VTD, but test causal hypotheses with experiments.
- Track whether customers are truly broadening their category repertoire year over year, or simply rotating among categories.

---

## 8. Not Accounting for Seasonality

**Description:** Making period-over-period or cohort comparisons without controlling for seasonal effects. Q4 cohorts behave differently from Q2 cohorts, and Q4 metrics look different from Q2 metrics.

**Why it matters:** For Madrigal, about 45% of annual acquisitions occur in Q4. Q4 cohorts have higher initial repeat-purchase rates (driven by holiday shopping) but may not sustain that pattern. Comparing a Q4 cohort to a Q2 cohort without accounting for seasonality can produce misleading conclusions about cohort quality.

**How to avoid it:**
- Compare same-season cohorts (e.g., Q4/2016 vs. Q4/2017) to control for seasonal effects.
- Use calendar-aligned plots alongside left-aligned plots to separate seasonal from cohort effects.
- When analyzing quarterly data, be aware that Q4 spikes affect both activity rates and average spend.
- Decompose seasonal effects in AOF and AOV separately.

---

## 9. Using Wrong Time Granularity

**Description:** Choosing an analysis period that is too coarse or too fine for the business. Annual analysis may miss important quarterly dynamics; weekly analysis may introduce too much noise.

**Why it matters:** For Madrigal, annual analysis is a natural starting point, but quarterly analysis reveals critical seasonal patterns (especially the Q4 acquisition spike). Conversely, the authors chose not to present full quarterly Lens 5 analyses because there was "an overwhelming amount of detail." The right granularity depends on purchase frequency and business rhythm.

**How to avoid it:**
- Start with the granularity that matches your business reporting cycle (annual or quarterly).
- Move to finer granularity only when coarser analysis reveals patterns that need further exploration.
- For time-to-second-purchase analysis, use weekly granularity to capture early dynamics.
- For cross-cohort comparisons, quarterly cohorts often provide the best balance of detail and interpretability.

---

## 10. Ignoring Acquisition Cost in Bottom Deciles

**Description:** Evaluating customer profitability based solely on gross margin from transactions, without considering the cost of acquiring the customer. Bottom-decile customers who appear marginally profitable may actually be value-destroying when acquisition costs are included.

**Why it matters:** Many firms spend substantial amounts on customer acquisition via digital advertising, promotions, and other channels. A UK retailer discovered that at the keyword level, "the vast majority had customer acquisition costs of more than 30 GBP" while "most of their customers had a value of less than 30 GBP." The aggregate averages had given "a completely misleading picture of performance."

**How to avoid it:**
- Track customer acquisition cost (CAC) by channel and campaign.
- Compare CAC to expected customer value (VTD or projected CLV) at the channel/campaign level.
- Perform the "customer payback" analysis: how long does it take for a customer's cumulative profit to exceed their acquisition cost?
- Do not rely on averages across channels; analyze at the most granular level feasible.

---

## 11. Treating All Cohorts as Identical

**Description:** Assuming that customers acquired in different time periods have the same behavior and value. This ignores changes in acquisition strategy, competitive environment, product mix, and market conditions.

**Why it matters:** Cohort quality can degrade subtly over time. For Madrigal, more recently acquired cohorts showed "slightly slower" development of repeat buying. Companies that aggregate across cohorts will not detect this degradation until it has accumulated over 2-3 years and visibly impacts the customer base as a whole.

**How to avoid it:**
- Always perform Lens 4 comparisons when multiple cohorts are available.
- Track repeat-buying rates and time-to-second-purchase across cohorts.
- Investigate changes in acquisition channels, marketing spend, and promotions that may explain cross-cohort differences.
- Monitor for "acquisition-quality inflation" where acquisition targets are met but customer quality declines.

---

## 12. Not Validating Decomposition Arithmetic

**Description:** Reporting decomposition components (AOF, AOV, margin) without verifying that their product equals the reported total. Rounding, weighted vs. unweighted averages, and inconsistent definitions can cause decompositions to fail to reconcile.

**Why it matters:** The difference between weighted and unweighted averages of AOV can be meaningful (Madrigal: $96 weighted vs. $98 unweighted). Presenting a decomposition that does not reconcile to the known total undermines the credibility of the analysis and may indicate a data or methodology error.

**How to avoid it:**
- Always verify: `#customers x AOF x AOV x avg_margin = reported profit` (within rounding tolerance).
- Be explicit about whether averages are weighted or unweighted.
- Document which definition is used and why.
- Cross-check category-level decompositions against firm-level totals.

---

## 13. Over-Interpreting Small Cohorts

**Description:** Drawing strong conclusions from cohorts with small sample sizes. If a quarterly cohort has only a few hundred members, percentages and averages become unreliable.

**Why it matters:** Small cohorts produce noisy estimates. A cohort of 200 customers where 10 are in the top decile provides very unreliable estimates of top-decile behavior. Extreme values from individual customers can heavily influence small-cohort averages.

**How to avoid it:**
- Report cohort sizes alongside all cohort-level metrics.
- Be cautious about drawing conclusions from cohorts with fewer than several thousand members.
- Consider combining small cohorts when the analysis permits.
- When comparing cohorts, note the relative sizes and flag comparisons where one cohort is substantially smaller.

---

## 14. Ignoring the Product Dimension Entirely

**Description:** Conducting the entire customer-base audit on the customer x time face without ever reintroducing the product dimension. This leaves important questions unanswered: Which categories drive profitable relationships? Which products serve as entry points?

**Why it matters:** Product-level analysis reveals that higher-value customers buy more items per category order (not more categories per transaction), that entry categories predict lifetime value, and that category penetration is the primary driver of category-level profit differences. Without this analysis, the audit is incomplete.

**How to avoid it:**
- Include Chapter 8-style product-dimension analyses in every audit.
- Compute category-level decompositions: penetration, ACOF, ACOV, avg category margin.
- Analyze co-purchasing patterns and entry categories.
- Examine category buying breadth by decile and by cohort over time.
- Connect product insights to acquisition and retention strategies.

---

## Summary Checklist

Before finalizing a customer-base audit, verify that you have not:

- [ ] Relied on averages without examining distributions
- [ ] Excluded inactive or one-and-done customers from analyses
- [ ] Mixed cohorts in period-level analysis without acknowledgment
- [ ] Dismissed one-and-done customers as irrelevant
- [ ] Used revenue when profit was available
- [ ] Limited analysis to a single-period snapshot
- [ ] Assumed category correlations imply causation
- [ ] Compared different-season cohorts without seasonal adjustment
- [ ] Chosen an inappropriate time granularity
- [ ] Ignored acquisition costs in profitability assessment
- [ ] Assumed all cohorts behave identically
- [ ] Presented decompositions that do not reconcile
- [ ] Drawn conclusions from small sample sizes
- [ ] Omitted product-dimension analysis entirely
