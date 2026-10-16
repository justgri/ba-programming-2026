import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm

st.title("Week 5 - Econometrics")

# Streamlit page for Problem Set 7 — Binary Dependent Variable
# Uses Smoking.csv for the smoking exercises and interactive calculators for the others.

st.header("Problem Set 7 — Binary Dependent Variable (Interactive)")

st.markdown(
    """
This page contains the following assignment sections:
1) **Interpreting coefficients with Binary DV** (interactive calculator),
2) **The Probability of Smoking** (runs on the attached `Smoking.csv`),
3) **Determinants of Females as Household Heads** (placeholder; not yet implemented).

> Tip: Section 1 depends on coefficients from a handout/table. Enter the coefficients in the widgets below.
"""
)


# =========================
# Helpers
# =========================
def add_const(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    if "const" not in X.columns:
        X = sm.add_constant(X, has_constant="add")
    return X


def fit_lpm(y: pd.Series, X: pd.DataFrame):
    Xc = add_const(X).astype(float)
    model = sm.OLS(y, Xc).fit(cov_type="HC1")  # robust SE
    return model


def margins_for_binary_dummy(model, df: pd.DataFrame, dummy_col: str):
    """
    Average partial effects for a 0/1 dummy in an LPM equals the coefficient,
    but we also compute average predicted probabilities when setting the dummy to 0 vs 1.
    """
    X0 = add_const(df.assign(**{dummy_col: 0})[model.model.exog_names[1:]])
    X1 = add_const(df.assign(**{dummy_col: 1})[model.model.exog_names[1:]])
    p0 = (X0 @ model.params).mean()
    p1 = (X1 @ model.params).mean()
    diff = p1 - p0
    return p0, p1, diff


def logistic(x):
    return 1 / (1 + np.exp(-x))


# =========================
# DATA: Smoking.csv
# =========================
with st.sidebar:
    st.header("Data")
    st.write("The smoking exercises use **Smoking.csv** (10,000 indoor workers).")
    uploaded = st.file_uploader(
        "Upload Smoking.csv (optional; bundled data is used by default)", type=["csv"]
    )
    data_path_note = st.caption(
        "By default, the app uses data/week_5/raw_data/econometrics/Smoking.csv."
    )

if uploaded is not None:
    smoking_df = pd.read_csv(uploaded, sep=None, engine="python")
else:
    try:
        smoking_path = (
            Path(__file__).resolve().parents[1]
            / "data" / "week_5" / "raw_data" / "econometrics" / "Smoking.csv"
        )
        smoking_df = pd.read_csv(smoking_path, sep=None, engine="python")
    except FileNotFoundError:
        smoking_df = None

if smoking_df is not None:
    # Coerce expected columns to numeric ints (if needed)
    for col in [
        "smoker",
        "smkban",
        "female",
        "black",
        "hispanic",
        "hsdrop",
        "hsgrad",
        "colsome",
        "colgrad",
    ]:
        if col in smoking_df.columns:
            smoking_df[col] = pd.to_numeric(smoking_df[col], errors="coerce").astype(
                "Int64"
            )
    for col in ["age"]:
        if col in smoking_df.columns:
            smoking_df[col] = pd.to_numeric(smoking_df[col], errors="coerce")
    # Optionally create age^2
    if "age" in smoking_df.columns and "age2" not in smoking_df.columns:
        smoking_df["age2"] = smoking_df["age"] ** 2

# =========================
# Tabs
# =========================
tab1, tab2, tab3 = st.tabs(
    [
        "1) Interpreting Coefficients (LPM calculator)",
        "2) Probability of Smoking (with data)",
        "3) Females as Household Heads (planned)",
    ]
)

# =========================
# TAB 1 — Interpreting coefficients with Binary DV
# =========================
with tab1:
    st.subheader(
        "1) Interpreting coefficients with Binary DV (enter coefficients from the handout)"
    )

    st.markdown("**Column (2):** LPM with Experience only")
    c2_col1, c2_col2, c2_col3 = st.columns(3)
    with c2_col1:
        alpha2 = st.number_input(
            "α (intercept)", value=0.50, step=0.01, format="%.4f", key="alpha2"
        )
    with c2_col2:
        beta_exp2 = st.number_input(
            "β_exp (per year)", value=0.05, step=0.005, format="%.4f", key="beta_exp2"
        )
    with c2_col3:
        se_beta_exp2 = st.number_input(
            "SE(β_exp) (optional)",
            value=0.0200,
            step=0.001,
            format="%.4f",
            key="se_beta_exp2",
        )

    frank_p = alpha2 + beta_exp2 * 6
    simon_p = alpha2 + beta_exp2 * 1

    st.write("**(1a)** Does pass probability depend on Experience?")
    st.write(f"- β_exp = **{beta_exp2:.3f}** (SE ≈ {se_beta_exp2:.3f}).")
    st.write("  -> If statistically ≠ 0, then **yes**; otherwise **no**.")

    st.write(
        "**(1b)** Frank (6 years):  \n" f"Predicted pass probability: **{frank_p:.3f}**"
    )
    st.write(
        "**(1c)** Simon (1 year):  \n" f"Predicted pass probability: **{simon_p:.3f}**"
    )

    st.markdown("---")
    st.markdown("**Column (4):** LPM with Experience and Male")
    c4_col1, c4_col2, c4_col3, c4_col4 = st.columns(4)
    with c4_col1:
        alpha4 = st.number_input(
            "α (intercept) — col (4)",
            value=0.55,
            step=0.01,
            format="%.4f",
            key="alpha4",
        )
    with c4_col2:
        beta_exp4 = st.number_input(
            "β_exp — col (4)", value=0.04, step=0.005, format="%.4f", key="beta_exp4"
        )
    with c4_col3:
        beta_male4 = st.number_input(
            "β_male (Male=1) — col (4)",
            value=-0.08,
            step=0.01,
            format="%.4f",
            key="beta_male4",
        )
    with c4_col4:
        se_beta_male4 = st.number_input(
            "SE(β_male) — for CI",
            value=0.0300,
            step=0.001,
            format="%.4f",
            key="se_beta_male4",
        )

    # For (2a), compute probabilities for men vs women at a user-chosen years of experience
    exp_for_2a = st.slider(
        "Experience (years) to evaluate P(pass | male/female)",
        min_value=0,
        max_value=40,
        value=6,
        step=1,
    )
    p_male = alpha4 + beta_exp4 * exp_for_2a + beta_male4 * 1
    p_fem = alpha4 + beta_exp4 * exp_for_2a + beta_male4 * 0

    st.write("**(2a)** Probability of passing:")
    st.write(f"- **Men**: {p_male:.3f}")
    st.write(f"- **Women**: {p_fem:.3f}")

    diff_girl_minus_boy = p_fem - p_male  # = -beta_male4
    z_90 = 1.6448536269514722
    ci_low = (-beta_male4) - z_90 * se_beta_male4
    ci_high = (-beta_male4) + z_90 * se_beta_male4

    st.write("**(2b)** How much more likely is a girl than a boy?")
    st.write(
        f"- Difference (girl − boy) = **{diff_girl_minus_boy:.3f}** (equals **{-beta_male4:.3f}** in this LPM)."
    )
    st.write(f"- 90% CI: **[{ci_low:.3f}, {ci_high:.3f}]**")

    st.markdown("---")
    st.write("**(3)** LPM predicted value 1.3?")
    st.caption(
        "Yes, a linear probability model can output values outside [0,1]. "
        "It’s a drawback of LPM: predictions are linear in X. "
        "While the coefficient interpretation is convenient, probabilities >1 or <0 do not make literal sense."
    )

# =========================
# TAB 2 — Probability of Smoking (with data)
# =========================
with tab2:
    st.subheader("2) The Probability of Smoking — Estimation on Smoking.csv")

    if smoking_df is None:
        st.error(
            "Smoking.csv not found. Upload it in the sidebar or restore the bundled dataset."
        )
    else:
        st.write("Preview:")
        st.dataframe(smoking_df.head(), use_container_width=True)

        # --- Part 1: LPM smoker ~ smkban
        st.markdown("### (1) LPM: smoker ~ smkban (robust SE)")
        y = smoking_df["smoker"].astype(float)
        X1 = smoking_df[["smkban"]]
        mod1 = fit_lpm(y, X1)
        st.write(mod1.summary())

        p0, p1, diff = margins_for_binary_dummy(mod1, smoking_df, "smkban")
        st.write(f"Predicted smoking probability without a ban: **{p0:.3f}**")
        st.write(f"Predicted smoking probability with a ban: **{p1:.3f}**")
        st.write(f"Difference (ban − no ban): **{100 * diff:.2f} percentage points**")

with tab3:
    st.info("This section is not yet implemented. Use the handout for this exercise.")
