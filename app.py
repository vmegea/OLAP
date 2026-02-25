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
