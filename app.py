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
