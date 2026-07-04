import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_data, format_currency
from utils.sidebar import create_sidebar
from utils.layout import page_header
from utils.kpi import render_kpi_cards
from utils.insights import render_insights
from utils.calculations import rfm_summary
from utils.chart_style import apply_dark_theme


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="RFM Analysis",
    page_icon="💎",
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

rfm = rfm_summary(filtered_df)


# ==========================================================
# Page Header
# ==========================================================

page_header(
    "💎 RFM Analysis",
    "Customer Segmentation & Loyalty Analysis"
)


# ==========================================================
# KPI Cards
# ==========================================================




total_customers = len(rfm)

total_revenue = rfm["Monetary"].sum()

avg_frequency = rfm["Frequency"].mean()

avg_recency = rfm["Recency"].mean()


render_kpi_cards(

[
    (
        "👥",
        "Customers",
        f"{total_customers:,}"
    ),

    (
        "💰",
        "Revenue",
        format_currency(total_revenue)
    ),

    (
        "🔁",
        "Avg Frequency",
        f"{avg_frequency:.1f}"
    ),

    (
        "📅",
        "Avg Recency",
        f"{avg_recency:.0f} Days"
    )

]

)





# ==========================================================
# Customer Spotlight
# ==========================================================


st.markdown("---")

st.subheader("🌟 Customer Spotlight")


spotlight = (
    rfm.sort_values(
        "Monetary",
        ascending=False
    )
    .iloc[0]
)


st.markdown(f"""
<div style="
background: linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
">

<h2 style="color:#38bdf8;">
💎 Highest Value Customer
</h2>

<table style="width:100%;color:white;font-size:17px;">

<tr>
<td><b>Customer ID</b></td>
<td>{int(spotlight["CustomerID"])}</td>
</tr>

<tr>
<td><b>Total Revenue</b></td>
<td>{format_currency(spotlight["Monetary"])}</td>
</tr>

<tr>
<td><b>Purchase Frequency</b></td>
<td>{int(spotlight["Frequency"])}</td>
</tr>

<tr>
<td><b>Recency</b></td>
<td>{int(spotlight["Recency"])} Days</td>
</tr>

<tr>
<td><b>RFM Score</b></td>
<td>{spotlight["RFMScore"]}</td>
</tr>

<tr>
<td><b>Customer Segment</b></td>
<td>{spotlight["Segment"]}</td>
</tr>

</table>

</div>
""",
unsafe_allow_html=True)

# ==========================================================
# Business Insights
# ==========================================================

st.markdown("---")

highest_value = rfm.loc[
    rfm["Monetary"].idxmax()
]

most_frequent = rfm.loc[
    rfm["Frequency"].idxmax()
]

most_recent = rfm.loc[
    rfm["Recency"].idxmin()
]

champion = (
    rfm[rfm["Segment"] == "Champions"]
    .sort_values("Monetary", ascending=False)
)

if len(champion) > 0:
    champion_customer = champion.iloc[0]
    champion_text = f"Customer {int(champion_customer['CustomerID'])}"
else:
    champion_text = "No Champion"


render_insights(

[
    (
        "💰 Highest Revenue",
        f"Customer {int(highest_value['CustomerID'])}"
    ),

    (
        "🔁 Most Frequent",
        f"Customer {int(most_frequent['CustomerID'])}"
    ),

    (
        "🟢 Most Recent",
        f"Customer {int(most_recent['CustomerID'])}"
    ),

    (
        "🏆 Champion",
        champion_text
    )

]

)

# ==========================================================
# RFM Charts
# ==========================================================


st.markdown("---")

st.subheader("📊 Customer Behaviour Analysis")

col1, col2 = st.columns(2)




with col1:

    top_revenue = (
    rfm.nlargest(10, "Monetary")
    .sort_values("Monetary")
    .copy()
)

    top_revenue["CustomerID"] = top_revenue["CustomerID"].astype(str)

    fig_revenue = px.bar(
        top_revenue,
        x="Monetary",
        y="CustomerID",
        orientation="h",
        color="Monetary",
        color_continuous_scale="Blues",
        text="Monetary",
        template="plotly_dark"
    )

    fig_revenue.update_traces(
        texttemplate="£%{x:,.0f}",
        textposition="outside"
    )

    fig_revenue.update_layout(
        title="💰 Top 10 Customers by Revenue",
        height=500,
        xaxis_title="Revenue (£)",
        yaxis_title="Customer ID",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=60, b=10)
    )

    apply_dark_theme(fig_revenue)

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
        key="rfm_top_revenue"
    )





with col2:

    top_frequency = (
    rfm.nlargest(10, "Frequency")
    .sort_values("Frequency")
    .copy()
)

    top_frequency["CustomerID"] = top_frequency["CustomerID"].astype(str)

    fig_frequency = px.bar(
        top_frequency,
        x="Frequency",
        y="CustomerID",
        orientation="h",
        color="Frequency",
        color_continuous_scale="Viridis",
        text="Frequency",
        template="plotly_dark"
    )

    fig_frequency.update_traces(
        textposition="outside"
    )

    fig_frequency.update_layout(
        title="🔁 Top 10 Customers by Purchase Frequency",
        height=500,
        xaxis_title="Orders",
        yaxis_title="Customer ID",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=60, b=10)
    )

    apply_dark_theme(fig_frequency)

    st.plotly_chart(
        fig_frequency,
        use_container_width=True,
        key="rfm_top_frequency"
    )





st.markdown("---")

st.subheader("📈 Customer Distribution (RFM Analysis)")




fig = px.scatter(

    rfm,

    x="Recency",
    y="Monetary",

    size="Frequency",

    color="Segment",

    hover_name="CustomerID",

    hover_data={
        "Recency": True,
        "Frequency": True,
        "Monetary": ":,.2f",
        "Segment": True
    },

    template="plotly_dark"
)

fig.update_layout(

    title="Customer Distribution based on RFM",

    height=650,

    xaxis_title="Recency (Days)",

    yaxis_title="Revenue (£)",

    legend_title="Customer Segment"
)

apply_dark_theme(fig)

st.plotly_chart(

    fig,

    use_container_width=True,

    key="rfm_scatter"
)




# ==========================================================
# Customer Segment Analysis
# ==========================================================


st.markdown("---")

st.subheader("🍩 Customer Segment Analysis")

col1, col2 = st.columns(2)




with col1:

    segment_count = (
        rfm.groupby("Segment")
        .size()
        .reset_index(name="Customers")
    )

    fig_segment = px.pie(

        segment_count,

        names="Segment",

        values="Customers",

        hole=0.60,

        template="plotly_dark"
    )

    fig_segment.update_traces(

        textposition="inside",

        textinfo="percent+label"
    )

    fig_segment.update_layout(

        title="👥 Customer Distribution by Segment",

        height=500,

        showlegend=True
    )

    apply_dark_theme(fig_segment)

    st.plotly_chart(

        fig_segment,

        use_container_width=True,

        key="segment_distribution"
    )





with col2:

    segment_revenue = (
        rfm.groupby("Segment")["Monetary"]
        .sum()
        .reset_index()
        .sort_values("Monetary", ascending=False)
    )

    fig_revenue = px.bar(

        segment_revenue,

        x="Segment",

        y="Monetary",

        color="Monetary",

        text="Monetary",

        template="plotly_dark",

        color_continuous_scale="Blues"
    )

    fig_revenue.update_traces(

        texttemplate="£%{y:,.0f}",

        textposition="outside"
    )

    fig_revenue.update_layout(

        title="💰 Revenue Contribution by Segment",

        height=500,

        xaxis_title="Customer Segment",

        yaxis_title="Revenue (£)",

        coloraxis_showscale=False
    )

    apply_dark_theme(fig_revenue)

    st.plotly_chart(

        fig_revenue,

        use_container_width=True,

        key="segment_revenue"
    )




# ==========================================================
# Customer Table
# ==========================================================

st.markdown("---")

st.subheader("📋 Customer RFM Details")



rfm_table = (
    rfm[
        [
            "CustomerID",
            "Recency",
            "Frequency",
            "Monetary",
            "R",
            "F",
            "M",
            "RFMScore",
            "Segment"
        ]
    ]
    .sort_values(
        "Monetary",
        ascending=False
    )
)

st.dataframe(
    rfm_table,
    use_container_width=True,
    hide_index=True
)



csv = rfm_table.to_csv(index=False)

st.download_button(
    label="📥 Download RFM Report",
    data=csv,
    file_name="rfm_analysis.csv",
    mime="text/csv"
)





# ==========================================================
# Business Recommendations
# ==========================================================



st.markdown("---")

st.subheader("📌 Business Recommendations")



champions = (rfm["Segment"] == "Champions").sum()
loyal = (rfm["Segment"] == "Loyal Customers").sum()
potential = (rfm["Segment"] == "Potential Loyalists").sum()
risk = (rfm["Segment"] == "At Risk").sum()
lost = (rfm["Segment"] == "Lost Customers").sum()


st.markdown(f"""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
color:white;
">

<h2 style="color:#38bdf8;">
💡 Executive Recommendations
</h2>

<hr>

<h4>🏆 Champions ({champions} Customers)</h4>

<ul>
<li>Reward with VIP membership.</li>
<li>Offer exclusive early-access promotions.</li>
<li>Use them for referral programs.</li>
</ul>

<h4>❤️ Loyal Customers ({loyal} Customers)</h4>

<ul>
<li>Maintain engagement through loyalty rewards.</li>
<li>Recommend complementary products.</li>
<li>Provide personalized offers.</li>
</ul>

<h4>🌱 Potential Loyalists ({potential} Customers)</h4>

<ul>
<li>Encourage repeat purchases using coupons.</li>
<li>Promote seasonal campaigns.</li>
<li>Offer limited-time discounts.</li>
</ul>

<h4>⚠️ At Risk ({risk} Customers)</h4>

<ul>
<li>Launch win-back campaigns.</li>
<li>Send personalized reminder emails.</li>
<li>Provide special discounts.</li>
</ul>

<h4>❌ Lost Customers ({lost} Customers)</h4>

<ul>
<li>Identify reasons for churn.</li>
<li>Run aggressive reactivation campaigns.</li>
<li>Offer one-time comeback discounts.</li>
</ul>

</div>

""", unsafe_allow_html=True)