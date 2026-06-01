import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Curated HSL-tailored harmonious modern color palette (Indigo, Purple, Magenta, Emerald, Cyan)
COLOR_PALETTE = ["#6366f1", "#a855f7", "#ec4899", "#10b981", "#06b6d4", "#f59e0b", "#3b82f6"]
TEMPLATE = "plotly_dark"

def plot_sales_trend(trends_df, period="monthly", trend_line=False):
    """
    Plots interactive Line and Area charts for revenue trends.
    """
    if len(trends_df) == 0:
        return go.Figure()
        
    date_col = "Date"
    x_label = "Date"
    x_hover = "%B %Y"
    
    if period == "monthly":
        date_col = "Month_Year"
        x_label = "Month"
        x_hover = "%B %Y"
        # Sort values chronologically
        trends_df = trends_df.sort_values("Date")
    elif period == "quarterly":
        date_col = "Quarter_Year"
        x_label = "Quarter"
        x_hover = "Quarter"
    elif period == "yearly":
        date_col = "Year"
        x_label = "Year"
        x_hover = "Year"
        
    fig = px.area(
        trends_df,
        x=date_col,
        y="Revenue",
        title=f"{period.capitalize()} Revenue Trend Analysis",
        labels={"Revenue": "Revenue ($)", date_col: x_label},
        template=TEMPLATE,
        color_discrete_sequence=[COLOR_PALETTE[0]]
    )
    
    # Customise styling
    fig.update_traces(
        line=dict(width=3, color=COLOR_PALETTE[0]),
        fillcolor="rgba(99, 102, 241, 0.15)"
    )
    
    if trend_line and len(trends_df) > 1:
        # Calculate moving average or linear trend line
        y = trends_df["Revenue"].values
        x_indices = np.arange(len(y))
        slope, intercept = np.polyfit(x_indices, y, 1)
        trend_vals = slope * x_indices + intercept
        
        fig.add_trace(go.Scatter(
            x=trends_df[date_col],
            y=trend_vals,
            mode='lines',
            name='Growth Trendline',
            line=dict(color=COLOR_PALETTE[2], width=2, dash='dash')
        ))
        
    fig.update_layout(
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)")
    )
    
    return fig

def plot_volume_vs_revenue(trends_df, period="monthly"):
    """
    Plots a dual-axis chart showing Revenue and Units Sold together.
    """
    if len(trends_df) == 0:
        return go.Figure()
        
    x_data = trends_df["Month_Year"] if period == "monthly" else trends_df["Date"]
    
    fig = go.Figure()
    
    # Add Bar for Revenue
    fig.add_trace(go.Bar(
        x=x_data,
        y=trends_df["Revenue"],
        name="Revenue ($)",
        marker_color=COLOR_PALETTE[0],
        opacity=0.75,
        yaxis="y"
    ))
    
    # Add Line for Units Sold
    fig.add_trace(go.Scatter(
        x=x_data,
        y=trends_df["Units_Sold"],
        name="Units Sold",
        mode="lines+markers",
        line=dict(color=COLOR_PALETTE[3], width=3),
        marker=dict(size=6),
        yaxis="y2"
    ))
    
    # Set dual axis layout
    fig.update_layout(
        title=f"Revenue vs. Units Sold Comparison ({period.capitalize()})",
        template=TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title=dict(text="Revenue ($)", font=dict(color=COLOR_PALETTE[0])),
            tickfont=dict(color=COLOR_PALETTE[0]),
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)"
        ),
        yaxis2=dict(
            title=dict(text="Units Sold", font=dict(color=COLOR_PALETTE[3])),
            tickfont=dict(color=COLOR_PALETTE[3]),
            overlaying="y",
            side="right"
        )
    )
    
    return fig

def plot_category_revenue(cat_stats):
    """
    Plots category performance using horizontal bar and donut charts.
    """
    if len(cat_stats) == 0:
        return go.Figure(), go.Figure()
        
    # Donut Chart for Revenue Share
    donut_fig = px.pie(
        cat_stats,
        names="Category",
        values="Revenue",
        hole=0.45,
        title="Revenue Share by Product Category",
        color_discrete_sequence=COLOR_PALETTE,
        template=TEMPLATE
    )
    
    donut_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif")
    )
    donut_fig.update_traces(textposition='inside', textinfo='percent+label')
    
    # Bar Chart for Category Sales volume vs Revenue
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(
        x=cat_stats["Category"],
        y=cat_stats["Revenue"],
        name="Revenue ($)",
        marker_color=COLOR_PALETTE[1]
    ))
    bar_fig.add_trace(go.Bar(
        x=cat_stats["Category"],
        y=cat_stats["Units_Sold"],
        name="Units Sold",
        marker_color=COLOR_PALETTE[4],
        visible='legendonly' # Toggleable in UI
    ))
    
    bar_fig.update_layout(
        title="Category Performance Standings",
        barmode="group",
        template=TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)")
    )
    
    return donut_fig, bar_fig

def plot_top_products(prod_stats, top_n=10, ascending=True):
    """
    Plots top or bottom selling products.
    """
    if len(prod_stats) == 0:
        return go.Figure()
        
    df_plot = prod_stats.head(top_n) if not ascending else prod_stats.tail(top_n)
    title = f"Top {top_n} Products by Revenue" if not ascending else f"Lowest {top_n} Products by Revenue"
    color = COLOR_PALETTE[2] if not ascending else COLOR_PALETTE[5]
    
    # Sort for beautiful horizontal bar representation
    df_plot = df_plot.sort_values("Revenue", ascending=True)
    
    fig = px.bar(
        df_plot,
        y="Product_Name",
        x="Revenue",
        orientation="h",
        title=title,
        labels={"Revenue": "Revenue ($)", "Product_Name": "Product"},
        template=TEMPLATE,
        text_auto=".2s"
    )
    
    fig.update_traces(marker_color=color, hovertemplate="Product: %{y}<br>Revenue: $%{x:,.2f}")
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        xaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)"),
        yaxis=dict(showgrid=False)
    )
    
    return fig

def plot_product_treemap(df):
    """
    Generates a beautiful nested Product within Category hierarchy treemap.
    """
    if len(df) == 0:
        return go.Figure()
        
    df_grouped = df.groupby(["Category", "Product_Name"])["Revenue"].sum().reset_index()
    
    fig = px.treemap(
        df_grouped,
        path=["Category", "Product_Name"],
        values="Revenue",
        title="Revenue Breakdown Hierarchy (Category > Product)",
        color="Revenue",
        color_continuous_scale="Purples",
        template=TEMPLATE
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif")
    )
    
    return fig

def plot_region_channel_distribution(df):
    """
    Plots regional sales and marketing sales channel distributions.
    """
    if len(df) == 0:
        return go.Figure(), go.Figure()
        
    region_data = df.groupby("Region")["Revenue"].sum().reset_index()
    channel_data = df.groupby("Sales_Channel")["Revenue"].sum().reset_index()
    
    # Donut for regions
    fig_region = px.pie(
        region_data,
        values="Revenue",
        names="Region",
        hole=0.4,
        title="Territorial Revenue Distribution (Region)",
        color_discrete_sequence=COLOR_PALETTE[3:],
        template=TEMPLATE
    )
    fig_region.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif")
    )
    
    # Bar for Channels
    fig_channel = px.bar(
        channel_data.sort_values("Revenue", ascending=False),
        x="Sales_Channel",
        y="Revenue",
        title="Revenue by Sales Channel",
        labels={"Revenue": "Revenue ($)", "Sales_Channel": "Sales Channel"},
        template=TEMPLATE,
        color="Sales_Channel",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_channel.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)")
    )
    
    return fig_region, fig_channel

def plot_growth_rate(growth_df):
    """
    Plots the Period-over-Period Month-over-Month Revenue Growth Percentage.
    """
    if len(growth_df) == 0:
        return go.Figure()
        
    # We remove the first entry since growth is 0/NaN
    df_plot = growth_df.iloc[1:]
    
    # Colors depending on positive or negative growth
    colors = [COLOR_PALETTE[3] if x >= 0 else COLOR_PALETTE[2] for x in df_plot["MoM_Revenue_Growth_%"]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_plot["Month_Year"],
        y=df_plot["MoM_Revenue_Growth_%"],
        marker_color=colors,
        hovertemplate="Month: %{x}<br>Growth Rate: %{y:.2f}%"
    ))
    
    # Add a guide-line at 0%
    fig.add_trace(go.Scatter(
        x=df_plot["Month_Year"],
        y=[0] * len(df_plot),
        mode='lines',
        showlegend=False,
        line=dict(color='white', width=1, dash='solid'),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title="Month-over-Month Revenue Growth Percentage (%)",
        template=TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title="Growth Rate (%)",
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            ticksuffix="%"
        )
    )
    
    return fig

def plot_correlation_matrix(df):
    """
    Creates a correlation matrix heatmap of numerical columns.
    """
    numeric_cols = ["Units_Sold", "Unit_Price", "Revenue"]
    avail_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(avail_cols) < 2:
        return go.Figure()
        
    corr = df[avail_cols].corr()
    
    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Numeric Variable Correlation Grid",
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        template=TEMPLATE
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif")
    )
    
    return fig

def plot_monthly_heatmap(df):
    """
    Draws a Year vs. Month seasonal revenue heatmap.
    """
    if len(df) == 0:
        return go.Figure()
        
    df_temp = df.copy()
    df_temp["Year"] = df_temp["Order_Date"].dt.year
    df_temp["Month_Num"] = df_temp["Order_Date"].dt.month
    df_temp["Month_Name"] = df_temp["Order_Date"].dt.strftime("%b")
    
    # Pivot to aggregate
    pivot_df = df_temp.pivot_table(
        values="Revenue",
        index="Year",
        columns=["Month_Num", "Month_Name"],
        aggfunc="sum",
        fill_value=0
    )
    
    # Drop month multi-index, order strictly by month number
    pivot_df.columns = [col[1] for col in pivot_df.columns]
    
    fig = px.imshow(
        pivot_df,
        text_auto=".2s",
        aspect="auto",
        title="Seasonal Month-Year Performance Grid (Total Revenue)",
        color_continuous_scale="Purples",
        template=TEMPLATE
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Outfit, sans-serif"),
        xaxis=dict(title="Month"),
        yaxis=dict(title="Year", tickmode='linear')
    )
    
    return fig
