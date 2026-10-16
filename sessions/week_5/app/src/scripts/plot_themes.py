import matplotlib.cm as cm
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


# Common for all charts
my_font = "Sans-Serif"
my_font_color = "black"


# Plotly colors
cols_g10 = px.colors.qualitative.G10
cols_set1 = px.colors.qualitative.Set1

# Given the order of colors in cols_set1_plt
color_names = [
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "yellow",
    "brown",
    "pink",
    "grey",
]

# Create dictionary using a dictionary comprehension
cols_set1_px = {color_names[i]: cols_set1[i] for i in range(len(color_names))}

# Matplolib colors
cols_set1_plt = cm.Set1.colors
set1_red = cols_set1_plt[0]
set1_blue = cols_set1_plt[1]
set1_green = cols_set1_plt[2]
set1_purple = cols_set1_plt[3]
set1_orange = cols_set1_plt[4]
set1_yellow = cols_set1_plt[5]
set1_brown = cols_set1_plt[6]
set1_pink = cols_set1_plt[7]
set1_grey = cols_set1_plt[8]


##### MATPLOTLIB for THEORY
# src/styles/mpl_theme.py
import matplotlib as mpl
import matplotlib.cm as cm

def mpl_theme_theory():
    """Apply custom Matplotlib theme globally."""
    mpl.rcParams.update({
        # Fonts
        "font.family": "sans-serif",
        "font.sans-serif": ["Sans-Serif"],  # match your style
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "legend.fontsize": 11,
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,

        # Axes style
        "axes.edgecolor": "black",
        "axes.linewidth": 1.5,
        "axes.grid": False,
        "axes.grid.which": "both",
        "axes.titleweight": "bold",
        "axes.labelweight": "normal",

        # Ticks
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 5,
        "ytick.major.size": 5,
        "xtick.color": "black",
        "ytick.color": "black",

        # Legend
        "legend.frameon": True,
        "legend.framealpha": 1.0,
        "legend.edgecolor": "black",

        # Figure
        "figure.figsize": (6, 4),
        "figure.dpi": 100,
        "figure.facecolor": "white",

        # Lines and colors
        "lines.linewidth": 2.5,
        "axes.prop_cycle": mpl.cycler(color=cm.Set1.colors),

        # Savefig
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def use_mpl_theme(theme_dict):
    """Decorator to apply a Matplotlib theme only inside a function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            with mpl.rc_context(theme_dict):
                return func(*args, **kwargs)
        return wrapper
    return decorator

mpl_theme_theory_dict = {
    # Fonts
    "font.family": "sans-serif",
    "font.sans-serif": ["Sans-Serif"],  # match your style
    "font.size": 12,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,

    # Axes style
    "axes.edgecolor": "black",
    "axes.linewidth": 1.5,
    "axes.grid": False,
    "axes.grid.which": "both",
    "axes.titleweight": "bold",
    "axes.labelweight": "normal",

    # Ticks
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.color": "black",
    "ytick.color": "black",

    # Legend
    "legend.loc": "upper right",  # default location
    "legend.handlelength": 2.0,   # handle length in legend
    "legend.handletextpad": 0.5,  # space between handle and text
    "legend.borderaxespad": 0.5,  # space between legend and axes
    "legend.borderpad": 0.4,      # space inside legend box
    "legend.labelspacing": 0.5,   # vertical space between items
    "legend.fontsize": "small",

    # Figure
    "figure.figsize": (7, 4),
    "figure.dpi": 600,
    "figure.facecolor": "white",

    # Lines and colors
    "lines.linewidth": 2.5,
    "axes.prop_cycle": mpl.cycler(color=cm.Set1.colors),

    # Savefig
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}


# Sample template from plotly documentation
# https://plotly.com/python/templates/
pio.templates["draft"] = go.layout.Template(
    layout_annotations=[
        dict(
            name="draft watermark",
            text="DRAFT",
            textangle=-30,
            opacity=0.1,
            font=dict(color="black", size=100),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    ]
)

# Personal template for streamlit charts
pio.templates["my_streamlit"] = go.layout.Template(
    layout=dict(
        # Font options - streamlit overwrites those based on config.toml file
        font={
            "family": my_font,
            "size": 12,
            "color": my_font_color,
        },
        # Title options
        title=dict(
            # text="",
            font={
                "family": my_font,
                "size": 25,
                "color": my_font_color,
            },
            x=0.00,
            xanchor="left",
            xref="paper",
            y=0.98,
            yanchor="top",
            yref="container",
        ),
        # Legend options
        showlegend=True,
        legend=dict(
            orientation="h",
            x=-0.01,
            xanchor="left",
            y=1.00,
            yanchor="bottom",
            # bgcolor="red",
            # bordercolor="#333",
            # borderwidth=2,
            entrywidth=0,
            entrywidthmode="pixels",
            font={
                "family": my_font,
                "size": 12,
                "color": my_font_color,
            },
            itemclick="toggle",
            # tracegroupgap=10,
            traceorder="normal",
            valign="middle",
        ),
        # Paper options
        margin=dict(autoexpand=True, l=70, r=40, t=25, b=40, pad=0),
        width=500,
        height=400,
        autosize=False,
        paper_bgcolor="white",  # doesn't work with streamlit
        plot_bgcolor="white",  # doesn't work with streamlit
        separators=".,",
        # Chart interaction options
        dragmode=False,  # zoom
        # Hover options
        hovermode="closest",
        hoverlabel=dict(
            font=dict(family=my_font, color=my_font_color),
            # bgcolor="rgb(255, 255, 255)",  # rgb(0, 0, 0, 0)
            bordercolor="black",
            namelength=-1,
        ),
        # Gride options
        grid=dict(columns=2, rows=2, domain=dict(x=[0, 1], y=[0, 1])),
        # Axes options
        xaxis=dict(
            automargin=False,
            autorange=False,
            categoryorder="sum descending",
            color="black",
            gridcolor="white",
            showline=True,
            linecolor="black",
            linewidth=2,
            ticks="outside",
            tickcolor="black",
            tickformat="%b %Y",
            title=dict(standoff=0, text=""),
            zerolinecolor="black",
            zerolinewidth=2,
            layer="above traces",
            showticklabels=True,
            showspikes=True,
            spikethickness=1,
        ),
        yaxis=dict(
            automargin="left+right",
            autorange=False,
            categoryorder="sum descending",
            color="black",
            gridcolor="lightgrey",
            gridwidth=0.5,
            showline=True,
            linecolor="black",
            linewidth=2,
            # ticks="",
            ticks="outside",
            # tickformat="$,.0f",
            title=dict(
                standoff=0.05,
                text="",
                font=dict(family=my_font, color=my_font_color),
            ),
            separatethousands=True,
            zerolinecolor="black",
            zerolinewidth=2,
            layer="above traces",
            rangemode="tozero",
        ),
        colorway=px.colors.qualitative.G10,
    ),
    data=dict(
        scatter=[
            go.Scatter(
                line=dict(width=4.5),
                marker=dict(symbol="circle", size=10),
                mode="lines",
                connectgaps=False,
                # hovertemplate="%{fullData.name}<br>%{x}:%{y}<extra></extra>",
                # hovertemplate="%{x}<br>%{y}<extra></extra>",
                # xhoverformat="%b %Y",
                # yhoverformat="$,.0f",
            )
        ]
    ),
)

"""
Color templates
https://plotly.com/python/discrete-color/

Personal favorites

px.colors.qualitative.G10
['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099',
    '#0099C6', '#DD4477', '#66AA00', '#B82E2E', '#316395']

px.colors.qualitative.Set1
px.colors.qualitative.D3
"""
