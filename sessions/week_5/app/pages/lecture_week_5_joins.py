import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np

st.title("Week 5 - Combining Multiple Datasets")


st.link_button(
    "pandas User Guide",
    "https://pandas.pydata.org/docs/user_guide/merging.html",
    type="primary",
)

APP_ROOT = Path(__file__).resolve().parents[1]

st.write(APP_ROOT)
DATA = APP_ROOT / "data" / "week_5"

IMAGES = APP_ROOT / "src" / "images"

TABLES = DATA / "raw_data"

st.header("Concatenation")

st.subheader("Import and stack multiple clean CSV files")

DATA_DIR = TABLES / "disney_annual_clean"

st.markdown("**Found files:**")

all_paths = sorted(DATA_DIR.glob("*.csv"))
st.write([path.name for path in all_paths])

files_dict = {}

n = 0
for path in all_paths:
    # st.write(path)
    n += 1
    # st.write(n)
    files_dict[n] = pd.read_csv(path)
    files_dict[n]["file_path"] = str(path)

# st.write(files_dict)

# Concatenate all
st.markdown("### Combined dataset")

combined = pd.concat(files_dict.values(), ignore_index=True, sort=False)

st.write(combined)

st.write(combined.shape)

st.subheader("Import and stack multiple sheets from Excel")


# ---- Paths ----
excel_path = TABLES / "disney_annual.xlsx"
data_dict = pd.read_excel(excel_path, sheet_name=None)
combined = (
    pd.concat(data_dict, names=["source_sheet"])
    .reset_index(level=0)
    .reset_index(drop=True)
)

st.write(combined)

st.header("Merging")

col1, col2 = st.columns(2)

col1.image(IMAGES / "join_diagrams.png")
col2.image(IMAGES / "join_tables.png")

st.subheader("Toy example: Disney movies")

# -----------------------------
# 1) Make two simple DataFrames
# -----------------------------
# sales_df: keys + overlap + unique
sales_df = pd.DataFrame(
    [
        {"title": "Frozen", "year": 2013, "genre": "Animation", "sales": 1300},
        {"title": "Moana", "year": 2016, "genre": "Animation", "sales": 690},
        {"title": "Toy Story", "year": 1995, "genre": "Animation", "sales": 373},
        {"title": "The Lion King", "year": 1994, "genre": "Animation", "sales": 968},
        {
            "title": "Fantasia",
            "year": 1940,
            "genre": "Animation",
            "sales": 76,
        },  # no match in lookup
    ]
)

# lookup_df: TWO rows for Frozen (same keys) => one-to-many case
lookup_df = pd.DataFrame(
    [
        {
            "title": "Frozen",
            "year": 2013,
            "genre": "Animation/Adventure",
            "director": "Chris Buck",
        },
        {
            "title": "Frozen",
            "year": 2013,
            "genre": "Animation/Adventure",
            "director": "Jennifer Lee",
        },  # duplicate key
        {
            "title": "Moana",
            "year": 2016,
            "genre": "Animation/Adventure",
            "director": "Ron Clements",
        },
        {
            "title": "Toy Story",
            "year": 1995,
            "genre": "Animation/Adventure",
            "director": "John Lasseter",
        },
        {
            "title": "Inside Out",
            "year": 2015,
            "genre": "Animation/Comedy",
            "director": "Pete Docter",
        },  # only in lookup
        {
            "title": "The Lion King",
            "year": 1994,
            "genre": "Animation/Adventure",
            "director": "Roger Allers",
        },
    ]
)

# ---------------------------------------
# 2) Merges with small option differences
# ---------------------------------------
# A) LEFT join with one-to-many validation (Frozen duplicates in lookup)
left_one_to_many = pd.merge(
    sales_df,
    lookup_df,
    on=["title", "year"],
    how="left",
    suffixes=("_sales", "_lookup"),
    validate="one_to_many",
)

# B) LEFT join with one-to-one validation after de-duping lookup
lookup_unique = lookup_df.drop_duplicates(subset=["title", "year"])
left_one_to_one = pd.merge(
    sales_df,
    lookup_unique,
    on=["title", "year"],
    how="left",
    suffixes=("_sales", "_lookup"),
    validate="one_to_one",
)

# C) OUTER join to show all rows from both sides
outer_many_to_many = pd.merge(
    sales_df,
    lookup_df,
    on=["title", "year"],
    how="outer",
    suffixes=("_sales", "_lookup"),
    validate="many_to_many",
)

# --------------------------------
# 3) Show side-by-side in columns
# --------------------------------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**sales_df** (left table)")
    st.dataframe(sales_df, use_container_width=True)

with c2:
    st.markdown("**lookup_df** (right table)**")
    st.caption("Notice duplicate key for Frozen (one-to-many).")
    st.dataframe(lookup_df, use_container_width=True)

with c3:
    st.markdown("**LEFT (one_to_many)**")
    st.caption("Duplicate keys in lookup → multiple matches (e.g., Frozen)")
    st.dataframe(left_one_to_many, use_container_width=True)

c4, c5 = st.columns(2)
with c4:
    st.markdown("**LEFT (one_to_one)**")
    st.caption("After dropping duplicates in lookup")
    st.dataframe(left_one_to_one, use_container_width=True)

with c5:
    st.markdown("**OUTER (many_to_many)**")
    st.caption("Shows unmatched from both sides (e.g., Fantasia, Inside Out)")
    st.dataframe(outer_many_to_many, use_container_width=True)

# -------------------------------------------
# 4) New row: indicator + validate illustration
# -------------------------------------------
# LEFT merge with indicator=True to see where rows came from
left_with_indicator = pd.merge(
    sales_df,
    lookup_df,
    on=["title", "year"],
    how="left",
    indicator=True,  # <— adds `_merge` column
    suffixes=("_sales", "_lookup"),
    validate="one_to_many",  # still valid: left is 1x per key, right has duplicates
)

# Try a strict validate that will FAIL with duplicates (for teaching)
try:
    _ = pd.merge(
        sales_df,
        lookup_df,  # has duplicate Frozen
        on=["title", "year"],
        how="left",
        validate="one_to_one",  # <— this will raise a MergeError
    )
    validate_msg = "No error (unexpected here)."
except Exception as e:
    validate_msg = f"{type(e).__name__}: {e}"

c6, c7 = st.columns(2)
with c6:
    st.markdown("**LEFT + indicator=True**")
    st.caption("`_merge` shows left_only / right_only / both")
    st.dataframe(left_with_indicator, use_container_width=True)

with c7:
    st.markdown("**Validate demo**")
    st.caption(
        "For teaching: forcing `validate='one_to_one'` on duplicated keys raises an error."
    )
    st.code(validate_msg, language="text")
    st.caption("Fix by de-duplicating keys (see **LEFT (one_to_one)** above).")

st.info(
    "Notes: Keys are `title` + `year`. Overlap: `genre` → suffixes `_sales`/`_lookup`. "
    "Unique columns: `sales` (left) and `director` (right). "
    "`indicator=True` adds `_merge`. `validate` checks merge cardinality."
)
