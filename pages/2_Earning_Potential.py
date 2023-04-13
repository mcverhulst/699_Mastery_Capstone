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

##########################################
####### READ IN AND FORMAT DATA ##########
##########################################

# READ IN AND MELT DATASET
data_raw = load_data("edu_wages_2022.csv")
# data_raw.set_index("report_name")
data = data_raw.rename(columns={"report_name": "group"})

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

#####################################
####### RATIO CALCULATIONS ##########
#####################################
data_raw = data_raw.rename(columns={"report_name": "group"})
data_raw = data_raw[
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

data_raw = data_raw.T
data_raw.columns = data_raw.iloc[0]
data_raw = data_raw[1:]
data_raw

# CREATE NEW DF WITH RATIO VALUES
earn_ratios_df = pd.DataFrame()

## BY DEGREE
earn_ratios_df["ratio_HS_total"] = data_raw["High School"] / data_raw["total"]
earn_ratios_df["ratio_SC_total"] = data_raw["Some College"] / data_raw["total"]
earn_ratios_df["ratio_BA_total"] = data_raw["Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_AD_total"] = data_raw["Advanced Degree"] / data_raw["total"]

## BY DEGREE + RACE
# Asian
earn_ratios_df["ratio_A_BA_total"] = data_raw["Asian + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_A_AD_total"] = data_raw["Asian + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_A_SC_total"] = data_raw["Asian + Some College"] / data_raw["total"]
earn_ratios_df["ratio_A_HS_total"] = data_raw["Asian + High School"] / data_raw["total"]

# Black
earn_ratios_df["ratio_B_BA_total"] = data_raw["Black + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_B_AD_total"] = data_raw["Black + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_B_SC_total"] = data_raw["Black + Some College"] / data_raw["total"]
earn_ratios_df["ratio_B_HS_total"] = data_raw["Black + High School"] / data_raw["total"]

# White
earn_ratios_df["ratio_W_BA_total"] = data_raw["White + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_W_AD_total"] = data_raw["White + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_W_SC_total"] = data_raw["White + Some College"] / data_raw["total"]
earn_ratios_df["ratio_W_HS_total"] = data_raw["White + High School"] / data_raw["total"]

# Latino
earn_ratios_df["ratio_L_BA_total"] = data_raw["Hispanic or Latino + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_L_AD_total"] = data_raw["Hispanic or Latino + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_L_SC_total"] = data_raw["Hispanic or Latino + Some College"] / data_raw["total"]
earn_ratios_df["ratio_L_HS_total"] = data_raw["Hispanic or Latino + High School"] / data_raw["total"]

## BY DEGREE + GENDER

## BY DEGREE + RACE + GENDER


earn_ratios_df


### WRITE NEW DF TO CSV
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


csv = convert_df(earn_ratios_df)

st.download_button("Press to Download", csv, "earn_ratios_2022.csv", "text/csv", key="download-csv")

# SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv


#########################
####### INPUTS ##########
#########################

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

#########################
####### CHARTS ##########
#########################

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


#########################
####### LAYOUT ##########
#########################

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
