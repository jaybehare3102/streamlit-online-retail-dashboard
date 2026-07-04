import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data, format_currency
from utils.sidebar import create_sidebar
from utils.layout import page_header
from utils.kpi import render_kpi_cards
from utils.chart_style import apply_dark_theme
from utils.calculations import (
    product_summary,
    customer_summary,
    country_summary,
    sales_summary,
    rfm_summary
)


# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Recommendation Engine",
    page_icon="🎁",
    layout="wide"
)

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

products = product_summary(filtered_df)

customers = customer_summary(filtered_df)

countries = country_summary(filtered_df)

monthly, quarterly, yearly, weekday, hourly = sales_summary(filtered_df)

rfm = rfm_summary(filtered_df)


# ==========================================================
# Header
# ==========================================================

page_header(
    "🎁 Recommendation Engine",
    "AI Inspired Business Recommendations"
)



# ==========================================================
# KPI Cards
# ==========================================================

champions = (rfm["Segment"] == "Champions").sum()

a_products = (products["ABC"] == "A").sum()

top_country = countries.iloc[0]["Country"]

recommendations = 8


render_kpi_cards(

[
    (
        "🏆",
        "Champions",
        f"{champions:,}"
    ),

    (
        "📦",
        "A Products",
        f"{a_products:,}"
    ),

    (
        "🌍",
        "Top Market",
        top_country
    ),

    (
        "💡",
        "Recommendations",
        recommendations
    )

]

)


# ==========================================================
# Executive Recommendation
# ==========================================================

st.markdown("---")

st.subheader("💡 Executive Recommendations")

top_product = products.iloc[0]
top_country = countries.iloc[0]
top_customer = customers.iloc[0]

peak_hour = hourly.loc[
    hourly["Revenue"].idxmax(),
    "Hour"
]

peak_day = weekday.loc[
    weekday["Revenue"].idxmax(),
    "DayName"
]

champions = (rfm["Segment"] == "Champions").sum()
at_risk = (rfm["Segment"] == "At Risk").sum()

st.markdown(f"""
<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:30px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
📈 Executive Business Recommendations
</h2>

<hr>

<h3>📦 Product Strategy</h3>

<ul>
<li>Increase inventory of <b>{top_product["Description"]}</b> as it is the highest-performing product.</li>
<li>Maintain sufficient stock of all <b>ABC Category A</b> products.</li>
<li>Bundle low-performing (Category C) products with best-selling products to improve sales.</li>
</ul>

<h3>👥 Customer Strategy</h3>

<ul>
<li>Reward <b>{champions}</b> Champion customers with exclusive loyalty rewards.</li>
<li>Launch personalized campaigns to re-engage <b>{at_risk}</b> At-Risk customers.</li>
<li>Upsell premium products to your highest-value customers.</li>
</ul>

<h3>🌍 Market Strategy</h3>

<ul>
<li>Focus expansion and marketing efforts in <b>{top_country["Country"]}</b>, the highest revenue market.</li>
<li>Identify opportunities to improve sales in lower-performing countries.</li>
</ul>

<h3>📈 Sales Strategy</h3>

<ul>
<li>Schedule promotional campaigns on <b>{peak_day}</b>, your highest-performing sales day.</li>
<li>Run flash sales around <b>{peak_hour}:00</b>, the peak shopping hour.</li>
</ul>

<h3>💰 Revenue Growth Strategy</h3>

<ul>
<li>Increase repeat purchases through personalized product recommendations.</li>
<li>Monitor customer lifetime value using RFM segmentation.</li>
<li>Use data-driven marketing campaigns to improve customer retention and maximize profitability.</li>
</ul>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# Executive Recommendation
# ==========================================================

st.markdown("---")

st.subheader("💡 Executive Recommendations")

top_product = products.iloc[0]
top_country = countries.iloc[0]
top_customer = customers.iloc[0]

peak_hour = hourly.loc[
    hourly["Revenue"].idxmax(),
    "Hour"
]

peak_day = weekday.loc[
    weekday["Revenue"].idxmax(),
    "DayName"
]

champions = (rfm["Segment"] == "Champions").sum()
at_risk = (rfm["Segment"] == "At Risk").sum()

st.markdown(f"""
<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:30px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
📈 Executive Business Recommendations
</h2>

<hr>

<h3>📦 Product Strategy</h3>

<ul>
<li>Increase inventory of <b>{top_product["Description"]}</b> as it is the highest-performing product.</li>
<li>Maintain sufficient stock of all <b>ABC Category A</b> products.</li>
<li>Bundle low-performing (Category C) products with best-selling products to improve sales.</li>
</ul>

<h3>👥 Customer Strategy</h3>

<ul>
<li>Reward <b>{champions}</b> Champion customers with exclusive loyalty rewards.</li>
<li>Launch personalized campaigns to re-engage <b>{at_risk}</b> At-Risk customers.</li>
<li>Upsell premium products to your highest-value customers.</li>
</ul>

<h3>🌍 Market Strategy</h3>

<ul>
<li>Focus expansion and marketing efforts in <b>{top_country["Country"]}</b>, the highest revenue market.</li>
<li>Identify opportunities to improve sales in lower-performing countries.</li>
</ul>

<h3>📈 Sales Strategy</h3>

<ul>
<li>Schedule promotional campaigns on <b>{peak_day}</b>, your highest-performing sales day.</li>
<li>Run flash sales around <b>{peak_hour}:00</b>, the peak shopping hour.</li>
</ul>

<h3>💰 Revenue Growth Strategy</h3>

<ul>
<li>Increase repeat purchases through personalized product recommendations.</li>
<li>Monitor customer lifetime value using RFM segmentation.</li>
<li>Use data-driven marketing campaigns to improve customer retention and maximize profitability.</li>
</ul>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# Top Recommended Products
# ==========================================================

st.markdown("---")

st.subheader("⭐ Top Recommended Products")

top_products = (
    products[
        [
            "Description",
            "Revenue",
            "Quantity",
            "Orders",
            "ABC"
        ]
    ]
    .head(10)
)

fig_products = px.bar(

    top_products,

    x="Revenue",

    y="Description",

    orientation="h",

    color="ABC",

    text="Revenue",

    template="plotly_dark",

    color_discrete_map={
        "A": "#22c55e",
        "B": "#f59e0b",
        "C": "#ef4444"
    }

)

fig_products.update_traces(

    texttemplate="£%{x:,.0f}",

    textposition="outside"

)

fig_products.update_layout(

    title="Top 10 Recommended Products",

    height=600,

    xaxis_title="Revenue (£)",

    yaxis_title="",

    showlegend=True

)

apply_dark_theme(fig_products)

st.plotly_chart(

    fig_products,

    use_container_width=True,

    key="recommended_products"
)




st.markdown("### 📋 Product Recommendation Details")

recommendation_table = top_products.rename(
    columns={
        "Description": "Product",
        "Revenue": "Revenue (£)",
        "Quantity": "Units Sold",
        "Orders": "Orders",
        "ABC": "Priority"
    }
)

st.dataframe(

    recommendation_table,

    use_container_width=True,

    hide_index=True

)


st.markdown("---")

st.subheader("💡 Product Recommendations")

best_product = products.iloc[0]

a_products = (products["ABC"] == "A").sum()

b_products = (products["ABC"] == "B").sum()

c_products = (products["ABC"] == "C").sum()

st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
📦 Inventory Recommendations
</h2>

<ul>

<li><b>{best_product['Description']}</b> is the highest-performing product and should always remain in stock.</li>

<li><b>{a_products}</b> products belong to <b>ABC Category A</b>. These products generate the highest business value.</li>

<li>Maintain adequate stock levels for Category A products to avoid stockouts.</li>

<li>Promote Category B products through seasonal campaigns to increase revenue.</li>

<li>Bundle Category C products with popular products to improve inventory turnover.</li>

<li>Regularly monitor sales performance and update inventory planning based on demand.</li>

</ul>

</div>

""", unsafe_allow_html=True)



# ==========================================================
# Customer Recommendation Engine
# ==========================================================

st.markdown("---")

st.subheader("👥 Customer Recommendation Engine")


segment_summary = (
    rfm.groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        Revenue=("Monetary", "sum"),
        AvgFrequency=("Frequency", "mean")
    )
    .reset_index()
)



fig_segment = px.bar(

    segment_summary,

    x="Segment",

    y="Customers",

    color="Segment",

    text="Customers",

    template="plotly_dark"
)

fig_segment.update_layout(

    title="Customer Segments",

    height=500,

    xaxis_title="",

    yaxis_title="Customers",

    showlegend=False

)

apply_dark_theme(fig_segment)

st.plotly_chart(

    fig_segment,

    use_container_width=True,

    key="customer_segments"
)


st.markdown("### 📋 Segment Performance")

segment_table = segment_summary.rename(
    columns={
        "Customers": "No. of Customers",
        "Revenue": "Revenue (£)",
        "AvgFrequency": "Average Frequency"
    }
)

st.dataframe(

    segment_table,

    use_container_width=True,

    hide_index=True

)



st.markdown("---")

st.subheader("💡 Customer Strategies")


champions = (rfm["Segment"] == "Champions").sum()
loyal = (rfm["Segment"] == "Loyal Customers").sum()
potential = (rfm["Segment"] == "Potential Loyalists").sum()
risk = (rfm["Segment"] == "At Risk").sum()
lost = (rfm["Segment"] == "Lost Customers").sum()


col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon">🏆</div>

<div class="kpi-title">
Champions ({champions})
</div>

<div class="kpi-value" style="font-size:15px;">

Reward with VIP memberships

Exclusive discounts

Early-access offers

Referral incentives

</div>

</div>

""", unsafe_allow_html=True)

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon">❤️</div>

<div class="kpi-title">
Loyal Customers ({loyal})
</div>

<div class="kpi-value" style="font-size:15px;">

Cross-sell premium products

Reward repeat purchases

Personalized recommendations

</div>

</div>

""", unsafe_allow_html=True)

with col2:

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon">🌱</div>

<div class="kpi-title">
Potential Loyalists ({potential})
</div>

<div class="kpi-value" style="font-size:15px;">

Coupon campaigns

Limited-time offers

Membership promotions

</div>

</div>

""", unsafe_allow_html=True)

    st.markdown(f"""

<div class="kpi-card">

<div class="kpi-icon">⚠️</div>

<div class="kpi-title">
At Risk ({risk})
</div>

<div class="kpi-value" style="font-size:15px;">

Win-back campaigns

Personalized emails

Special discounts

</div>

</div>

""", unsafe_allow_html=True)
    



st.markdown("---")

st.subheader("🚀 Customer Recommendation Summary")

st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
🎯 Customer Action Plan
</h2>

<ul>

<li>Reward <b>{champions}</b> Champion customers with premium loyalty benefits.</li>

<li>Increase repeat purchases from Loyal Customers through cross-selling.</li>

<li>Convert Potential Loyalists into regular buyers using personalized promotions.</li>

<li>Launch win-back campaigns targeting <b>{risk}</b> At-Risk customers.</li>

<li>Analyze churn reasons for <b>{lost}</b> Lost Customers and design reactivation campaigns.</li>

<li>Use RFM segmentation continuously to improve customer retention and lifetime value.</li>

</ul>

</div>

""", unsafe_allow_html=True)




# ==========================================================
# Country Recommendation Engine
# ==========================================================

st.markdown("---")

st.subheader("🌍 Country Recommendation Engine")

top_countries = countries.head(10)

fig_country = px.bar(

    top_countries,

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

    title="Top Revenue Generating Countries",

    height=550,

    xaxis_title="Revenue (£)",

    yaxis_title="",

    coloraxis_showscale=False

)

apply_dark_theme(fig_country)

st.plotly_chart(

    fig_country,

    use_container_width=True,

    key="recommend_country"

)



best_country = countries.iloc[0]
lowest_country = countries.iloc[-1]

st.markdown("""

### 🌎 Country Strategy

""")

st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
🌍 Market Expansion Strategy
</h2>

<ul>

<li><b>{best_country['Country']}</b> is the highest revenue market and should receive priority inventory allocation.</li>

<li>Increase marketing investment in high-performing countries.</li>

<li>Study purchasing patterns in low-performing countries like <b>{lowest_country['Country']}</b>.</li>

<li>Introduce region-specific promotions to improve customer engagement.</li>

<li>Monitor country-wise sales regularly to identify emerging markets.</li>

</ul>

</div>

""", unsafe_allow_html=True)




# ==========================================================
# Sales Recommendation Engine
# ==========================================================

st.markdown("---")

st.subheader("📈 Sales Recommendation Engine")



peak_hour = hourly.loc[
    hourly["Revenue"].idxmax(),
    "Hour"
]

peak_day = weekday.loc[
    weekday["Revenue"].idxmax(),
    "DayName"
]



st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
📊 Sales Growth Strategy
</h2>

<ul>

<li>Launch promotional campaigns during <b>{peak_day}</b>.</li>

<li>Schedule flash sales around <b>{peak_hour}:00</b>.</li>

<li>Increase staffing during peak shopping hours.</li>

<li>Focus advertising during high-performing months.</li>

<li>Track monthly revenue trends for demand forecasting.</li>

</ul>

</div>

""", unsafe_allow_html=True)



# ==========================================================
# Inventory Recommendation Engine
# ==========================================================

st.markdown("---")

st.subheader("📦 Inventory Recommendations")

abc_summary = (

    products.groupby("ABC")

    .agg(

        Products=("Description","count"),

        Revenue=("Revenue","sum")

    )

    .reset_index()

)

fig_abc = px.pie(

    abc_summary,

    names="ABC",

    values="Revenue",

    hole=0.55,

    template="plotly_dark"

)

fig_abc.update_layout(

    title="ABC Revenue Distribution",

    height=500

)

apply_dark_theme(fig_abc)

st.plotly_chart(

    fig_abc,

    use_container_width=True,

    key="abc_recommendation"

)



a = (products["ABC"]=="A").sum()
b = (products["ABC"]=="B").sum()
c = (products["ABC"]=="C").sum()

st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
📦 Inventory Optimization
</h2>

<ul>

<li><b>{a}</b> Category A products should always remain in stock.</li>

<li><b>{b}</b> Category B products require periodic inventory reviews.</li>

<li><b>{c}</b> Category C products should be promoted using bundle offers.</li>

<li>Monitor stock levels continuously to reduce stockouts.</li>

<li>Optimize procurement based on ABC analysis and seasonal demand.</li>

</ul>

</div>

""", unsafe_allow_html=True)




# ==========================================================
# Download Recommendation Report
# ==========================================================

st.markdown("---")

st.subheader("📥 Download Recommendation Report")

report = pd.DataFrame({

    "Recommendation":[

        "Increase inventory of Category A products",

        "Reward Champion customers",

        "Run win-back campaigns for At-Risk customers",

        "Expand marketing in top-performing countries",

        "Schedule promotions during peak sales hours",

        "Bundle Category C products with Category A products",

        "Monitor RFM segmentation monthly",

        "Track monthly revenue trends"

    ]

})

csv = report.to_csv(index=False)

st.download_button(

    "📄 Download Business Recommendation Report",

    csv,

    "Business_Recommendations.csv",

    "text/csv"

)



