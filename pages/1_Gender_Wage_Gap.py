import streamlit as st
import altair as alt

import pandas as pd
import os
from utils.util_funcs import load_data


st.set_page_config(page_title="Gender Wage Gap", page_icon="⚖️")

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


# READ IN AND MELT DATASET
data = load_data("edu_wages.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

data = pd.melt(data, id_vars="group")
data = data.rename(columns={"variable": "year"})
data_only = data[:2340]
# data_only

# FILTER TO SUBSET OF DATA
data_filtered = data_only[(data_only["group"] == "total men") | (data_only["group"] == "total women")]
data_filtered

# TEST BAR PLOT
# inspiration: https://altair-viz.github.io/gallery/us_population_pyramid_over_time.html
c = (
    alt.Chart(data_filtered)
    .mark_bar()
    .encode(x="year:N", y=alt.Y("value:Q"), color="group:N", tooltip="value")
)

st.write("## Not a good chart, just a test chart")
st.altair_chart(c, theme="streamlit", use_container_width=True)

# TEST PYRAMID PLOT
slider = alt.binding_range(name="year:", min=1995, max=2020)
selector = alt.selection_single(name="Year", fields=["year"], bind=slider, init={"year": 2020})

base = alt.Chart(data_filtered).add_selection(selector).transform_filter(selector).properties(width=250)


color_scale = alt.Scale(domain=["total men", "total women"], range=["#1f77b4", "#e377c2"])

left = (
    base.transform_filter(alt.datum.group == "total women")
    .encode(
        alt.Y("year:N"),
        alt.X("sum(value):Q").title("wages").sort("descending"),
        alt.Color("group:N").scale(color_scale).legend(None),
    )
    .mark_bar()
    .properties(title="Total Women")
)


right = (
    base.transform_filter(alt.datum.group == "total men")
    .encode(
        alt.Y("year:N"),
        alt.X("sum(value):Q").title("wages"),
        alt.Color("group:N").scale(color_scale).legend(None),
    )
    .mark_bar()
    .properties(title="Total Men")
)

# alt.concat(left, right, spacing=5)
st.write("## Testing...")
ch = left + right
st.altair_chart(ch, theme="streamlit", use_container_width=True)
