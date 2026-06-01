import streamlit as st
import pandas as pd
import numpy as np
import datetime
from src.helpers import load_custom_css, render_kpi_card, convert_df_to_csv, convert_df_to_excel
from src.data_loader import load_data, validate_dataset, get_data_quality_metrics
from src.preprocessing import clean_dataset
from src.analytics import (
    calculate_kpis, get_time_trends, get_product_performance, 
    get_category_performance, analyze_growth, generate_automated_insights
)
from src.visualizations import (
    plot_sales_trend, plot_volume_vs_revenue, plot_category_revenue, 
    plot_top_products, plot_product_treemap, plot_region_channel_distribution, 
    plot_growth_rate, plot_correlation_matrix, plot_monthly_heatmap,
    COLOR_PALETTE
)

# 1. Page Configuration and Theming
st.set_page_config(
    page_title="Sales Trend Analytics - Intern ID CITS2983",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium custom CSS styles
st.markdown(load_custom_css(), unsafe_allow_html=True)

# Initialize Session States for Data & Cleaning State
if 'raw_df' not in st.session_state:
    st.session_state.raw_df = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'cleaning_report' not in st.session_state:
    st.session_state.cleaning_report = None
if 'is_cleaned' not in st.session_state:
    st.session_state.is_cleaned = False
if 'data_source' not in st.session_state:
    st.session_state.data_source = "Sample Dataset"

# 2. Sidebar Layout
with st.sidebar:
    st.markdown('<div style="text-align: center;"><span style="font-size: 3rem;">📊</span></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align: center; margin-bottom: 20px;">'
        '<h2 style="margin: 0; color: #f8fafc; font-size: 1.4rem; font-weight: 700;">SALES TREND VISUALIZATION</h2>'
        '<p style="margin: 5px 0 0 0; color: #6366f1; font-weight: 600; font-size: 0.85rem;">Intern ID: CITS2983</p>'
        '</div>', 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Data Upload Module
    st.subheader("📁 Data Source")
    uploaded_file = st.file_uploader("Upload CSV Sales Dataset", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Load uploaded dataset
            uploaded_df = pd.read_csv(uploaded_file)
            is_valid, missing_cols = validate_dataset(uploaded_df)
            
            if is_valid:
                st.session_state.raw_df = uploaded_df
                # Reset cleaning state on new upload
                st.session_state.cleaned_df = uploaded_df.copy()
                st.session_state.is_cleaned = False
                st.session_state.cleaning_report = None
                st.session_state.data_source = "Uploaded Dataset"
                st.sidebar.success("Dataset loaded successfully!")
            else:
                st.sidebar.error(f"Invalid format! Missing columns: {', '.join(missing_cols)}")
        except Exception as e:
            st.sidebar.error(f"Error loading CSV: {e}")
            
    # Load default sample if no upload
    if st.session_state.raw_df is None:
        df, err = load_data("data/sales_data.csv")
        if err is None:
            st.session_state.raw_df = df
            st.session_state.cleaned_df = df.copy()
            st.session_state.data_source = "Sample Dataset"
        else:
            st.sidebar.error(f"Critical error loading sample data: {err}")
            
    # Display Active Badge
    badge_style = "badge-success" if st.session_state.data_source == "Uploaded Dataset" else "badge-warning"
    st.markdown(
        f'<div style="text-align: center; margin-bottom: 15px;">'
        f'Active Source: <span class="badge {badge_style}">{st.session_state.data_source}</span>'
        f'</div>', 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Active DataFrame based on whether user cleaned it or not
    active_df = st.session_state.cleaned_df if st.session_state.is_cleaned else st.session_state.raw_df
    
    # Safety Check
    if active_df is not None:
        # Pre-convert Order_Date to datetime for filtering
        active_df = active_df.copy()
        active_df["Order_Date"] = pd.to_datetime(active_df["Order_Date"], errors="coerce")
        
        # Interactive Dashboard Filters
        st.subheader("🔍 Filters")
        
        # Date Range Filter
        min_date = active_df["Order_Date"].min().to_pydatetime() if not active_df["Order_Date"].isnull().all() else datetime.date(2024, 1, 1)
        max_date = active_df["Order_Date"].max().to_pydatetime() if not active_df["Order_Date"].isnull().all() else datetime.date(2026, 12, 31)
        
        selected_dates = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Category Filter
        available_categories = sorted(active_df["Category"].dropna().unique().tolist())
        selected_categories = st.multiselect("Select Categories", options=available_categories, default=[])
        
        # Product Filter (dynamic based on Category)
        if selected_categories:
            filtered_prods = active_df[active_df["Category"].isin(selected_categories)]
        else:
            filtered_prods = active_df
        available_products = sorted(filtered_prods["Product_Name"].dropna().unique().tolist())
        selected_products = st.multiselect("Select Products", options=available_products, default=[])
        
        # Region Filter
        available_regions = sorted(active_df["Region"].dropna().unique().tolist())
        selected_regions = st.multiselect("Select Regions", options=available_regions, default=[])
        
        # Sales Channel Filter
        available_channels = sorted(active_df["Sales_Channel"].dropna().unique().tolist())
        selected_channels = st.multiselect("Select Sales Channels", options=available_channels, default=[])
        
        # Apply filtering
        filtered_df = active_df.copy()
        
        # 1. Date filter
        if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
            start_dt, end_dt = pd.to_datetime(selected_dates[0]), pd.to_datetime(selected_dates[1])
            filtered_df = filtered_df[(filtered_df["Order_Date"] >= start_dt) & (filtered_df["Order_Date"] <= end_dt)]
            
        # 2. Category filter
        if selected_categories:
            filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
            
        # 3. Product filter
        if selected_products:
            filtered_df = filtered_df[filtered_df["Product_Name"].isin(selected_products)]
            
        # 4. Region filter
        if selected_regions:
            filtered_df = filtered_df[filtered_df["Region"].isin(selected_regions)]
            
        # 5. Sales Channel filter
        if selected_channels:
            filtered_df = filtered_df[filtered_df["Sales_Channel"].isin(selected_channels)]
            
        st.markdown("---")
        
        # Export Module
        st.subheader("📥 Export Reports")
        csv_data = convert_df_to_csv(filtered_df)
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_sales_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        excel_data = convert_df_to_excel(filtered_df)
        st.download_button(
            label="Download Filtered Data (Excel)",
            data=excel_data,
            file_name="filtered_sales_data.xlsx",
            mime="application/vnd.ms-excel",
            use_container_width=True
        )
    else:
        st.sidebar.warning("No active dataset loaded.")
        filtered_df = pd.DataFrame()

# 3. Main Dashboard Body
st.markdown('<h1 class="dashboard-header">SALES TREND VISUALIZATION</h1>', unsafe_allow_html=True)
st.markdown('<p class="dashboard-subheader">Data Analytics Internship Project Dashboard | Intern: <b>Anirudh V S</b> (ID: <b>CITS2983</b>)</p>', unsafe_allow_html=True)

# Basic sanity check
if len(filtered_df) == 0:
    st.warning("⚠️ No records match the active filter criteria. Please broaden your filters in the sidebar.")
else:
    # 4. KPI Summary Cards Calculation
    kpi = calculate_kpis(filtered_df)
    
    # Calculate historical MoM reference details to show Growth Indicators
    # Note: Growth indicators compare last active month with previous month in filtered dataframe
    growth_df = analyze_growth(filtered_df)
    
    growth_pct = 0.0
    growth_dir = "up"
    if len(growth_df) > 1:
        last_row = growth_df.iloc[-1]
        growth_pct = last_row["MoM_Revenue_Growth_%"]
        growth_dir = "up" if growth_pct >= 0 else "down"
        
    # Render KPI Cards in a modern 4-column layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            render_kpi_card(
                "Total Revenue", 
                f"${kpi['total_revenue']:,.2f}", 
                delta_val=f"{abs(growth_pct):.1f}% MoM" if len(growth_df) > 1 else None,
                delta_dir=growth_dir
            ), 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            render_kpi_card(
                "Total Orders", 
                f"{kpi['total_orders']:,}", 
                info_text="Distinct sales transactions"
            ), 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            render_kpi_card(
                "Units Sold", 
                f"{kpi['total_units_sold']:,}", 
                info_text="Quantity of physical items sold"
            ), 
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            render_kpi_card(
                "Avg Order Value (AOV)", 
                f"${kpi['average_order_value']:,.2f}", 
                info_text="Average spending per order"
            ), 
            unsafe_allow_html=True
        )
        
    # Best-seller indicator row
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f'<div class="insight-card" style="border-left-color: #ec4899; margin-top: 10px;">'
            f'<div class="insight-title">⭐️ BEST SELLING PRODUCT</div>'
            f'<div class="insight-text"><b>{kpi["top_product"]}</b> has generated the highest cumulative revenue of <b>${kpi["top_product_rev"]:,.2f}</b> in the current filtered selection.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col_b:
        st.markdown(
            f'<div class="insight-card" style="border-left-color: #10b981; margin-top: 10px;">'
            f'<div class="insight-title">📦 BEST SELLING CATEGORY</div>'
            f'<div class="insight-text">The top performing product category is <b>{kpi["top_category"]}</b>, contributing <b>${kpi["top_category_rev"]:,.2f}</b> in revenue.</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 5. Core Tab Implementation
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Overview Dashboard", 
        "📈 Sales Trends", 
        "💰 Revenue Analysis", 
        "🛍️ Product Analysis", 
        "🏷️ Category Analysis", 
        "🚀 Growth Analysis",
        "💡 Business Insights", 
        "🔍 Raw Data & Quality"
    ])
    
    # ---------------- TAB 1: OVERVIEW DASHBOARD ----------------
    with tab1:
        st.subheader("Executive Sales Overview")
        st.markdown("A consolidated strategic performance view illustrating volume, cash flow, territorial breakdown, and channel yield.")
        
        # Row 1: Dual axis revenue vs quantity chart
        trends = get_time_trends(filtered_df)
        fig_dual = plot_volume_vs_revenue(trends["monthly"], period="monthly")
        st.plotly_chart(fig_dual, use_container_width=True, key="overview_fig_dual")
        
        # Row 2: Territorial and Channel Side-by-Side
        col1, col2 = st.columns(2)
        fig_reg, fig_chan = plot_region_channel_distribution(filtered_df)
        with col1:
            st.plotly_chart(fig_reg, use_container_width=True, key="overview_fig_reg")
        with col2:
            st.plotly_chart(fig_chan, use_container_width=True, key="overview_fig_chan")
            
    # ---------------- TAB 2: SALES TRENDS ----------------
    with tab2:
        st.subheader("Time-Series Trend & Seasonality Module")
        st.markdown("Examine performance dynamics grouped by custom temporal bounds and trace seasonality cycles.")
        
        # Selection granularities
        col_opt1, col_opt2 = st.columns([1, 3])
        with col_opt1:
            period_opt = st.radio(
                "Time Window Granularity",
                options=["daily", "weekly", "monthly", "quarterly", "yearly"],
                index=2,
                key="trend_period"
            )
            trend_line_chk = st.checkbox("Plot Growth Trendline", value=True)
        
        with col_opt2:
            fig_trend = plot_sales_trend(trends[period_opt], period=period_opt, trend_line=trend_line_chk)
            st.plotly_chart(fig_trend, use_container_width=True, key="trends_fig_trend")
            
        st.markdown("---")
        st.subheader("Seasonal Revenue Performance Grid")
        st.markdown("An advanced analytical heat matrix highlighting monthly cyclic surges across fiscal years.")
        fig_heat = plot_monthly_heatmap(filtered_df)
        st.plotly_chart(fig_heat, use_container_width=True, key="trends_fig_heat")
        
    # ---------------- TAB 3: REVENUE ANALYSIS ----------------
    with tab3:
        st.subheader("Multidimensional Revenue Distributions")
        st.markdown("Explore sales returns and percentages dissected by categories, channels, and geographical territories.")
        
        # Category statistics donut & rankings
        cat_stats = get_category_performance(filtered_df)
        fig_donut, fig_cat_bar = plot_category_revenue(cat_stats)
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_donut, use_container_width=True, key="revenue_fig_donut")
        with col2:
            st.plotly_chart(fig_cat_bar, use_container_width=True, key="revenue_fig_cat_bar")
            
        # Interactive metric pivot tool
        st.markdown("---")
        st.subheader("Dynamic Cross-Tabulation Explorer")
        st.markdown("Choose categorical and continuous fields to quickly analyze revenue pivots.")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            pivot_row = st.selectbox("Row Category", options=["Category", "Region", "Sales_Channel"], index=0)
        with col_p2:
            pivot_col = st.selectbox("Column Category", options=["Region", "Sales_Channel", "Category"], index=1)
        with col_p3:
            pivot_agg = st.selectbox("Aggregate Field", options=["Revenue", "Units_Sold"], index=0)
            
        if pivot_row != pivot_col:
            p_table = filtered_df.pivot_table(
                values=pivot_agg,
                index=pivot_row,
                columns=pivot_col,
                aggfunc="sum",
                fill_value=0
            )
            # Add Total rows and columns
            p_table_display = p_table.copy()
            p_table_display["Total"] = p_table_display.sum(axis=1)
            p_table_display.loc["Total"] = p_table_display.sum()
            
            st.dataframe(
                p_table_display.style.format(precision=2).background_gradient(cmap="Purples", axis=None),
                use_container_width=True
            )
        else:
            st.error("Row and Column categories must be distinct to pivot.")
            
    # ---------------- TAB 4: PRODUCT ANALYSIS ----------------
    with tab4:
        st.subheader("Product Performance and Catalog Concentration")
        st.markdown("Analyze inventory rankings, sales volumes, and revenue contributions to isolate high and low performers.")
        
        prod_stats = get_product_performance(filtered_df)
        
        col1, col2 = st.columns(2)
        with col1:
            fig_top_prod = plot_top_products(prod_stats, top_n=10, ascending=False)
            st.plotly_chart(fig_top_prod, use_container_width=True, key="product_fig_top_prod")
        with col2:
            fig_bot_prod = plot_top_products(prod_stats, top_n=5, ascending=True)
            st.plotly_chart(fig_bot_prod, use_container_width=True, key="product_fig_bot_prod")
            
        st.markdown("---")
        st.subheader("Product Revenue Treemap Breakdown")
        st.markdown("A hierarchical treemap displaying revenue sizes of individual product catalog entries clustered inside parent categories.")
        fig_tree = plot_product_treemap(filtered_df)
        st.plotly_chart(fig_tree, use_container_width=True, key="product_fig_tree")
        
        # Interactive searchable product metrics table
        st.subheader("Detailed Product Sales Ledger")
        st.markdown("Searchable and sortable performance grid for all products in current selection.")
        
        search_prod = st.text_input("🔍 Search Product Name", value="")
        display_prod_df = prod_stats.copy()
        if search_prod:
            display_prod_df = display_prod_df[display_prod_df["Product_Name"].str.contains(search_prod, case=False)]
            
        st.dataframe(
            display_prod_df.style.format({
                "Revenue": "${:,.2f}",
                "Units_Sold": "{:,}",
                "Orders": "{:,}",
                "Revenue_Contribution_%": "{:.2f}%",
                "Cumulative_Contribution_%": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )
        
    # ---------------- TAB 5: CATEGORY ANALYSIS ----------------
    with tab5:
        st.subheader("Strategic Category Analytics")
        st.markdown("Inspect performance standings, volume metrics, and contribution indices of primary categories.")
        
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown("#### Category Metrics Overview")
            st.markdown("Each product category is ranked according to its cumulative revenue generation. The index provides insights on catalog focus.")
            
            for idx, row in cat_stats.iterrows():
                percentage = row["Revenue_Contribution_%"]
                st.markdown(
                    f'<div class="insight-card" style="border-left-color: {COLOR_PALETTE[idx % len(COLOR_PALETTE)]};">'
                    f'<div class="insight-title">Rank #{row["Rank"]}: {row["Category"]}</div>'
                    f'<div class="insight-text">'
                    f'• Total Revenue: <b>${row["Revenue"]:,.2f}</b><br>'
                    f'• Volume Sold: <b>{row["Units_Sold"]:,} items</b><br>'
                    f'• Orders: <b>{row["Orders"]:,} transactions</b><br>'
                    f'• Revenue Contribution: <b>{percentage}%</b>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        with col2:
            st.markdown("#### Category Cumulative Contribution Share")
            # Donut figure (re-rendered here to utilize wider tab width nicely)
            st.plotly_chart(fig_donut, use_container_width=True, key="category_fig_donut")
            
            st.markdown("#### Strategic Insights")
            if len(cat_stats) > 1:
                leader = cat_stats.iloc[0]["Category"]
                runner_up = cat_stats.iloc[1]["Category"]
                gap = cat_stats.iloc[0]["Revenue"] - cat_stats.iloc[1]["Revenue"]
                st.info(
                    f"💡 **Category Standings Summary:** The **{leader}** category represents the largest single sector. "
                    f"It maintains a lead of **${gap:,.2f}** over the runner-up category **{runner_up}**. "
                    f"Promotional activities or operational reviews should align with these core high-yield divisions."
                )
                
    # ---------------- TAB 6: GROWTH ANALYSIS ----------------
    with tab6:
        st.subheader("Period-over-Period Performance Dynamics")
        st.markdown("Track growth indicators, month-over-month growth directions, and review statistical variables correlation.")
        
        # MoM growth rate chart
        fig_growth = plot_growth_rate(growth_df)
        st.plotly_chart(fig_growth, use_container_width=True, key="growth_fig_growth")
        
        # Dual layout: correlation grid and numeric stats table
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Numerical Matrix Correlations")
            st.markdown("Highlights standard statistical relationships between Units Sold, Unit Price, and Revenue.")
            fig_corr = plot_correlation_matrix(filtered_df)
            st.plotly_chart(fig_corr, use_container_width=True, key="growth_fig_corr")
        with col2:
            st.markdown("#### Historical Period-over-Period Table")
            st.markdown("A complete record of month-over-month growth values and percentage metrics.")
            
            # Format display df
            growth_df_disp = growth_df.copy().sort_values("Date", ascending=False)
            st.dataframe(
                growth_df_disp[[
                    "Month_Year", "Revenue", "MoM_Revenue_Growth_%", 
                    "Units_Sold", "MoM_Volume_Growth_%"
                ]].style.format({
                    "Revenue": "${:,.2f}",
                    "MoM_Revenue_Growth_%": "{:+.2f}%",
                    "Units_Sold": "{:,}",
                    "MoM_Volume_Growth_%": "{:+.2f}%"
                }),
                use_container_width=True,
                hide_index=True
            )
            
    # ---------------- TAB 7: BUSINESS INSIGHTS ----------------
    with tab7:
        st.subheader("Automated Business Insights Engine")
        st.markdown("Advanced analytical observations and strategic operational recommendations automatically derived from the active dataset.")
        
        insights, recommendations = generate_automated_insights(filtered_df)
        
        st.markdown("### 🔍 Analytical Observations")
        # Loop through insights and display
        for title, text in insights:
            st.markdown(
                f'<div class="insight-card">'
                f'<div class="insight-title">🔹 {title}</div>'
                f'<div class="insight-text">{text}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🚀 Actionable Strategic Recommendations")
        # Loop through recommendations
        for idx, rec in enumerate(recommendations):
            st.markdown(
                f'<div style="background-color: rgba(99, 102, 241, 0.05); padding: 12px 18px; border-radius: 8px; margin-bottom: 10px; border: 1px solid rgba(99, 102, 241, 0.15);">'
                f'<span style="font-weight: 700; color: #a855f7; margin-right: 8px;">{idx+1}.</span> '
                f'<span style="color: #cbd5e1; font-size: 0.95rem;">{rec}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
            
    # ---------------- TAB 8: RAW DATA & QUALITY ----------------
    with tab8:
        st.subheader("Data Cleaning Module & Preview")
        st.markdown("Monitor and handle anomalous records (duplicates, missing values, incorrect datatypes) dynamically.")
        
        # Quality Metrics Before/After Cleaning
        metrics = get_data_quality_metrics(st.session_state.raw_df)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Row Count", f"{metrics['total_rows']:,}")
        with col_m2:
            dup_badge = "🟢 Perfect" if metrics["duplicate_count"] == 0 else "🔴 Action Required"
            st.metric("Identified Duplicates", f"{metrics['duplicate_count']} rows", help=f"{metrics['duplicate_percentage']}% of records")
        with col_m3:
            total_missing = sum(metrics["missing_counts"].values())
            missing_badge = "🟢 Perfect" if total_missing == 0 else "🟡 Action Required"
            st.metric("Missing Data Fields", f"{total_missing} values")
            
        # Interactive Cleaning Panel
        st.markdown("---")
        st.subheader("🛠️ Clean Dataset Options")
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cleaning_strategy = st.radio(
                "Missing Value Strategy",
                options=[("fill_mode", "Fill Categorical with Mode/Unknown"), ("drop", "Drop rows containing missing values")],
                format_func=lambda x: x[1]
            )
        with col_c2:
            rm_duplicates_chk = st.checkbox("Remove Duplicate Records", value=True)
            
        clean_btn = st.button("🚀 Execute Data Cleaning Pipeline", use_container_width=True)
        
        if clean_btn:
            cleaned, report = clean_dataset(
                st.session_state.raw_df, 
                handle_missing=cleaning_strategy[0], 
                remove_duplicates=rm_duplicates_chk
            )
            st.session_state.cleaned_df = cleaned
            st.session_state.cleaning_report = report
            st.session_state.is_cleaned = True
            st.success("🎉 Data cleaning completed successfully!")
            st.rerun() # Refresh app to update data state
            
        if st.session_state.is_cleaned and st.session_state.cleaning_report:
            rep = st.session_state.cleaning_report
            st.markdown("### 📋 Preprocessing Quality Report")
            
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.info(f"**Rows Processed:** {rep['initial_rows']} ➔ {rep['final_rows']}")
            with col_r2:
                st.warning(f"**Duplicates Removed:** {rep['duplicates_removed']} rows")
            with col_r3:
                missing_info = sum([v["count"] for v in rep["missing_filled"].values()]) if rep["missing_filled"] else rep["missing_dropped"]
                st.error(f"**Missing Fixed/Dropped:** {missing_info} instances")
                
            if rep["type_corrections"]:
                with st.expander("Show DataType and Formatting Corrections"):
                    for tc in rep["type_corrections"]:
                        st.write(f"✔️ {tc}")
                        
            # Reset Button
            reset_btn = st.button("🔄 Reset to Raw Dataset", type="secondary")
            if reset_btn:
                st.session_state.cleaned_df = st.session_state.raw_df.copy()
                st.session_state.is_cleaned = False
                st.session_state.cleaning_report = None
                st.success("Dataset reset to original raw state.")
                st.rerun()
                
        st.markdown("---")
        st.subheader("🔍 Active Dataset Preview")
        st.markdown("The preview displays the active dataset records according to selected filters.")
        
        # Display dataset
        st.dataframe(
            filtered_df.style.format({
                "Units_Sold": "{:,}",
                "Unit_Price": "${:,.2f}",
                "Revenue": "${:,.2f}"
            }),
            use_container_width=True
        )
