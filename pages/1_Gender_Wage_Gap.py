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
data = load_data("edu_wages_2022.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

ratio_df = data[(data.group == "total men") | (data.group == "total women")]

data = pd.melt(data, id_vars=["group"])
data = data.rename(columns={"variable": "year"})
data_only = data[:2340]

ratio_df = ratio_df[
    [
        "group",
        "1995",
        "1996",
        "1997",
        "1998",
        "1999",
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
    ]
]
ratio_df = ratio_df.T
ratio_df = ratio_df.tail(-1)
ratio_df.rename(columns={1: "total men", 2: "total women"}, inplace=True)
ratio_df["ratio"] = ratio_df["total women"] / ratio_df["total men"]
ratio_df = ratio_df.reset_index()
ratio_df.rename(columns={"index": "year"}, inplace=True)


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
### Pyramid Plot ###
####################

color_scale = alt.Scale(domain=["total men", "total women"], range=["#1f77b4", "#e377c2"])
base = alt.Chart(ratio_df).mark_bar().encode(tooltip=["ratio"]).properties(width=250)

# left chart
left = base.encode(
    alt.X("total men:Q", title="wages", sort="descending", scale=alt.Scale(domain=[0, 1200])),
    alt.Y("year:N", axis=None, sort="descending"),
    color=alt.value("#31b0a5"),
)

# right chart
right = base.encode(
    alt.X("total women:Q", title="wages", sort="ascending", scale=alt.Scale(domain=[0, 1200])),
    alt.Y("year:N", axis=None, sort="descending"),
    color=alt.value("#de8b33")
    # alt.Color('group:O', scale=color_scale)
)

# middle chart
middle = (
    base.encode(
        alt.Y("year:N", axis=None, sort="descending"),
        alt.Text("year"),
    )
    .mark_text()
    .properties(width=35)
)

# concating 3 charts for the tree diagram
ch = alt.hconcat(left, middle, right, spacing=5)

# line chart
line = (
    alt.Chart(ratio_df)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year", axis=alt.Axis(labelAngle=-45)),
        y=alt.Y("ratio:Q", scale=alt.Scale(domain=(0.65, 1)), title="Female to male wage ratio"),
    )
)

# concating tree and line charts
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

data = load_data("edu_wages_2022.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

# male baseline
male = data[(data['male'] == 1) & (data['all_edu'] == 1) & data['all_races'] == 1]
male = male.T
male = male.tail(-1)
male = male.reset_index()
male.rename(columns={"index": "year", 1: "men"}, inplace=True)
male = male.iloc[:26, :]

# female by race
female = data[(data['female'] == 1) & data['all_edu'] == 1]
female = female.T
female = female.tail(-1)
female = female.reset_index()
female.rename(columns={2: "Total women", 42: "White women",
                       43: "Hispanic or Latino women", 66: "Black women",
                       84: "Asian women", "index": 'year'}, inplace=True)
female = female.iloc[:26, :]


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
