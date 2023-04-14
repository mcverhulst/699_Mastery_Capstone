import streamlit as st
import altair as alt
import pandas as pd

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

# import additional functions and data filters as modules
from preprocessing.earning_filters import *

###############################################
######### SAVED CODE FOR DOWNLAOD BUTTON ######
###############################################

# ### WRITE NEW DF TO CSV
# @st.cache_data
# def convert_df(df):
#     return df.to_csv(index=True).encode("utf-8")

# csv = convert_df(earn_ratios_df)

# st.download_button("Download the Raw Data", csv, "earn_ratios_2022.csv", "text/csv", key="download-csv")

# # SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv


#########################
####### INPUTS ##########
#########################

####### SET UP SELECT BOX ########

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

######### SET UP RADIO BUTTONS ########

filters = st.radio("Select a filter: ", ("By Degree", "By Gender & Degree", "By Race & Degree"))

if filters == "By Degree":
    data = all_degrees
elif filters == "By Gender & Degree":
    data = all_gender_degrees
elif filters == "By Race & Degree":
    data = all_race_degrees

##########################################
################ CHARTS ##################
##########################################

############# CHART WITH MULTILINE TOOL TIP ##############
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


############ CHART WITH SINGLE LINE HIGHLIGHT ########################
highlight = alt.selection(type="single", on="mouseover", fields=["group"], nearest=True)

base = alt.Chart(all_gender_degrees).encode(x="year:T", y="value:Q", color="group")

points = base.mark_circle().encode(opacity=alt.value(0)).add_selection(highlight).properties(width=600)

lines = base.mark_line().encode(size=alt.condition(~highlight, alt.value(1), alt.value(3)))

highlight_chart = points + lines


##############################
####### PAGE LAYOUT ##########
##############################
earn_ratios_df

# SET UP COLUMN GRID LAYOUT
col1, col2 = st.columns([3, 3], gap="large")

col1.markdown("**MultiLine Chart**")
col1.altair_chart(multilineChart, use_container_width=True, theme="streamlit")

col1.markdown("**Placeholder**")
col1.altair_chart(highlight_chart, use_container_width=True, theme="streamlit")

col2.markdown("**Placeholder**")
# col2.altair_chart(multilineChart, use_container_width=True)

col2.markdown("**Placeholder**")
# col2.altair_chart(multilineChart, use_container_width=True)
