import streamlit as st

st.set_page_config(page_title="Python for DA Playground", page_icon="🐍", layout="wide")

home_page = st.Page(
    "pages/home.py", title="Introduction", icon="🏠", default=True
)
sample_page = st.Page(
    "pages/sample_page.py", title="Sample Student Page", icon="👥"
)
jg_page = st.Page("pages/jg.py", title="Justinas Page", icon="🏄‍♂️")
lec_4_page = st.Page(
    "pages/lecture_week_4.py", title="Week 4 - Data wrangling", icon="📊"
)

lec_5_page_joins = st.Page(
    "pages/lecture_week_5_joins.py", title="Week 5 - Combine data", icon="📊"
)

lec_5_page_data_viz = st.Page(
    "pages/lecture_week_5_data_viz.py", title="Week 5 - Visualization", icon="📊"
)

lec_5_page_metrics = st.Page(
    "pages/lecture_week_5_econometrics.py",
    title="Week 5 - Econometrics",
    icon="📊",
)


shared_pages = [
    home_page,
    jg_page,
    sample_page,
    lec_4_page,
    lec_5_page_joins,
    lec_5_page_data_viz,
    lec_5_page_metrics,
]

pg = st.navigation(
    {"Common": shared_pages},
    position="sidebar",
    expanded=True,
)
pg.run()
