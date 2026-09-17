import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Hangman Test", layout="wide")


st.title("Hello world!")
st.header("This is our first python class")

st.markdown("Why don't we write a *little bit* more")

# maybe I want to leave some comment for myself

# I'll try learning some loops

fruit = "apple"

for letter in fruit:
    # print(letter)
    st.write(letter)

st.code(
    """
# This is some multi-line python code
print("hello world")
""",
    language="python",
)

print("hello world")

# Let's learn some functions


def multi_words(word, times):
    st.write(word, times)
    st.write("Oops, I wanted to write the word ", word, " ", times, " number of times")
    st.write(word * times)


multi_words("orange", 3)

st.subheader("This is for apples only")
multi_words("apple", 10)
