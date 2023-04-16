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

# ###############################################
# ######### SAVED CODE FOR DOWNLAOD BUTTON ######
# ###############################################

# csv = convert_df(earn_perc_chng_df_melted)

# st.download_button("Download the Raw Data", csv, "earn_perc_diff.csv", "text/csv", key="download-csv")

# # # SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv

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
    ######## TAB 1: CHART 1 ##########
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
        width=400,
        height=500,
        title=title,
    ).configure_legend(orient="bottom", columnPadding=25, padding=10)

    ##################################
    ########TAB 1: CHART 2 ###########
    ##################################

    ## FILTER DIFFS DATA TO DEGREES ONLY
    total = earn_perc_chng_df_melted[earn_perc_chng_df_melted.group_legend == "total"]
    degrees = earn_perc_chng_df_melted[
        earn_perc_chng_df_melted["group_legend"].isin(
            [
                "High School",
                "Some College",
                "Bachelors Degree",
                "Advanced Degree",
            ]
        )
    ]
    title = alt.TitleParams(
        "Percent Change Median Weekly Earnings vs. Total Median",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Dotted Line",
    )
    line1 = (
        alt.Chart(degrees)
        .mark_line()
        .encode(
            x="year:T",
            y="earn_perc_chng_from_total:Q",
            color="group_legend:N",
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule().encode(y="y")
    DegreeChngChart = (
        (line1 + line2)
        .properties(width=400, height=500, title=title)
        .configure_legend(orient="bottom", columnPadding=25, padding=10)
    )

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.altair_chart(DegreeWageChart, theme="streamlit", use_container_width=True)

    with col2:
        st.altair_chart(DegreeChngChart, theme="streamlit", use_container_width=True)


with tab2:
    ##################################
    #########RADIO GENDER#############
    ##################################
    genre = st.radio(
        "Select a filter: ",
        ("All", "Female", "Male"),
    )

    if genre == "All":
        data = all_gender_degrees
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Male + High School",
                    "Male + Some College",
                    "Male + Bachelors Degree",
                    "Male + Advanced Degree",
                    "Female + High School",
                    "Female + Some College",
                    "Female + Bachelors Degree",
                    "Female + Advanced Degree",
                ]
            )
        ]
    elif genre == "Female":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Female + High School",
                    "Female + Some College",
                    "Female + Bachelors Degree",
                    "Female + Advanced Degree",
                ]
            )
        ]
        data = all_gender_degrees[
            all_gender_degrees["group"].isin(
                [
                    "Female + High School",
                    "Female + Some College",
                    "Female + Bachelors Degree",
                    "Female + Advanced Degree",
                ]
            )
        ]
    elif genre == "Male":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Male + High School",
                    "Male + Some College",
                    "Male + Bachelors Degree",
                    "Male + Advanced Degree",
                ]
            )
        ]
        data = all_gender_degrees[
            all_gender_degrees["group"].isin(
                [
                    "Male + High School",
                    "Male + Some College",
                    "Male + Bachelors Degree",
                    "Male + Advanced Degree",
                ]
            )
        ]
    ##################################
    ########TAB 2: CHART 1 ###########
    ##################################
    ## BY GENDER and DEGREE WAGE CHART
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
        data=data,
        width=400,
        height=500,
        title=title,
    ).configure_legend(orient="bottom", direction="horizontal", columns=2, columnPadding=25, padding=10)

    ##################################
    ########TAB 2: CHART 2 ###########
    ##################################

    ## FILTER DIFFS DATA TO GEnder and DEGREES ONLY
    total = earn_perc_chng_df_melted[earn_perc_chng_df_melted.group_legend == "total"]
    title = alt.TitleParams(
        "Percent Change Median Weekly Earnings vs. Total Median",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Dotted Line",
    )
    line1 = (
        alt.Chart(chng_data)
        .mark_line()
        .encode(
            x="year:T",
            y="earn_perc_chng_from_total:Q",
            color="group_legend:N",
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule().encode(y="y")
    GenderDegreeChngChart = (
        (line1 + line2)
        .properties(width=400, height=500, title=title)
        .configure_legend(orient="bottom", direction="horizontal", columns=2, columnPadding=25, padding=10)
    )

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################

    col3, col4 = st.columns(2, gap="medium")

    with col3:
        st.altair_chart(GenderDegreeChart, theme="streamlit", use_container_width=True)

    with col4:
        st.altair_chart(GenderDegreeChngChart, theme="streamlit", use_container_width=True)

with tab3:
    ##################################
    ########TAB 3: CHART 1 ###########
    ##################################
    st.write("add radio button A + W + B + L")
    ## BY RACE and DEGREE WAGE CHART
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
    RaceDegreeChart = alt.layer(
        line,
        line2,
        selectors,
        points,
        points2,
        rules,
        text,
        text2,
        data=all_race_degrees,
        width=400,
        height=500,
        title=title,
    ).configure_legend(orient="bottom", direction="horizontal", columns=2, columnPadding=25, padding=10)

    ##################################
    ########TAB 3: CHART 2 ###########
    ##################################
    ## FILTER DIFFS DATA TO RACE and DEGREES ONLY
    total = earn_perc_chng_df_melted[earn_perc_chng_df_melted.group_legend == "total"]
    race_degrees = earn_perc_chng_df_melted[
        earn_perc_chng_df_melted["group_legend"].isin(
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
                "Latinx + Bachelors Degree",
                "Latinx + Advanced Degree",
                "Latinx + Some College",
                "Latinx + High School",
            ]
        )
    ]
    title = alt.TitleParams(
        "Percent Change Median Weekly Earnings vs. Total Median",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Dotted Line",
    )
    line1 = (
        alt.Chart(race_degrees)
        .mark_line()
        .encode(
            x="year:T",
            y="earn_perc_chng_from_total:Q",
            color="group_legend:N",
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule().encode(y="y")
    RaceDegreeChngChart = (
        (line1 + line2)
        .properties(width=400, height=500, title=title)
        .configure_legend(orient="bottom", direction="horizontal", columns=2, columnPadding=25, padding=10)
    )

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################
    col5, col6 = st.columns(2, gap="medium")

    with col5:
        st.altair_chart(RaceDegreeChart, theme="streamlit", use_container_width=True)

    with col6:
        st.altair_chart(RaceDegreeChngChart, theme="streamlit", use_container_width=True)

with tab4:
    ##################################
    ########TAB 4: CHART 1 ###########
    ##################################
    ## BY GENDER RACE and DEGREE WAGE CHART
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
    RaceGenderDegreeChart = alt.layer(
        line,
        line2,
        selectors,
        points,
        points2,
        rules,
        text,
        text2,
        data=all_race_gender_degrees,
        width=400,
        height=500,
        title=title,
    ).configure_legend(orient="bottom", direction="horizontal", columns=3, columnPadding=25, padding=10)

    ##################################
    ########TAB 4: CHART 2 ###########
    ##################################
    st.write("add radio button A + W + B + L + M + F")
    ## FILTER DIFFS DATA TO RACE and DEGREES ONLY
    total = earn_perc_chng_df_melted[earn_perc_chng_df_melted.group_legend == "total"]
    race_gender_degrees = earn_perc_chng_df_melted[
        earn_perc_chng_df_melted["group_legend"].isin(
            [
                "Asian + Male + Bachelors Degree",
                "Asian + Male + Advanced Degree",
                "Asian + Male + Some College",
                "Asian + Male + High School",
                "Black + Male + Bachelors Degree",
                "Black + Male + Advanced Degree",
                "Black + Male + Some College",
                "Black + Male + High School",
                "White + Male + Bachelors Degree",
                "White + Male + Advanced Degree",
                "White + Male + Some College",
                "White + Male + High School",
                "Latinx + Male + Bachelors Degree",
                "Latinx + Male + Advanced Degree",
                "Latinx + Male + Some College",
                "Latinx + Male + High School",
                "Asian + Female + Bachelors Degree",
                "Asian + Female + Advanced Degree",
                "Asian + Female + Some College",
                "Asian + Female + High School",
                "Black + Female + Bachelors Degree",
                "Black + Female + Advanced Degree",
                "Black + Female + Some College",
                "Black + Female + High School",
                "White + Female + Bachelors Degree",
                "White + Female + Advanced Degree",
                "White + Female + Some College",
                "White + Female + High School",
                "Latinx + Female + Bachelors Degree",
                "Latinx+ Female + Advanced Degree",
                "Latinx + Female + Some College",
                "Latinx + Female + High School",
            ]
        )
    ]
    title = alt.TitleParams(
        "Percent Change Median Weekly Earnings vs. Total Median",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Dotted Line",
    )
    line1 = (
        alt.Chart(race_gender_degrees)
        .mark_line()
        .encode(
            x="year:T",
            y="earn_perc_chng_from_total:Q",
            color="group_legend:N",
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule().encode(y="y")
    RaceGenderDegreeChngChart = (
        (line1 + line2)
        .properties(width=400, height=500, title=title)
        .configure_legend(orient="bottom", direction="horizontal", columns=3, columnPadding=25, padding=10)
    )

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################
    col7, col8 = st.columns(2, gap="medium")

    with col7:
        st.altair_chart(RaceGenderDegreeChart, theme="streamlit", use_container_width=True)

    with col8:
        st.altair_chart(RaceGenderDegreeChngChart, theme="streamlit", use_container_width=True)
