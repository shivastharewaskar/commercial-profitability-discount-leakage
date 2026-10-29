"""
Commercial Profitability & Discount Leakage Data Generator
Generates relational tables adhering to an enterprise Star Schema:
- dim_customers.csv
- dim_products.csv
- dim_regions.csv
- fact_sales.csv

Simulates real commercial dynamics:
- Revenue growth with declining net margin %
- Deep discounting (>25%) on low-margin product lines leading to negative profit
- Regional sales rep discounting variance
"""

import csv
import random
import datetime
import os

random.seed(202)

START_DATE = datetime.date(2025, 1, 1)
END_DATE = datetime.date(2025, 12, 31)
TOTAL_TRANSACTIONS = 7500

# Dimension 1: Regions
REGIONS = [
    {"region_key": 1, "region_name": "North America - East", "territory_manager": "Sarah Jenkins", "country": "USA"},
    {"region_key": 2, "region_name": "North America - West", "territory_manager": "Marcus Vance", "country": "USA"},
    {"region_key": 3, "region_name": "EMEA - Central", "territory_manager": "Elena Rostova", "country": "Germany"},
    {"region_key": 4, "region_name": "APAC - South", "territory_manager": "Rajesh Kumar", "country": "Singapore"},
    {"region_key": 5, "region_name": "LATAM", "territory_manager": "Carlos Mendez", "country": "Brazil"}
]

# Dimension 2: Products (Categories with base cost & list price)
PRODUCTS = [
    {"product_key": 101, "product_name": "Enterprise Server Rack X1", "category": "Hardware", "unit_cost": 3200.00, "list_price": 4200.00},
    {"product_key": 102, "product_name": "Cloud Security Suite Pro", "category": "Software", "unit_cost": 250.00, "list_price": 1200.00},
    {"product_key": 103, "product_name": "Edge AI Gateway Node", "category": "Hardware", "unit_cost": 850.00, "list_price": 1150.00},
    {"product_key": 104, "product_name": "Data Analytics Platform (Annual)", "category": "Software", "unit_cost": 400.00, "list_price": 2800.00},
    {"product_key": 105, "product_name": "Implementation & Deployment Pack", "category": "Professional Services", "unit_cost": 1500.00, "list_price": 2200.00},
    {"product_key": 106, "product_name": "Managed Infrastructure Support (24/7)", "category": "Professional Services", "unit_cost": 1800.00, "list_price": 3100.00},
    {"product_key": 107, "product_name": "Industrial IoT Sensor Hub", "category": "Hardware", "unit_cost": 420.00, "list_price": 540.00},
    {"product_key": 108, "product_name": "Cyber Threat Scanner (Endpoint)", "category": "Software", "unit_cost": 80.00, "list_price": 450.00}
]

# Dimension 3: Customers
CUSTOMER_NAMES = [
    "Acme Global", "Apex Financial", "Nexus Health", "Vanguard Logistics", "Omni Retail",
    "Pinnacle Tech", "Starlight Media", "BlueWave Energy", "Horizon Bio", "Summit Telecom",
    "Titan Heavy Industries", "Nova Consulting", "Crestview Capital", "Aegis Security", "Synergy Corp"
]

def generate_relational_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate Customers
    customers = []
    for c_key in range(1, 201):
        c_name = f"{random.choice(CUSTOMER_NAMES)} {random.choice(['Group', 'International', 'Holdings', 'LLC', 'Inc'])} #{c_key}"
        segment = random.choices(["Enterprise", "Mid-Market", "SMB"], weights=[0.25, 0.40, 0.35])[0]
        credit = random.choices(["Tier 1 (Prime)", "Tier 2 (Standard)", "Tier 3 (Review)"], weights=[0.50, 0.40, 0.10])[0]
        customers.append({
            "customer_key": c_key,
            "customer_id": f"CUST-REL-{c_key:04d}",
            "customer_name": c_name,
            "customer_segment": segment,
            "credit_tier": credit
        })
        
    # Write Dimension Tables
    with open(os.path.join(base_dir, "dim_regions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(REGIONS[0].keys()))
        w.writeheader()
        w.writerows(REGIONS)
        
    with open(os.path.join(base_dir, "dim_products.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(PRODUCTS[0].keys()))
        w.writeheader()
        w.writerows(PRODUCTS)
        
    with open(os.path.join(base_dir, "dim_customers.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(customers[0].keys()))
        w.writeheader()
        w.writerows(customers)
        
    # Generate Fact Sales
    delta_days = (END_DATE - START_DATE).days
    sales_facts = []
    
    for line_id in range(1, TOTAL_TRANSACTIONS + 1):
        tx_date = START_DATE + datetime.timedelta(days=random.randint(0, delta_days))
        cust = random.choice(customers)
        prod = random.choice(PRODUCTS)
        reg = random.choice(REGIONS)
        
        # Quantity based on product category
        if prod["category"] == "Hardware":
            qty = random.choices([1, 2, 3, 5, 10], weights=[0.45, 0.25, 0.15, 0.10, 0.05])[0]
        elif prod["category"] == "Software":
            qty = random.choices([5, 10, 20, 50, 100], weights=[0.30, 0.30, 0.20, 0.15, 0.05])[0]
        else:
            qty = random.choices([1, 2, 3, 4], weights=[0.50, 0.30, 0.15, 0.05])[0]
            
        list_price = prod["list_price"]
        unit_cost = prod["unit_cost"]
        gross_rev = round(list_price * qty, 2)
        total_cost = round(unit_cost * qty, 2)
        
        # Realistic Discount Distribution:
        # Aggressive discounting frequently seen in NA-West and APAC, or SMB accounts
        if reg["region_name"] in ["North America - West", "APAC - South"] or cust["customer_segment"] == "SMB":
            discount_pct = random.choices([0.0, 0.10, 0.15, 0.20, 0.25, 0.32, 0.38], weights=[0.15, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05])[0]
        else:
            discount_pct = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.35, 0.25, 0.20, 0.15, 0.05])[0]
            
        discount_amount = round(gross_rev * discount_pct, 2)
        net_rev = round(gross_rev - discount_amount, 2)
        net_profit = round(net_rev - total_cost, 2)
        margin_pct = round((net_profit / net_rev) * 100, 2) if net_rev > 0 else -100.0
        
        is_negative_margin = 1 if net_profit < 0 else 0
        
        sales_facts.append({
            "order_line_id": line_id,
            "order_id": f"ORD-2025-{1000 + (line_id // 2)}",
            "order_date": tx_date.strftime("%Y-%m-%d"),
            "customer_key": cust["customer_key"],
            "product_key": prod["product_key"],
            "region_key": reg["region_key"],
            "quantity": qty,
            "unit_list_price": list_price,
            "unit_cost": unit_cost,
            "gross_revenue": gross_rev,
            "discount_pct": discount_pct,
            "discount_amount": discount_amount,
            "net_revenue": net_rev,
            "total_cogs": total_cost,
            "net_profit": net_profit,
            "margin_pct": margin_pct,
            "is_negative_margin": is_negative_margin
        })
        
    with open(os.path.join(base_dir, "fact_sales.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(sales_facts[0].keys()))
        w.writeheader()
        w.writerows(sales_facts)
        
    print(f"Generated Star Schema: 3 Dimensions + {len(sales_facts)} Fact Sales records at {base_dir}")

if __name__ == "__main__":
    generate_relational_data()
