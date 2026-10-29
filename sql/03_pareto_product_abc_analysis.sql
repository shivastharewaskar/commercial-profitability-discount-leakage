-- ==============================================================================
-- PROJECT 3: Commercial Profitability & Discount Leakage Executive Dashboard
-- SCRIPT: 03_pareto_product_abc_analysis.sql
-- DESCRIPTION: Product ABC Pareto classification ranking cumulative revenue vs margin
-- ==============================================================================

WITH product_financials AS (
    SELECT 
        p.product_key,
        p.product_name,
        p.category,
        SUM(f.net_revenue) AS product_net_revenue,
        SUM(f.net_profit) AS product_net_profit,
        ROUND(SUM(f.net_profit) * 100.0 / NULLIF(SUM(f.net_revenue), 0), 2) AS product_margin_pct
    FROM fact_sales f
    JOIN dim_products p ON f.product_key = p.product_key
    GROUP BY p.product_key, p.product_name, p.category
),
ranked_products AS (
    SELECT 
        product_key,
        product_name,
        category,
        product_net_revenue,
        product_net_profit,
        product_margin_pct,
        SUM(product_net_revenue) OVER () AS total_company_revenue,
        SUM(product_net_revenue) OVER (ORDER BY product_net_revenue DESC) AS running_net_revenue
    FROM product_financials
)
SELECT 
    product_name,
    category,
    ROUND(product_net_revenue, 2) AS net_revenue_usd,
    ROUND(product_net_profit, 2) AS net_profit_usd,
    product_margin_pct,
    ROUND(running_net_revenue, 2) AS cumulative_revenue_usd,
    ROUND((running_net_revenue * 100.0) / total_company_revenue, 2) AS cumulative_revenue_pct,
    CASE 
        WHEN (running_net_revenue * 100.0) / total_company_revenue <= 70.0 THEN 'Class A (Core Growth Engine)'
        WHEN (running_net_revenue * 100.0) / total_company_revenue <= 90.0 THEN 'Class B (Stable Mid-Tier)'
        ELSE 'Class C (Long Tail / Evaluate Margins)'
    END AS pareto_abc_classification
FROM ranked_products
ORDER BY product_net_revenue DESC;
