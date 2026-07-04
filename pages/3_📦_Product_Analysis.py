import streamlit as st
import plotly.express as px

from utils.data_loader import load_data, format_currency
from utils.sidebar import create_sidebar
from utils.layout import page_header
from utils.kpi import render_kpi_cards
from utils.insights import render_insights
from utils.calculations import product_summary




st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
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
    "📦 Product Analysis",
    "Product Performance & Revenue Insights"
)


products = product_summary(filtered_df)

total_products = products["StockCode"].nunique()

total_quantity = products["Quantity"].sum()

avg_revenue = products["Revenue"].mean()

avg_price = products["UnitPrice"].mean()



render_kpi_cards(

[
    ("📦","Products",f"{total_products:,}"),

    ("🛒","Quantity Sold",f"{int(total_quantity):,}"),

    ("💰","Avg Revenue",format_currency(avg_revenue)),

    ("💷","Avg Price",f"£{avg_price:.2f}")

]

)


st.markdown("---")

st.subheader("🌟 Product Spotlight")


spotlight = products.sort_values(
    "Revenue",
    ascending=False
).iloc[0]


st.markdown(f"""
<div style="
background: linear-gradient(135deg,#1e293b,#0f172a);
padding:25px;
border-radius:20px;
border:1px solid #334155;
">

<h2 style="color:#34d399;">
⭐ Highest Revenue Product
</h2>

<table style="width:100%;color:white;font-size:17px;">

<tr>
<td><b>Product</b></td>
<td>{spotlight["Description"]}</td>
</tr>

<tr>
<td><b>Stock Code</b></td>
<td>{spotlight["StockCode"]}</td>
</tr>

<tr>
<td><b>Revenue</b></td>
<td>{format_currency(spotlight["Revenue"])}</td>
</tr>

<tr>
<td><b>Quantity Sold</b></td>
<td>{int(spotlight["Quantity"]):,}</td>
</tr>

<tr>
<td><b>Orders</b></td>
<td>{spotlight["Orders"]}</td>
</tr>

<tr>
<td><b>Countries Sold</b></td>
<td>{spotlight["Countries"]}</td>
</tr>

<tr>
<td><b>Average Unit Price</b></td>
<td>£{spotlight["UnitPrice"]:.2f}</td>
</tr>

</table>

</div>
""",
unsafe_allow_html=True)

st.markdown("---")


highest_revenue = products.sort_values(
    "Revenue",
    ascending=False
).iloc[0]

highest_quantity = products.sort_values(
    "Quantity",
    ascending=False
).iloc[0]

highest_price = products.sort_values(
    "UnitPrice",
    ascending=False
).iloc[0]

widest_market = products.sort_values(
    "Countries",
    ascending=False
).iloc[0]


render_insights(

[
    (
        "🏆 Highest Revenue Product",
        highest_revenue["Description"]
    ),

    (
        "🛒 Most Purchased Product",
        highest_quantity["Description"]
    ),

    (
        "💷 Highest Unit Price",
        highest_price["Description"]
    ),

    (
        "🌍 Sold in Most Countries",
        widest_market["Description"]
    )

]
)


st.markdown("---")

st.subheader("📊 Product Performance Analysis")

col1, col2 = st.columns(2)


with col1:

    top_revenue = (
        products.nlargest(10, "Revenue")
        .sort_values("Revenue")
    )

    fig_revenue = px.bar(
        top_revenue,
        x="Revenue",
        y="Description",
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

    fig_revenue.update_layout(
        title="🏆 Top 10 Products by Revenue",
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

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
        key="top_revenue_products"
    )



with col2:

    top_quantity = (
        products.nlargest(10, "Quantity")
        .sort_values("Quantity")
    )

    fig_quantity = px.bar(
        top_quantity,
        x="Quantity",
        y="Description",
        orientation="h",
        color="Quantity",
        color_continuous_scale="Blues",
        text="Quantity",
        template="plotly_dark"
    )

    fig_quantity.update_traces(
        textposition="outside"
    )

    fig_quantity.update_layout(
        title="📦 Top 10 Products by Quantity",
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

    st.plotly_chart(
        fig_quantity,
        use_container_width=True,
        key="top_quantity_products"
    )



st.markdown("---")

st.subheader("📈 Revenue vs Quantity Analysis")



fig_scatter = px.scatter(
    products,
    x="Quantity",
    y="Revenue",
    size="Orders",
    color="ABC",
    hover_name="Description",
    hover_data=[
        "Revenue",
        "Quantity",
        "Orders",
        "Countries",
        "UnitPrice"
    ],
    template="plotly_dark",
    color_discrete_map={
        "A":"#1d4ed8",
        "B":"#3b82f6",
        "C":"#93c5fd"
    }
)

fig_scatter.update_layout(
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

st.plotly_chart(
    fig_scatter,
    use_container_width=True,
    key="revenue_quantity_scatter"
)



st.markdown("---")

st.subheader("🌍 Global Product Reach")

col1, col2 = st.columns(2)




with col1:

    top_countries = (
        products.nlargest(10, "Countries")
        .sort_values("Countries")
    )

    fig_country = px.bar(
        top_countries,
        x="Countries",
        y="Description",
        orientation="h",
        color="Countries",
        color_continuous_scale="Blues",
        text="Countries",
        template="plotly_dark"
    )

    fig_country.update_layout(
        title="🌍 Top Products by Global Reach",
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

    st.plotly_chart(
        fig_country,
        use_container_width=True,
        key="global_products"
    )





with col2:

    premium = (
        products.nlargest(10, "UnitPrice")
        .sort_values("UnitPrice")
    )

    fig_price = px.bar(
        premium,
        x="UnitPrice",
        y="Description",
        orientation="h",
        color="UnitPrice",
        color_continuous_scale="Blues",
        text="UnitPrice",
        template="plotly_dark"
    )

    fig_price.update_traces(
        texttemplate="£%{x:.2f}",
        textposition="outside"
    )

    fig_price.update_layout(
        title="💷 Highest Average Unit Price",
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

    st.plotly_chart(
        fig_price,
        use_container_width=True,
        key="highest_price_products"
    )



st.markdown("---")

st.subheader("📊 ABC Product Classification")

col1, col2 = st.columns([1, 2])




with col1:

    abc_summary = (
        products.groupby("ABC")
        .size()
        .reset_index(name="Products")
    )

    fig_abc = px.pie(
        abc_summary,
        names="ABC",
        values="Products",
        hole=0.60,
        color="ABC",
        color_discrete_sequence=[
            "#1d4ed8",
            "#3b82f6",
            "#93c5fd"
        ],
        template="plotly_dark"
    )

    fig_abc.update_layout(
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

    st.plotly_chart(
        fig_abc,
        use_container_width=True,
        key="abc_distribution"
    )



with col2:

    abc_table = (
        products.groupby("ABC")
        .agg(
            Products=("Description", "count"),
            Revenue=("Revenue", "sum")
        )
        .reset_index()
    )

    abc_table["Revenue %"] = (
        abc_table["Revenue"] /
        abc_table["Revenue"].sum()
    ) * 100

    st.subheader("ABC Summary")

    st.dataframe(
        abc_table,
        use_container_width=True,
        hide_index=True
    )


st.markdown("---")

st.subheader("📋 Product Performance")



display_table = products.copy()

display_table["Revenue"] = display_table["Revenue"].round(2)
display_table["UnitPrice"] = display_table["UnitPrice"].round(2)
display_table["RevenuePercent"] = display_table["RevenuePercent"].round(2)

display_table = display_table[
    [
        "StockCode",
        "Description",
        "Revenue",
        "Quantity",
        "Orders",
        "Countries",
        "UnitPrice",
        "RevenuePercent",
        "ABC"
    ]
]

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True,
    height=500
)



st.markdown("---")
st.subheader("🏅 Product Rankings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🥇 Top 5 Products")
    st.dataframe(
        products.nlargest(5, "Revenue")[
            ["Description", "Revenue"]
        ],
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.markdown("### 📉 Bottom 5 Products")
    st.dataframe(
        products.nsmallest(5, "Revenue")[
            ["Description", "Revenue"]
        ],
        hide_index=True,
        use_container_width=True
    )



st.markdown("---")

st.subheader("📝 Executive Summary")

top_product = products.loc[products["Revenue"].idxmax(), "Description"]
top_country_count = products["Countries"].max()
a_products = (products["ABC"] == "A").sum()

st.info(f"""
- **{top_product}** is the highest revenue-generating product.
- **{a_products} products** are classified as **A-Class**, contributing the majority of total revenue.
- The widest product distribution spans **{top_country_count} countries**.
- Premium-priced products generate significant value despite lower sales volumes.
- ABC Analysis helps prioritize inventory and marketing efforts.
""")


st.markdown("---")

st.subheader("💡 Business Recommendations")

st.success("""
✅ Maintain high inventory levels for **A-Class** products as they generate the majority of revenue.
""")

st.info("""
📦 Promote products with high sales quantity but lower revenue using bundle offers or upselling strategies.
""")

st.warning("""
💷 Review pricing and marketing for **B-Class** products to increase their contribution to total revenue.
""")

st.error("""
⚠ Evaluate **C-Class** products for discontinuation, replacement, or targeted promotional campaigns.
""")

