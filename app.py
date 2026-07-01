import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Number Formatter
# ----------------------------

def format_number(num):
    if abs(num) >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"${num/1_000:.0f}K"
    else:
        return f"${num:.2f}"

st.set_page_config(
    page_title="Business Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Sales Performance Dashboard")

st.markdown(
    """
### Future Interns — Data Science & Analytics Task 1

Interactive dashboard built using **Python, Streamlit, Plotly, and Pandas**.

This dashboard helps businesses analyze sales performance, profitability, customer segments, regional performance, and product trends.
"""
)

df = pd.read_csv("processed_data/Superstore_Final.csv")

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segment = st.sidebar.multiselect(
    "Select Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]

st.sidebar.markdown("---")

st.sidebar.info(
    """
## FUTURE_DS_01

**Business Sales Analytics**

Dataset:
Superstore Sales

Tools:
- Python
- Pandas
- Plotly
- Streamlit

Developer:
**Durlabh Thareja**
"""
)

# ----------------------------
# KPI Calculations
# ----------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
avg_order = total_sales / total_orders if total_orders else 0

# ----------------------------
# KPI Cards
# ----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", format_number(total_sales))
col2.metric("📈 Total Profit", format_number(total_profit))
col3.metric("📦 Total Orders", f"{total_orders:,}")
col4.metric("🛒 Avg Order", format_number(avg_order))

# ----------------------------
# Monthly Sales Trend
# ----------------------------

monthly_sales = (
    filtered_df
    .groupby(["Year", "Month Number"])["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Date"] = pd.to_datetime(
    monthly_sales["Year"].astype(str)
    + "-"
    + monthly_sales["Month Number"].astype(str)
    + "-01"
)

monthly_sales = monthly_sales.sort_values("Date")

fig = px.line(
    monthly_sales,
    x="Date",
    y="Sales",
    markers=True,
    title="📈 Monthly Sales Trend",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales (USD)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Sales & Profit by Category
# ----------------------------

category_data = (
    filtered_df
    .groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        category_data,
        x="Category",
        y="Sales",
        color="Category",
        title="💰 Sales by Category",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.bar(
        category_data,
        x="Category",
        y="Profit",
        color="Category",
        title="📈 Profit by Category",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
# Regional Performance
# ----------------------------

region_data = (
    filtered_df
    .groupby("Region")[["Sales","Profit"]]
    .sum()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        region_data,
        x="Region",
        y="Sales",
        color="Region",
        title="🌍 Sales by Region",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.bar(
        region_data,
        x="Region",
        y="Profit",
        color="Region",
        title="💵 Profit by Region",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
# Products & Segments
# ----------------------------

top_products = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

segment_data = (
    filtered_df
    .groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="🏆 Top 10 Products",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        segment_data,
        values="Sales",
        names="Segment",
        title="👥 Sales by Segment",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
# Discount Analysis
# ----------------------------

discount_data = (
    filtered_df
    .groupby("Discount")["Profit"]
    .mean()
    .reset_index()
)

fig = px.line(
    discount_data,
    x="Discount",
    y="Profit",
    markers=True,
    title="📉 Average Profit by Discount",
    color_discrete_sequence=px.colors.sequential.Blues_r
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📋 Key Business Insights")

st.markdown("""
- 📈 Sales increased steadily over the analysis period.
- 💰 Technology products generated the highest revenue.
- 🌍 Regional performance varied significantly across markets.
- 👥 Consumer customers contributed the largest share of sales.
- 🎯 Higher discounts generally reduced average profitability.
""")