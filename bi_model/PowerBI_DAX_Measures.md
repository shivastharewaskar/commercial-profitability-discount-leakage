# Power BI Enterprise DAX Calculation Reference
**Project:** Commercial Profitability & Discount Leakage Executive Dashboard  
**Author:** Shivastha Rewaskar  

---

### 1. Revenue & Margin Base Measures

#### Total Gross Revenue
```dax
Total Gross Revenue = SUM(fact_sales[gross_revenue])
```

#### Total Discounts Granted (Discount Leakage)
```dax
Total Discount Amount = SUM(fact_sales[discount_amount])
```

#### Total Net Realized Revenue
```dax
Total Net Revenue = SUM(fact_sales[net_revenue])
```

#### Total Cost of Goods Sold (COGS)
```dax
Total COGS = SUM(fact_sales[total_cogs])
```

#### Total Net Operating Profit
```dax
Total Net Profit = [Total Net Revenue] - [Total COGS]
```

#### Realized Operating Margin %
```dax
Operating Margin % = 
DIVIDE(
    [Total Net Profit],
    [Total Net Revenue],
    0
)
```

---

### 2. Discount Sensitivity & Underwater Audit Measures

#### Average Effective Discount Rate %
```dax
Effective Discount Rate % = 
DIVIDE(
    [Total Discount Amount],
    [Total Gross Revenue],
    0
)
```

#### Loss-Making Transactions Count
```dax
Underwater Deals Count = 
CALCULATE(
    COUNTROWS(fact_sales),
    fact_sales[net_profit] < 0
)
```

#### Direct Profit Drain from Underwater Deals ($)
```dax
Underwater Profit Drain = 
CALCULATE(
    SUM(fact_sales[net_profit]),
    fact_sales[net_profit] < 0
)
```

---

### 3. Dynamic "What-If" Parameter Capping Slider

*Enables C-suite executives to slide a discount cap from 0% to 30% and instantly see recovered EBITDA.*

#### Dynamic Discount Capped Profit ($)
```dax
Simulated Capped Profit = 
VAR CapRate = 'Discount Cap Parameter'[Discount Cap Value] -- e.g. 0.18
RETURN
    SUMX(
        fact_sales,
        VAR EffectiveDisc = MIN(fact_sales[discount_pct], CapRate)
        VAR NewNetRev = fact_sales[gross_revenue] * (1 - EffectiveDisc)
        RETURN NewNetRev - fact_sales[total_cogs]
    )
```

#### EBITDA Expansion Delta ($)
```dax
EBITDA Expansion Delta = [Simulated Capped Profit] - [Total Net Profit]
```
