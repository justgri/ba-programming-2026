import streamlit as st

st.title("Intro to Data Analysis with Python")

st.header("Welcome to the Playground!")

st.markdown(
    """We will use this page to share our progress and takeaways,
    learning how to work on collaborative projects along the way."""
)

st.subheader("Instructions")

st.markdown(
    """This app is on a **private** GitHub repo.<br>
    You will be granted a collaborator access, so that you can clone it and contribute to it.<br>
    We will run this app only locally - the content will be visible to other students,
    but not to the public.<br>
    Once you clone the app to your personal device, you will add content to your personal file
    and push updates with *git*.<br>
    Rule #1: **always** *git pull* before *git push* to avoid conflicts.""",
    unsafe_allow_html=True,
)
