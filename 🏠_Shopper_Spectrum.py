import streamlit as st

from utils.data_loader import load_data
from utils.layout import page_header


# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
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


# ==========================================================
# Hero Header
# ==========================================================

page_header(
    "🛒 Shopper Spectrum",
    "Retail Business Intelligence & Customer Analytics Dashboard"
)



st.markdown("""

<div style="
background:linear-gradient(135deg,#1e293b,#0f172a);
padding:35px;
border-radius:20px;
border:1px solid #334155;
margin-bottom:25px;
">

<h1 style="color:#38bdf8;">
Welcome to Shopper Spectrum
</h1>

<h3 style="color:white;">
Transforming Retail Transactions into Actionable Business Insights
</h3>

<p style="color:#CBD5E1;font-size:18px;line-height:1.8;">

Shopper Spectrum is an interactive Retail Business Intelligence dashboard
developed using Python and Streamlit.

The project analyzes customer purchasing behaviour, product performance,
sales trends, geographical insights and customer segmentation using
RFM Analysis to support data-driven business decisions.

</p>

</div>

""", unsafe_allow_html=True)





st.markdown("## 📊 Dataset Overview")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Transactions",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Customers",
        f"{df['CustomerID'].nunique():,}"
    )

with col3:
    st.metric(
        "Products",
        f"{df['StockCode'].nunique():,}"
    )

with col4:
    st.metric(
        "Countries",
        f"{df['Country'].nunique():,}"
    )



st.markdown("---")

st.subheader("📖 Project Overview")

st.markdown("""

This dashboard was developed to analyze an online retail dataset and
provide meaningful business insights through interactive visualizations.

The application enables users to:

- Analyze sales performance
- Understand customer behaviour
- Monitor product performance
- Compare country-wise revenue
- Perform RFM customer segmentation
- Generate business recommendations

""")




st.markdown("---")

st.subheader("🛠 Technology Stack")

st.subheader("🛠 Technology Stack")

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("🐍", "Python"),
    ("📊", "Streamlit"),
    ("📈", "Plotly"),
    ("🐼", "Pandas")
]

for col, (icon, title) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)





st.markdown("---")

st.subheader("📂 Dashboard Modules")

col1,col2,col3 = st.columns(3)

with col1:

    st.success("""
🏠 Executive Dashboard

Overall Business Performance
""")

    st.success("""
👥 Customer Analysis

Customer Behaviour & Spending
""")

    st.success("""
📦 Product Analysis

ABC Classification & Performance
""")

with col2:

    st.success("""
📈 Sales Analysis

Revenue Trends & KPIs
""")

    st.success("""
🌍 Country Analysis

Geographical Performance
""")

with col3:

    st.success("""
💎 RFM Analysis

Customer Segmentation
""")

    st.success("""
🎁 Recommendation System

Product Recommendation Engine
""")
    





st.markdown("---")

st.subheader("🎯 Business Objectives")

left,right = st.columns(2)

with left:

    st.markdown("""

✅ Improve Customer Retention

✅ Increase Revenue

✅ Identify High Value Customers

✅ Optimize Inventory

""")

with right:

    st.markdown("""

✅ Improve Marketing Strategy

✅ Discover Sales Trends

✅ Understand Customer Behaviour

✅ Support Business Decisions

""")
    



st.markdown("---")

st.subheader("🚀 How to Use")

st.info("""

1️⃣ Select a dashboard page from the left sidebar.

2️⃣ Apply filters such as Year, Quarter, Month or Country.

3️⃣ Explore KPIs and interactive charts.

4️⃣ Analyze customers, products and sales.

5️⃣ Generate actionable business insights.

""")





st.markdown("---")

st.markdown("""

<div style="text-align:center;color:#94A3B8;">

<h3 style="color:#38bdf8;">
Shopper Spectrum
</h3>

<p>

Retail Business Intelligence Dashboard

</p>

<p>

Developed by <b>Jay Behare</b>

</p>

</div>

""", unsafe_allow_html=True)



