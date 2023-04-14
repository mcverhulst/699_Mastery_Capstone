import streamlit as st
import altair as alt

import pandas as pd
import os
from utils.util_funcs import load_data

st.set_page_config(page_title="Gender Wage Gap",
                   page_icon="⚖️",
                   layout="wide",
                   initial_sidebar_state="collapsed",
)

### IMPORT FILTERED DATA
from preprocessing.gender_ratios import *

st.markdown("# Education and the gender wage gap")
st.sidebar.header("Gender Wage Gap")
st.write(
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum."""
)

# FILTER TO SUBSET OF DATA
data_filtered = data_only[(data_only["group"] == "total men") | (data_only["group"] == "total women")]

# TEST BAR PLOT
# inspiration: https://altair-viz.github.io/gallery/us_population_pyramid_over_time.html
# c = (
#     alt.Chart(data_filtered)
#     .mark_bar()
#     .encode(x="year:N", y=alt.Y("value:Q"), color="group:N", tooltip="value")
# )

# st.write("## Not a good chart, just a test chart")
# st.altair_chart(c, use_container_width=True)


####################
### PYRAMID PLOT ###
####################

color_scale = alt.Scale(domain=["total men", "total women"], range=["#1f77b4", "#e377c2"])
base = alt.Chart(ratio_df).mark_bar().encode(tooltip=["ratio"]).properties(width=250)

# LEFT CHART
left = base.encode(
    alt.X("total men:Q", title="wages", sort="descending", scale=alt.Scale(domain=[0, 1200])),
    alt.Y("year:N", axis=None, sort="descending"),
    color=alt.value("#31b0a5"),
)

# RIGHT CHART
right = base.encode(
    alt.X("total women:Q", title="wages", sort="ascending", scale=alt.Scale(domain=[0, 1200])),
    alt.Y("year:N", axis=None, sort="descending"),
    color=alt.value("#de8b33")
    # alt.Color('group:O', scale=color_scale)
)

# MIDDLE CHART
middle = (
    base.encode(
        alt.Y("year:N", axis=None, sort="descending"),
        alt.Text("year"),
    )
    .mark_text()
    .properties(width=35)
)

# CONCATING FINAL TREE DIAGRAM
ch = alt.hconcat(left, middle, right, spacing=5)

# PAY GAP RATIO CHART
line = (
    alt.Chart(ratio_df)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("ratio:Q", scale=alt.Scale(domain=(0.65, 1)), title="Female to male wage ratio"),
    )
)

# CONCATING PYRAMID AND RATIO CHARTS
combo = alt.vconcat(ch, line)
st.altair_chart(combo, theme="streamlit", use_container_width=True)

#########################
### Stacked bar chart ###
#########################

st.write("## Testing2...")
pink_blue = alt.Scale(domain=("Male", "Female"), range=["#31b0a5", "#de8b33"])  # ['#31b0a5', '#de8b33']

values = st.slider("Select a range of years", 1995, 2020, (1995, 2020))

bar2 = (
    alt.Chart(data_filtered)
    .mark_bar()
    .encode(
        x=alt.X("group:N", title=None, axis=None),
        y=alt.Y("value:Q", title="Median Weekly Pay", scale=alt.Scale(domain=(0, 1200))),
        color=alt.Color("group:N", scale=pink_blue),
        column=alt.Column(
            "year:N",
            title=None,
            header=alt.Header(labelAngle=-45, labelFontSize=13, labelOrient="bottom", labelPadding=35),
        ),
        tooltip=["group", "value", "year"],
    )
    .properties(width=25)
    .transform_filter(values[0] <= alt.datum.year)
    .transform_filter(alt.datum.year <= values[1])
    .transform_calculate("group", alt.expr.if_(alt.datum.group == "total men", "Male", "Female"))
    .configure_facet(spacing=8)
)

st.altair_chart(bar2, theme="streamlit", use_container_width=False)

#####################
### Women by race ###
#####################

cuts = ["Total women:Q", "White women:Q", "Hispanic or Lation women:Q", "Black women", "Asian women"]

title = alt.TitleParams("Median Weekly Earnings in 2022 Dollars", anchor='middle')

base = alt.Chart(male, title=title, height=600).mark_line(point=True, strokeDash=[6,1]).encode(
    x = alt.X("year:N", title="Year", axis=alt.Axis(labelAngle=-45)),
    y = alt.Y("men:Q", scale=alt.Scale(domain=(500, 1400)), title="Median Weekly Wages ($2022)"),
    color = alt.value("black"),
)#.interactive()

base_women = alt.Chart(female).mark_line(point=True).encode(
    x = alt.X("year:N", axis=alt.Axis(labelAngle=-45)),
    y = alt.Y("Total women:Q", scale=alt.Scale(domain=(500, 1400)), title=""),
    color = alt.value("blue")
)

white_women = base_women.encode(
    y = alt.Y("White women:Q"),
    color = alt.value("red")
)

his_women = base_women.encode(
    y = alt.Y("Hispanic or Latino women:Q"),
    color = alt.value("green")
)

black_women = base_women.encode(
    y = alt.Y("Black women:Q"),
    color = alt.value("orange")
)

asian_women = base_women.encode(
    y = alt.Y("Asian women:Q"),
    color = alt.value("pink")
)

races = base + base_women + white_women + his_women + black_women + asian_women

st.markdown("""### How much do women make by race?""")
st.write("""The median wage for all men is indicated by the black line...
""")
st.altair_chart(races, theme="streamlit", use_container_width=True)
