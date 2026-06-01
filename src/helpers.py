import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
import io

def generate_sales_dataset(file_path):
    """
    Generates a highly realistic sales dataset of ~2,500 records.
    Features:
    - Products and categories with consistent price ranges
    - Regional distributions and distinct sales channels
    - Realistic quantity and price correlations (e.g. wholesale discounts and larger quantities)
    - Date distribution from Jan 1, 2024 to May 31, 2026
    - Seasonal trends (holiday shopping peaks in Nov/Dec, back-to-school in Aug/Sep)
    - Simulated data anomalies (missing values, duplicates) for cleaning demo
    """
    np.random.seed(42)
    
    # Core Product & Category Mapping
    products_db = {
        "Electronics": {
            "Smart TV": (599.99, 649.99),
            "Laptop": (899.99, 999.99),
            "Wireless Headphones": (129.99, 149.99),
            "Smartphone": (699.99, 799.99),
            "Bluetooth Speaker": (59.99, 79.99),
            "Smartwatch": (199.99, 249.99)
        },
        "Fashion": {
            "Designer Jeans": (79.99, 99.99),
            "Leather Jacket": (149.99, 199.99),
            "Running Shoes": (89.99, 119.99),
            "Sunglasses": (49.99, 79.99),
            "Casual T-Shirt": (19.99, 29.99),
            "Winter Coat": (129.99, 179.99)
        },
        "Home & Kitchen": {
            "Air Fryer": (89.99, 119.99),
            "Coffee Maker": (79.99, 99.99),
            "Blender": (49.99, 69.99),
            "Robotic Vacuum": (249.99, 299.99),
            "Cookware Set": (119.99, 159.99),
            "Ergonomic Chair": (179.99, 229.99)
        },
        "Sports & Outdoors": {
            "Yoga Mat": (24.99, 39.99),
            "Camping Tent": (129.99, 189.99),
            "Hiking Backpack": (69.99, 99.99),
            "Fitness Tracker": (49.99, 79.99),
            "Water Bottle": (14.99, 24.99),
            "Dumbbells": (34.99, 59.99)
        },
        "Beauty & Personal Care": {
            "Skincare Gift Set": (39.99, 59.99),
            "Hair Dryer": (49.99, 79.99),
            "Essential Oil Diffuser": (24.99, 34.99),
            "Makeup Kit": (45.99, 65.99),
            "Perfume": (59.99, 89.99)
        },
        "Books & Stationery": {
            "Leather Journal": (19.99, 29.99),
            "Self-Help Best Seller": (14.99, 22.99),
            "Fountain Pen": (29.99, 49.99),
            "Desk Organizer": (24.99, 34.99),
            "Sci-Fi Novel": (12.99, 18.99)
        }
    }
    
    categories = list(products_db.keys())
    regions = ["North", "South", "East", "West"]
    channels = ["Online", "In-Store", "Wholesale", "Affiliate"]
    
    # Generate customer IDs
    num_customers = 400
    customer_ids = [f"CUST-{1000 + i}" for i in range(num_customers)]
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 5, 31)
    days_range = (end_date - start_date).days
    
    records = []
    num_records = 2500
    
    for i in range(num_records):
        order_id = f"ORD-{100000 + i}"
        
        # Decide date with seasonal probabilities
        random_day = np.random.randint(0, days_range)
        order_date = start_date + timedelta(days=random_day)
        
        # Seasonality factors:
        # Nov-Dec (Holiday surge): high transaction count
        # Aug-Sep (Back to school surge): mid transaction count
        # Let's use rejection sampling or direct scaling to build realistic seasonality
        month = order_date.month
        surge_prob = 1.0
        if month in [11, 12]:
            surge_prob = 1.4  # 40% higher chance
        elif month in [8, 9]:
            surge_prob = 1.2  # 20% higher chance
            
        if np.random.rand() > (surge_prob / 1.4):
            # Regenerate the date to give higher density in high months
            random_day = np.random.randint(0, days_range)
            order_date = start_date + timedelta(days=random_day)
            month = order_date.month
            
        category = np.random.choice(categories)
        product_list = list(products_db[category].keys())
        product = np.random.choice(product_list)
        
        # Price range
        price_range = products_db[category][product]
        unit_price = round(np.random.uniform(price_range[0], price_range[1]), 2)
        
        region = np.random.choice(regions)
        channel = np.random.choice(channels, p=[0.5, 0.3, 0.1, 0.1])
        
        # Wholesale channel characteristics
        if channel == "Wholesale":
            units_sold = int(np.random.randint(15, 60))
            # 15% wholesale discount
            unit_price = round(unit_price * 0.85, 2)
        else:
            # Retail channels
            units_sold = int(np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05]))
            
        revenue = round(units_sold * unit_price, 2)
        customer_id = np.random.choice(customer_ids)
        
        records.append({
            "Order_ID": order_id,
            "Order_Date": order_date.strftime("%Y-%m-%d"),
            "Product_Name": product,
            "Category": category,
            "Region": region,
            "Sales_Channel": channel,
            "Units_Sold": units_sold,
            "Unit_Price": unit_price,
            "Revenue": revenue,
            "Customer_ID": customer_id
        })
        
    df = pd.DataFrame(records)
    
    # Introduce ~1.5% simulated duplicates (approx 35 duplicate records)
    dup_indices = np.random.choice(df.index, size=35, replace=False)
    dups = df.iloc[dup_indices].copy()
    # Shift duplicate order IDs slightly or keep identical
    df = pd.concat([df, dups], ignore_index=True)
    
    # Introduce ~1.0% simulated missing values in Category, Region, and Sales_Channel
    for col in ["Region", "Sales_Channel"]:
        missing_indices = np.random.choice(df.index, size=25, replace=False)
        df.loc[missing_indices, col] = np.nan
        
    # Ensure directory exists and save
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"Realistic dataset generated successfully at: {file_path}")

def load_custom_css():
    """
    Returns custom CSS code designed with glassmorphism aesthetics, 
    custom hover-effects, elegant KPI cards, and refined dashboard layout options.
    """
    css = """
    <style>
        /* Base styles */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Glassmorphism containers */
        .glass-card {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, border 0.3s ease;
            margin-bottom: 20px;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Metrics styling */
        .kpi-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 15px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            margin-bottom: 15px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .kpi-container:hover {
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            border-color: rgba(99, 102, 241, 0.4);
            transform: scale(1.03);
        }
        
        .kpi-title {
            font-size: 0.9rem;
            color: #94a3b8;
            font-weight: 500;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .kpi-val {
            font-size: 1.8rem;
            font-weight: 700;
            color: #f8fafc;
            line-height: 1.2;
        }
        
        .kpi-delta {
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .kpi-delta.up {
            color: #10b981;
        }
        
        .kpi-delta.down {
            color: #ef4444;
        }
        
        /* Modern headers */
        .dashboard-header {
            background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.8rem;
            margin-bottom: 5px;
            letter-spacing: -0.02em;
        }
        
        .dashboard-subheader {
            color: #94a3b8;
            font-size: 1.1rem;
            margin-bottom: 30px;
            font-weight: 400;
        }
        
        /* Status badge */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-success {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .badge-warning {
            background-color: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        
        .badge-danger {
            background-color: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        /* Custom side navigation improvements */
        div[data-testid="stSidebar"] {
            background-color: #0b0f19;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Button style refinements */
        .stButton>button {
            background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        }
        
        /* Insights panel */
        .insight-card {
            background-color: rgba(30, 41, 59, 0.4);
            border-left: 4px solid #6366f1;
            padding: 15px;
            border-radius: 0 12px 12px 0;
            margin-bottom: 12px;
        }
        
        .insight-title {
            color: #e2e8f0;
            font-weight: 600;
            margin-bottom: 5px;
            font-size: 1rem;
        }
        
        .insight-text {
            color: #94a3b8;
            font-size: 0.92rem;
            line-height: 1.5;
        }
    </style>
    """
    return css

def render_kpi_card(title, value, delta_val=None, delta_dir=None, info_text=None):
    """
    Renders an elegant glassmorphic HTML KPI card.
    """
    delta_html = ""
    if delta_val is not None:
        direction = "up" if delta_dir == "up" else "down"
        arrow = "▲" if delta_dir == "up" else "▼"
        delta_html = f'<div class="kpi-delta {direction}">{arrow} {delta_val}</div>'
        
    html = f"""
    <div class="kpi-container">
        <div class="kpi-title">{title}</div>
        <div class="kpi-val">{value}</div>
        {delta_html}
    </div>
    """
    return html

def convert_df_to_csv(df):
    """
    Converts a pandas DataFrame into CSV format for Streamlit download.
    """
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    """
    Converts a pandas DataFrame into Excel format for Streamlit download.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sales Analytics')
    processed_data = output.getvalue()
    return processed_data
