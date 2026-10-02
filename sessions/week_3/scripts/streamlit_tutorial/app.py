"""Streamlit companion to 03_data_cleaning_full.ipynb.

From the repository root:
python3 -m streamlit run sessions/week_3/scripts/app.py
"""

from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Week 3 - Data cleaning", layout="wide")
st.title("Week 3 - Intro to Data Analysis")

# Paths are relative to this script, regardless of where Streamlit is launched.
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"


# 1. Import and investigate
st.header("Import and investigate")
df_raw = pd.read_csv(RAW / "disney" / "disney_plus_shows.csv")
df = df_raw.copy(deep=True)

preview_rows = st.slider("Rows to preview", 5, 50, 10)
st.write("Shape (rows, columns):", df.shape)
st.dataframe(df.head(preview_rows))

with st.expander("Column types, missing values, and summary statistics"):
    left, right = st.columns(2)
    with left:
        st.write("Column types")
        st.dataframe(df.dtypes.astype(str).rename("dtype"))
    with right:
        st.write("Missing values per column")
        st.dataframe(df.isna().sum().rename("missing"))
    st.dataframe(df.describe())
    # df.info() prints text; collect that text to display it in the app.
    info = StringIO()
    df.info(buf=info)
    st.text(info.getvalue())


# 2. Series vs. DataFrame and sorting
with st.expander("Series vs. DataFrame"):
    titles = df["title"]
    title_frame = df[["title"]]
    left, right = st.columns(2)
    with left:
        st.code('titles = df["title"]')
        st.write("Type:", str(type(titles)), "Shape:", titles.shape)
        st.dataframe(titles.head(preview_rows))
    with right:
        st.code('title_frame = df[["title"]]')
        st.write("Type:", str(type(title_frame)), "Shape:", title_frame.shape)
        st.dataframe(title_frame.head(preview_rows))

    titles_sorted = titles.sort_values(ascending=False)
    st.write("Titles sorted in descending order (a new Series)")
    st.dataframe(titles_sorted.head(preview_rows))
    st.write("DataFrame sorted by year and title")
    st.dataframe(df.sort_values(by=["year", "title"]).head(preview_rows))


# 3. Modifying, creating, renaming, and removing columns
st.header("Clean the data")
df["year_clean"] = df["year"]
df["metascore_pct"] = df["metascore"] / 100
df["imdb_pct"] = df["imdb_rating"] / 10
df["avg_score"] = (df["metascore_pct"] + df["imdb_pct"]) / 2
df["avg_score_clean"] = df[["metascore_pct", "imdb_pct"]].mean(axis=1)
df[["year_clean", "release_date_clean"]] = df[["year", "released_at"]]

df = df.rename(
    columns={
        "avg_score": "avg_score_imdb_meta",
        "metascore_pct": "meta_drop",
        "imdb_pct": "imdb_drop",
    }
)
df = df.drop(columns=["year_clean", "meta_drop", "imdb_drop"])

# Convert types; 9999 represents a missing year, as in the notebook.
df["avg_score_char"] = df["avg_score_imdb_meta"].astype(str)
df["year_clean"] = pd.to_numeric(df["year"].str[0:4], errors="raise")
df["year_clean"] = df["year_clean"].fillna(9999).astype(int)

# Overwrite missing ratings using a condition and .loc.
df["rated_clean"] = df["rated"]
missing_rating = df["rated_clean"].isna()
df.loc[missing_rating, "rated_clean"] = "missing"

with st.expander("Inspect the new columns"):
    st.caption("year_clean uses 9999 for a missing year.")
    st.caption("avg_score_clean uses the available score if one score is missing.")
    st.dataframe(
        df[
            [
                "title",
                "year",
                "year_clean",
                "rated",
                "rated_clean",
                "metascore",
                "imdb_rating",
                "avg_score_imdb_meta",
                "avg_score_clean",
            ]
        ].head(preview_rows)
    )

with st.expander("Rename all columns on a separate copy"):
    cols_raw_clean = [col.lower() + "_raw" for col in df_raw.columns]
    df_temp = df_raw.copy()
    df_temp.columns = cols_raw_clean
    st.dataframe(df_temp.head(preview_rows))

with st.expander("Indexing, missing values, and duplicates"):
    st.write("Select rows by their index labels")
    st.dataframe(df.loc[[0, 1, 2, 3, 7]])
    st.write("Drop rows with any missing values:", len(df.dropna()))
    st.write("Drop rows with a missing plot:", len(df.dropna(subset=["plot"])))
    st.write("Unique ratings")
    st.dataframe(df["rated"].drop_duplicates())
    st.write("Unique year/rating pairs")
    st.dataframe(df[["year_clean", "rated"]].drop_duplicates())
    st.write("Keep the first full row for each year/rating pair")
    st.dataframe(df.drop_duplicates(subset=["year_clean", "rated"]).head(preview_rows))


# 4. Flags based on conditions (same thresholds as the notebook)
df["quality_flag"] = np.where(df["imdb_rating"] >= 7, "good", "bad")
conditions = [
    df["imdb_rating"].ge(8.5),
    df["imdb_rating"].between(7, 8.5, inclusive="left"),
    df["imdb_rating"].between(5, 7, inclusive="left"),
]
choices = ["top", "good", "mid"]
df["quality_group"] = np.select(conditions, choices, default="bad")

with st.expander("Quality flags: np.where() and np.select()"):
    st.caption("Top: 8.5+, good: 7–8.5, mid: 5–7, bad: below 5.")
    st.caption(
        "As in the notebook, missing IMDb ratings also receive the default 'bad' label."
    )
    st.dataframe(
        df[["title", "imdb_rating", "quality_flag", "quality_group"]].head(preview_rows)
    )


# 5. Widget values become ordinary Python variables used in filters.
st.header("Filter and select")
left, right = st.columns(2)
with left:
    show_type = st.radio("Type", ["All", "movie", "series", "episode"])
    rating_range = st.slider("IMDb rating range", 0.0, 10.0, (6.0, 8.0), 0.1)
    include_unrated = st.checkbox("Include missing IMDb ratings")
    ratings = st.multiselect(
        "Content ratings (empty = all)",
        sorted(df["rated_clean"].unique()),
    )
with right:
    known_years = df.loc[df["year_clean"] != 9999, "year_clean"]
    year_range = st.slider(
        "Year range",
        int(known_years.min()),
        int(known_years.max()),
        (int(known_years.min()), int(known_years.max())),
    )
    include_unknown_year = st.checkbox("Include missing years")
    only_pg = st.checkbox("Only ratings containing PG")
    drop_missing_plot = st.checkbox("Drop rows with a missing plot")
    drop_duplicates = st.checkbox("Drop duplicates by title and year")

rating_filter = df["imdb_rating"].between(rating_range[0], rating_range[1])
if include_unrated:
    rating_filter = rating_filter | df["imdb_rating"].isna()

year_filter = df["year_clean"].between(year_range[0], year_range[1])
if include_unknown_year:
    year_filter = year_filter | (df["year_clean"] == 9999)

df_filtered = df.loc[rating_filter & year_filter].copy()
if show_type != "All":
    df_filtered = df_filtered.loc[df_filtered["type"] == show_type]
if ratings:
    df_filtered = df_filtered.loc[df_filtered["rated_clean"].isin(ratings)]
if only_pg:
    pg_condition = df_filtered["rated_clean"].str.contains("PG", na=False)
    df_filtered = df_filtered.loc[pg_condition]
if drop_missing_plot:
    df_filtered = df_filtered.dropna(subset=["plot"])
if drop_duplicates:
    df_filtered = df_filtered.drop_duplicates(subset=["title", "year_clean"])

sort_order = st.radio(
    "Sort IMDb rating", ["Highest first", "Lowest first"], horizontal=True
)
df_filtered = df_filtered.sort_values(
    "imdb_rating", ascending=(sort_order == "Lowest first")
)
selected_columns = st.multiselect(
    "Columns to display and download",
    df.columns.tolist(),
    default=[
        "title",
        "type",
        "year_clean",
        "rated_clean",
        "imdb_rating",
        "quality_group",
    ],
)
st.write("Matching rows:", len(df_filtered))
if df_filtered.empty:
    st.info("No rows match these filters. Try a wider range.")
if selected_columns:
    st.dataframe(df_filtered[selected_columns])
else:
    st.info("Select at least one column to display and download.")


# 6. Export: downloads use the filters; local files use the full cleaned data.
st.header("Export data")
st.download_button(
    "Download the filtered table",
    data=df_filtered[selected_columns].to_csv(index=False),
    file_name="disney_filtered.csv",
    mime="text/csv",
    disabled=not selected_columns,
)

with st.expander("Save the full cleaned dataset locally"):
    st.caption("Writes all rows and columns, regardless of the filters above.")
    st.caption("Existing files with the same names will be replaced.")
    st.write("Folder:", str(CLEAN / "disney"))
    if st.button("Save cleaned CSV and one CSV per year"):
        df_clean = df.copy(deep=True)
        annual_folder = CLEAN / "disney" / "annual"
        annual_folder.mkdir(parents=True, exist_ok=True)
        df_clean.to_csv(CLEAN / "disney" / "disney_movies_clean.csv", index=False)

        unique_years = df_clean["year_clean"].drop_duplicates().sort_values()
        for year in unique_years:
            df_clean_year = df_clean.loc[df_clean["year_clean"] == year]
            out_path = annual_folder / f"disney_movies_clean_{year}.csv"
            df_clean_year.to_csv(out_path, index=False)
        st.success(f"Saved the full dataset and {len(unique_years)} annual files.")
