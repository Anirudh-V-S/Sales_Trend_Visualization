# SALES TREND VISUALIZATION

### 🎓 CODTECH IT SOLUTIONS DATA ANALYTICS INTERNSHIP
---
**🆔 Intern ID:** `CITS2983`  
**👤 Intern Name:** Anirudh V S  
**💼 Domain:** Sales Performance Trend Visualization & Data Preprocessing  
**🏆 Project Status:** Production-Ready (QA Audited & Verified 100/100)  
---

---

## 📋 Project Overview

The **Sales Trend Visualization Dashboard** is an end-to-end, high-performance web-based data analytics application. It is designed to clean, preprocess, explore, analyze, and visualize corporate transaction logs to unlock strategic revenue-driving patterns. The platform serves as an interactive business intelligence suite, processing large-scale sales datasets to deliver granular insights regarding revenue, product shelf performance, product categories, growth rates, territorial footprints, and marketing channels.

This application is built with a **modular architecture** using Python and Streamlit, featuring interactive Plotly visualizations, a dynamic Data Cleaning pipeline, and an Automated Business Insights engine.

---

## 🎯 Objectives

1. **Transaction Lifecycle Auditing:** Cleanse raw corporate transaction data by removing duplicates, handling missing elements, validating order dates, and standardizing datatypes dynamically.
2. **Key Performance Indicators (KPIs) Monitoring:** Aggregate core metrics such as Total Revenue, Units Sold, Total Orders, and Average Order Value (AOV) with live growth trend indicators.
3. **Temporal Trend Analysis:** Track sales velocities and patterns over customizable daily, weekly, monthly, quarterly, and yearly intervals.
4. **Product Portfolio Performance:** Evaluate best-selling and underperforming catalog items, mapping revenue concentrations utilizing Pareto analysis (80/20 rule validation).
5. **Hierarchical and Territorial Share Analysis:** Investigate category revenue shares and regional distributions.
6. **Strategic Decision Support:** Generate automated statistical insights and list actionable executive business recommendations to optimize logistics, inventory, and marketing campaigns.

---

## 🛠️ Technology Stack

- **Core Logic:** Python 3.10+
- **Interactive UI Framework:** Streamlit
- **Data Engineering & Manipulation:** Pandas, NumPy
- **High-Fidelity Visualizations:** Plotly Express, Plotly Graphical Objects
- **Scientific Computations:** Scikit-Learn (linear regression for trendlines)
- **Reporting & File Handling:** OpenPyXL (Excel generation), Pillow (Image assets)

---

## 📊 Dataset Description

The system includes a generator script that builds a highly realistic transactional dataset of **2,500+ records** spanning from **January 1, 2024 to May 31, 2026**. 

The dataset contains the following critical fields:
*   **`Order_ID`**: Unique transaction identifier.
*   **`Order_Date`**: Timestamp of purchase (spans ~2.5 years, simulating seasonal peaks).
*   **`Product_Name`**: 36 unique products distributed logically across 6 sectors.
*   **`Category`**: Parent categories (Electronics, Fashion, Home & Kitchen, Sports & Outdoors, Beauty & Personal Care, Books & Stationery).
*   **`Region`**: Target markets (North, South, East, West).
*   **`Sales_Channel`**: Marketing channels (Online, In-Store, Wholesale, Affiliate).
*   **`Units_Sold`**: Quantities per purchase (logical variations: retail vs. bulk wholesale).
*   **`Unit_Price`**: Unit costs matching category profiles, including wholesale discounts.
*   **`Revenue`**: Total cash receipt (`Units_Sold * Unit_Price`).
*   **`Customer_ID`**: Customer identifier for shopping frequency.

*Note: For validation testing, the generator introduces ~1.5% duplicate records and ~1.0% missing fields in categorical attributes.*

---

## 🖥️ Dashboard Architecture & Tab Features

The dashboard layout is structured using a responsive double-column layout (Sidebar Control + Central Analysis Area) containing **8 analytical tabs**:

1.  **📊 Overview Dashboard:** Executive summary cards (Total Revenue, Orders, Volume, AOV), dual-axis Revenue-Volume comparisons, territorial shares (Donut), and Sales Channel bar charts.
2.  **📈 Sales Trends:** Dynamic time granularity plotters (Daily, Weekly, Monthly, Quarterly, Yearly) with interactive Scikit-Learn linear regression trendlines, and a Year-Month seasonal heatmap.
3.  **💰 Revenue Analysis:** High-fidelity category revenue share models and an interactive **Dynamic Cross-Tabulation Explorer** to pivot tables dynamically.
4.  **🛍️ Product Analysis:** Horizontal rankings of top 10 and bottom 5 revenue generators, an interactive Treemap detailing Category-Product nesting, and a searchable product database.
5.  **🏷️ Category Analysis:** Complete standings showing Rank, Revenue, Volumes, Orders, and Contribution percentages per sector with contextual leadership summaries.
6.  **🚀 Growth Analysis:** Month-over-Month growth rate charts (color-coded for positive/negative growth), numeric variable correlation grids, and historical growth datasets.
7.  **💡 Business Insights:** Automatic calculation of seasonal peaks, product concentrations, region leaders, channel yields, Pareto concentration validation, and 5 structured business recommendations.
8.  **🔍 Raw Data & Quality:** Live **Data Preprocessing & Cleaning Module** where users customize duplicate removals, missing value strategies (imputation vs. row dropping), audit reports, and browse the active data.

---

## 📂 Project Structure

```
Sales_Trend_Visualization/
│
├── app.py                  # Main Streamlit executable dashboard application
├── requirements.txt        # Full project python dependency file
├── LICENSE                 # MIT License details
├── .gitignore              # Standard Python project git ignores
├── README.md               # User portfolio documentation
│
├── data/
│   └── sales_data.csv      # Auto-generated 2,500+ record transaction dataset
│
├── src/
│   ├── data_loader.py      # File loader, schema validator, quality metrics auditor
│   ├── preprocessing.py    # Preprocessing engines, duplicates, imputations
│   ├── analytics.py        # Financial KPIs, time groupings, growth, insights
│   ├── visualizations.py   # Plotly interactive graphs, heatmaps, treemaps
│   └── helpers.py          # Custom HSL styling, dataset generator, download exporters
│
├── screenshots/            # Dashboard operational interface capture guidelines
│
├── assets/                 # Custom graphic elements, icons, logos
│
└── report/
    └── Project_Report.md   # Final academic-grade Internship Project Report
```

---

## ⚙️ Installation Guide

### Prerequisites
*   Python 3.10 or higher installed.
*   Access to a terminal/command prompt.

### Steps

1.  **Clone or Unpack the Workspace:**
    ```bash
    git clone https://github.com/your-portfolio/Sales_Trend_Visualization.git
    cd Sales_Trend_Visualization
    ```

2.  **Establish a Virtual Environment:**
    ```bash
    python -m venv venv
    ```
    *   *Windows Activation:*
        ```bash
        venv\Scripts\activate
        ```
    *   *macOS/Linux Activation:*
        ```bash
        source venv/bin/activate
        ```

3.  **Install Required Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Launch the Streamlit Platform:**
    ```bash
    streamlit run app.py
    ```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## ⚡ Usage Instructions

*   **Load Datasets:** The application starts by automatically generating the `data/sales_data.csv` sample dataset. To test custom files, upload any formatted CSV matching the REQUIRED fields in the sidebar.
*   **Narrow Selections:** Use the sidebar to restrict observations by date brackets, product lists, categories, target regions, or sales channels. All charts and KPI metrics recalculate instantly.
*   **Run Preprocessing Pipeline:** Go to **Tab 8 (Raw Data & Quality)**, choose your missing value strategy, click "Execute Data Cleaning Pipeline", and review the before/after preprocessing reports.
*   **Download Custom Data:** Apply filters in the sidebar and download your customized subsets via the CSV or Excel export buttons in the sidebar.
*   **Review automated insights:** Navigate to **Tab 7 (Business Insights)** for high-level business briefings and concrete optimization directives.

---

## 📈 Future Scope

1.  **Machine Learning Forecasting:** Integrate Scikit-Learn ARIMA, Prophet, or LSTM models to predict future revenue and inventory needs for upcoming quarters.
2.  **Customer Cohort Analysis:** Track customer lifetime value (CLV) and cohort retention rates based on `Customer_ID` patterns.
3.  **Live Database Integration:** Connect loader modules directly to Snowflake, PostgreSQL, BigQuery, or AWS S3 buckets for live transactional processing.
4.  **Automatic PDF Report Generating:** Implement an automated compiler generating printable monthly executive reports summarizing KPIs and visual graphs.
