import streamlit as st
import altair as alt
import bokeh as b
import pandas as pd
from utils.util_funcs import load_data


st.set_page_config(
    page_title="Earning Potential",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("# Higher Education Degrees and Earning Potential")
# st.sidebar.header("Earning Potential")
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
# data = pd.read_csv("../data/edu_wages.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

data = pd.melt(data, id_vars="group")
data = data.rename(columns={"variable": "year"})
data_only = data[:2340]


# FILTER DATASET BY GENDER/RACE/DEGREE
all_degrees = data_only[
    data_only["group"].isin(
        [
            "Less than HS",
            "High School",
            "Some College",
            "Bachelors Degree",
            "Advanced Degree",
        ]
    )
]

all_gender_degrees = data_only[
    data_only["group"].isin(
        [
            "Male + Less than HS",
            "Male + High School",
            "Male + Some College",
            "Male + Bachelors Degree",
            "Male + Advanced Degree",
            "Female + Less than HS",
            "Female + High School",
            "Female + Some College",
            "Female + Bachelors Degree",
            "Female + Advanced Degree",
        ]
    )
]
male_degrees = data_only[
    data_only["group"].isin(
        [
            "Male + Less than HS",
            "Male + High School",
            "Male + Some College",
            "Male + Bachelors Degree",
            "Male + Advanced Degree",
        ]
    )
]
female_degrees = data_only[
    data_only["group"].isin(
        [
            "Female + Less than HS",
            "Female + High School",
            "Female + Some College",
            "Female + Bachelors Degree",
            "Female + Advanced Degree",
        ]
    )
]
all_races = data_only[data_only["group"].isin(["Asian", "Black", "Hispanic or Latino", "White"])]
all_race_degrees = data_only[
    data_only["group"].isin(
        [
            "Asian + Bachelors Degree",
            "Asian + Advanced Degree",
            "Asian + Some College",
            "Asian + High School",
            "Black + Bachelors Degree",
            "Black + Advanced Degree",
            "Black + Some College",
            "Black + High School",
            "White + Bachelors Degree",
            "White + Advanced Degree",
            "White + Some College",
            "White + High School",
            "Hispanic or Latino + Bachelors Degree",
            "Hispanic or Latino + Advanced Degree",
            "Hispanic or Latino + Some College",
            "Hispanic or Latino + High School",
        ]
    )
]
all_races_advan = data_only[
    data_only["group"].isin(
        [
            "Asian + Advanced Degree",
            "Black + Advanced Degree",
            "Hispanic or Latino + Advanced Degree",
            "White + Advanced Degree",
        ]
    )
]
all_races_bach = data_only[
    data_only["group"].isin(
        [
            "Asian + Bachelors Degree",
            "Black + Bachelors Degree",
            "Hispanic or Latino + Advanced Degree",
            "White + Advanced Degree",
        ]
    )
]
asian_degrees = data_only[
    data_only["group"].isin(
        ["Asian + Bachelors Degree", "Asian + Advanced Degree", "Asian + Some College", "Asian + High School"]
    )
]
black_degrees = data_only[
    data_only["group"].isin(
        ["Black + Bachelors Degree", "Black + Advanced Degree", "Black + Some College", "Black + High School"]
    )
]
white_degrees = data_only[
    data_only["group"].isin(
        ["White + Bachelors Degree", "White + Advanced Degree", "White + Some College", "White + High School"]
    )
]
latino_degrees = data_only[
    data_only["group"].isin(
        [
            "Hispanic or Latino + Bachelors Degree",
            "Hispanic or Latino + Advanced Degree",
            "Hispanic or Latino + Some College",
            "Hispanic or Latino + High School",
        ]
    )
]

# LIST OF FILTERED SELECTIONS
filters = [
    "By Gender and Education Level",
    "Male By Education Level",
    "Female By Education Level",
    "By Race",
    "Bachelors Degrees By Race",
    "Advanced Degrees By Race",
    "Asian By Education Level",
    "Black By Education Level",
    "White By Education Level",
    "Hispanic or Latino By Education Level",
]

# # SET UP SELECT BOX
# chart_options_select = st.sidebar.selectbox("Select a category:", filters)

# if chart_options_select == "By Education Level":
#     data = all_degrees

# if chart_options_select == "By Gender and Education Level":
#     data = all_gender_degrees

# elif chart_options_select == "Male By Education Level":
#     data = male_degrees

# elif chart_options_select == "Female By Education Level":
#     data = female_degrees

# elif chart_options_select == "By Race":
#     data = all_races

# elif chart_options_select == "Bachelors Degrees By Race":
#     data = all_races_bach

# elif chart_options_select == "Advanced Degrees By Race":
#     data = all_races_advan

# elif chart_options_select == "Asian By Education Level":
#     data = asian_degrees

# elif chart_options_select == "Black By Education Level":
#     data = black_degrees

# elif chart_options_select == "White By Education Level":
#     data = white_degrees

# elif chart_options_select == "Hispanic or Latino By Education Level":
#     data = latino_degrees

# SET UP RADIO BUTTONS

filters = st.radio("Select a filter: ", ("By Degree", "By Gender & Degree", "By Race & Degree"))

if filters == "By Degree":
    data = all_degrees
elif filters == "By Gender & Degree":
    data = all_gender_degrees
elif filters == "By Race & Degree":
    data = all_race_degrees


# CHART WITH MULTILINE TOOL TIP
# Source: https://matthewkudija.com/blog/2018/06/22/altair-interactive/#building-interactive-altair-charts:~:text=in%20Vega%20Editor-,Stocks,-Example

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["year"], empty="none")

# The basic line
line = (
    alt.Chart()
    .mark_line(interpolate="basis")
    .encode(
        alt.X("year:T", axis=alt.Axis(title="")),
        alt.Y("value:Q", axis=alt.Axis(title="", format="$f")),
        color=alt.Color("group:N", legend=None),
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
multilineChart = alt.layer(line, selectors, points, rules, text, data=data, width=600, height=300, title="")

# st.altair_chart(multilineChart)

# SET UP COLUMN GRID LAYOUT
col1, col2 = st.columns([3, 3], gap="large")

col1.markdown("**MultiLine Chart**")
col1.altair_chart(multilineChart, use_container_width=True, theme="streamlit")

col1.markdown("**Placeholder**")
col1.altair_chart(multilineChart, use_container_width=True, theme="streamlit")

col2.markdown("**Placeholder**")
col2.altair_chart(multilineChart, use_container_width=True)

col2.markdown("**Placeholder**")
col2.altair_chart(multilineChart, use_container_width=True)
