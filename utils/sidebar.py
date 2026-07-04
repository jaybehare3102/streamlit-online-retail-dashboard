import streamlit as st
def create_sidebar(df):

    st.write("Sidebar Loaded")


def create_sidebar(df):
        print("Sidebar Called")

        st.sidebar.write("Sidebar Initialized")
    

        st.sidebar.image(
        "https://img.icons8.com/fluency/96/shopping-cart.png",
        width=80
    )

        st.sidebar.markdown("""
    # 🛒 Shopper Spectrum

    ### Business Intelligence
    """)

        st.sidebar.divider()

    # ------------------------
    # Date Filters
    # ------------------------

        st.sidebar.subheader("📅 Date Filters")

        years = sorted(df["Year"].dropna().unique())

        selected_year = st.sidebar.selectbox(
        "Year",
        ["All"] + list(years),
        key="sidebar_year"
    )

        quarters = ["Q1", "Q2", "Q3", "Q4"]

        selected_quarter = st.sidebar.selectbox(
        "Quarter",
        ["All"] + quarters,
        key="sidebar_quarter"
    )

        month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

        months = [
        m for m in month_order
        if m in df["MonthName"].unique()
    ]

        selected_month = st.sidebar.selectbox(
        "Month",
        ["All"] + months,
        key="sidebar_month"
    )

        st.sidebar.divider()

    # ------------------------
    # Geography
    # ------------------------

        st.sidebar.subheader("🌍 Geography")

        countries = sorted(df["Country"].dropna().unique())

        selected_country = st.sidebar.selectbox(
        "Country",
        ["All"] + countries,
        key="sidebar_country"
    )

        st.sidebar.divider()

    # ------------------------
    # Product Search
    # ------------------------

        st.sidebar.subheader("📦 Product Search")

        selected_product = st.sidebar.text_input(
        "Product Name",
        key="sidebar_product"
    )

        selected_stock = st.sidebar.text_input(
        "Stock Code",
        key="sidebar_stock"
    )

        st.sidebar.divider()

    # ------------------------
    # Customer Search
    # ------------------------

        st.sidebar.subheader("👤 Customer")

        selected_customer = st.sidebar.number_input(
        "Customer ID",
        min_value=0,
        value=0,
        step=1,
        key="sidebar_customer"
    )

        st.sidebar.divider()

    # ------------------------
    # Active Filters
    # ------------------------

        st.sidebar.subheader("📋 Active Filters")

        st.sidebar.write(f"Year : {selected_year}")
        st.sidebar.write(f"Quarter : {selected_quarter}")
        st.sidebar.write(f"Month : {selected_month}")
        st.sidebar.write(f"Country : {selected_country}")

    # ========================
    # Apply Filters
    # ========================

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

        if selected_product:
            filtered_df = filtered_df[
                filtered_df["Description"]
                .str.contains(
                    selected_product,
                    case=False,
                    na=False
                )
            ]

        if selected_stock:
            filtered_df = filtered_df[
                filtered_df["StockCode"]
                .astype(str)
                .str.contains(
                    selected_stock,
                    case=False
                )
            ]

        if selected_customer != 0:
            filtered_df = filtered_df[
                filtered_df["CustomerID"] == selected_customer
            ]

        return filtered_df