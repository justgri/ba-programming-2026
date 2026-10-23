import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


st.title("Sample Project")

st.header("Hello world!")

st.markdown("Some additional text")


# define relative path
# note the double parent, since this file is in pages folder
ROOT_APP = Path(__file__).parent.parent
st.write(ROOT_APP)


@st.cache_data
def read_data_cache():
    return pd.read_csv(ROOT_APP / "data" / "disney_movies_clean.csv")


df_disney = read_data_cache()


st.header("Introduction")

st.markdown("This is some text describing what my project is about")

st.markdown(
    """My data contains the following variables:
1. Variable A
2. Variable B
3. Variable C
""",
    unsafe_allow_html=True,
)

st.markdown(
    """These are the main questions I want to answer:
1. Questions A
2. Questions B
3. Questions C
""",
    unsafe_allow_html=True,
)


st.header("Data overview")
st.dataframe(df_disney)

with st.sidebar:
    user_input_password = st.text_input("Enter your password:", width=300)


true_pw = st.secrets["true_password"]


if user_input_password == true_pw:

    st.title("This is a secret insights page")

    col_data, _, col_chart = st.columns((0.8, 0.05, 1))

    with col_data:
        st.subheader("My unique ideas")
        st.markdown("Placeholder for unique ideas")

    with col_chart:
        st.subheader("Movie imdb votes")
        fig, ax = plt.subplots(figsize=(8, 4))

        ax.hist(df_disney["imdb_votes"])
        st.pyplot(fig)
