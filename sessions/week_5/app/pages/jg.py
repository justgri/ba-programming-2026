import streamlit as st
from pathlib import Path
import pandas as pd

st.title("Personal Page - Justinas")

st.header("Course Progress Tracker")

st.subheader("Week 2 was great")

st.markdown("Below you will find my notes and assignments.")

ROOT = Path(__file__).resolve().parents[1]
st.write(ROOT)

DATA = ROOT / "data" / "week_3"
DISNEY = DATA / "disney_plus_shows.csv"

st.write(DATA)

disney_df = pd.read_csv(DISNEY)

st.write(disney_df)

st.dataframe(disney_df)

st.subheader("Why am I here?")

st.markdown(
    """I like teaching, experimenting, and watching people learn.<br>
        Programming itself brings me joy.<br>
        I want to better understand how AI changes programming and learning.<br>
        I'm curious to see your final projects!""",
    unsafe_allow_html=True,
)


st.subheader("Lecture 1 - Notes and Assignments")

st.markdown("### Notes")

st.markdown(
    """Today was a good day! I'm so excited to learn Python.🥳🥳""",
    unsafe_allow_html=True,
)

st.markdown("I'm testing GitHub workflow")
st.markdown("I'm adding some additional ideas")

st.markdown("### Assignments")

st.write("This is what I've learnt today")
st.code(
    """
import streamlit as st
import numpy as np

x = 10
y = 5

if x > y:
    z = True
else:
    z = False

st.write(f"x is greater than y: {z}")
        """,
    language="python",
)

st.write("Let's see if this code works:")

x = 10
y = 5

# or try with streamlit widgets

x = st.number_input(label="*x* value", min_value=0, max_value=10, step=1)
y = st.number_input(label="*y* value", min_value=0, max_value=10, step=1)

if x > y:
    z = True
else:
    z = False

st.write(f"x is greater than y: {z}")
