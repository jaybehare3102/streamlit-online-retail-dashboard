import streamlit as st
import plotly.express as px

from utils.data_loader import load_data, format_currency
from utils.sidebar import create_sidebar
from utils.layout import page_header
from utils.kpi import render_kpi_cards
from utils.insights import render_insights
from utils.calculations import country_summary
from utils.chart_style import apply_dark_theme


st.set_page_config(
    page_title="Country Analysis",
    page_icon="🌍",
    layout="wide"
)


with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


df = load_data()

filtered_df = create_sidebar(df)

countries = country_summary(filtered_df)


page_header(
    "🌍 Country Analysis",
    "Geographical Revenue & Market Performance"
)



# ==========================================================
# KPI Cards
# ==========================================================

total_countries = len(countries)

total_revenue = countries["Revenue"].sum()

total_orders = countries["Orders"].sum()

total_customers = countries["Customers"].sum()

avg_order_value = countries["AverageOrderValue"].mean()


render_kpi_cards(

[
    (
        "🌍",
        "Countries",
        f"{total_countries:,}"
    ),

    (
        "💰",
        "Revenue",
        format_currency(total_revenue)
    ),

    (
        "🛒",
        "Orders",
        f"{int(total_orders):,}"
    ),

    (
        "💷",
        "Avg Order Value",
        format_currency(avg_order_value)
    )

]

)


st.markdown("---")

st.subheader("🌟 Country Spotlight")

spotlight = countries.iloc[0]

st.markdown(f"""
<div style="
background: linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
">

<h2 style="color:#38bdf8;">
🌍 Highest Revenue Country
</h2>

<table style="width:100%;color:white;font-size:17px;">

<tr>
<td><b>Country</b></td>
<td>{spotlight["Country"]}</td>
</tr>

<tr>
<td><b>Revenue</b></td>
<td>{format_currency(spotlight["Revenue"])}</td>
</tr>

<tr>
<td><b>Orders</b></td>
<td>{int(spotlight["Orders"]):,}</td>
</tr>

<tr>
<td><b>Customers</b></td>
<td>{int(spotlight["Customers"]):,}</td>
</tr>

<tr>
<td><b>Quantity Sold</b></td>
<td>{int(spotlight["Quantity"]):,}</td>
</tr>

<tr>
<td><b>Average Order Value</b></td>
<td>{format_currency(spotlight["AverageOrderValue"])}</td>
</tr>

<tr>
<td><b>Revenue Share</b></td>
<td>{spotlight["RevenuePercent"]:.2f}%</td>
</tr>

</table>

</div>
""",
unsafe_allow_html=True)




st.markdown("---")

highest_revenue = countries.loc[countries["Revenue"].idxmax()]
highest_orders = countries.loc[countries["Orders"].idxmax()]
highest_customers = countries.loc[countries["Customers"].idxmax()]
highest_quantity = countries.loc[countries["Quantity"].idxmax()]
highest_aov = countries.loc[countries["AverageOrderValue"].idxmax()]
largest_market = countries.loc[countries["RevenuePercent"].idxmax()]

render_insights(

[
    (
        "🏆 Highest Revenue",
        highest_revenue["Country"]
    ),

    (
        "🛒 Highest Orders",
        highest_orders["Country"]
    ),

    (
        "👥 Most Customers",
        highest_customers["Country"]
    ),

    (
        "📦 Highest Quantity",
        highest_quantity["Country"]
    ),

    (
        "💷 Highest AOV",
        highest_aov["Country"]
    ),

    (
        "🌍 Largest Market",
        largest_market["Country"]
    )

]

)


st.markdown("---")

st.subheader("📊 Country Performance Analysis")

col1, col2 = st.columns(2)



with col1:

    top_revenue = (
        countries.nlargest(10, "Revenue")
        .sort_values("Revenue")
    )

    fig_revenue = px.bar(
        top_revenue,
        x="Revenue",
        y="Country",
        orientation="h",
        color="Revenue",
        color_continuous_scale="Blues",
        text="Revenue",
        template="plotly_dark"
    )

    fig_revenue.update_traces(
        texttemplate="£%{x:,.0f}",
        textposition="outside"
    )

    fig_revenue = apply_dark_theme(fig_revenue)

    fig_revenue.update_layout(
        title="💰 Top 10 Countries by Revenue",
        height=500,
        xaxis_title="Revenue (£)",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
        key="country_revenue"
    )






with col2:

    top_orders = (
        countries.nlargest(10, "Orders")
        .sort_values("Orders")
    )

    fig_orders = px.bar(
        top_orders,
        x="Orders",
        y="Country",
        orientation="h",
        color="Orders",
        color_continuous_scale="Blues",
        text="Orders",
        template="plotly_dark"
    )

    fig_orders.update_traces(
        textposition="outside"
    )

    fig_orders = apply_dark_theme(fig_orders)

    fig_orders.update_layout(
        title="🛒 Top 10 Countries by Orders",
        height=500,
        xaxis_title="Orders",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_orders,
        use_container_width=True,
        key="country_orders"
    )





st.markdown("---")

st.subheader("👥 Customer & Quantity Analysis")

col1, col2 = st.columns(2)


with col1:

    top_customers = (
        countries.nlargest(10, "Customers")
        .sort_values("Customers")
    )

    fig_customers = px.bar(
        top_customers,
        x="Customers",
        y="Country",
        orientation="h",
        color="Customers",
        color_continuous_scale="Blues",
        text="Customers",
        template="plotly_dark"
    )

    fig_customers.update_traces(
        textposition="outside"
    )

    fig_customers = apply_dark_theme(fig_customers)

    fig_customers.update_layout(
        title="👥 Top 10 Countries by Customers",
        height=500,
        xaxis_title="Customers",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_customers,
        use_container_width=True,
        key="country_customers"
    )



with col2:

    top_quantity = (
        countries.nlargest(10, "Quantity")
        .sort_values("Quantity")
    )

    fig_quantity = px.bar(
        top_quantity,
        x="Quantity",
        y="Country",
        orientation="h",
        color="Quantity",
        color_continuous_scale="Blues",
        text="Quantity",
        template="plotly_dark"
    )

    fig_quantity.update_traces(
        textposition="outside"
    )

    fig_quantity = apply_dark_theme(fig_quantity)

    fig_quantity.update_layout(
        title="📦 Top 10 Countries by Quantity Sold",
        height=500,
        xaxis_title="Quantity Sold",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig_quantity,
        use_container_width=True,
        key="country_quantity"
    )




st.markdown("---")

st.subheader("📈 Revenue vs Orders Analysis")



fig_scatter = px.scatter(

    countries,

    x="Orders",

    y="Revenue",

    size="Customers",

    color="RevenuePercent",

    hover_name="Country",

    hover_data=[
        "Revenue",
        "Orders",
        "Customers",
        "Quantity",
        "AverageOrderValue"
    ],

    color_continuous_scale="Blues",

    template="plotly_dark"
)

fig_scatter = apply_dark_theme(fig_scatter)

fig_scatter.update_layout(

    title="Revenue vs Orders by Country",

    height=650,

    xaxis_title="Orders",

    yaxis_title="Revenue (£)",

    coloraxis_colorbar_title="Revenue %"

)

st.plotly_chart(

    fig_scatter,

    use_container_width=True,

    key="country_scatter"

)



st.markdown("---")

st.subheader("🌍 Revenue Distribution")

col1, col2 = st.columns(2)




with col1:

    revenue_share = countries.copy()

    revenue_share.loc[10:, "Country"] = "Others"

    revenue_share = (
        revenue_share
        .groupby("Country", as_index=False)
        .sum(numeric_only=True)
    )

    fig_donut = px.pie(

        revenue_share,

        names="Country",

        values="Revenue",

        hole=0.65,

        color_discrete_sequence=px.colors.sequential.Blues_r,

        template="plotly_dark"
    )

    fig_donut = apply_dark_theme(fig_donut)

    fig_donut.update_layout(

        title="Revenue Share by Country",

        height=500

    )

    st.plotly_chart(

        fig_donut,

        use_container_width=True,

        key="country_donut"

    )






with col2:

    fig_map = px.choropleth(

        countries,

        locations="Country",

        locationmode="country names",

        color="Revenue",

        hover_name="Country",

        color_continuous_scale="Blues",

        template="plotly_dark"
    )

    fig_map = apply_dark_theme(fig_map)

    fig_map.update_layout(

        title="Global Revenue Distribution",

        height=500,

        geo=dict(
            bgcolor="#1e293b",
            showframe=False,
            showcoastlines=False,
            projection_type="natural earth"
        )

    )

    st.plotly_chart(

        fig_map,

        use_container_width=True,

        key="country_map"

    )




st.markdown("---")

st.subheader("📋 Country Performance")



country_table = countries.copy()



country_table["Revenue"] = country_table["Revenue"].round(2)

country_table["AverageOrderValue"] = (
    country_table["AverageOrderValue"].round(2)
)

country_table["RevenuePercent"] = (
    country_table["RevenuePercent"].round(2)
)

country_table["Quantity"] = (
    country_table["Quantity"]
    .map(lambda x: f"{int(x):,}")
)

country_table["Orders"] = (
    country_table["Orders"]
    .map(lambda x: f"{int(x):,}")
)

country_table["Customers"] = (
    country_table["Customers"]
    .map(lambda x: f"{int(x):,}")
)




country_table = country_table[
    [
        "Country",
        "Revenue",
        "Orders",
        "Customers",
        "Quantity",
        "AverageOrderValue",
        "RevenuePercent"
    ]
]




st.dataframe(
    country_table,
    use_container_width=True,
    hide_index=True,
    height=500
)



st.markdown("---")

st.subheader("💡 Business Recommendations")



st.success("""
✅ Continue investing in high-revenue countries to maximize profitability and maintain market leadership.
""")

st.info("""
🌍 Expand marketing efforts in countries with high customer counts but comparatively lower revenue to improve conversion.
""")

st.warning("""
📦 Optimize inventory and logistics in countries with high order volumes to reduce delivery costs and improve efficiency.
""")

st.error("""
⚠ Review low-performing countries and evaluate pricing, promotions, or distribution strategies to increase market penetration.
""")




st.markdown("---")

st.subheader("📝 Executive Summary")



st.markdown("---")

st.subheader("📝 Executive Summary")



