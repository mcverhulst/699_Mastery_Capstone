import streamlit as st
import altair as alt
import bokeh as b
import pandas as pd
from utils.util_funcs import load_data

st.set_page_config(page_title="Earning Potential", page_icon="💰")

st.markdown("# Higher Education Degrees and Earning Potential")
st.sidebar.header("Earning Potential")
st.write(
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum."""
)

# READ IN AND MELT DATASET
data = load_data("edu_wages.csv")
# data = pd.read_csv("../data/edu_wages.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

data = pd.melt(data, id_vars="group")
data = data.rename(columns={"variable": "year"})
data_only = data[:2340]


# FILTER DATA BY RACE + BACHELOR'S DEGREE
race_bach = data_only[
    data_only["group"].isin(
        [
            "Asian + Bachelors Degree",
            "Black + Bachelors Degree",
            "Hispanic or Latino + Bachelors Degree",
            "White + Bachelors Degree",
        ]
    )
]
# race_bach

# LINE CHART WITH HOVER EFFECT
# # Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["year"], empty="none")

# The basic line
line = (
    alt.Chart()
    .mark_line(interpolate="basis")
    .encode(
        alt.X("year:T", axis=alt.Axis(title="")),
        alt.Y("value:Q", axis=alt.Axis(title="", format="$f")),
        color="group:N",
    )
)

# Transparent selectors across the chart. This is what tells us
# the x-value of the cursor
selectors = (
    alt.Chart()
    .mark_point()
    .encode(
        x="year:T",
        opacity=alt.value(0),
    )
    .add_selection(nearest)
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

# Draw text labels near the points, and highlight based on selection
text = line.mark_text(align="left", dx=5, dy=-5).encode(
    text=alt.condition(nearest, "value:Q", alt.value(" "))
)

# Draw a rule at the location of the selection
rules = (
    alt.Chart()
    .mark_rule(color="gray")
    .encode(
        x="year:T",
    )
    .transform_filter(nearest)
)

# Put the five layers into a chart and bind the data
raceBachChart = alt.layer(
    line,
    selectors,
    points,
    rules,
    text,
    data=race_bach,
    width=600,
    height=300,
    title="Weekly Wages by Race with a Bachelor's Degree",
)

st.altair_chart(raceBachChart)
