import pandas as pd

print("CALCULATIONS FILE LOADED")

# ==========================================================
# Customer Summary
# ==========================================================

def customer_summary(df):

    summary = (
        df.groupby("CustomerID")
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Quantity=("Quantity", "sum"),
            Country=("Country", lambda x: x.mode().iloc[0])
        )
        .reset_index()
    )

    summary["AverageOrderValue"] = (
        summary["Revenue"] /
        summary["Orders"]
    )

    return summary.sort_values(
        "Revenue",
        ascending=False
    )


# ==========================================================
# Product Summary
# ==========================================================

def product_summary(df):

    summary = (
        df.groupby(["StockCode", "Description"])
        .agg(
            Revenue=("TotalPrice", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Countries=("Country", "nunique"),
            UnitPrice=("UnitPrice", "mean")
        )
        .reset_index()
    )

    summary["AvgRevenuePerOrder"] = (
        summary["Revenue"] /
        summary["Orders"]
    )

    total_revenue = summary["Revenue"].sum()

    summary["RevenuePercent"] = (
        summary["Revenue"] /
        total_revenue
    ) * 100

    summary = summary.sort_values(
        "Revenue",
        ascending=False
    )

    summary["CumulativeRevenue"] = (
        summary["RevenuePercent"].cumsum()
    )

    summary["ABC"] = "C"

    summary.loc[
        summary["CumulativeRevenue"] <= 80,
        "ABC"
    ] = "A"

    summary.loc[
        (summary["CumulativeRevenue"] > 80)
        &
        (summary["CumulativeRevenue"] <= 95),
        "ABC"
    ] = "B"

    return summary


# ==========================================================
# Country Summary
# ==========================================================

def country_summary(df):

    summary = (
        df.groupby("Country")
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Customers=("CustomerID", "nunique"),
            Quantity=("Quantity", "sum"),
            AvgPrice=("UnitPrice", "mean")
        )
        .reset_index()
    )

    summary["AverageOrderValue"] = (
        summary["Revenue"] /
        summary["Orders"]
    )

    summary["RevenuePercent"] = (
        summary["Revenue"] /
        summary["Revenue"].sum()
    ) * 100

    return summary.sort_values(
        "Revenue",
        ascending=False
    )


# ==========================================================
# Sales Summary
# ==========================================================

def sales_summary(df):

    monthly = (
        df.groupby(["Year", "Month", "MonthName"])
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
        .sort_values(["Year", "Month"])
    )

    monthly["AverageOrderValue"] = (
        monthly["Revenue"] /
        monthly["Orders"]
    )

    quarterly = (
        df.groupby(["Year", "Quarter"])
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    yearly = (
        df.groupby("Year")
        .agg(
            Revenue=("TotalPrice", "sum"),
            Orders=("InvoiceNo", "nunique"),
            Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    weekday = (
        df.groupby("DayName")
        .agg(
            Revenue=("TotalPrice", "sum")
        )
        .reindex([
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ])
        .reset_index()
    )

    hourly = (
        df.groupby("Hour")
        .agg(
            Revenue=("TotalPrice", "sum")
        )
        .reset_index()
    )

    return (
        monthly,
        quarterly,
        yearly,
        weekday,
        hourly
    )


# ==========================================================
# RFM Summary
# ==========================================================

def rfm_summary(df):

    df = df.copy()

    # Ensure InvoiceDate is datetime
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        errors="coerce"
    )

    # Remove customers with missing IDs
    df = df.dropna(subset=["CustomerID"])

    # Reference date (1 day after latest transaction)
    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    # Create RFM table
    rfm = (
        df.groupby("CustomerID")
        .agg(
            Recency=(
                "InvoiceDate",
                lambda x: (reference_date - x.max()).days
            ),
            Frequency=(
                "InvoiceNo",
                "nunique"
            ),
            Monetary=(
                "TotalPrice",
                "sum"
            )
        )
        .reset_index()
    )

    # -----------------------------
    # RFM Scores (1-5)
    # -----------------------------

    # Lower Recency = Better
    rfm["R"] = pd.qcut(
        rfm["Recency"],
        5,
        labels=[5, 4, 3, 2, 1],
        duplicates="drop"
    ).astype(int)

    # Higher Frequency = Better
    rfm["F"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
        duplicates="drop"
    ).astype(int)

    # Higher Monetary = Better
    rfm["M"] = pd.qcut(
        rfm["Monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5],
        duplicates="drop"
    ).astype(int)

    # -----------------------------
    # RFM Score
    # -----------------------------

    rfm["RFMScore"] = (
        rfm["R"].astype(str)
        + rfm["F"].astype(str)
        + rfm["M"].astype(str)
    )

    # Average Score (1–5)
    rfm["Score"] = (
        rfm["R"] +
        rfm["F"] +
        rfm["M"]
    ) / 3

    # -----------------------------
    # Customer Segmentation
    # -----------------------------

    def segment(row):

        if row["Score"] >= 4.5:
            return "Champions"

        elif row["Score"] >= 4:
            return "Loyal Customers"

        elif row["Score"] >= 3.5:
            return "Potential Loyalists"

        elif row["Score"] >= 3:
            return "Need Attention"

        elif row["Score"] >= 2:
            return "At Risk"

        else:
            return "Lost Customers"

    rfm["Segment"] = rfm.apply(
        segment,
        axis=1
    )

    return rfm.sort_values(
        "Monetary",
        ascending=False
    )