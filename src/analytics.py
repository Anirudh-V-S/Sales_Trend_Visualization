import pandas as pd
import numpy as np

def calculate_kpis(df):
    """
    Computes core financial and operational KPIs from the sales dataset.
    """
    if len(df) == 0:
        return {
            "total_revenue": 0.0,
            "total_units_sold": 0,
            "total_orders": 0,
            "average_order_value": 0.0,
            "top_product": "N/A",
            "top_product_rev": 0.0,
            "top_category": "N/A",
            "top_category_rev": 0.0
        }
        
    total_revenue = float(df["Revenue"].sum())
    total_units_sold = int(df["Units_Sold"].sum())
    total_orders = int(df["Order_ID"].nunique())
    average_order_value = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0
    
    # Top Product by Revenue
    prod_sales = df.groupby("Product_Name")["Revenue"].sum()
    top_product = prod_sales.idxmax() if not prod_sales.empty else "N/A"
    top_product_rev = float(prod_sales.max()) if not prod_sales.empty else 0.0
    
    # Top Category by Revenue
    cat_sales = df.groupby("Category")["Revenue"].sum()
    top_category = cat_sales.idxmax() if not cat_sales.empty else "N/A"
    top_category_rev = float(cat_sales.max()) if not cat_sales.empty else 0.0
    
    return {
        "total_revenue": total_revenue,
        "total_units_sold": total_units_sold,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "top_product": top_product,
        "top_product_rev": top_product_rev,
        "top_category": top_category,
        "top_category_rev": top_category_rev
    }

def get_time_trends(df):
    """
    Aggregates revenue and sales volumes across different time windows:
    Daily, Weekly, Monthly, Quarterly, and Yearly.
    """
    trends = {}
    
    if len(df) == 0:
        empty_df = pd.DataFrame(columns=["Date", "Revenue", "Units_Sold", "Orders"])
        return {
            "daily": empty_df, "weekly": empty_df, "monthly": empty_df,
            "quarterly": empty_df, "yearly": empty_df
        }
        
    # Daily Trend
    daily = df.groupby(df["Order_Date"].dt.date).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index().rename(columns={"Order_Date": "Date"})
    daily["Date"] = pd.to_datetime(daily["Date"])
    trends["daily"] = daily.sort_values("Date")
    
    # Weekly Trend
    weekly = df.groupby(df["Order_Date"].dt.to_period("W")).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    weekly["Date"] = weekly["Order_Date"].dt.to_timestamp()
    trends["weekly"] = weekly.sort_values("Date")
    
    # Monthly Trend
    monthly = df.groupby(df["Order_Date"].dt.to_period("M")).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    monthly["Date"] = monthly["Order_Date"].dt.to_timestamp()
    # Format month name for display
    monthly["Month_Year"] = monthly["Date"].dt.strftime("%b %Y")
    trends["monthly"] = monthly.sort_values("Date")
    
    # Quarterly Trend
    quarterly = df.groupby(df["Order_Date"].dt.to_period("Q")).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    quarterly["Date"] = quarterly["Order_Date"].dt.to_timestamp()
    quarterly["Quarter_Year"] = quarterly["Order_Date"].astype(str)
    trends["quarterly"] = quarterly.sort_values("Date")
    
    # Yearly Trend
    yearly = df.groupby(df["Order_Date"].dt.to_period("Y")).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    yearly["Date"] = yearly["Order_Date"].dt.to_timestamp()
    yearly["Year"] = yearly["Order_Date"].astype(str)
    trends["yearly"] = yearly.sort_values("Date")
    
    return trends

def get_product_performance(df):
    """
    Computes rankings, revenue contributions, and volume sales for all products.
    """
    if len(df) == 0:
        return pd.DataFrame()
        
    prod_stats = df.groupby(["Product_Name", "Category"]).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    
    # Sorting and ranking
    prod_stats = prod_stats.sort_values("Revenue", ascending=False)
    total_rev = prod_stats["Revenue"].sum()
    
    prod_stats["Revenue_Contribution_%"] = ((prod_stats["Revenue"] / total_rev) * 100).round(2)
    prod_stats["Cumulative_Contribution_%"] = prod_stats["Revenue_Contribution_%"].cumsum().round(2)
    prod_stats["Rank"] = range(1, len(prod_stats) + 1)
    
    return prod_stats

def get_category_performance(df):
    """
    Analyzes sales metrics grouped by product categories.
    """
    if len(df) == 0:
        return pd.DataFrame()
        
    cat_stats = df.groupby("Category").agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Orders=("Order_ID", "nunique")
    ).reset_index()
    
    cat_stats = cat_stats.sort_values("Revenue", ascending=False)
    total_rev = cat_stats["Revenue"].sum()
    cat_stats["Revenue_Contribution_%"] = ((cat_stats["Revenue"] / total_rev) * 100).round(2)
    cat_stats["Rank"] = range(1, len(cat_stats) + 1)
    
    return cat_stats

def analyze_growth(df):
    """
    Performs period-over-period revenue growth analysis (Month-over-Month).
    """
    if len(df) == 0:
        return pd.DataFrame()
        
    monthly_data = df.groupby(df["Order_Date"].dt.to_period("M")).agg(
        Revenue=("Revenue", "sum"),
        Units_Sold=("Units_Sold", "sum")
    ).reset_index()
    
    monthly_data["Date"] = monthly_data["Order_Date"].dt.to_timestamp()
    monthly_data = monthly_data.sort_values("Date")
    
    monthly_data["Prev_Revenue"] = monthly_data["Revenue"].shift(1)
    monthly_data["MoM_Revenue_Growth_$"] = (monthly_data["Revenue"] - monthly_data["Prev_Revenue"]).round(2)
    monthly_data["MoM_Revenue_Growth_%"] = (
        (monthly_data["MoM_Revenue_Growth_$"] / monthly_data["Prev_Revenue"]) * 100
    ).round(2)
    
    monthly_data["Prev_Units_Sold"] = monthly_data["Units_Sold"].shift(1)
    monthly_data["MoM_Volume_Growth_Units"] = monthly_data["Units_Sold"] - monthly_data["Prev_Units_Sold"]
    monthly_data["MoM_Volume_Growth_%"] = (
        (monthly_data["MoM_Volume_Growth_Units"] / monthly_data["Prev_Units_Sold"]) * 100
    ).round(2)
    
    # Fill NaN values (first row) with 0
    monthly_data = monthly_data.fillna(0)
    monthly_data["Month_Year"] = monthly_data["Date"].dt.strftime("%b %Y")
    
    return monthly_data

def generate_automated_insights(df):
    """
    Generates rich, high-fidelity automated business insights using data science criteria:
    - Peak performance periods (best/worst months)
    - Product and Category dominance
    - Pareto concentration (80/20 rule validation)
    - Sales channel & Region rankings
    - Concrete, actionable business recommendations
    """
    insights = []
    recommendations = []
    
    if len(df) == 0:
        return [("No Data Available", "Please upload or load the dataset to generate insights.")], []
        
    total_rev = df["Revenue"].sum()
    
    # 1. Highest & Lowest Revenue Month
    monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"].sum().reset_index()
    monthly["Month_Name"] = monthly["Order_Date"].dt.to_timestamp().dt.strftime("%B %Y")
    max_idx = monthly["Revenue"].idxmax()
    min_idx = monthly["Revenue"].idxmin()
    
    best_month = monthly.loc[max_idx, "Month_Name"]
    best_month_rev = monthly.loc[max_idx, "Revenue"]
    worst_month = monthly.loc[min_idx, "Month_Name"]
    worst_month_rev = monthly.loc[min_idx, "Revenue"]
    
    insights.append((
        "Peak and Trough Revenue Periods",
        f"The highest performing period was **{best_month}** with a total revenue of **${best_month_rev:,.2f}**. "
        f"Conversely, the lowest revenue month was **{worst_month}** generating **${worst_month_rev:,.2f}**."
    ))
    
    # 2. Product and Category Concentration
    cat_perf = get_category_performance(df)
    prod_perf = get_product_performance(df)
    
    top_cat = cat_perf.iloc[0]["Category"]
    top_cat_rev = cat_perf.iloc[0]["Revenue"]
    top_cat_share = cat_perf.iloc[0]["Revenue_Contribution_%"]
    
    top_prod = prod_perf.iloc[0]["Product_Name"]
    top_prod_rev = prod_perf.iloc[0]["Revenue"]
    top_prod_share = prod_perf.iloc[0]["Revenue_Contribution_%"]
    
    insights.append((
        "Product & Category Dominance",
        f"The **{top_cat}** category dominates sales, contributing **${top_cat_rev:,.2f}** "
        f"({top_cat_share}% of total revenue). At an individual product level, the top revenue generator "
        f"is **{top_prod}** (under {prod_perf.iloc[0]['Category']}), earning **${top_prod_rev:,.2f}** ({top_prod_share}% share)."
    ))
    
    # 3. Pareto 80/20 Rule Check
    # How many products make up 80% of revenue?
    num_products = len(prod_perf)
    products_under_80 = prod_perf[prod_perf["Cumulative_Contribution_%"] <= 80]
    num_under_80 = len(products_under_80) + 1 # Include the boundary product
    pct_under_80 = round((num_under_80 / num_products) * 100, 1) if num_products > 0 else 0
    
    is_pareto = pct_under_80 <= 30
    pareto_text = (
        f"Yes, our analysis indicates strong revenue concentration: **{num_under_80} out of {num_products} products** "
        f"({pct_under_80}%) account for 80% of total revenue. This aligns closely with Pareto's Law."
        if is_pareto else
        f"No, revenue is relatively distributed. It requires **{num_under_80} out of {num_products} products** "
        f"({pct_under_80}%) to reach the 80% revenue milestone, indicating a healthy, diversified catalog."
    )
    insights.append(("Pareto Revenue Concentration (80/20 Rule)", pareto_text))
    
    # 4. Regional and Channel Performance
    region_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    top_region = region_rev.index[0] if not region_rev.empty else "N/A"
    top_region_rev = region_rev.iloc[0] if not region_rev.empty else 0.0
    top_region_share = round((top_region_rev / total_rev) * 100, 1) if total_rev > 0 else 0
    
    channel_rev = df.groupby("Sales_Channel")["Revenue"].sum().sort_values(ascending=False)
    top_channel = channel_rev.index[0] if not channel_rev.empty else "N/A"
    top_channel_rev = channel_rev.iloc[0] if not channel_rev.empty else 0.0
    top_channel_share = round((top_channel_rev / total_rev) * 100, 1) if total_rev > 0 else 0
    
    insights.append((
        "Region & Sales Channel Performance",
        f"The **{top_region}** region is the top-performing territory, generating **${top_region_rev:,.2f}** "
        f"({top_region_share}% share). Sales are heavily driven by the **{top_channel}** channel, "
        f"which brings in **${top_channel_rev:,.2f}** ({top_channel_share}% of total)."
    ))
    
    # 5. Seasonal Patterns
    df_temp = df.copy()
    df_temp["Month_Num"] = df_temp["Order_Date"].dt.month
    monthly_avg = df_temp.groupby("Month_Num")["Revenue"].mean()
    high_months = monthly_avg[monthly_avg > monthly_avg.mean() * 1.15].index.tolist()
    
    month_names = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 
                   7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
    high_month_names = [month_names[m] for m in high_months]
    
    if len(high_month_names) > 0:
        seasonal_text = f"We detected a strong seasonal peak during the months of **{', '.join(high_month_names)}**."
    else:
        seasonal_text = "Sales trends display stability throughout the year without pronounced seasonality anomalies."
    insights.append(("Seasonal Revenue Trajectories", seasonal_text))
    
    # Generate business recommendations
    recommendations.append(
        f"**Optimize Inventory for {top_prod}:** Since {top_prod} is your best-selling product, "
        f"ensure sufficient inventory buffers, particularly during known seasonal peaks in Q4 to prevent out-of-stock losses."
    )
    recommendations.append(
        f"**Replicate {top_region} Region Best Practices:** Investigate the specific marketing or logistical "
        f"strategies operating in {top_region} and replicate them in lagging regions (e.g. West or South)."
    )
    if is_pareto:
        recommendations.append(
            f"**Customer Retention for Key Catalog Items:** The top {num_under_80} items generate 80% of revenue. "
            f"Set up customized loyalty discounts, bundled pricing, or post-purchase customer satisfaction follow-ups on these specific items."
        )
    else:
        recommendations.append(
            "**Diversified Promotion Strategy:** Since your product revenue is diversified, run multi-product bundle campaigns "
            "(e.g., cross-selling Beauty with Fashion products) to boost the Average Order Value (AOV) further."
        )
    recommendations.append(
        f"**Scale {top_channel} Digital Marketing:** With {top_channel} emerging as the highest-yield channel, "
        f"allocate a larger budget to target online retargeting or physical customer relationship campaigns based on this channel's style."
    )
    
    return insights, recommendations
