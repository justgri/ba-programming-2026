import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np

st.title("Week 4 - Data wrangling")

st.header("Reshaping, aggregation, and summarization")

st.subheader("Load the data")

APP_ROOT = Path(__file__).resolve().parents[1]
st.write(APP_ROOT)

DATA = APP_ROOT / "data" / "week_4"
DISNEY = DATA / "disney_movies_clean.csv"

st.write(DATA)
st.write(DISNEY)

st.subheader("Inspection")

disney_df = pd.read_csv(DISNEY)

col_left, col_right = st.columns((2, 1))

with col_left:
    st.subheader("Raw Data")
    st.dataframe(disney_df)

st.subheader("Filtered Data")
min_year = st.number_input(
    "Min Year", value=2000, min_value=2000, max_value=2025, width=200
)
max_year = st.number_input(
    "Max Year", value=2025, min_value=2000, max_value=2025, width=200
)

disney_lim = disney_df.loc[disney_df["year"].between(min_year, max_year)]
disney_lim = disney_lim.sort_values(by=["year", "title"])
st.dataframe(disney_lim)


st.subheader("Reshaping")

st.subheader("Summarization")

st.subheader("Transformation")
