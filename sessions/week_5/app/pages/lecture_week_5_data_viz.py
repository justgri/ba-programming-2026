import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Week 5 - Data Visualization")

col1, col2, col3, _ = st.columns((1, 1, 1, 3))
with col1:
    st.subheader("Inspiration")

    st.link_button(
        "pinterest style inspiration",
        "https://www.dataviz-inspiration.com/",
        type="primary",
    )

    st.link_button(
        "CH data geographer",
        "https://tobias-stalder.netlify.app/dataviz/",
        type="primary",
    )

    st.link_button(
        "data art beyond charts", "https://eolay.tilda.ws/dataart/en", type="primary"
    )

    st.link_button(
        "historical maps",
        "https://www.mapklimantas.com/gallery",
        type="primary",
    )


with col2:
    st.subheader("Science")

    st.link_button(
        "all chart types",
        "https://www.data-to-viz.com/",
        type="primary",
    )

    st.link_button(
        "more examples of chart types",
        "https://datavizproject.com/",
        type="primary",
    )

    st.link_button(
        "story telling with data makeovers",
        "https://www.storytellingwithdata.com/makeovers",
        type="primary",
    )
    st.link_button(
        "story telling with data youtube",
        "https://www.youtube.com/@storytellingwithdata/videos",
        type="primary",
    )

with col3:
    st.subheader("Tutorials")

    st.link_button(
        "matplotlib tutorial",
        "https://python-graph-gallery.com/matplotlib/",
        type="primary",
    )

    st.link_button(
        "matplotlib official cheat sheets, handouts, tutorials",
        "https://matplotlib.org/cheatsheets/",
        type="primary",
    )

    st.link_button(
        "python chart gallery with code",
        "https://python-graph-gallery.com/",
        type="primary",
    )

    st.link_button(
        "plotly fundamentals",
        "https://plotly.com/python/plotly-fundamentals/",
        type="primary",
    )


st.header("Data Viz with Python")


APP_ROOT = Path(__file__).resolve().parents[1]

DATA = APP_ROOT / "data" / "week_5" / "raw_data"
DISNEY = DATA / "disney_movies_clean.csv"
COUNTRIES = DATA / "Countries.csv"

disney_df = pd.read_csv(DISNEY)
countries_df = pd.read_csv(COUNTRIES)


col_filt, col_df, col_df_lim, _ = st.columns((1, 1, 1, 3))


with col_filt:
    all_countries = countries_df["country"].unique()

    countries_keep = st.multiselect(
        "Select countries:",
        all_countries,
        default=["United States", "China", "Switzerland"],
    )

if not countries_keep:
    st.info("Select at least one country to display the visualization examples.")
    st.stop()


with col_df:
    ### Data cleaning ###
    df = (
        countries_df.loc[
            countries_df["country"].isin(countries_keep),
            ["country", "year", "population"],
        ]
        .sort_values(["country", "year"])
        .assign(
            base_pop=lambda d: d.groupby("country")["population"].transform("first"),
            growth_pct=lambda d: (d["population"] / d["base_pop"]) * 100 - 100,
        )
    )

    # Quick sanity checks (optional)
    st.dataframe(df.head(n=20), width="content")

with col_df_lim:
    st.dataframe(
        df.groupby("country").agg(
            first_year=("year", "min"), last_year=("year", "max")
        ),
        width="content",
    )


st.subheader("Examples with matplotlib")


def chart_cols():

    return st.columns((1, 2))


col_code, col_chart = chart_cols()

with col_code:

    st.code(
        """
fig, ax = plt.subplots()
for name, g in df.groupby("country"):
    ax.plot(g["year"], g["growth_pct"], marker="o", label=name)

ax.set_title("Population Growth over Time – US, China, and Nigeria")
ax.set_xlabel("Year")
ax.set_ylabel("Percent Change to Base Year")
ax.set_xlim(df["year"].min(), df["year"].max())
ax.set_xticks(sorted(df["year"].unique()))
ax.grid(True, alpha=0.4)
ax.legend()
plt.tight_layout()
plt.show()
"""
    )
with col_chart:

    def plot_with_loop():
        fig, ax = plt.subplots(figsize=(6, 4))
        lines = []
        for name, g in df.groupby("country"):
            g = g.sort_values("year")
            (line,) = ax.plot(g["year"], g["growth_pct"], marker="o", label=name)
            lines.append((name, g.iloc[-1]["year"], g.iloc[-1]["growth_pct"], line))

        # --- Axes + scales ---
        # ax.set_title("Population Growth over Time TEST")  # remove external title
        ax.set_xlabel("Year")
        # ax.set_ylabel("Percent Change to Base Year")      # replace with in-chart label
        ax.set_xlim(df["year"].min(), df["year"].max() + 15)
        ax.set_ylim(0, df["growth_pct"].max() + 10)
        ax.set_xticks(sorted(df["year"].unique())[::2])
        yticks = np.linspace(df["growth_pct"].min(), df["growth_pct"].max(), 3)
        ax.set_yticks(np.round(yticks / 50) * 50)
        ax.grid(False)

        # --- Keep only x/y axes (hide the rest) ---
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)

        # --- Add end labels (same color), with right margin ---
        ax.margins(x=0.15)
        x_off = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
        for name, x_last, y_last, line in lines:
            ax.text(
                x_last + x_off,
                y_last,
                name,
                va="center",
                color=line.get_color(),
                fontsize=9,
                clip_on=False,
            )

        # --- In-chart y-title (concise + descriptive) ---
        y_title = "Population growth vs base year (%)"
        ax.text(
            0.02,
            0.98,
            y_title,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=11,
            fontweight="bold",
        )

        plt.tight_layout()
        return fig

    st.pyplot(plot_with_loop(), width="content")


col_code, col_chart = chart_cols()


with col_code:

    st.code(
        """
    def plot_with_shade(
        df,
        countries_keep,
        a="United States",
        b="China",
        title="Shaded Difference: US vs China",
    ):
        '''
        Plot growth_pct for two countries with a shaded band between them.
        Returns a matplotlib.figure.Figure (or None if countries not available).
        '''
        wide = (
            df.loc[
                df["country"].isin(countries_keep), ["year", "country", "growth_pct"]
            ]
            .pivot(index="year", columns="country", values="growth_pct")
            .sort_index()
        )

        # Both series must exist
        if not {a, b}.issubset(wide.columns):
            return None

        # Drop rows where either is missing so fill_between works cleanly
        xy = wide[[a, b]].dropna()
        if xy.empty:
            return None

        x = xy.index.to_numpy()
        ya = xy[a].to_numpy()
        yb = xy[b].to_numpy()

        fig, ax = plt.subplots()
        ax.plot(x, ya, marker="o", label=a)
        ax.plot(x, yb, marker="o", label=b)
        ax.fill_between(x, ya, yb, alpha=0.25)

        ax.set_title(title if title else f"Shaded Difference: {a} vs {b}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percent Change to Base Year")
        ax.grid(True, alpha=0.4)
        ax.legend()
        fig.tight_layout()

        return fig

    fig = plot_with_shade(df, countries_keep=["United States", "China", "Switzerland"])

    if fig is not None:
        st.pyplot(fig, width="content")
    else:
        st.info("Select both United States and China to show the shaded comparison.")
    """
    )

with col_chart:

    def plot_with_shade(
        df,
        countries_keep,
        a="United States",
        b="China",
        title="Shaded Difference: US vs China",
    ):
        """
        Plot growth_pct for two countries with a shaded band between them.
        Returns a matplotlib.figure.Figure (or None if countries not available).
        """
        wide = (
            df.loc[
                df["country"].isin(countries_keep), ["year", "country", "growth_pct"]
            ]
            .pivot(index="year", columns="country", values="growth_pct")
            .sort_index()
        )

        # Both series must exist
        if not {a, b}.issubset(wide.columns):
            return None

        # Drop rows where either is missing so fill_between works cleanly
        xy = wide[[a, b]].dropna()
        if xy.empty:
            return None

        x = xy.index.to_numpy()
        ya = xy[a].to_numpy()
        yb = xy[b].to_numpy()

        fig, ax = plt.subplots()
        ax.plot(x, ya, marker="o", label=a)
        ax.plot(x, yb, marker="o", label=b)
        ax.fill_between(x, ya, yb, alpha=0.25)

        ax.set_title(title if title else f"Shaded Difference: {a} vs {b}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percent Change to Base Year")
        ax.grid(True, alpha=0.4)
        ax.legend()
        fig.tight_layout()

        return fig

    fig = plot_with_shade(df, countries_keep=["United States", "China", "Switzerland"])

    if fig is not None:
        st.pyplot(fig, width="content")
    else:
        st.info("Select both United States and China to show the shaded comparison.")

st.subheader("Same chart with small multiples")

col_code, col_chart = chart_cols()

with col_code:
    st.code(
        """
countries_order = countries_keep  # or df["country"].unique().tolist()
    n = len(countries_order)

    def plot_small_multiples():
        fig, axes = plt.subplots(1, n, sharey=True, figsize=(4 * n, 3))

        if n == 1:
            axes = [axes]  # normalize to iterable

        for ax, name in zip(axes, countries_order):
            g = df[df["country"] == name]
            ax.plot(g["year"], g["growth_pct"], marker="o", label=name)
            ax.set_title(name)
            ax.set_xlabel("Year")
            ax.grid(True, alpha=0.4)
            # Only the first subplot gets the shared y-label
            if ax is axes[0]:
                ax.set_ylabel("Percent Change to Base Year")
            # Consistent x ticks across panels
            ax.set_xticks(sorted(df["year"].unique()))

        fig.suptitle("Population Growth over Time")
        plt.tight_layout()
        return fig

    st.pyplot(plot_small_multiples(), width="content")
"""
    )


with col_chart:
    countries_order = countries_keep  # or df["country"].unique().tolist()
    n = len(countries_order)

    def plot_small_multiples():
        fig, axes = plt.subplots(1, n, sharey=True, figsize=(4 * n, 3))

        if n == 1:
            axes = [axes]  # normalize to iterable

        for ax, name in zip(axes, countries_order):
            g = df[df["country"] == name]
            ax.plot(g["year"], g["growth_pct"], marker="o", label=name)
            ax.set_title(name)
            ax.set_xlabel("Year")
            ax.grid(True, alpha=0.4)
            # Only the first subplot gets the shared y-label
            if ax is axes[0]:
                ax.set_ylabel("Percent Change to Base Year")
            # Consistent x ticks across panels
            ax.set_xticks(sorted(df["year"].unique()))

        fig.suptitle("Population Growth over Time")
        plt.tight_layout()
        return fig

    st.pyplot(plot_small_multiples(), width="content")

st.header("Cool built-in styles in matplotlib")

from contextlib import nullcontext

wide = df.pivot(index="year", columns="country", values="growth_pct").sort_index()

# Compare up to two of the selected countries.
style_countries = wide.columns.tolist()[:2]

# keep only years where both exist
xy = wide[style_countries].dropna()
x = xy.index.to_numpy()
ys = [xy[country].to_numpy() for country in style_countries]

# optional: nicer title/labels
title = " vs ".join(style_countries)
xlabel = "Year"
ylabel = "Percent change vs base"


def line_chart(x, ys, labels, title, xlabel, ylabel, use_xkcd=False, style=None):
    """
    Returns a matplotlib Figure.
    - use_xkcd: apply XKCD style (scoped)
    - style: any Matplotlib style name (e.g., 'fivethirtyeight', 'ggplot', 'Solarize_Light2')
    If both are provided, `style` wins (they shouldn't be combined).
    """
    # choose a scoped style context
    if style:
        ctx = plt.style.context(style)
    elif use_xkcd:
        ctx = plt.xkcd()
    else:
        ctx = nullcontext()

    with ctx:
        fig, ax = plt.subplots(figsize=(7, 4))
        for y, label in zip(ys, labels):
            ax.plot(x, y, marker="o", label=label)
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        ax.grid(True, alpha=0.4)
        ax.legend(frameon=False)
        fig.tight_layout()
    return fig


# 0) xkcd

fig = line_chart(x, ys, style_countries, title, "Year", "% vs base", use_xkcd=True)

st.pyplot(fig, width="content")

# 1) FiveThirtyEight
fig1 = line_chart(
    x, ys, style_countries, title, "Year", "% vs base", style="fivethirtyeight"
)

# 2) ggplot
fig2 = line_chart(x, ys, style_countries, title, "Year", "% vs base", style="ggplot")

# 3) Solarized Light
fig3 = line_chart(
    x, ys, style_countries, title, "Year", "% vs base", style="Solarize_Light2"
)

col1, col2, col3 = st.columns(3)
col1.pyplot(fig1, width="content")
col2.pyplot(fig2, width="content")
col3.pyplot(fig3, width="content")


st.divider()


st.header("Examples with plotly")

import plotly.io as pio
import src.scripts.plot_themes as thm
import src.scripts.utils as utl
import statsmodels.api as sm
import streamlit as st
from matplotlib import pyplot as plt
import plotly.graph_objs as go
from matplotlib.ticker import FuncFormatter
from plotly.subplots import make_subplots
from scipy.stats import t

### PAGE START ###
# Dashboard header

@st.fragment
def cake_eating_fragment():
    st.title("Cake Eating Problem (Optimal Consumption)")
    st.header("Finite Time Horizong")

    (
        col1,
        col2,
        _,
    ) = st.columns((1, 1, 2))

    with col1:
        st.markdown(
            r"""Suppose you get a cake of size $W$ and you want to eat it over ($T+1$) day.
        You want to be smart about it and ask yourself: what is the **optimal consumption** each day to maximize your happiness derived from eating the entire cake?
        We formulate this problem as follows:<br>
        """,
            unsafe_allow_html=True,
        )

        st.latex(
            r""" \max_{\{c_t\}_{t=0}^T} \sum_{t=0}^{T} \beta^t u(c_t) \\
        \\[5pt]
        \text{s.t.} \sum_{t=0}^{T} c_t \leq W\\
        \\[5pt]
            w_{t+1} = w_t - c_t,\; c_t\geq 0 \; \forall t\\
                """
        )

    with col2:
        st.markdown(
            r"""Given a specific utility function, an analytical solution can be found by setting $c_T = w_T$, using Euler equation from FOC, and solving backwards.
        The solution is given below with $u(c) = \text{ln}(c)$. If utility function is CRRA, then $\beta$ has to be replaced with $\beta^{\frac{1}{\gamma}}$.
        """,
            unsafe_allow_html=True,
        )
        st.latex(
            r""" c_0 = \dfrac{W}{\sum_{t=0}^{T} \beta^t} = W \dfrac{1-\beta}{1-\beta^{T+1}} \\
        \\[5pt]
                c_t = \beta c_{t-1} = \beta^t c_0 \; \forall t \\"""
        )

        st.markdown(
            r"""
        Let's see how you should optimally eat the cake, given different $\beta$, $u(c)$, and $T$. Cake size is fixed to $W=100$.
    
        """,
            unsafe_allow_html=True,
        )

    input_col, _, chart_col = st.columns((0.5, 0.05, 1))

    ### WIDGETS
    ### Input widgets
    with input_col:
        beta = st.number_input(
            r"Select $\beta$ (patience factor):",
            min_value=0.0,
            max_value=1.0,
            value=0.95,
            step=0.01,
        )
        T = st.number_input(
            r"Select $T$ (last period):",
            min_value=2,
            max_value=100,
            value=15,
            step=1,
        )
        utility_function = st.selectbox(r"Select utility function:", ["Log", "CRRA"])

        if utility_function == "Log":
            st.latex(r"u(c) = \text{ln}(c)")

        if utility_function == "CRRA":
            gamma = st.number_input(
                r"Select $\gamma$ (preference for smoothing):",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1,
            )
            st.latex(
                r"""u(c) = \begin{cases}
    \frac{c^{1-\gamma}}{1-\gamma} & \gamma > 0, \gamma \neq 1 \\
    \ln(c) & \gamma = 1
    \end{cases}"""
            )
        else:
            gamma = None


    ### DEFINE CAKE EATING SOLVER
    def solve_cake_finite(W, T, beta, utility_fn, gamma=None):
        V = np.zeros(T + 2)
        consumption = np.zeros(
            T + 2
        )  # add additional period to show when consumption drops to 0
        remaining_cake = np.zeros(T + 2)  # cake at the start of each period

        # using analytical solution
        if utility_fn == "Log":
            disc = beta

        elif utility_fn == "CRRA":
            if gamma == 1 or gamma == 0:  # By definition gamma > 0 and gamma != 1
                disc = beta
            else:
                disc = beta ** (1 / gamma)

        if beta < 1:
            numerator = W
            denominator = (1 - disc ** (T + 1)) / (1 - disc)
            c_0 = numerator / denominator
        else:
            c_0 = W / (T + 1)

        consumption[0] = c_0
        remaining_cake[0] = W  # initial cake size
        remaining_cake[1] = W - consumption[0]

        for t in range(1, T + 2):  # 1 through T+2 periods, but T+2 should be 0
            if t <= T:
                consumption[t] = disc * consumption[t - 1]
                remaining_cake[t + 1] = remaining_cake[t] - consumption[t]
            elif t == T + 1:
                # remaining cake should at T+1 should be 0, so cons also 0.
                consumption[t] = 0
                if -0.001 < remaining_cake[t] < 0.001:
                    remaining_cake[t] = 0
                else:
                    # Display an error message if final remaining cake calculation out of expected range.
                    st.error(
                        "Error: Final remaining cake calculation out of expected range."
                    )

        return consumption, remaining_cake


    consumption, remaining_cake = solve_cake_finite(100, T, beta, utility_function, gamma)


    pio.templates.default = "my_streamlit"


    def plot_consumption_plotly(
        consumption, remaining_cake, T, beta, utility_fn, gamma=None
    ):
        # Create subplots and specify we want two y-axes
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add consumption series
        fig.add_trace(
            go.Scatter(
                x=list(range(T + 2)),
                y=consumption,
                mode="lines",
                name="Consumption",
                line=dict(color="green", width=2),
                hovertemplate="t = %{x}<br>c<sub>t</sub> = %{y:.1f}<extra></extra>",
                showlegend=False,
            ),
            secondary_y=False,
        )

        # Add remaining cake series
        fig.add_trace(
            go.Scatter(
                x=list(range(T + 2)),
                y=remaining_cake,
                mode="lines",
                name="Remaining Cake",
                line=dict(color="blue", width=2, dash="dash"),
                hovertemplate="t = %{x}<br>w<sub>t</sub> = %{y:.1f}<extra></extra>",
                showlegend=False,
            ),
            secondary_y=True,
        )

        # Add vertical line and text for T
        fig.add_vline(x=T, line=dict(color="grey", dash="dash", width=2))
        fig.add_annotation(
            x=T * 1.03,
            y=consumption[0],
            text=f"t={T}",
            showarrow=False,
            xshift=10,
            font=dict(color="grey", size=15),
        )

        # x axis limit
        if T < 10:
            x_ub = T + 1.2
        else:
            x_ub = T * 1.12

        # Add horizontal line shape
        fig.add_shape(
            type="line",
            x0=-0.5,  # Start line at the beginning of the x-axis range
            y0=1.1 * max(consumption),
            x1=x_ub,  # End line at the end of the x-axis range
            y1=1.1 * max(consumption),
            line=dict(color="black", width=2),
            xref="x",  # Refer to the x-axis
            yref="y",  # Use "y2" if the line should refer to the right y-axis
        )

        # Layout settings - in addition to my_streamlit default theme from custom thm module
        fig.update_layout(
            width=600,  # Width in pixels
            height=400,
            margin=dict(autoexpand=True, l=30, r=40, t=30, b=40, pad=0),
            font=dict(family="Sans-Serif"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            title=dict(
                text=f"<b>Cake Eating with {utility_fn} Utility</b>",
                font=dict(size=20),
                x=0.5,
                xanchor="center",
                xref="paper",
                y=0.98,
                yanchor="top",
                yref="container",
            ),
            hovermode="closest",
            hoverlabel=dict(
                font=dict(family="Sans-Serif", color="black"),
                bgcolor="rgb(255, 255, 255)",  # rgb(0, 0, 0, 0)
                bordercolor="black",
                namelength=-1,
            ),
            xaxis=dict(
                range=[-0.5, x_ub],
                showgrid=False,
                zeroline=False,
                autorange=False,
                title=dict(text="<b>period t</b>", font=dict(size=16)),
            ),
            yaxis=dict(
                range=[0, 1.1 * max(consumption)],
                autorange=False,
                showgrid=False,
                title=dict(
                    text="<b>Consumption (cₜ)</b>",
                    font=dict(size=16, color="green"),
                ),
            ),
            yaxis2=dict(
                range=[0, 1.1 * max(remaining_cake)],
                autorange=False,
                showgrid=False,
                title=dict(
                    text="<b>Remaining Cake (wₜ)</b>",
                    font=dict(size=16, color="blue"),
                ),
            ),
        )

        return fig


    chart_fig = plot_consumption_plotly(
        consumption, remaining_cake, T, beta, utility_function, gamma
    )

    # Plot chart
    with chart_col:
        st.plotly_chart(chart_fig, theme=None, use_container_width=True)


    ### PREPARE DATA FOR TABLE
    # Convert data to DataFrame
    data_dict = {"t": range(T + 2), "c_t": consumption, "w_t": remaining_cake}
    data_df = pd.DataFrame(data_dict)


    # Define a function to display the table
    def display_table(df, N=5):
        col_config = {
            "c_t": st.column_config.NumberColumn(format="%.2f"),
            "w_t": st.column_config.NumberColumn(format="%.2f"),
        }

        if T < 10:
            st.dataframe(df, hide_index=True, column_config=col_config)
        else:
            show_all = st.checkbox("Show all periods")
            if show_all:
                st.dataframe(df, hide_index=True, column_config=col_config)
            else:
                col_t1, col_t2 = st.columns((1, 1))
                with col_t1:
                    st.markdown("First 5 periods:")
                    st.dataframe(df.head(N), hide_index=True, column_config=col_config)
                with col_t2:
                    st.markdown("Last 5 periods:")
                    st.dataframe(df.tail(N), hide_index=True, column_config=col_config)


    pie_col, table_col = st.columns((1, 0.7))


    ### BUILD ANIMATED PIE CHART
    def pie_chart_animated(consumption, remaining_cake, T):
        fig = go.Figure()

        def create_title(t_title):
            font_settings = dict(family="Sans-Serif", size=16)

            if t_title <= T:
                rem_cake_label = remaining_cake[t_title + 1]
            else:
                rem_cake_label = 0

            title_dict = dict(
                text=f"<b>t = {t_title}<br>"
                + f"Σc<sub>t</sub> = {sum(consumption[: t_title + 1]):.2f},"
                + f"w<sub>t+1</sub> = {rem_cake_label:.2f}</b>",
                y=0.9,
                x=0.5,
                xanchor="center",
                yanchor="top",
                font=font_settings,
            )

            return title_dict

        # Make data
        def make_pie_data(consumption, remaining_cake, T, t):
            values_eaten = list(consumption[: t + 1])

            # filter to not show values for slices below 4
            labels_eaten = [
                f"c_{i}<br>{consumption[i]:.1f}" if consumption[i] > 4 else f"c_{i}"
                for i in range(t + 1)
            ]
            # filter to not show any label for slices below 1
            # empty space doesn't work, since plotly treats identical labels as a single trace
            # create labels with invisible character * slice number to keep them unique but invisible
            invisible_char = "\u200b"

            labels_eaten = [
                labels_eaten[i] if consumption[i] > 1 else "\u200b" * i
                for i in range(t + 1)
            ]

            hovertext_eaten = [f"c_{i} = {consumption[i]:.1f}" for i in range(t + 1)]

            if t < T:
                labels = labels_eaten + [f"w_{t+1}<br>{remaining_cake[t+1]:.1f}"]
                value_remaining = [remaining_cake[t + 1]]
                hovertext = hovertext_eaten + [f"w_{t+1} = {remaining_cake[t+1]:.1f}"]
            else:
                labels = labels_eaten
                hovertext = hovertext_eaten
                value_remaining = []

            values = values_eaten + value_remaining
            pull_values = [0.05] * len(values_eaten) + [0] * len(value_remaining)
            colors = ["green"] * len(values_eaten) + ["blue"] * len(value_remaining)

            return dict(
                labels=labels,
                values=values,
                pull=pull_values,
                marker=dict(colors=colors),
                hovertext=hovertext,  # Set custom hovertext for each slice
                hoverinfo="text",  # Ensure that the custom hovertext is used
                textinfo="label",
                textposition="inside",
            )

        # Make first frame
        fig.add_trace(go.Pie(**make_pie_data(consumption, remaining_cake, T, t=0)))

        fig.update_traces(
            textinfo="label",
            # texttemplate="%{label}<br>%{value:.1f}", # this is helpful without conditional labels
            hoverinfo="label",
            direction="clockwise",
            sort=False,
            showlegend=False,
        )

        fig.update_layout(
            margin=dict(t=80, l=0, b=0, r=0),
            title=create_title(0),
            font=dict(family="Sans-Serif"),
        )

        # Define slider properties
        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Time:",
                "visible": False,  # Don't show current value to save space
                "xanchor": "right",
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 50, "t": 50},
            "len": 0.9,
            "x": 0.0,
            "y": 0.0,  # Adjusted slider vertical position
            "pad": {"b": 20, "t": 0},  # Reduced top padding
            "steps": [],
        }

        # Make frames for animation and slider
        frames = []

        for t_frame in range(T + 1):
            frame = go.Frame(
                data=[go.Pie(**make_pie_data(consumption, remaining_cake, T, t_frame))],
                name=str(t_frame),
                layout=go.Layout(title=create_title(t_frame)),
            )

            frames.append(frame)

            slider_step = {
                "args": [
                    [str(t_frame)],
                    {
                        "frame": {"duration": 300, "redraw": True},
                        "mode": "immediate",
                        "transition": {"duration": 300},
                    },
                ],
                "label": "" if t_frame % 3 != 0 else str(t_frame),
                "method": "animate",
            }

            sliders_dict["steps"].append(slider_step)

        fig["frames"] = frames
        fig["layout"]["sliders"] = [sliders_dict]

        # Define animation button properties
        play_button = {
            "args": [
                [str(t) for t in range(0, T + 1)],
                {
                    "frame": {"duration": 500, "redraw": True},
                    "fromcurrent": True,
                    "transition": {
                        "duration": 300,
                        "easing": "quadratic-in-out",
                    },
                },
            ],
            "label": "Play",
            "method": "animate",
        }

        pause_button = {
            "args": [
                [None],
                {
                    "frame": {"duration": 0, "redraw": False},
                    "mode": "immediate",
                    "transition": {"duration": 0},
                },
            ],
            "label": "Pause",
            "method": "animate",
        }

        # Define reset button properties
        reset_button = {
            "args": [
                [str(0)],
                {
                    "frame": {"duration": 0, "redraw": True},
                    "mode": "immediate",
                    "transition": {"duration": 0},
                },
            ],
            "label": "Reset to 0",
            "method": "animate",
        }

        fig["layout"]["updatemenus"] = [
            {
                "buttons": [play_button, pause_button],
                "direction": "left",
                "pad": {"r": 20, "t": 0, "b": 10},
                "showactive": False,
                "type": "buttons",
                "x": 0.0,
                "xanchor": "left",
                "y": 1.1,
                "yanchor": "bottom",
            },
            {
                "buttons": [reset_button],
                "direction": "left",
                "pad": {"r": 20, "t": 25},
                "showactive": False,
                "type": "buttons",
                "x": 0.0,
                "xanchor": "left",
                "y": 1.0,
                "yanchor": "bottom",
            },
        ]

        return fig


    # PLOT ANIMATED PIE CHART
    with pie_col:
        st.plotly_chart(
            pie_chart_animated(consumption, remaining_cake, T),
            use_container_width=True,
        )


    with table_col:
        # display data table
        st.markdown("#### Chart data")
        display_table(data_df)

    s0, c02, s1 = utl.wide_col()


cake_eating_fragment()
