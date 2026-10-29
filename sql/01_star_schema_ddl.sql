-- ==============================================================================
-- PROJECT 3: Commercial Profitability & Discount Leakage Executive Dashboard
-- SCRIPT: 01_star_schema_ddl.sql
-- DESCRIPTION: Star Schema Enterprise Data Warehouse DDL with referential integrity
-- AUTHOR: Shivastha Rewaskar
-- ==============================================================================

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_regions;

-- Dimension 1: Customers
CREATE TABLE dim_customers (
    customer_key        INTEGER PRIMARY KEY,
    customer_id         VARCHAR(20) UNIQUE NOT NULL,
    customer_name       VARCHAR(100) NOT NULL,
    customer_segment    VARCHAR(30) NOT NULL, -- Enterprise, Mid-Market, SMB
    credit_tier         VARCHAR(30) NOT NULL
);

-- Dimension 2: Products
CREATE TABLE dim_products (
    product_key         INTEGER PRIMARY KEY,
    product_name        VARCHAR(100) NOT NULL,
    category            VARCHAR(50) NOT NULL, -- Hardware, Software, Services
    unit_cost           DECIMAL(10, 2) NOT NULL,
    list_price          DECIMAL(10, 2) NOT NULL
);

-- Dimension 3: Regions
CREATE TABLE dim_regions (
    region_key          INTEGER PRIMARY KEY,
    region_name         VARCHAR(50) NOT NULL,
    territory_manager   VARCHAR(50) NOT NULL,
    country             VARCHAR(50) NOT NULL
);

-- Central Fact Table: Sales Transactions
CREATE TABLE fact_sales (
    order_line_id       INTEGER PRIMARY KEY,
    order_id            VARCHAR(30) NOT NULL,
    order_date          DATE NOT NULL,
    customer_key        INTEGER NOT NULL,
    product_key         INTEGER NOT NULL,
    region_key          INTEGER NOT NULL,
    quantity            INTEGER NOT NULL CHECK (quantity > 0),
    unit_list_price     DECIMAL(10, 2) NOT NULL,
    unit_cost           DECIMAL(10, 2) NOT NULL,
    gross_revenue       DECIMAL(12, 2) NOT NULL,
    discount_pct        DECIMAL(4, 2) NOT NULL,
    discount_amount     DECIMAL(12, 2) NOT NULL,
    net_revenue         DECIMAL(12, 2) NOT NULL,
    total_cogs          DECIMAL(12, 2) NOT NULL,
    net_profit          DECIMAL(12, 2) NOT NULL,
    margin_pct          DECIMAL(6, 2) NOT NULL,
    is_negative_margin  INTEGER CHECK (is_negative_margin IN (0, 1)),
    
    FOREIGN KEY (customer_key) REFERENCES dim_customers (customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_products (product_key),
    FOREIGN KEY (region_key) REFERENCES dim_regions (region_key)
);

-- Performance Indexes for OLAP & BI Queries
CREATE INDEX idx_fact_date ON fact_sales (order_date);
CREATE INDEX idx_fact_cust ON fact_sales (customer_key);
CREATE INDEX idx_fact_prod ON fact_sales (product_key);
CREATE INDEX idx_fact_reg ON fact_sales (region_key);
CREATE INDEX idx_fact_neg ON fact_sales (is_negative_margin);
