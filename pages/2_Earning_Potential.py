import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from utils.util_funcs import convert_df, load_data

st.set_page_config(
    page_title="Earning Potential",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# import additional functions and data filters as modules
## WARN: handle this import after the streamlit set_page_config as that needs to be the first element
from preprocessing.earning_filters import *

st.markdown("# Higher Education Degrees and Earning Potential")
# st.sidebar.header("Earning Potential")
st.write(
    """What is a person's earning potential based on their most recent completed degree?
    How do Gender and Race impact earning potential?"""
)
earn_perc_diff_df_melted

# ###############################################
# ######### SAVED CODE FOR DOWNLAOD BUTTON ######
# ###############################################

# csv = convert_df(earn_perc_diff_df)

# st.download_button("Download the Raw Data", csv, "earn_perc_diff.csv", "text/csv", key="download-csv")

# # # SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv

##################################
######## TEST RADIO BUTTON #######
##################################

genre = st.radio(
    "Select a filter: ",
    ("By Degree", "By Degree and Race", "By Degree and Gender", "By Degree, Gender, and Race"),
)

if genre == "By Degree":
    data = earn_perc_diff_df_melted[
        earn_perc_diff_df_melted["group_legend"].isin(
            [
                "High School",
                "Some College",
                "Bachelors Degree",
                "Advanced Degree",
            ]
        )
    ]
elif genre == "By Degree and Race":
    pass
elif genre == "By Degree and Gender":
    pass
elif genre == "By Degree, Gender, and Race":
    pass

##################################
######### TEST CHART #############
##################################

st.write("## test line chart")

test = (
    alt.Chart(data)
    .mark_line()
    .encode(
        x="year:T",
        y="earn_perc_diff_from_total",
        color="group_legend",
        strokeDash="group_legend",
    )
)
test
###############################
####### SAVED INPUT CODE ######
###############################
# filters1 = st.radio(
#         "Select a filter: ",
#         (
#             "All",
#             "High School",
#             "Some College",
#             "Bachelors Degree",
#             "Advanced Degree",
#         ),
#     )

#     if filters1 == "All":
#         data1 = all_degrees
#     elif filters1 == "High School":
#         data1 = all_degrees[all_degrees.group == "High School"]
#     elif filters1 == "Some College":
#         pass
#     elif filters1 == "Bachelors Degree":
#         pass
#     elif filters1 == "Advanced Degree":
#         pass

######################################################################
########################### PAGE LAYOUT ##############################
######################################################################

##########
## TABS ##
##########

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "By Degree   ",
        "  By Gender and Degree   ",
        "  By Race and Degree   ",
        "  By Gender, Race and Degree   ",
    ]
)

with tab1:
    ##################################
    ########TAB 1: CHART 1 ###########
    ##################################

    ## BY DEGREE WAGE CHART
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["year"], empty="none")
    title = alt.TitleParams(
        "Median Weekly Earnings in 2022 Dollars",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Weekly Wages Indicated by Black Dotted Line",
    )
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

    line2 = (
        alt.Chart(total_median)
        .mark_line(interpolate="basis", color="black", strokeDash=[5, 1])
        .encode(
            x="year:T",
            y="value:Q",
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
    points2 = line2.mark_point(color="black").encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, "value:Q", alt.value(" "))
    )
    text2 = line2.mark_text(align="left", dx=5, dy=-5).encode(
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
    DegreeWageChart = alt.layer(
        line,
        line2,
        selectors,
        points,
        points2,
        rules,
        text,
        text2,
        data=all_degrees,
        width=700,
        height=400,
        title=title,
    ).configure_legend(orient="bottom", columnPadding=25, padding=10)

    ##################################
    ########TAB 1: CHART 2 ###########
    ##################################

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.altair_chart(DegreeWageChart, theme="streamlit", use_container_width=True)

    with col2:
        pass


with tab2:
    ##################################
    ########TAB 2: CHART 1 ###########
    ##################################

    ## BY DEGREE WAGE CHART
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["year"], empty="none")
    title = alt.TitleParams(
        "Median Weekly Earnings in 2022 Dollars",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Weekly Wages Indicated by Black Dotted Line",
    )
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

    line2 = (
        alt.Chart(total_median)
        .mark_line(interpolate="basis", color="black", strokeDash=[5, 1])
        .encode(
            x="year:T",
            y="value:Q",
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
    points2 = line2.mark_point(color="black").encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, "value:Q", alt.value(" "))
    )
    text2 = line2.mark_text(align="left", dx=5, dy=-5).encode(
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
    GenderDegreeChart = alt.layer(
        line,
        line2,
        selectors,
        points,
        points2,
        rules,
        text,
        text2,
        data=all_gender_degrees,
        width=800,
        height=600,
        title=title,
    ).configure_legend(orient="bottom", direction="horizontal", columns=2, columnPadding=25, padding=10)

    ##################################
    ########TAB 2: CHART 2 ###########
    ##################################

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################

    col3, col4 = st.columns(2, gap="medium")

    with col3:
        st.altair_chart(GenderDegreeChart, theme="streamlit", use_container_width=True)

    with col4:
        pass

with tab3:
    ##################################
    ########TAB 3: CHART 1 ###########
    ##################################

    ##################################
    ########TAB 3: CHART 2 ###########
    ##################################

    col5, col6 = st.columns(2, gap="medium")

    with col5:
        pass

    with col6:
        pass

with tab4:
    ##################################
    ########TAB 4: CHART 1 ###########
    ##################################

    ##################################
    ########TAB 4: CHART 2 ###########
    ##################################
    col7, col8 = st.columns(2, gap="medium")

    with col7:
        pass

    with col8:
        pass
