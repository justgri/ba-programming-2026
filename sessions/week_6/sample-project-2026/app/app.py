import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config("Class Sample Project", page_icon="🐍", layout="wide")

home_page = st.Page("pages/homepage.py", icon="🏠", title="Homepage")
data_page = st.Page("pages/data_overview.py", icon="📊", title="Data Overview")

user_pages = [home_page, data_page]

pg = st.navigation(user_pages, position="sidebar", expanded=True)

pg.run()
