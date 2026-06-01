# 📸 Dashboard Interface Capture & Verification Checklist

This directory contains visual captures of the fully interactive Streamlit analytical application. For portfolio showcases and final academic reviews, use this guide to verify or update the visual documentation.

---

## 📋 Screenshot Verification Points

### 1. Executive Dashboard Overview (`01_dashboard_overview.png`)
*   **Target Tab:** `📊 Overview Dashboard`
*   **Verification Checklist:**
    *   [ ] The four KPI Glassmorphism cards (Total Revenue, Total Orders, Units Sold, and Average Order Value) render correctly.
    *   [ ] The MoM Revenue Growth delta indicator is visible.
    *   [ ] The "Best Selling Product" and "Best Selling Category" highlight panels are displayed under the metrics.
    *   [ ] The dual-axis Plotly chart comparing "Revenue vs. Units Sold" renders properly.
    *   [ ] The territorial Donut chart and Sales Channel Bar chart display without errors.

### 2. Dataset Upload & Side-filters (`02_dataset_upload.png`)
*   **Target Tab:** Sidebar Control
*   **Verification Checklist:**
    *   [ ] The header displays `SALES TREND VISUALIZATION` and the **Intern ID: CITS2983**.
    *   [ ] The dynamic source badge renders `Active Source: Sample Dataset` (orange) or `Uploaded Dataset` (green).
    *   [ ] The date range slider inputs display current bounds correctly.
    *   [ ] The multi-select input blocks (Categories, Products, Regions, Sales Channels) populate properly.
    *   [ ] The CSV and Excel export download buttons are visible in the sidebar.

### 3. Temporal Trend Analysis (`03_sales_trend_analysis.png`)
*   **Target Tab:** `📈 Sales Trends`
*   **Verification Checklist:**
    *   [ ] The radio button selection for daily, weekly, monthly, quarterly, and yearly intervals works.
    *   [ ] The Plotly Area chart changes dynamically based on the selected interval.
    *   [ ] The dashed "Growth Trendline" regression line overlay displays when checked.
    *   [ ] The large "Seasonal Month-Year Performance Grid" heatmap renders successfully at the bottom.

### 4. Revenue Analysis (`04_revenue_analysis.png`)
*   **Target Tab:** `💰 Revenue Analysis`
*   **Verification Checklist:**
    *   [ ] The Donut chart for category revenue shares displays percentages correctly.
    *   [ ] The standing ranks bar chart renders next to it.
    *   [ ] The **Dynamic Cross-Tabulation Explorer** creates clean tables when changing rows and columns.
    *   [ ] The cross-tab displays a purple gradient highlighting high-performing cross-sections.

### 5. Product Catalog Performance (`05_product_performance.png`)
*   **Target Tab:** `🛍️ Product Analysis`
*   **Verification Checklist:**
    *   [ ] The "Top 10 Products by Revenue" horizontal bar chart is visible.
    *   [ ] The "Lowest 5 Products by Revenue" (red) chart displays next to it.
    *   [ ] The nested hierarchical Treemap (Categories > Products) renders properly.
    *   [ ] The searchable product database filters records instantly when typing a name.

### 6. Category Performance (`06_category_analysis.png`)
*   **Target Tab:** `🏷️ Category Analysis`
*   **Verification Checklist:**
    *   [ ] The category ranks render in alternating glassmorphism cards.
    *   [ ] The category revenue shares are represented in a large donut layout.
    *   [ ] The warning/info alert boxes summarize category leader gaps correctly.

### 7. MoM Growth Dynamics (`07_growth_analysis.png`)
*   **Target Tab:** `🚀 Growth Analysis`
*   **Verification Checklist:**
    *   [ ] The Month-over-Month Growth Bar chart displays with conditional colors (green for growth, red for decline).
    *   [ ] The Numeric Variable Correlation matrix renders showing coefficients.
    *   [ ] The complete growth dataset table lists positive and negative percentages.

### 8. Automated Business Insights (`08_business_insights.png`)
*   **Target Tab:** `💡 Business Insights`
*   **Verification Checklist:**
    *   [ ] All 5 dynamic insights (Peak Months, Product Dominance, Pareto Concentrate, Region leaders, and Seasonal Trajectories) display.
    *   [ ] The actionable recommendations are numbered (1-5) and colored with light indigo frames.

### 9. Preprocessing & Raw Data (`09_raw_data_view.png`)
*   **Target Tab:** `🔍 Raw Data & Quality`
*   **Verification Checklist:**
    *   [ ] The three quality metrics (Rows, Duplicates, and Missing) are highlighted.
    *   [ ] The strategy options for handling missing values render as radio buttons.
    *   [ ] Executing the pipeline shows a successful completion message and updates the quality report.
    *   [ ] The scrollable data frame displays the tabular dataset correctly.
