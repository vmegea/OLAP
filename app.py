import streamlit as st
import pandas as pd
st.set_page_config(page_title="OLAP Retail Dashboard", layout="wide")

st.title("OLAP Tier 2 App")

@st.cache_data
def load_data():
    df = pd.read_csv("data/global_retail_sales.csv")
    return df

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

st.subheader("Basic Info")
st.write("Number of rows:", df.shape[0])
st.write("Number of columns:", df.shape[1])

# ------------------------------------
# SLICE & DICE FILTERS
# ------------------------------------

st.subheader("Filters")

col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.selectbox(
        "Select Year",
        sorted(df["Year"].unique())
    )

with col2:
    selected_category = st.selectbox(
        "Select Category",
        ["All"] + sorted(df["Category"].unique().tolist())
    )

with col3:
    selected_region_filter = st.selectbox(
        "Select Region",
        ["All"] + sorted(df["Region"].unique().tolist())
    )

filtered_df = df[df["Year"] == selected_year]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_region_filter != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region_filter]

st.write("Filtered Rows:", filtered_df.shape[0])
st.dataframe(filtered_df)

# ------------------------------------
# KPI METRICS
# ------------------------------------

st.subheader("Key Metrics")

total_revenue = filtered_df["Revenue"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_transactions = filtered_df.shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Quantity Sold", f"{total_quantity:,}")
col3.metric("Total Transactions", f"{total_transactions:,}")
# ------------------------------------
# GROUP BY REGION - TOTAL REVENUE
# ------------------------------------

st.subheader("Total Revenue by Region")

grouped = (
    filtered_df
    .groupby("Region")["Revenue"]
    .sum()
    .reset_index()
)

st.dataframe(grouped)


# ------------------------------------
# BAR CHART - REVENUE BY REGION
# ------------------------------------

st.subheader("Revenue by Region - Bar Chart")

st.bar_chart(
    grouped.set_index("Region")["Revenue"]
)




# ------------------------------------
# DRILL DOWN - REGION TO COUNTRY
# ------------------------------------

st.subheader("Drill Down: Region → Country")

selected_region = st.selectbox(
    "Select Region for Drill Down",
    grouped["Region"]
)

drill_df = filtered_df[filtered_df["Region"] == selected_region]

country_grouped = (
    drill_df
    .groupby("Country")["Revenue"]
    .sum()
    .reset_index()
)

st.dataframe(country_grouped)

st.bar_chart(
    country_grouped.set_index("Country")["Revenue"]
)




# ------------------------------------
# COMPARE 2023 vs 2024
# ------------------------------------

st.subheader("Compare Revenue: 2023 vs 2024")

compare_df = (
    df
    .groupby(["Year", "Region"])["Revenue"]
    .sum()
    .reset_index()
)

pivot_compare = compare_df.pivot(
    index="Region",
    columns="Year",
    values="Revenue"
)

st.dataframe(pivot_compare)

st.bar_chart(pivot_compare)