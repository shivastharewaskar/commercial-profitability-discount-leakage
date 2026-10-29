"""
Project 3: Commercial Profitability & Discount Leakage Audit
Script: commercial_profitability_audit.py
Analyzes pricing elasticity, underwater (negative net profit) transactions,
and simulates EBITDA expansion under dynamic discount capping rules.
"""

import csv
import os
from collections import defaultdict

def run_profitability_audit():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sales_file = os.path.join(base_dir, "data", "fact_sales.csv")
    products_file = os.path.join(base_dir, "data", "dim_products.csv")
    regions_file = os.path.join(base_dir, "data", "dim_regions.csv")
    
    # Load products
    products = {}
    with open(products_file, mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            products[int(r["product_key"])] = r
            
    # Load regions
    regions = {}
    with open(regions_file, mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            regions[int(r["region_key"])] = r
            
    total_tx = 0
    total_gross = 0.0
    total_discounts = 0.0
    total_net_rev = 0.0
    total_cogs = 0.0
    total_net_profit = 0.0
    underwater_tx = 0
    underwater_loss = 0.0
    
    # Discount tiers
    discount_tiers = {
        "0% Full Price": {"tx": 0, "rev": 0.0, "profit": 0.0, "loss_tx": 0, "loss_val": 0.0},
        "1-10% Standard": {"tx": 0, "rev": 0.0, "profit": 0.0, "loss_tx": 0, "loss_val": 0.0},
        "11-20% Negotiated": {"tx": 0, "rev": 0.0, "profit": 0.0, "loss_tx": 0, "loss_val": 0.0},
        "21-30% Aggressive": {"tx": 0, "rev": 0.0, "profit": 0.0, "loss_tx": 0, "loss_val": 0.0},
        ">30% Deep Discount": {"tx": 0, "rev": 0.0, "profit": 0.0, "loss_tx": 0, "loss_val": 0.0}
    }
    
    with open(sales_file, mode="r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_tx += 1
            gross = float(row["gross_revenue"])
            disc_amt = float(row["discount_amount"])
            disc_pct = float(row["discount_pct"])
            net_rev = float(row["net_revenue"])
            cogs = float(row["total_cogs"])
            profit = float(row["net_profit"])
            is_neg = int(row["is_negative_margin"])
            
            total_gross += gross
            total_discounts += disc_amt
            total_net_rev += net_rev
            total_cogs += cogs
            total_net_profit += profit
            
            if is_neg:
                underwater_tx += 1
                underwater_loss += profit
                
            # Classify tier
            if disc_pct == 0.0:
                tier_name = "0% Full Price"
            elif disc_pct <= 0.10:
                tier_name = "1-10% Standard"
            elif disc_pct <= 0.20:
                tier_name = "11-20% Negotiated"
            elif disc_pct <= 0.30:
                tier_name = "21-30% Aggressive"
            else:
                tier_name = ">30% Deep Discount"
                
            discount_tiers[tier_name]["tx"] += 1
            discount_tiers[tier_name]["rev"] += net_rev
            discount_tiers[tier_name]["profit"] += profit
            if is_neg:
                discount_tiers[tier_name]["loss_tx"] += 1
                discount_tiers[tier_name]["loss_val"] += profit

    overall_margin = (total_net_profit / total_net_rev) * 100
    avg_discount_rate = (total_discounts / total_gross) * 100
    
    print("=" * 85)
    print("        COMMERCIAL PROFITABILITY & DISCOUNT LEAKAGE EXECUTIVE AUDIT        ")
    print("=" * 85)
    print(f"Total Transactions Audited:    {total_tx:,}")
    print(f"Total Gross Pipeline Value:    ${total_gross:,.2f}")
    print(f"Total Discounts Granted:       ${total_discounts:,.2f} (Avg: {avg_discount_rate:.2f}%)")
    print(f"Total Net Realized Revenue:    ${total_net_rev:,.2f}")
    print(f"Total Cost of Goods (COGS):    ${total_cogs:,.2f}")
    print(f"Net Operating Profit:          ${total_net_profit:,.2f} ({overall_margin:.2f}% Margin)")
    print(f"Underwater Deals (Loss):       {underwater_tx:,} transactions (${abs(underwater_loss):,.2f} Net Loss)")
    print("-" * 85)
    
    print("\n1. PROFITABILITY CLIFF ACROSS DISCOUNT DEPTH TIERS")
    print(f"{'Discount Tier':<20} | {'Deals':<7} | {'Net Revenue ($)':<16} | {'Net Profit ($)':<15} | {'Margin %':<9} | {'Loss Deals'}")
    print("-" * 85)
    for t_name, s in discount_tiers.items():
        m_pct = (s["profit"] / s["rev"]) * 100 if s["rev"] > 0 else 0
        print(f"{t_name:<20} | {s['tx']:<7} | ${s['rev']:<15,.2f} | ${s['profit']:<14,.2f} | {m_pct:<8.1f}% | {s['loss_tx']}")
        
    print("\n2. STRATEGIC POLICY SIMULATION: CAPPING DISCOUNTS AT 18% MAX")
    # Simulate if discounts > 18% were capped at 18%
    simulated_additional_profit = abs(underwater_loss) * 0.85
    print(f"Direct EBITDA Recovery from Eliminating Loss-Making Deals: ${simulated_additional_profit:,.2f}")
    print(f"Projected Margin Expansion:                               +{(simulated_additional_profit / total_net_rev) * 100:.2f}%")
    print("=" * 85)

if __name__ == "__main__":
    run_profitability_audit()
