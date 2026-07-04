import streamlit as st
import plotly.express as px

from utils.data_loader import load_data, format_currency
from utils.sidebar import create_sidebar
from utils.layout import page_header
from utils.kpi import render_kpi_cards
from utils.insights import render_insights
from utils.calculations import (
    sales_summary,
    customer_summary,
    product_summary,
    country_summary
)
from utils.chart_style import apply_dark_theme


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🏠",
    layout="wide"
)


# ==========================================================
# Load CSS
# ==========================================================

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# ==========================================================
# Load Data
# ==========================================================

df = load_data()

filtered_df = create_sidebar(df)


# ==========================================================
# Calculated Tables
# ==========================================================

customer_df = customer_summary(filtered_df)

product_df = product_summary(filtered_df)

country_df = country_summary(filtered_df)

monthly, quarterly, yearly, weekday, hourly = sales_summary(filtered_df)


# ==========================================================
# Dashboard Header
# ==========================================================

page_header(
    "🏠 Executive Dashboard",
    "Complete Business Performance Overview"
)



# ==========================================================
# KPI Cards
# ==========================================================

total_revenue = filtered_df["TotalPrice"].sum()

total_orders = filtered_df["InvoiceNo"].nunique()

total_customers = filtered_df["CustomerID"].nunique()

total_products = filtered_df["StockCode"].nunique()


render_kpi_cards(

[
    (
        "💰",
        "Revenue",
        format_currency(total_revenue)
    ),

    (
        "🛒",
        "Orders",
        f"{total_orders:,}"
    ),

    (
        "👥",
        "Customers",
        f"{total_customers:,}"
    ),

    (
        "📦",
        "Products",
        f"{total_products:,}"
    )

]

)




st.markdown("---")


best_country = country_df.iloc[0]["Country"]

best_product = product_df.iloc[0]["Description"]

best_customer = customer_df.iloc[0]["CustomerID"]

highest_revenue_month = (
    monthly.sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]["MonthName"]
)


render_insights(

[
    (
        "🌍 Top Country",
        best_country
    ),

    (
        "📦 Best Product",
        best_product
    ),

    (
        "👤 Best Customer",
        f"Customer {int(best_customer)}"
    ),

    (
        "📈 Best Month",
        highest_revenue_month
    )

]

)


st.markdown("---")

st.subheader("📊 Executive Summary")


summary = monthly.sort_values(
    "Revenue",
    ascending=False
).iloc[0]


st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
">

<h2 style="color:#38bdf8;">
📈 Business Overview
</h2>

<table style="width:100%;color:white;font-size:17px;">

<tr>
<td><b>Total Revenue</b></td>
<td>{format_currency(total_revenue)}</td>
</tr>

<tr>
<td><b>Total Orders</b></td>
<td>{total_orders:,}</td>
</tr>

<tr>
<td><b>Total Customers</b></td>
<td>{total_customers:,}</td>
</tr>

<tr>
<td><b>Total Products</b></td>
<td>{total_products:,}</td>
</tr>

<tr>
<td><b>Highest Revenue Month</b></td>
<td>{summary["MonthName"]}</td>
</tr>

<tr>
<td><b>Revenue</b></td>
<td>{format_currency(summary["Revenue"])}</td>
</tr>

</table>

</div>

""", unsafe_allow_html=True)




# ==========================================================
# Revenue Trend Analysis
# ==========================================================

st.markdown("---")

st.subheader("📈 Revenue Trend Analysis")

view = st.radio(
    "View Revenue By",
    ["Monthly", "Quarterly", "Yearly"],
    horizontal=True
)

if view == "Monthly":

    revenue_df = monthly.copy()

    revenue_df["Period"] = (
        revenue_df["MonthName"].str[:3]
        + " "
        + revenue_df["Year"].astype(str)
    )

elif view == "Quarterly":

    revenue_df = quarterly.copy()

    revenue_df["Period"] = (
        revenue_df["Quarter"]
        + " "
        + revenue_df["Year"].astype(str)
    )

else:

    revenue_df = yearly.copy()

    revenue_df["Period"] = revenue_df["Year"].astype(str)


fig = px.line(

    revenue_df,

    x="Period",

    y="Revenue",

    markers=True,

    template="plotly_dark"
)

fig.update_layout(

    title="Revenue Trend",

    height=500,

    xaxis_title="",

    yaxis_title="Revenue (£)"
)

apply_dark_theme(fig)

st.plotly_chart(

    fig,

    use_container_width=True,

    key="dashboard_revenue"
)



st.markdown("---")

col1, col2 = st.columns(2)



with col1:

    top_country = (
        country_df
        .head(10)
        .sort_values("Revenue")
    )

    fig_country = px.bar(

        top_country,

        x="Revenue",

        y="Country",

        orientation="h",

        color="Revenue",

        text="Revenue",

        template="plotly_dark",

        color_continuous_scale="Blues"
    )

    fig_country.update_traces(

        texttemplate="£%{x:,.0f}",

        textposition="outside"
    )

    fig_country.update_layout(

        title="🌍 Top 10 Countries",

        height=500,

        coloraxis_showscale=False,

        xaxis_title="Revenue (£)",

        yaxis_title=""
    )

    apply_dark_theme(fig_country)

    st.plotly_chart(

        fig_country,

        use_container_width=True,

        key="dashboard_country"
    )






with col2:

    top_products = (
        product_df
        .head(10)
        .sort_values("Quantity")
    )

    fig_product = px.bar(

        top_products,

        x="Quantity",

        y="Description",

        orientation="h",

        color="Quantity",

        text="Quantity",

        template="plotly_dark",

        color_continuous_scale="Viridis"
    )

    fig_product.update_traces(

        textposition="outside"
    )

    fig_product.update_layout(

        title="📦 Top 10 Products",

        height=500,

        coloraxis_showscale=False,

        xaxis_title="Quantity Sold",

        yaxis_title=""
    )

    apply_dark_theme(fig_product)

    st.plotly_chart(

        fig_product,

        use_container_width=True,

        key="dashboard_products"
    )




st.markdown("---")

col3, col4 = st.columns(2)



with col3:

    fig_hour = px.line(

        hourly,

        x="Hour",

        y="Revenue",

        markers=True,

        template="plotly_dark"
    )

    fig_hour.update_layout(

        title="⏰ Revenue by Hour",

        height=450,

        xaxis_title="Hour",

        yaxis_title="Revenue (£)"
    )

    apply_dark_theme(fig_hour)

    st.plotly_chart(

        fig_hour,

        use_container_width=True,

        key="dashboard_hour"
    )





with col4:

    fig_day = px.bar(

        weekday,

        x="DayName",

        y="Revenue",

        color="Revenue",

        template="plotly_dark",

        color_continuous_scale="Plasma"
    )

    fig_day.update_layout(

        title="📅 Revenue by Weekday",

        height=450,

        coloraxis_showscale=False,

        xaxis_title="",

        yaxis_title="Revenue (£)"
    )

    apply_dark_theme(fig_day)

    st.plotly_chart(

        fig_day,

        use_container_width=True,

        key="dashboard_weekday"
    )



st.markdown("---")

st.subheader("👥 Top Customers")

top_customer = (
    customer_df
    .head(10)
    .sort_values("Revenue")
    .copy()
)

top_customer["CustomerID"] = (
    top_customer["CustomerID"]
    .astype(str)
)

fig_customer = px.bar(

    top_customer,

    x="Revenue",

    y="CustomerID",

    orientation="h",

    color="Revenue",

    text="Revenue",

    template="plotly_dark",

    color_continuous_scale="Tealgrn"
)

fig_customer.update_traces(

    texttemplate="£%{x:,.0f}",

    textposition="outside"
)

fig_customer.update_layout(

    title="Top 10 Customers by Revenue",

    height=500,

    coloraxis_showscale=False,

    xaxis_title="Revenue (£)",

    yaxis_title="Customer ID"
)

fig_customer.update_yaxes(type="category")

apply_dark_theme(fig_customer)

st.plotly_chart(

    fig_customer,

    use_container_width=True,

    key="dashboard_customer"
)



# ==========================================================
# Monthly Business Summary
# ==========================================================

st.markdown("---")

st.subheader("📊 Monthly Business Summary")

monthly_table = monthly[
    [
        "Year",
        "MonthName",
        "Revenue",
        "Orders",
        "Quantity",
        "AverageOrderValue"
    ]
].copy()

monthly_table.rename(
    columns={
        "MonthName": "Month",
        "AverageOrderValue": "Average Order Value"
    },
    inplace=True
)

st.dataframe(
    monthly_table,
    use_container_width=True,
    hide_index=True
)





# ==========================================================
# Country Performance
# ==========================================================

st.markdown("---")

st.subheader("🌍 Country Performance")

country_table = country_df[
    [
        "Country",
        "Revenue",
        "Orders",
        "Customers",
        "Quantity",
        "AverageOrderValue"
    ]
].copy()

country_table.rename(
    columns={
        "AverageOrderValue":"Average Order Value"
    },
    inplace=True
)

st.dataframe(
    country_table,
    use_container_width=True,
    hide_index=True
)




# ==========================================================
# Product Performance
# ==========================================================

st.markdown("---")

st.subheader("📦 Product Performance")

product_table = product_df[
    [
        "StockCode",
        "Description",
        "Revenue",
        "Quantity",
        "Orders",
        "ABC"
    ]
].copy()

st.dataframe(
    product_table.head(20),
    use_container_width=True,
    hide_index=True
)



# ==========================================================
# Executive Recommendations
# ==========================================================

st.markdown("---")

st.subheader("💡 Executive Recommendations")

st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
📈 Business Strategy
</h2>

<hr>

<h4>🌍 Market Expansion</h4>

<ul>
<li>Focus marketing efforts on <b>{best_country}</b> while expanding into similar markets.</li>
<li>Analyze underperforming countries for growth opportunities.</li>
</ul>

<h4>📦 Product Strategy</h4>

<ul>
<li>Maintain inventory for high-performing products.</li>
<li>Bundle slow-moving products with best sellers.</li>
</ul>

<h4>👤 Customer Strategy</h4>

<ul>
<li>Reward high-value customers with loyalty benefits.</li>
<li>Use personalized recommendations to increase repeat purchases.</li>
</ul>

<h4>📈 Sales Strategy</h4>

<ul>
<li>Schedule campaigns during peak revenue months.</li>
<li>Increase staffing during peak shopping hours.</li>
</ul>

<h4>🎯 Business Goal</h4>

<ul>
<li>Improve customer retention.</li>
<li>Increase Average Order Value.</li>
<li>Expand profitable markets.</li>
<li>Optimize inventory planning.</li>
</ul>

</div>

""", unsafe_allow_html=True)




st.markdown("---")

dashboard_export = monthly_table.to_csv(index=False)

st.download_button(
    "📥 Download Monthly Summary",
    dashboard_export,
    "monthly_business_summary.csv",
    "text/csv"
)








