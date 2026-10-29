-- ==============================================================================
-- PROJECT 3: Commercial Profitability & Discount Leakage Executive Dashboard
-- SCRIPT: 02_margin_leakage_audit.sql
-- DESCRIPTION: Diagnoses margin erosion, negative net profit transactions, and rep variance
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- QUERY 1: The Discount Cliff - Profitability by Discount Depth Tier
-- Uncovers the exact tipping point where discounts destroy unit margins
-- ------------------------------------------------------------------------------
SELECT 
    CASE 
        WHEN discount_pct = 0.0 THEN '0% Full Price'
        WHEN discount_pct <= 0.10 THEN '1% - 10% Standard'
        WHEN discount_pct <= 0.20 THEN '11% - 20% Negotiated'
        WHEN discount_pct <= 0.30 THEN '21% - 30% Aggressive'
        ELSE '> 30% Deep Discount'
    END AS discount_tier,
    COUNT(order_line_id) AS transaction_count,
    ROUND(SUM(gross_revenue), 2) AS total_gross_revenue,
    ROUND(SUM(discount_amount), 2) AS total_discounts_given,
    ROUND(SUM(net_revenue), 2) AS total_net_revenue,
    ROUND(SUM(net_profit), 2) AS total_net_profit,
    ROUND(SUM(net_profit) * 100.0 / NULLIF(SUM(net_revenue), 0), 2) AS realized_margin_pct,
    SUM(is_negative_margin) AS loss_making_transactions,
    ROUND(SUM(CASE WHEN is_negative_margin = 1 THEN net_profit ELSE 0 END), 2) AS total_negative_profit_loss
FROM fact_sales
GROUP BY discount_tier
ORDER BY total_discounts_given DESC;

-- ------------------------------------------------------------------------------
-- QUERY 2: Product Category Margin Sensitivity & Loss Exposure
-- Identifies low-margin Hardware being sold at software-level discounts
-- ------------------------------------------------------------------------------
SELECT 
    p.category,
    p.product_name,
    COUNT(f.order_line_id) AS units_sold,
    ROUND(AVG(f.discount_pct) * 100, 1) AS avg_discount_pct,
    ROUND(SUM(f.gross_revenue), 2) AS gross_sales,
    ROUND(SUM(f.discount_amount), 2) AS discount_leakage,
    ROUND(SUM(f.net_revenue), 2) AS net_sales,
    ROUND(SUM(f.total_cogs), 2) AS total_cogs,
    ROUND(SUM(f.net_profit), 2) AS net_profit,
    ROUND(SUM(f.net_profit) * 100.0 / NULLIF(SUM(f.net_revenue), 0), 2) AS category_margin_pct,
    SUM(f.is_negative_margin) AS loss_making_orders
FROM fact_sales f
JOIN dim_products p ON f.product_key = p.product_key
GROUP BY p.category, p.product_name
ORDER BY loss_making_orders DESC, net_profit ASC;

-- ------------------------------------------------------------------------------
-- QUERY 3: Regional Sales Rep Discounting Accountability Ledger
-- Analyzes territory managers overusing discounts to hit top-line quotas
-- ------------------------------------------------------------------------------
SELECT 
    r.region_name,
    r.territory_manager,
    COUNT(f.order_line_id) AS total_deals_closed,
    ROUND(SUM(f.net_revenue), 2) AS total_net_revenue,
    ROUND(SUM(f.discount_amount), 2) AS total_discount_granted,
    ROUND(AVG(f.discount_pct) * 100, 1) AS avg_discount_pct,
    ROUND(SUM(f.net_profit), 2) AS total_net_profit,
    ROUND(SUM(f.net_profit) * 100.0 / NULLIF(SUM(f.net_revenue), 0), 2) AS realized_margin_pct,
    SUM(f.is_negative_margin) AS underwater_deals_count,
    ROUND(SUM(CASE WHEN f.is_negative_margin = 1 THEN f.net_profit ELSE 0 END), 2) AS underwater_margin_drain_usd
FROM fact_sales f
JOIN dim_regions r ON f.region_key = r.region_key
GROUP BY r.region_name, r.territory_manager
ORDER BY underwater_deals_count DESC;
