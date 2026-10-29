"""
Verification script for Project 3 Star Schema SQL scripts.
"""
import sqlite3
import csv
import os

db = sqlite3.connect(":memory:")
cursor = db.cursor()

base_dir = os.path.dirname(os.path.abspath(__file__))
schema_file = os.path.join(base_dir, "sql", "01_star_schema_ddl.sql")
data_dir = os.path.join(base_dir, "data")

with open(schema_file, "r") as f:
    cursor.executescript(f.read())

# Ingest Dimensions
with open(os.path.join(data_dir, "dim_regions.csv"), "r", encoding="utf-8") as f:
    cursor.executemany("INSERT INTO dim_regions VALUES (?,?,?,?)", 
        [(int(r["region_key"]), r["region_name"], r["territory_manager"], r["country"]) for r in csv.DictReader(f)])

with open(os.path.join(data_dir, "dim_products.csv"), "r", encoding="utf-8") as f:
    cursor.executemany("INSERT INTO dim_products VALUES (?,?,?,?,?)", 
        [(int(r["product_key"]), r["product_name"], r["category"], float(r["unit_cost"]), float(r["list_price"])) for r in csv.DictReader(f)])

with open(os.path.join(data_dir, "dim_customers.csv"), "r", encoding="utf-8") as f:
    cursor.executemany("INSERT INTO dim_customers VALUES (?,?,?,?,?)", 
        [(int(r["customer_key"]), r["customer_id"], r["customer_name"], r["customer_segment"], r["credit_tier"]) for r in csv.DictReader(f)])

# Ingest Fact Sales
with open(os.path.join(data_dir, "fact_sales.csv"), "r", encoding="utf-8") as f:
    cursor.executemany("INSERT INTO fact_sales VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
        [(int(r["order_line_id"]), r["order_id"], r["order_date"], int(r["customer_key"]), int(r["product_key"]),
          int(r["region_key"]), int(r["quantity"]), float(r["unit_list_price"]), float(r["unit_cost"]),
          float(r["gross_revenue"]), float(r["discount_pct"]), float(r["discount_amount"]),
          float(r["net_revenue"]), float(r["total_cogs"]), float(r["net_profit"]), float(r["margin_pct"]),
          int(r["is_negative_margin"])) for r in csv.DictReader(f)])

db.commit()
print("Project 3: Ingested Star Schema into SQLite successfully.")

# Test Query 2
with open(os.path.join(base_dir, "sql", "02_margin_leakage_audit.sql"), "r") as f:
    for i, q in enumerate([q.strip() for q in f.read().split(";") if q.strip()], 1):
        cursor.execute(q)
        print(f"Audit Query {i} returned {len(cursor.fetchall())} rows.")

# Test Query 3
with open(os.path.join(base_dir, "sql", "03_pareto_product_abc_analysis.sql"), "r") as f:
    for i, q in enumerate([q.strip() for q in f.read().split(";") if q.strip()], 1):
        cursor.execute(q)
        print(f"Pareto Query {i} returned {len(cursor.fetchall())} rows.")

db.close()
print("All Project 3 SQL queries executed cleanly with 0 errors!")
