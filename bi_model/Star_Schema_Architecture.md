# Star Schema Enterprise Architecture & Data Modeling
**Project:** Commercial Profitability & Discount Leakage Executive Dashboard  
**Author:** Shivastha Rewaskar  

---

### Entity Relationship Diagram (ERD) - Star Schema (1-to-Many)

```mermaid
erDiagram
    DIM_CUSTOMERS ||--o{ FACT_SALES : "places (1:N)"
    DIM_PRODUCTS ||--o{ FACT_SALES : "contains (1:N)"
    DIM_REGIONS ||--o{ FACT_SALES : "executes_in (1:N)"

    DIM_CUSTOMERS {
        int customer_key PK
        string customer_id
        string customer_name
        string customer_segment
        string credit_tier
    }

    DIM_PRODUCTS {
        int product_key PK
        string product_name
        string category
        decimal unit_cost
        decimal list_price
    }

    DIM_REGIONS {
        int region_key PK
        string region_name
        string territory_manager
        string country
    }

    FACT_SALES {
        int order_line_id PK
        string order_id
        date order_date
        int customer_key FK
        int product_key FK
        int region_key FK
        int quantity
        decimal unit_list_price
        decimal unit_cost
        decimal gross_revenue
        decimal discount_pct
        decimal discount_amount
        decimal net_revenue
        decimal total_cogs
        decimal net_profit
        decimal margin_pct
        int is_negative_margin
    }
```

---

### Data Warehouse Design Principles Applied

1. **Dimensional Integrity & Normalization:**
   - Single-grain transactions captured in `fact_sales` at the individual order-line level.
   - Dimension tables (`dim_customers`, `dim_products`, `dim_regions`) are normalized to eliminate duplicate descriptive text and optimize memory consumption in VertiPaq / Power BI.
2. **Surrogate Keys:**
   - Integer surrogate keys (`customer_key`, `product_key`, `region_key`) used for lightning-fast join performance, isolating the warehouse from upstream source system changes.
3. **Additive vs. Semi-Additive Measures:**
   - Fully additive: `Gross Revenue`, `Discount Amount`, `Net Revenue`, `Total COGS`, `Net Profit`.
   - Non-additive / Calculated via DAX: `Margin %`, `Average Discount %`, `Discount Leakage Index`.
