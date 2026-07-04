import pandas as pd
import streamlit as st


# ==========================================================
# Load Data
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/cleaned_online_retail.csv"
    )

    # -----------------------------
    # Data Type Conversions
    # -----------------------------

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    df["CustomerID"] = (
        pd.to_numeric(
            df["CustomerID"],
            errors="coerce"
        )
        .fillna(0)
        .astype(int)
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"],
        errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"],
        errors="coerce"
    )

    df["TotalPrice"] = pd.to_numeric(
        df["TotalPrice"],
        errors="coerce"
    )

    # -----------------------------
    # Date Columns
    # -----------------------------

    df["Year"] = df["InvoiceDate"].dt.year

    df["Quarter"] = (
        "Q" +
        df["InvoiceDate"]
        .dt.quarter
        .astype(str)
    )

    df["Month"] = df["InvoiceDate"].dt.month

    df["MonthName"] = df["InvoiceDate"].dt.month_name()

    df["Day"] = df["InvoiceDate"].dt.day

    df["DayName"] = df["InvoiceDate"].dt.day_name()

    df["Hour"] = df["InvoiceDate"].dt.hour

    return df


# ==========================================================
# Currency Formatter
# ==========================================================

def format_currency(value):

    if pd.isna(value):
        return "£0.00"

    if value >= 1_000_000:
        return f"£{value/1_000_000:.2f} M"

    elif value >= 1_000:
        return f"£{value/1_000:.2f} K"

    return f"£{value:.2f}"