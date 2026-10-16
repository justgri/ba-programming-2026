import streamlit as st


st.title("Sample Student Personal Page")

st.header("Course Progress Tracker")

st.markdown("Below you will find my notes and assignments.")

st.subheader("Lecture 1 - Notes and Assignments")

st.markdown("### Notes")

st.markdown(
    """Today was a good day! I'm so excited to learn Python.🥳🥳""",
    unsafe_allow_html=True,
)

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
