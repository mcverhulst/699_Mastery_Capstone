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
# data = pd.read_csv("../data/edu_wages.csv")
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
st.altair_chart(c, use_container_width=True)


# TEST PYRAMID PLOT
color_scale = alt.Scale(domain=["total men", "total women"], range=["#1f77b4", "#e377c2"])
base = alt.Chart(data_filtered).mark_bar().encode().properties(width=250)

left = base.transform_filter(
    alt.datum.group == 'total men'
).encode(
    alt.X('sum(value):Q', title="wages", sort="descending", scale=alt.Scale(domain=[0, 1200])),
    alt.Y('year:N', axis=None, sort='descending'),
    alt.Color('group:O', scale=color_scale)
)

right = base.transform_filter(
    alt.datum.group == 'total women'
).encode(
    alt.X('sum(value):Q', title="wages", sort="ascending", scale=alt.Scale(domain=[0, 1200])),
    alt.Y('year:N', axis=None, sort='descending'),
    alt.Color('group:O', scale=color_scale)
)

middle = base.encode(
    alt.Y('year:N', axis=None, sort='descending'),
    alt.Text('year'),
).mark_text().properties(width=35)

st.write("## Testing...")
ch = alt.hconcat(left, middle, right, spacing=5)
st.altair_chart(ch, theme="streamlit", use_container_width=True)
# ch


st.write("## Testing2...")
pink_blue = alt.Scale(domain=('Male', 'Female'),
                      range=["#1f77b4", "#e377c2"])

slider = alt.binding_range(min=1995, max=2020, step=1)
select_year = alt.selection_single(name='Year', fields=['year'],
                                   bind=slider)

bar2 = alt.Chart(data_filtered).mark_bar().encode(
    x=alt.X('group:N', title=None),
    y=alt.Y('value:Q', title='Wages', scale=alt.Scale(domain=(0, 1200))),
    color=alt.Color('group:N', scale=pink_blue),
    column='year:N'
).properties(
    width=20
).add_selection(
    select_year
).transform_calculate(
    "group", alt.expr.if_(alt.datum.group == "total men", "Male", "Female")
).transform_filter(
    select_year
).configure_facet(
    spacing=8
)
st.altair_chart(bar2, theme="streamlit", use_container_width=False)