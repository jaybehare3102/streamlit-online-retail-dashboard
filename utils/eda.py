# Shopper Spectrum - Exploratory Data Analysis
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chart Style
plt.style.use("ggplot")



# Load Clean Dataset
# ============================================

df = pd.read_csv(
    "data/cleaned_online_retail.csv",
    parse_dates=["InvoiceDate"]
)

print("Clean dataset loaded successfully.")




# KPI Calculations
# ============================================

total_revenue = df["TotalPrice"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

total_products = df["StockCode"].nunique()

print("\n========== BUSINESS KPIs ==========")

print(f"Total Revenue   : £{total_revenue:,.2f}")

print(f"Total Orders    : {total_orders}")

print(f"Total Customers : {total_customers}")

print(f"Total Products  : {total_products}")