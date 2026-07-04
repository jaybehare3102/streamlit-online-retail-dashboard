import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data, format_currency
from utils.layout import page_header
from utils.charts import apply_dark_theme

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
    layout="wide"
)

# -------------------------------------------------------
# Load CSS
# -------------------------------------------------------

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = load_data()









# ===========================
# SIDEBAR
# ===========================

st.sidebar.image(
    "https://img.icons8.com/fluency/96/shopping-cart.png",
    width=80
)

st.sidebar.markdown("""
# 🛒 Shopper Spectrum

### Business Intelligence
""")

st.sidebar.divider()

# -------------------------
# Date Filters
# -------------------------

st.sidebar.subheader("📅 Date Filters")

# Year
years = sorted(df["Year"].unique())

selected_year = st.sidebar.selectbox(
    "Year",
    ["All"] + list(years)
)

# Quarter
quarters = ["Q1", "Q2", "Q3", "Q4"]

selected_quarter = st.sidebar.selectbox(
    "Quarter",
    ["All"] + quarters
)

# Month
month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

months = [m for m in month_order if m in df["MonthName"].unique()]

selected_month = st.sidebar.selectbox(
    "Month",
    ["All"] + months
)

st.sidebar.divider()

# -------------------------
# Geography
# -------------------------

st.sidebar.subheader("🌍 Geography")

countries = sorted(df["Country"].unique())

selected_country = st.sidebar.selectbox(
    "Country",
    ["All"] + countries
)

st.sidebar.divider()

# -------------------------
# Product Search
# -------------------------

st.sidebar.subheader("📦 Product Search")

selected_product = st.sidebar.text_input(
    "Product Name"
)

selected_stock = st.sidebar.text_input(
    "Stock Code"
)

st.sidebar.divider()

# -------------------------
# Customer Search
# -------------------------

st.sidebar.subheader("👤 Customer")

selected_customer = st.sidebar.number_input(
    "Customer ID",
    min_value=0,
    value=0,
    step=1
)

st.sidebar.divider()

# -------------------------
# Reset Information
# -------------------------

st.sidebar.info("Leave fields empty or select 'All' to view all records.")


# ===========================
# APPLY FILTERS
# ===========================

filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == selected_year
    ]

if selected_quarter != "All":
    filtered_df = filtered_df[
        filtered_df["Quarter"] == selected_quarter
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["MonthName"] == selected_month
    ]

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == selected_country
    ]

if selected_product != "":
    filtered_df = filtered_df[
        filtered_df["Description"]
        .str.contains(selected_product, case=False, na=False)
    ]

if selected_stock != "":
    filtered_df = filtered_df[
        filtered_df["StockCode"]
        .astype(str)
        .str.contains(selected_stock, case=False)
    ]

if selected_customer != 0:
    filtered_df = filtered_df[
        filtered_df["CustomerID"] == selected_customer
    ]

st.sidebar.divider()

st.sidebar.subheader("📋 Active Filters")

st.sidebar.write(f"Year : {selected_year}")

st.sidebar.write(f"Quarter : {selected_quarter}")

st.sidebar.write(f"Month : {selected_month}")

st.sidebar.write(f"Country : {selected_country}")







page_header(
    "👥 Customer Analysis",
    "Customer Purchasing Behaviour & Revenue Insights"
)


st.info(
"""
Analyze customer purchasing behaviour,
identify high-value customers,
understand buying frequency,
and explore customer spending patterns.
"""
)




total_customers = filtered_df["CustomerID"].nunique()

total_revenue = filtered_df["TotalPrice"].sum()

total_orders = filtered_df["InvoiceNo"].nunique()

avg_revenue = (
    total_revenue / total_customers
    if total_customers else 0
)

avg_orders = (
    total_orders / total_customers
    if total_customers else 0
)

avg_order_value = (
    total_revenue / total_orders
    if total_orders else 0
)



col1,col2,col3,col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-icon">👥</div>

    <div class="kpi-title">
    Customers
    </div>

    <div class="kpi-value">
    {total_customers:,}
    </div>

    </div>
    """,
    unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-icon">💰</div>

    <div class="kpi-title">
    Avg Revenue
    </div>

    <div class="kpi-value">
    {format_currency(avg_revenue)}
    </div>

    </div>
    """,
    unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-icon">🧾</div>

    <div class="kpi-title">
    Avg Orders
    </div>

    <div class="kpi-value">
    {avg_orders:.1f}
    </div>

    </div>
    """,
    unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="kpi-card">

    <div class="kpi-icon">💳</div>

    <div class="kpi-title">
    Avg Order Value
    </div>

    <div class="kpi-value">
    {format_currency(avg_order_value)}
    </div>

    </div>
    """,
    unsafe_allow_html=True)



st.markdown("---")

st.subheader("🏆 Customer Spotlight")


customer_summary = (
    filtered_df.groupby("CustomerID")
    .agg(
        Revenue=("TotalPrice", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum"),
        Country=("Country", lambda x: x.mode().iloc[0])
    )
    .reset_index()
)

customer_summary["Average Order Value"] = (
    customer_summary["Revenue"] /
    customer_summary["Orders"]
)

spotlight = customer_summary.sort_values(
    "Revenue",
    ascending=False
).iloc[0]





st.markdown(f"""
<div style="
background: linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
margin-bottom:25px;
">

<h3 style="color:#38bdf8;">
👑 Highest Value Customer
</h3>

<table style="width:100%;color:white;font-size:17px;">

<tr>
<td><b>Customer ID</b></td>
<td>{int(spotlight["CustomerID"])}</td>
</tr>

<tr>
<td><b>Country</b></td>
<td>{spotlight["Country"]}</td>
</tr>

<tr>
<td><b>Total Revenue</b></td>
<td>{format_currency(spotlight["Revenue"])}</td>
</tr>

<tr>
<td><b>Total Orders</b></td>
<td>{spotlight["Orders"]}</td>
</tr>

<tr>
<td><b>Items Purchased</b></td>
<td>{int(spotlight["Quantity"]):,}</td>
</tr>

<tr>
<td><b>Average Order Value</b></td>
<td>{format_currency(spotlight["Average Order Value"])}</td>
</tr>

</table>

</div>
""", unsafe_allow_html=True)



st.subheader("💡 Customer Insights")

col1, col2, col3 = st.columns(3)




col1.success(
    f"""
🏆 Highest Revenue Customer

Customer **{int(spotlight['CustomerID'])}**

Revenue: **{format_currency(spotlight['Revenue'])}**
"""
)



freq_customer = customer_summary.sort_values(
    "Orders",
    ascending=False
).iloc[0]

col2.info(
    f"""
⭐ Most Frequent Customer

Customer **{int(freq_customer['CustomerID'])}**

Orders: **{freq_customer['Orders']}**
"""
)



aov_customer = customer_summary.sort_values(
    "Average Order Value",
    ascending=False
).iloc[0]

col3.warning(
    f"""
💰 Highest Average Order Value

Customer **{int(aov_customer['CustomerID'])}**

AOV: **{format_currency(aov_customer['Average Order Value'])}**
"""
)




st.markdown("---")

left, right = st.columns(2)




with left:

    st.subheader("🏆 Top 10 Customers by Revenue")

    top_customers = (
        customer_summary
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig_top = px.bar(
        top_customers,
        x="Revenue",
        y=top_customers["CustomerID"].astype(str),
        orientation="h",
        text="Revenue",
        color="Revenue",
        color_continuous_scale="Purples",
        template="plotly_dark"
    )

    fig_top.update_traces(
        texttemplate="£%{x:,.0f}",
        textposition="outside"
    )

    fig_top.update_layout(
     template="plotly_dark",
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(
        color="white",
        size=13
    ),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=13,
        font_color="white"
    )
)

    fig_top = apply_dark_theme(fig_top)

    st.plotly_chart(
        fig_top,
        use_container_width=True,
        key="top_customer_chart"
    )


with right:

    st.subheader("🧾 Purchase Frequency")

    purchase_frequency = (
        filtered_df.groupby("CustomerID")["InvoiceNo"]
        .nunique()
        .reset_index(name="Orders")
        .sort_values("Orders", ascending=False)
        .head(10)
    )

    fig_freq = px.bar(
        purchase_frequency,
        x="Orders",
        y=purchase_frequency["CustomerID"].astype(str),
        orientation="h",
        color="Orders",
        color_continuous_scale="Blues",
        template="plotly_dark",
        text="Orders"
    )

    fig_freq.update_layout(
   template="plotly_dark",
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(
        color="white",
        size=13
    ),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=13,
        font_color="white"
    )
)

    fig_freq = apply_dark_theme(fig_freq)

    st.plotly_chart(
        fig_freq,
        use_container_width=True,
        key="purchase_frequency_chart"
    )




st.markdown("---")

col3, col4 = st.columns(2)


with col3:

    st.subheader("🥇 Customer Segments by Revenue")

    customer_summary["Segment"] = pd.cut(
        customer_summary["Revenue"],
        bins=[0, 1000, 5000, 10000, 50000, customer_summary["Revenue"].max()],
        labels=[
            "Occasional",
            "Low Value",
            "Medium Value",
            "High Value",
            "VIP"
        ],
        include_lowest=True
    )

    segment_df = (
        customer_summary["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_df.columns = ["Segment", "Customers"]

    segment_order = [
        "VIP",
        "High Value",
        "Medium Value",
        "Low Value",
        "Occasional"
    ]

    segment_df["Segment"] = pd.Categorical(
        segment_df["Segment"],
        categories=segment_order,
        ordered=True
    )

    segment_df = segment_df.sort_values("Segment")

    colors = [
        "#FBBF24",  # VIP - Gold
        "#A855F7",  # High Value - Purple
        "#3B82F6",  # Medium - Blue
        "#10B981",  # Low - Green
        "#64748B"   # Occasional - Gray
    ]

    fig_segment = px.pie(
        segment_df,
        names="Segment",
        values="Customers",
        hole=0.55,
        color="Segment",
        color_discrete_sequence=colors,
        template="plotly_dark"
    )

    fig_segment.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig_segment.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(
        color="white",
        size=13
    ),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=13,
        font_color="white"
    )
)

    fig_segment = apply_dark_theme(fig_segment)

    st.plotly_chart(
        fig_segment,
        use_container_width=True,
        key="customer_segment_chart"
    )




with col4:

    st.subheader("💰 Customer Lifetime Value")

    fig_clv = px.scatter(
        customer_summary,
        x="Orders",
        y="Revenue",
        size="Quantity",
        hover_name=customer_summary["CustomerID"].astype(str),
        template="plotly_dark",
        color="Revenue",
        color_continuous_scale="Purples"
    )

    fig_clv.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(
        color="white",
        size=13
    ),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_size=13,
        font_color="white"
    )
)
    fig_clv = apply_dark_theme(fig_clv)

    st.plotly_chart(
        fig_clv,
        use_container_width=True,
        key="customer_clv"
    )






st.markdown("---")

st.subheader("📋 Customer Performance Summary")

customer_table = (
    filtered_df.groupby("CustomerID")
    .agg(
        Country=("Country", lambda x: x.mode().iloc[0]),
        Revenue=("TotalPrice", "sum"),
        Orders=("InvoiceNo", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
)

customer_table["Average Order Value"] = (
    customer_table["Revenue"] /
    customer_table["Orders"]
)

customer_table = customer_table.sort_values(
    "Revenue",
    ascending=False
)

# Format values
customer_table["Revenue"] = customer_table["Revenue"].map(lambda x: f"£{x:,.2f}")
customer_table["Average Order Value"] = customer_table["Average Order Value"].map(
    lambda x: f"£{x:,.2f}"
)

st.dataframe(
    customer_table,
    use_container_width=True,
    hide_index=True,
    height=500
)




st.markdown("### 📌 Customer Performance Summary")

c1, c2, c3 = st.columns(3)

highest_customer = customer_summary.loc[
    customer_summary["Revenue"].idxmax(),
    "CustomerID"
]

highest_revenue = customer_summary["Revenue"].max()

avg_customer_revenue = customer_summary["Revenue"].mean()

c1.metric(
    "🏆 Top Customer",
    int(highest_customer)
)

c2.metric(
    "💰 Highest Revenue",
    format_currency(highest_revenue)
)

c3.metric(
    "📊 Avg Customer Revenue",
    format_currency(avg_customer_revenue)
)




st.markdown("---")

st.subheader("💡 Business Recommendations")

recommendations = [
    "Retain VIP customers through loyalty and exclusive offers.",
    "Target High Value customers with premium product bundles.",
    "Encourage Medium Value customers to increase purchase frequency.",
    "Provide personalized discounts to Low Value customers.",
    "Run re-engagement campaigns for Occasional customers."
]

for rec in recommendations:
    st.success(f"✔ {rec}")