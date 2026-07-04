import pandas as pd


df = pd.read_csv("data/online_retail.csv", encoding="ISO-8859-1")



print("Dataset Loaded Successfully!")


# ============================================
# : Dataset Information


print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns)

print("\nDataset Information")
print(df.info())


#  : Missing Values

print("\nMissing Values")
print(df.isnull().sum())


# : Duplicate Records

duplicates = df.duplicated().sum()

print("\nDuplicate Rows :", duplicates)


print("\nSummary Statistics")
print(df.describe())


# ============================================

# : Data Quality Report

print("\n" + "="*50)
print("DATA QUALITY REPORT")
print("="*50)

print(f"Total Rows              : {len(df)}")
print(f"Missing CustomerID      : {df['CustomerID'].isnull().sum()}")
print(f"Duplicate Records       : {df.duplicated().sum()}")

cancelled_orders = df['InvoiceNo'].astype(str).str.startswith('C').sum()
print(f"Cancelled Invoices      : {cancelled_orders}")

invalid_quantity = (df['Quantity'] <= 0).sum()
print(f"Invalid Quantity        : {invalid_quantity}")

invalid_price = (df['UnitPrice'] <= 0).sum()
print(f"Invalid Unit Price      : {invalid_price}")



# ============================================
#  : StockCode Analysis

print("\nTop 20 StockCodes")
print(df['StockCode'].value_counts().head(20))


print("\nUnique StockCodes :", df['StockCode'].nunique())



print("\nNon-Numeric StockCodes")

non_numeric = df[
    ~df['StockCode'].astype(str).str.match(r'^[0-9A-Za-z]+$')
]

print(non_numeric[['StockCode', 'Description']].drop_duplicates())


special_codes = [
    'POST',
    'DOT',
    'M',
    'BANK CHARGES',
    'AMAZONFEE',
    'CRUK',
    'D',
    'PADS',
    'S'
]

print("\nSpecial StockCodes Found")

print(df[df['StockCode'].isin(special_codes)]
      [['StockCode','Description']]
      .drop_duplicates())




# : Create Working Copy
# ============================================

clean_df = df.copy()

print("\nWorking copy created successfully.")


# : Remove Missing CustomerID
# ============================================

clean_df = clean_df.dropna(subset=['CustomerID'])

print("Rows after removing missing CustomerID:", len(clean_df))


# : Remove Duplicate Records
# ============================================

clean_df = clean_df.drop_duplicates()

print("Rows after removing duplicates:", len(clean_df))



#  : Remove Cancelled Orders
# ============================================

clean_df = clean_df[
    ~clean_df['InvoiceNo'].astype(str).str.startswith('C')
]

print("Rows after removing cancelled invoices:", len(clean_df))




# : Remove Invalid Quantity
# ============================================

clean_df = clean_df[
    clean_df['Quantity'] > 0
]

print("Rows after removing invalid quantity:", len(clean_df))


#  : Remove Invalid UnitPrice
# ============================================

clean_df = clean_df[
    clean_df['UnitPrice'] > 0
]

print("Rows after removing invalid UnitPrice:", len(clean_df))


# 
# 
# 
# # Step 16 : Convert InvoiceDate
# ============================================

clean_df["InvoiceDate"] = pd.to_datetime(clean_df["InvoiceDate"])



# : Identify Special StockCodes
# ============================================

special_codes = [
    "POST",
    "DOT",
    "M",
    "BANK CHARGES",
    "AMAZONFEE",
    "CRUK",
    "D",
    "PADS",
    "S"
]

clean_df["IsSpecialStockCode"] = clean_df["StockCode"].isin(special_codes)

print("\nSpecial StockCode Count:")
print(clean_df["IsSpecialStockCode"].value_counts())


#  : Convert InvoiceDate
# ============================================

clean_df["InvoiceDate"] = pd.to_datetime(clean_df["InvoiceDate"])


#  : Create TotalPrice
# ============================================

clean_df["TotalPrice"] = (
    clean_df["Quantity"] *
    clean_df["UnitPrice"]
)



# : Save Clean Dataset
# ============================================

clean_df.to_csv(
    "data/cleaned_online_retail.csv",
    index=False
)

print("\nClean dataset saved successfully!")



print("\nFinal Dataset Shape:")
print(clean_df.shape)

print("\nFirst 5 Rows:")
print(clean_df.head())


#  : Date Features
# ============================================

clean_df["Year"] = clean_df["InvoiceDate"].dt.year

clean_df["Month"] = clean_df["InvoiceDate"].dt.month

clean_df["MonthName"] = clean_df["InvoiceDate"].dt.month_name()

clean_df["Quarter"] = "Q" + clean_df["InvoiceDate"].dt.quarter.astype(str)

clean_df["Day"] = clean_df["InvoiceDate"].dt.day

clean_df["DayName"] = clean_df["InvoiceDate"].dt.day_name()

clean_df["Hour"] = clean_df["InvoiceDate"].dt.hour

print("Date features created successfully.")


clean_df["DayType"] = clean_df["DayName"].apply(
    lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
)


invoice_value = (
    clean_df.groupby("InvoiceNo")["TotalPrice"]
    .sum()
    .reset_index()
)

invoice_value.rename(
    columns={"TotalPrice": "InvoiceValue"},
    inplace=True
)

clean_df = clean_df.merge(
    invoice_value,
    on="InvoiceNo",
    how="left"
)



print("\nFinal Columns")

print(clean_df.columns)


clean_df.to_csv(
    "data/cleaned_online_retail.csv",
    index=False
)