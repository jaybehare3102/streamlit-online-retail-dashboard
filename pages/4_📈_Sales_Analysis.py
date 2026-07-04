import streamlit as st
import plotly.express as px

from utils.data_loader import load_data, format_currency
from utils.sidebar import create_sidebar
from utils.layout import page_header
from utils.kpi import render_kpi_cards
from utils.insights import render_insights
from utils.calculations import sales_summary



st.set_page_config(
    page_title="Sales Analysis",
    page_icon="📈",
    layout="wide"
)




with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )



df = load_data()

filtered_df = create_sidebar(df)



page_header(
    "📈 Sales Analysis",
    "Sales Trends & Time-Based Performance"
)




monthly, quarterly, yearly, weekday, hourly = sales_summary(filtered_df)



total_revenue = filtered_df["TotalPrice"].sum()

total_orders = filtered_df["InvoiceNo"].nunique()

total_quantity = filtered_df["Quantity"].sum()

avg_order_value = total_revenue / total_orders



render_kpi_cards(
[
    ("💰","Revenue",format_currency(total_revenue)),
    ("🛒","Orders",f"{total_orders:,}"),
    ("📦","Quantity",f"{int(total_quantity):,}"),
    ("💷","Avg Order",format_currency(avg_order_value))
]
)



st.markdown("---")

st.subheader("📈 Revenue Trend")

view = st.radio(
    "View Revenue By",
    ["Monthly", "Quarterly", "Yearly"],
    horizontal=True
)




if view == "Monthly":

    monthly["Period"] = (
        monthly["MonthName"].str[:3]
        + " "
        + monthly["Year"].astype(str)
    )

    fig = px.line(
        monthly,
        x="Period",
        y="Revenue",
        markers=True,
        template="plotly_dark"
    )




elif view == "Quarterly":

    quarterly["Period"] = (
        quarterly["Quarter"]
        + " "
        + quarterly["Year"].astype(str)
    )

    fig = px.line(
        quarterly,
        x="Period",
        y="Revenue",
        markers=True,
        template="plotly_dark"
    )



else:

    yearly["Period"] = yearly["Year"].astype(str)

    fig = px.line(
        yearly,
        x="Period",
        y="Revenue",
        markers=True,
        template="plotly_dark"
    )



fig.update_layout(
    height=550,
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(color="white"),
    hoverlabel=dict(
        bgcolor="#1e293b",
        font_color="white"
    ),
    xaxis_title="",
    yaxis_title="Revenue (£)"
)

fig.update_traces(
    line=dict(width=4, color="#3b82f6"),
    marker=dict(size=8)
)



st.plotly_chart(
    fig,
    use_container_width=True,
    key="sales_trend"
)


st.markdown("---")

st.subheader("📊 Sales Breakdown")

col1, col2 = st.columns(2)



with col1:

    monthly_chart = monthly.copy()

    monthly_chart["Label"] = (
        monthly_chart["MonthName"].str[:3]
        + " "
        + monthly_chart["Year"].astype(str)
    )

    fig_month = px.bar(
        monthly_chart,
        x="Label",
        y="Revenue",
        template="plotly_dark",
        color="Revenue",
        color_continuous_scale="Blues"
    )

    fig_month.update_layout(
        title="📅 Monthly Revenue",
        height=450,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="white"),
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True,
        key="monthly_revenue"
    )




with col2:

    quarterly_chart = quarterly.copy()

    quarterly_chart["Label"] = (
        quarterly_chart["Quarter"]
        + " "
        + quarterly_chart["Year"].astype(str)
    )

    fig_quarter = px.bar(
        quarterly_chart,
        x="Label",
        y="Revenue",
        template="plotly_dark",
        color="Revenue",
        color_continuous_scale="Blues"
    )

    fig_quarter.update_layout(
        title="📆 Quarterly Revenue",
        height=450,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="white"),
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_quarter,
        use_container_width=True,
        key="quarterly_revenue"
    )





st.markdown("---")

st.subheader("🕒 Time-Based Sales Analysis")

col1, col2 = st.columns(2)



with col1:

    fig_hour = px.line(
        hourly,
        x="Hour",
        y="Revenue",
        markers=True,
        template="plotly_dark"
    )

    fig_hour.update_traces(
        line=dict(
            color="#3b82f6",
            width=4
        ),
        marker=dict(size=8)
    )

    fig_hour.update_layout(
        title="🕒 Revenue by Hour",
        height=450,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="white"),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_color="white"
        ),
        xaxis_title="Hour",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True,
        key="hourly_sales"
    )




with col2:

    fig_day = px.bar(
        weekday,
        x="DayName",
        y="Revenue",
        template="plotly_dark",
        color="Revenue",
        color_continuous_scale="Blues"
    )

    fig_day.update_layout(
        title="📅 Revenue by Weekday",
        height=450,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="white"),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_color="white"
        ),
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_day,
        use_container_width=True,
        key="weekday_sales"
    )



st.markdown("---")

st.subheader("📦 Sales Seasonality")

col1, col2 = st.columns(2)



with col1:

    qty_chart = monthly.copy()

    qty_chart["Period"] = (
        qty_chart["MonthName"].str[:3]
        + " "
        + qty_chart["Year"].astype(str)
    )

    fig_qty = px.bar(
        qty_chart,
        x="Period",
        y="Quantity",
        template="plotly_dark",
        color="Quantity",
        color_continuous_scale="Blues"
    )

    fig_qty.update_layout(
        title="📦 Quantity Sold by Month",
        height=450,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="white"),
        coloraxis_showscale=False,
        xaxis_title="",
        yaxis_title="Quantity"
    )

    st.plotly_chart(
        fig_qty,
        use_container_width=True,
        key="monthly_quantity"
    )


with col2:

    fig_aov = px.line(
        qty_chart,
        x="Period",
        y="AverageOrderValue",
        markers=True,
        template="plotly_dark"
    )

    fig_aov.update_traces(
        line=dict(
            color="#3b82f6",
            width=4
        ),
        marker=dict(size=8)
    )

    fig_aov.update_layout(
        title="💷 Average Order Value",
        height=450,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="white"),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_color="white"
        ),
        xaxis_title="",
        yaxis_title="Average Order (£)"
    )

    st.plotly_chart(
        fig_aov,
        use_container_width=True,
        key="monthly_aov"
    )




st.markdown("---")

st.subheader("📌 Executive Sales Insights")




best_month = monthly.loc[
    monthly["Revenue"].idxmax()
]

best_quarter = quarterly.loc[
    quarterly["Revenue"].idxmax()
]

best_day = weekday.loc[
    weekday["Revenue"].idxmax()
]

best_hour = hourly.loc[
    hourly["Revenue"].idxmax()
]

highest_aov = monthly.loc[
    monthly["AverageOrderValue"].idxmax()
]

highest_quantity = monthly.loc[
    monthly["Quantity"].idxmax()
]



render_insights(

[
    (
        "🏆 Best Revenue Month",
        f'{best_month["MonthName"]} {best_month["Year"]}'
    ),

    (
        "📆 Best Quarter",
        f'{best_quarter["Quarter"]} {best_quarter["Year"]}'
    ),

    (
        "📅 Best Sales Day",
        best_day["DayName"]
    ),

    (
        "🕒 Peak Sales Hour",
        f'{int(best_hour["Hour"]):02d}:00'
    ),

    (
        "💷 Highest AOV",
        f'{highest_aov["MonthName"]} {highest_aov["Year"]}'
    ),

    (
        "📦 Highest Quantity",
        f'{highest_quantity["MonthName"]} {highest_quantity["Year"]}'
    )

]

)


st.markdown("---")

st.subheader("💡 Business Recommendations")


st.success(f"""
✅ Focus marketing campaigns during **{best_month['MonthName']} {best_month['Year']}**, as it generated the highest revenue.
""")

st.info(f"""
📦 Increase inventory before **{best_quarter['Quarter']} {best_quarter['Year']}** to meet expected customer demand.
""")

st.warning(f"""
🕒 Schedule promotional campaigns around **{int(best_hour['Hour']):02d}:00**, the peak shopping hour.
""")

st.error(f"""
📅 Use **{best_day['DayName']}** for flash sales and product launches, as it consistently delivers the highest revenue.
""")


st.markdown("---")

st.subheader("📝 Executive Summary")



st.info(f"""
### Sales Performance Overview

• **{best_month['MonthName']} {best_month['Year']}** recorded the highest revenue.

• **{best_quarter['Quarter']} {best_quarter['Year']}** was the strongest performing quarter.

• Customers purchased the largest quantity of products during **{highest_quantity['MonthName']}**.

• The peak shopping time was **{int(best_hour['Hour']):02d}:00**, making it an ideal period for targeted promotions.

• **{best_day['DayName']}** generated the highest revenue, indicating stronger customer activity on this day.

Overall, sales trends indicate clear seasonal demand patterns, helping the business optimize inventory planning, staffing, and promotional campaigns.
""")