import streamlit as st
import pandas as pd

@st.cache_data
def df_to_csv_utf8(df: pd.DataFrame):
    return df.to_csv(index=False).encode('utf-8')