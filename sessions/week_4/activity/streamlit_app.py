"""Week 4 live-coding solution to the synthetic Disney activity.

From the repository root:
python3 -m streamlit run sessions/week_4/scripts/activity_solution/streamlit_app.py

The script runs from top to bottom on each widget change.
Outputs are saved under Week 4's output/data_clean/disney_activity,
output/tables/disney_activity, and output/charts/disney_activity folders.
Reruns overwrite the corresponding files; browser downloads remain available.
"""

# BEGIN imports
from io import BytesIO
from pathlib import Path

import matplotlib
import pandas as pd
import streamlit as st

matplotlib.use("Agg")
import matplotlib.pyplot as plt
# END imports


# BEGIN functions
# Read the actual source so code boxes follow edits made during live coding.
APP_SOURCE = Path(__file__).read_text()


def show_change(df_before, df_after):
    """Keep the outline visible and reveal each comparison when needed."""
    with st.expander("See data:", expanded=False):
        left, right = st.columns(2)
        with left:
            st.subheader("Before")
            st.dataframe(df_before, hide_index=True, width="stretch")
        with right:
            st.subheader("After")
            st.dataframe(df_after, hide_index=True, width="stretch")


def show_code(section_id):
    """Display a marked source block without executing code from a string."""
    code = APP_SOURCE.split(f"# BEGIN {section_id}\n", 1)[1]
    code = code.split(f"# END {section_id}\n", 1)[0].strip()
    with st.expander("See code:", expanded=False):
        st.code(code, language="python")
# END functions


st.set_page_config(page_title="Week 4 - Disney activity solution", layout="wide")
st.title("Week 4 - Disney activity solution")

# BEGIN paths
# __file__ makes input and output paths independent of the working directory.
WEEK_4 = Path(__file__).resolve().parents[2]
WORKBOOK = WEEK_4 / "activity" / "disney_messy_data_activity.xlsx"
OUT_CLEAN = WEEK_4 / "output" / "data_clean" / "disney_activity"
OUT_TABLES = WEEK_4 / "output" / "tables" / "disney_activity"
OUT_CHARTS = WEEK_4 / "output" / "charts" / "disney_activity"
for folder in [OUT_CLEAN, OUT_TABLES, OUT_CHARTS]:
    folder.mkdir(parents=True, exist_ok=True)
# END paths


st.header("Setup")

st.subheader("Library imports")
st.markdown("Import the libraries we use to read, clean, display, and export the data.")
show_code("imports")

st.subheader("General functions")
st.markdown("Define reusable functions for the before-and-after tables and the code expanders.")
show_code("functions")

st.subheader("Input and output paths")
st.markdown("Locate the workbook and output folders relative to this script so it works from any working directory.")
show_code("paths")


# 1. A dictionary of sheet names and DataFrames is our starting point.
st.header("1. Plan the output and inspect the sources")
st.markdown(
    "Our clean table will have one row per movie and market, with revenue in millions of USD."
)

# BEGIN 1.
raw = pd.read_excel(WORKBOOK, sheet_name=None)
with st.expander("See data:", expanded=False):
    left, right = st.columns(2)
    with left:
        for sheet_name in ["movies_1994", "movies_1995"]:
            st.subheader(sheet_name)
            st.dataframe(raw[sheet_name], hide_index=True, width="stretch")
    with right:
        for sheet_name in ["movies_2013", "movie_lookup"]:
            st.subheader(sheet_name)
            st.dataframe(raw[sheet_name], hide_index=True, width="stretch")
# END 1.
show_code("1.")


# 2. Clean the two older files together, then clean the newer layout separately.
st.header("2. Clean each source layout")

st.subheader("2.1 Stack the older files and preserve their years")
st.markdown("Extract the year from each sheet name before stacking its rows.")

# BEGIN 2.1
older_parts = []
for sheet_name in ["movies_1994", "movies_1995"]:
    df_part = raw[sheet_name].copy()
    df_part["source_year"] = int(sheet_name.split("_")[1])
    older_parts.append(df_part)

df_older = pd.concat(older_parts, ignore_index=True)
df_older_without_year = pd.concat(
    [raw["movies_1994"], raw["movies_1995"]], ignore_index=True
)
show_change(
    df_older_without_year[["movie_id", "title", "release_date"]],
    df_older[["movie_id", "title", "release_date", "source_year"]],
)
# END 2.1
show_code("2.1")

st.subheader("2.2 Reconstruct the full dates")
st.markdown("Combine each month/day string with its sheet year before converting it to a date.")

# BEGIN 2.2
df_older_dates = df_older.copy()
full_date_strings = (
    df_older_dates["source_year"].astype(str) + "/" + df_older_dates["release_date"]
)
df_older_dates["release_date"] = pd.to_datetime(full_date_strings, format="%Y/%m/%d")
show_change(
    df_older[["movie_id", "release_date", "source_year"]],
    df_older_dates[["movie_id", "release_date", "source_year"]],
)
# END 2.2
show_code("2.2")

st.subheader("2.3 Inspect and reshape the revenue headers")
st.markdown("The instructor confirms that US means USA, EU means Europe, and these amounts are millions of USD before we melt the columns.")

# BEGIN 2.3
id_columns = [
    "movie_id", "title", "rated", "release_date", "source_year", "runtime_minutes"
]
revenue_columns = ["rev_US_usd", "rev_EU_usd"]
df_older_long = df_older_dates.melt(
    id_vars=id_columns,
    value_vars=revenue_columns,
    var_name="source_column",
    value_name="revenue",
)
df_older_long["market_code"] = (
    df_older_long["source_column"]
    .str.replace("rev_", "", regex=False)
    .str.replace("_usd", "", regex=False)
)
# Market coverage and the million-unit scale come from confirmed metadata.
confirmed_markets = {"US": "USA", "EU": "Europe"}
df_older_long["market"] = df_older_long["market_code"].map(confirmed_markets)
df_older_long["currency"] = "USD"
show_change(
    df_older_dates[["movie_id"] + revenue_columns],
    df_older_long[["movie_id", "market", "revenue", "currency"]],
)
# END 2.3
show_code("2.3")

st.subheader("2.4 Standardize the 2013 ratings")
st.markdown("Strip spaces, standardize case, and remove the rating prefix to recover the same categories.")

# BEGIN 2.4
df_newer = raw["movies_2013"].copy()
df_newer["source_year"] = int("movies_2013".split("_")[1])
df_newer_ratings = df_newer.copy()
df_newer_ratings["rated"] = (
    df_newer_ratings["rated"]
    .str.strip()
    .str.upper()
    .str.replace("RATED ", "", regex=False)
)
show_change(
    df_newer[["movie_id", "rated"]].drop_duplicates(),
    df_newer_ratings[["movie_id", "rated"]].drop_duplicates(),
)
# END 2.4
show_code("2.4")

st.subheader("2.5 Parse the 2013 full dates")
st.markdown("The 2013 dates already contain a year and use month/day/year order.")

# BEGIN 2.5
df_newer_dates = df_newer_ratings.copy()
df_newer_dates["release_date"] = pd.to_datetime(
    df_newer_dates["release_date"], format="%m/%d/%Y"
)
show_change(
    df_newer_ratings[["movie_id", "release_date"]].drop_duplicates(),
    df_newer_dates[["movie_id", "release_date"]].drop_duplicates(),
)
# END 2.5
show_code("2.5")

st.subheader("2.6 Confirm the missing currency and units")
st.markdown(
    "For this exercise, the instructor confirms that 2013 USA revenues are USD and Europe revenues are EUR, all in millions."
)

# This mapping is confirmed classroom information, not a guess based on geography.
# BEGIN 2.6
confirmed_currencies = {"USA": "USD", "Europe": "EUR"}
df_newer_currency = df_newer_dates.copy()
df_newer_currency["currency"] = df_newer_currency["market"].map(confirmed_currencies)
show_change(
    df_newer_dates[["movie_id", "market", "revenue"]],
    df_newer_currency[["movie_id", "market", "revenue", "currency"]],
)
# END 2.6
show_code("2.6")


# 3. Align the schemas before applying the remaining steps to all movies.
st.header("3. Combine the cleaned inputs")

st.subheader("3.1 Align columns and stack all three files")
st.markdown("Matching columns and types allow the same concatenation step to combine both layouts.")

# BEGIN 3.1
common_columns = [
    "movie_id", "title", "rated", "release_date", "source_year",
    "market", "revenue", "currency", "runtime_minutes",
]
df_older_ready = df_older_long[common_columns].copy()
df_newer_ready = df_newer_currency.copy()
df_newer_ready["runtime_minutes"] = pd.NA
df_newer_ready = df_newer_ready[common_columns]

for df_frame in [df_older_ready, df_newer_ready]:
    df_frame["runtime_minutes"] = df_frame["runtime_minutes"].astype("Float64")
    df_frame["revenue"] = df_frame["revenue"].astype(float)

df_combined = pd.concat([df_older_ready, df_newer_ready], ignore_index=True)
show_change(
    df_older_ready[["movie_id", "market", "revenue", "currency", "runtime_minutes"]],
    df_combined[["movie_id", "market", "revenue", "currency", "runtime_minutes"]],
)
# END 3.1
show_code("3.1")

st.subheader("3.2 Extract year and month, then check the year")
st.markdown("Full dates provide year and month values, and their years should agree with the sheet names.")

# BEGIN 3.2
df_dated = df_combined.copy()
df_dated["release_year"] = df_dated["release_date"].dt.year
df_dated["release_month"] = df_dated["release_date"].dt.month
df_dated["year_matches_sheet"] = df_dated["release_year"] == df_dated["source_year"]
show_change(
    df_combined[["movie_id", "release_date", "source_year"]].drop_duplicates(),
    df_dated[["movie_id", "release_year", "release_month", "year_matches_sheet"]].drop_duplicates(),
)
# END 3.2
show_code("3.2")

st.subheader("3.3 Convert revenues to the same currency")
st.markdown("Use the classroom rate of 1 EUR = 1.10 USD, keeping USD values unchanged and all amounts in millions.")

# Synthetic teaching rate; this is not a live exchange-rate feed.
# BEGIN 3.3
usd_rates = {"USD": 1.0, "EUR": 1.10}
df_converted = df_dated.copy()
df_converted["usd_rate"] = df_converted["currency"].map(usd_rates)
df_converted["revenue_usd_m"] = (
    df_converted["revenue"] * df_converted["usd_rate"]
).round(2)
show_change(
    df_dated[["movie_id", "market", "revenue", "currency"]],
    df_converted[["movie_id", "market", "usd_rate", "revenue_usd_m"]],
)
# END 3.3
show_code("3.3")


# 4. Check coverage and compare independent values before filling or correcting.
st.header("4. Merge and verify the lookup")

st.subheader("4.1 Left-join on the movie ID")
st.markdown("A left join retains every movie, while validation requires each lookup ID to be unique.")

# BEGIN 4.1
lookup = raw["movie_lookup"].copy()
df_joined = df_converted.merge(
    lookup, on="movie_id", how="left", validate="many_to_one", indicator=True
)
show_change(
    df_converted[["movie_id", "title", "runtime_minutes"]].drop_duplicates(),
    df_joined[["movie_id", "title", "category", "runtime_hours", "_merge"]].drop_duplicates(),
)
# END 4.1
show_code("4.1")

st.subheader("4.2 Inspect the unmatched movies")
st.markdown("The two 1994 movies have no lookup records, so their existing runtimes must be retained.")

# BEGIN 4.2
df_unmatched = df_joined.loc[
    df_joined["_merge"] == "left_only",
    ["movie_id", "title", "runtime_minutes", "category"],
].drop_duplicates()
with st.expander("See data:", expanded=False):
    st.dataframe(df_unmatched, hide_index=True, width="stretch")
# END 4.2
show_code("4.2")

st.subheader("4.3 Convert hours to minutes and compare")
st.markdown("Convert the lookup values to minutes before checking movies with two available runtime measurements.")

# BEGIN 4.3
df_compared = df_joined.copy()
df_compared["runtime_lookup_minutes"] = df_compared["runtime_hours"] * 60
both_runtimes = (
    df_compared["runtime_minutes"].notna()
    & df_compared["runtime_lookup_minutes"].notna()
)
df_compared["runtime_mismatch"] = (
    both_runtimes
    & (df_compared["runtime_minutes"] != df_compared["runtime_lookup_minutes"])
).fillna(False)
show_change(
    df_joined[["movie_id", "title", "runtime_minutes", "runtime_hours"]].drop_duplicates(),
    df_compared[["movie_id", "runtime_minutes", "runtime_lookup_minutes", "runtime_mismatch"]].drop_duplicates(),
)
# END 4.3
show_code("4.3")

st.subheader("4.4 Resolve the confirmed error and fill missing runtimes")
st.markdown("The instructor confirms Toy Story should be 90 minutes, and the lookup supplies the missing 2013 runtimes.")

# BEGIN 4.4
df_resolved = df_compared.copy()
toy_story = df_resolved["movie_id"] == "D03"
df_resolved.loc[toy_story, "runtime_minutes"] = df_resolved.loc[
    toy_story, "runtime_lookup_minutes"
]
missing_runtime = df_resolved["runtime_minutes"].isna()
df_resolved.loc[missing_runtime, "runtime_minutes"] = df_resolved.loc[
    missing_runtime, "runtime_lookup_minutes"
]
show_change(
    df_compared[["movie_id", "title", "runtime_minutes"]].drop_duplicates(),
    df_resolved[["movie_id", "title", "runtime_minutes"]].drop_duplicates(),
)
# END 4.4
show_code("4.4")

st.subheader("4.5 Fill the confirmed category and retain unknowns")
st.markdown("Fill Monsters University's confirmed category and label the unmatched movies as Unknown until their metadata is supplied.")

# BEGIN 4.5
df_categorized = df_resolved.copy()
df_categorized.loc[df_categorized["movie_id"] == "D06", "category"] = "Animation"
df_categorized["category"] = df_categorized["category"].fillna("Unknown")
show_change(
    df_resolved[["movie_id", "title", "category"]].drop_duplicates(),
    df_categorized[["movie_id", "title", "category"]].drop_duplicates(),
)
# END 4.5
show_code("4.5")

st.subheader("4.6 Tidy data: the starting point for analysis")
st.markdown("One row per movie and market gives us a single tidy dataset that every summary and chart can reuse without cleaning again.")

# BEGIN 4.6
clean_columns = [
    "movie_id", "title", "release_date", "release_year", "release_month",
    "rated", "market", "revenue_usd_m", "runtime_minutes", "category",
]
df_clean_data = df_categorized[clean_columns].copy()
df_clean_data.to_csv(OUT_CLEAN / "disney_clean.csv", index=False)
with st.expander("See data:", expanded=False):
    st.dataframe(df_clean_data, hide_index=True, width="stretch")
    st.download_button(
        "Download clean tidy data (CSV)",
        data=df_clean_data.to_csv(index=False),
        file_name="disney_clean.csv",
        mime="text/csv",
    )
# END 4.6
show_code("4.6")


# 5. Aggregation changes the number of observations; pivot changes their layout.
st.header("5. Summary A: revenue by category and year")

st.subheader("5.1 Select columns and aggregate the movie-market rows")
st.markdown("Reuse the same tidy dataset, select the category and year variables, then sum their revenues.")

# BEGIN 5.1
analysis_columns = ["category", "release_year", "revenue_usd_m"]
df_summary_a_input = df_clean_data[analysis_columns].copy()
df_summary_a_long = (
    df_summary_a_input.groupby(["category", "release_year"], as_index=False, dropna=False)
    .agg({"revenue_usd_m": "sum"})
)
with st.expander("See data:", expanded=False):
    before, intermediate, after = st.columns(3)
    with before:
        st.subheader("Before: same tidy data")
        st.dataframe(df_clean_data, hide_index=True, width="stretch")
    with intermediate:
        st.subheader("Intermediate: selected columns")
        st.dataframe(df_summary_a_input, hide_index=True, width="stretch")
    with after:
        st.subheader("After: grouped totals")
        st.dataframe(df_summary_a_long, hide_index=True, width="stretch")
# END 5.1
show_code("5.1")

st.subheader("5.2 Pivot years into columns")
st.markdown("The grouped totals are an intermediate result from the same tidy dataset that we can pivot for comparison.")

# BEGIN 5.2
df_summary_a = (
    df_summary_a_long.pivot(
        index="category", columns="release_year", values="revenue_usd_m"
    )
    .fillna(0)
    .reset_index()
    .rename(columns=str)
)
with st.expander("See data:", expanded=False):
    before, intermediate, after = st.columns(3)
    with before:
        st.subheader("Before: same tidy data")
        st.dataframe(df_clean_data, hide_index=True, width="stretch")
    with intermediate:
        st.subheader("Intermediate: grouped totals")
        st.dataframe(df_summary_a_long, hide_index=True, width="stretch")
    with after:
        st.subheader("After: category by year")
        st.dataframe(df_summary_a, hide_index=True, width="stretch")
# END 5.2
show_code("5.2")


# 6. A different set of keys produces a different view of the same revenue data.
st.header("6. Summary B: revenue by movie and market")
st.markdown("Reuse the same tidy dataset, select the movie and market variables, then summarize and pivot their revenues.")

# BEGIN 6.
summary_b_columns = ["movie_id", "title", "market", "revenue_usd_m"]
df_summary_b_input = df_clean_data[summary_b_columns].copy()
df_summary_b_long = (
    df_summary_b_input.groupby(["movie_id", "title", "market"], as_index=False, dropna=False)
    .agg({"revenue_usd_m": "sum"})
)
df_summary_b = df_summary_b_long.pivot(
    index=["movie_id", "title"], columns="market", values="revenue_usd_m"
).reset_index()
with st.expander("See data:", expanded=False):
    before, intermediate, after = st.columns(3)
    with before:
        st.subheader("Before: same tidy data")
        st.dataframe(df_clean_data, hide_index=True, width="stretch")
    with intermediate:
        st.subheader("Intermediate: selected columns")
        st.dataframe(df_summary_b_input, hide_index=True, width="stretch")
    with after:
        st.subheader("After: movie by market")
        st.dataframe(df_summary_b, hide_index=True, width="stretch")
# END 6.
show_code("6.")


# 7. A dictionary and a loop let us apply the same export command to three tables.
st.header("7. Export the summary tables")
st.markdown("Export both summary layouts separately from the tidy data saved before analysis.")
# BEGIN 7.
with st.expander("See data:", expanded=False):
    exports = {
        "category_by_year.csv": df_summary_a,
        "movies_by_market.csv": df_summary_b,
    }
    for filename, df_table in exports.items():
        df_table.to_csv(OUT_TABLES / filename, index=False)
        st.subheader(filename)
        st.dataframe(df_table, hide_index=True, width="stretch")
        st.download_button(
            f"Download {filename}",
            data=df_table.to_csv(index=False),
            file_name=filename,
            mime="text/csv",
        )
# END 7.
show_code("7.")


# 8. Widget return values become ordinary Python strings used in our analysis.
st.header("8. Plot and export a chart")
st.markdown("Choose the grouping and chart type to turn the same tidy data into selected columns, grouped totals, and a convenient plotting layout.")

# BEGIN 8.
with st.expander("See data:", expanded=False):
    left, right = st.columns(2)
    with left:
        series_column = st.selectbox("Group the series by", ["category", "market", "rated"])
    with right:
        chart_type = st.selectbox("Chart type", ["Bar", "Line"])

    chart_columns = ["release_year", series_column, "revenue_usd_m"]
    df_chart_input = df_clean_data[chart_columns].copy()
    df_chart_grouped = (
        df_chart_input.groupby(["release_year", series_column], as_index=False, dropna=False)
        .agg({"revenue_usd_m": "sum"})
    )
    df_chart_wide = df_chart_grouped.pivot(
        index="release_year", columns=series_column, values="revenue_usd_m"
    ).fillna(0).sort_index()
    # Melt the wide summary so both views contain the same values, including zeros.
    df_chart_long = df_chart_wide.reset_index().melt(
        id_vars="release_year",
        var_name=series_column,
        value_name="revenue_usd_m",
    ).sort_values(["release_year", series_column], ignore_index=True)
    plot_layout = "wide" if chart_type == "Bar" else "long"

    before, intermediate, after = st.columns(3)
    with before:
        st.subheader("Before: same tidy data")
        st.dataframe(df_clean_data, hide_index=True, width="stretch")
    with intermediate:
        st.subheader("Intermediate: selected columns")
        st.dataframe(df_chart_input, hide_index=True, width="stretch")
        st.subheader("Then: grouped totals")
        st.dataframe(df_chart_grouped, hide_index=True, width="stretch")
    with after:
        st.subheader("After: chart data")
        show_wide = st.toggle("View chart data as wide", value=True, key="chart_data_view_wide")
        view_layout = "wide" if show_wide else "long"
        st.markdown(f"The table shows {view_layout} data while the {chart_type.lower()} plotting call uses {plot_layout} data.")
        if show_wide:
            st.dataframe(df_chart_wide.reset_index(), hide_index=True, width="stretch")
        else:
            st.dataframe(df_chart_long, hide_index=True, width="stretch")

    # Pick the convenient plotting input independently of the displayed data view.
    if chart_type == "Bar":
        st.bar_chart(
            df_chart_wide,
            x_label="Release year",
            y_label="Revenue (million USD)",
            stack=False,
        )
    else:
        st.line_chart(
            df_chart_long,
            x="release_year",
            y="revenue_usd_m",
            color=series_column,
            x_label="Release year",
            y_label="Revenue (million USD)",
        )

    # Matplotlib makes an image of the same data for the downloadable chart.
    fig, ax = plt.subplots(figsize=(8, 4))
    if chart_type == "Bar":
        df_chart_wide.plot.bar(ax=ax)
    else:
        for name, df_values in df_chart_long.groupby(series_column):
            ax.plot(df_values["release_year"], df_values["revenue_usd_m"], marker="o", label=name)
        ax.legend(title=series_column)
    ax.set_xlabel("Release year")
    ax.set_ylabel("Revenue (million USD)")
    fig.tight_layout()

    chart_image = BytesIO()
    fig.savefig(chart_image, format="png", dpi=150)
    plt.close(fig)
    chart_filename = f"disney_{series_column}_{chart_type.lower()}.png"
    (OUT_CHARTS / chart_filename).write_bytes(chart_image.getvalue())
    st.download_button(
        "Download the chart (PNG)",
        data=chart_image.getvalue(),
        file_name=chart_filename,
        mime="image/png",
    )
# END 8.
show_code("8.")
