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

st.markdown("# How does higher education impact earning potential?")
# st.sidebar.header("Earning Potential")
st.markdown(
    """Higher Education degrees can lead to a high earning potential
    during the course of one's career. Studies have shown that individuals with higher education degrees, such as bachelor's, master's, or doctoral degrees, tend to earn more on average than those with only a high school diploma or some college education. In this series of visualizations,
    we explore those impacts of educational attainment on a
    person's earning potential. In order to dig deeper into additional factors impacting a person's 
    earning potential, we have also analyzed earning potential by race and gender."""
)

st.markdown(
    """More information can be found at the following links:
- [**Bureau of Labor Statistics:** _Measuring the value of education_](https://www.bls.gov/careeroutlook/2018/data-on-display/education-pays.htm)
- [**Bureau of Labor Statistics:** _Employment Projections_](https://www.bls.gov/emp/chart-unemployment-earnings-education.htm)
- [**National Center for Education Statistics:** _Annual Earnings by Educational Attainment_](https://nces.ed.gov/programs/coe/indicator/cba/annual-earnings)
- [**Northeastern University:** _Average Salary by Education Level_](https://bachelors-completion.northeastern.edu/news/average-salary-by-education-level/)
"""
)

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
            alt.X("year:T", axis=alt.Axis(title="Year")),
            alt.Y("value:Q", axis=alt.Axis(title="", format="$f")),
            color="group:N",
        )
    )

    line2 = (
        alt.Chart(total_median)
        .mark_line(interpolate="basis", color="black", strokeDash=[5, 1])
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("value:Q", axis=alt.Axis(title="Median Weekly Wage", format="$f")),
        )
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart()
        .mark_point()
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
        "Percent Change of Median Weekly Earnings",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Solid Line",
    )
    line1 = (
        alt.Chart(degrees)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("earn_perc_chng_from_total:Q", axis=alt.Axis(title="Percent Change", format="%")),
            color="group_legend:N",
            tooltip=["group_legend", "earn_perc_chng_from_total"],
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeWidth=1.5).encode(y="y")
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
    gender = st.radio(
        "Select a filter: ",
        ("Female", "Male", "All"),
        key="gender",
        horizontal=True,
    )

    if gender == "All":
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
    elif gender == "Female":
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
    elif gender == "Male":
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("value:Q", axis=alt.Axis(title="Median Weekly Wage", format="$f")),
        )
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart()
        .mark_point()
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
        "Percent Change of Median Weekly Earnings",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Solid Line",
    )
    line1 = (
        alt.Chart(chng_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("earn_perc_chng_from_total:Q", axis=alt.Axis(title="Percent Change", format="%")),
            color="group_legend:N",
            tooltip=["group_legend", "earn_perc_chng_from_total"],
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeWidth=1.5).encode(y="y")
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
        st.write()

    with col4:
        st.altair_chart(GenderDegreeChngChart, theme="streamlit", use_container_width=True)
        st.write()

with tab3:
    ##################################
    ######### RADIO RACE #############
    ##################################
    race = st.radio(
        "Select a filter: ",
        ("Asian", "Black", "Hispanic or Latino", "White", "All"),
        key="race",
        horizontal=True,
    )

    if race == "All":
        data = all_race_degrees
        chng_data = earn_perc_chng_df_melted[
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
                    "Hispanic or Latino + Bachelors Degree",
                    "Hispanic or Latino + Advanced Degree",
                    "Hispanic or Latino + Some College",
                    "Hispanic or Latino + High School",
                ]
            )
        ]
    elif race == "Asian":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Asian + Bachelors Degree",
                    "Asian + Advanced Degree",
                    "Asian + Some College",
                    "Asian + High School",
                ]
            )
        ]
        data = all_race_degrees[
            all_race_degrees["group"].isin(
                [
                    "Asian + Bachelors Degree",
                    "Asian + Advanced Degree",
                    "Asian + Some College",
                    "Asian + High School",
                ]
            )
        ]
    elif race == "Black":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Black + Bachelors Degree",
                    "Black + Advanced Degree",
                    "Black + Some College",
                    "Black + High School",
                ]
            )
        ]
        data = all_race_degrees[
            all_race_degrees["group"].isin(
                [
                    "Black + Bachelors Degree",
                    "Black + Advanced Degree",
                    "Black + Some College",
                    "Black + High School",
                ]
            )
        ]
    elif race == "Hispanic or Latino":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Hispanic or Latino + Bachelors Degree",
                    "Hispanic or Latino + Advanced Degree",
                    "Hispanic or Latino + Some College",
                    "Hispanic or Latino + High School",
                ]
            )
        ]
        data = all_race_degrees[
            all_race_degrees["group"].isin(
                [
                    "Hispanic or Latino + Bachelors Degree",
                    "Hispanic or Latino + Advanced Degree",
                    "Hispanic or Latino + Some College",
                    "Hispanic or Latino + High School",
                ]
            )
        ]
    elif race == "White":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "White + Bachelors Degree",
                    "White + Advanced Degree",
                    "White + Some College",
                    "White + High School",
                ]
            )
        ]
        data = all_race_degrees[
            all_race_degrees["group"].isin(
                [
                    "White + Bachelors Degree",
                    "White + Advanced Degree",
                    "White + Some College",
                    "White + High School",
                ]
            )
        ]
    ##################################
    ########TAB 3: CHART 1 ###########
    ##################################
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("value:Q", axis=alt.Axis(title="Median Weekly Wage", format="$f")),
            color="group:N",
        )
    )

    line2 = (
        alt.Chart(total_median)
        .mark_line(interpolate="basis", color="black", strokeDash=[5, 1])
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("value:Q", axis=alt.Axis(title="Median Weekly Wage", format="$f")),
        )
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart()
        .mark_point()
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
        data=data,
        width=400,
        height=500,
        title=title,
    ).configure_legend(orient="bottom", direction="horizontal", columns=2, columnPadding=25, padding=10)

    ##################################
    ########TAB 3: CHART 2 ###########
    ##################################
    ## FILTER DIFFS DATA TO RACE and DEGREES ONLY
    total = earn_perc_chng_df_melted[earn_perc_chng_df_melted.group_legend == "total"]
    title = alt.TitleParams(
        "Percent Change of Median Weekly Earnings",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Solid Line",
    )
    line1 = (
        alt.Chart(chng_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("earn_perc_chng_from_total:Q", axis=alt.Axis(title="Percent Change", format="%")),
            color="group_legend:N",
            tooltip=["group_legend", "earn_perc_chng_from_total"],
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeWidth=1.5).encode(y="y")
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
    #########################################
    ######### RADIO RACE GENDER #############
    #########################################
    race_gender = st.radio(
        "Select a filter: ",
        ("Asian", "Black", "Hispanic or Latino", "White"),
        key="race_gender",
        horizontal=True,
    )

    if race_gender == "Asian":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Asian + Male + Bachelors Degree",
                    "Asian + Male + Advanced Degree",
                    "Asian + Male + Some College",
                    "Asian + Male + High School",
                    "Asian + Female + Bachelors Degree",
                    "Asian + Female + Advanced Degree",
                    "Asian + Female + Some College",
                    "Asian + Female + High School",
                ]
            )
        ]
        data = all_race_gender_degrees[
            all_race_gender_degrees["group"].isin(
                [
                    "Asian + Male + Bachelors Degree",
                    "Asian + Male + Advanced Degree",
                    "Asian + Male + Some College",
                    "Asian + Male + High School",
                    "Asian + Female + Bachelors Degree",
                    "Asian + Female + Advanced Degree",
                    "Asian + Female + Some College",
                    "Asian + Female + High School",
                ]
            )
        ]
    elif race_gender == "Black":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Black + Male + Bachelors Degree",
                    "Black + Male + Advanced Degree",
                    "Black + Male + Some College",
                    "Black + Male + High School",
                    "Black + Female + Bachelors Degree",
                    "Black + Female + Advanced Degree",
                    "Black + Female + Some College",
                    "Black + Female + High School",
                ]
            )
        ]
        data = all_race_gender_degrees[
            all_race_gender_degrees["group"].isin(
                [
                    "Black + Male + Bachelors Degree",
                    "Black + Male + Advanced Degree",
                    "Black + Male + Some College",
                    "Black + Male + High School",
                    "Black + Female + Bachelors Degree",
                    "Black + Female + Advanced Degree",
                    "Black + Female + Some College",
                    "Black + Female + High School",
                ]
            )
        ]
    elif race_gender == "Hispanic or Latino":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "Hispanic or Latino + Male + Bachelors Degree",
                    "Hispanic or Latino + Male + Advanced Degree",
                    "Hispanic or Latino + Male + Some College",
                    "Hispanic or Latino + Male + High School",
                    "Hispanic or Latino + Female + Bachelors Degree",
                    "Hispanic or Latino + Female + Advanced Degree",
                    "Hispanic or Latino + Female + Some College",
                    "Hispanic or Latino + Female + High School",
                ]
            )
        ]
        data = all_race_gender_degrees[
            all_race_gender_degrees["group"].isin(
                [
                    "Hispanic or Latino + Male + Bachelors Degree",
                    "Hispanic or Latino + Male + Advanced Degree",
                    "Hispanic or Latino + Male + Some College",
                    "Hispanic or Latino + Male + High School",
                    "Hispanic or Latino + Female + Bachelors Degree",
                    "Hispanic or Latino + Female + Advanced Degree",
                    "Hispanic or Latino + Female + Some College",
                    "Hispanic or Latino + Female + High School",
                ]
            )
        ]
    elif race_gender == "White":
        chng_data = earn_perc_chng_df_melted[
            earn_perc_chng_df_melted["group_legend"].isin(
                [
                    "White + Male + Bachelors Degree",
                    "White + Male + Advanced Degree",
                    "White + Male + Some College",
                    "White + Male + High School",
                    "White + Female + Bachelors Degree",
                    "White + Female + Advanced Degree",
                    "White + Female + Some College",
                    "White + Female + High School",
                ]
            )
        ]
        data = all_race_gender_degrees[
            all_race_gender_degrees["group"].isin(
                [
                    "White + Male + Bachelors Degree",
                    "White + Male + Advanced Degree",
                    "White + Male + Some College",
                    "White + Male + High School",
                    "White + Female + Bachelors Degree",
                    "White + Female + Advanced Degree",
                    "White + Female + Some College",
                    "White + Female + High School",
                ]
            )
        ]
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("value:Q", axis=alt.Axis(title="Median Weekly Wage", format="$f")),
        )
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart()
        .mark_point()
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
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
        data=data,
        width=400,
        height=500,
        title=title,
    ).configure_legend(
        orient="bottom", direction="horizontal", columns=3, columnPadding=25, padding=10, labelFontSize=10
    )

    ##################################
    ########TAB 4: CHART 2 ###########
    ##################################
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
                "Hispanic or Latino + Male + Bachelors Degree",
                "Hispanic or Latino + Male + Advanced Degree",
                "Hispanic or Latino + Male + Some College",
                "Hispanic or Latino + Male + High School",
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
                "Hispanic or Latino + Female + Bachelors Degree",
                "Hispanic or Latino+ Female + Advanced Degree",
                "Hispanic or Latino + Female + Some College",
                "Hispanic or Latino + Female + High School",
            ]
        )
    ]
    title = alt.TitleParams(
        "Percent Change of Median Weekly Earnings",
        anchor="middle",
        fontSize=25,
        subtitle="Total Median Percent Change Indicated by Black Solid Line",
    )
    line1 = (
        alt.Chart(chng_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:T", axis=alt.Axis(title="Year")),
            y=alt.Y("earn_perc_chng_from_total:Q", axis=alt.Axis(title="Percent Change", format="%")),
            color="group_legend:N",
            tooltip=["group_legend", "earn_perc_chng_from_total"],
            strokeDash="group_legend:N",
        )
    )
    line2 = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(strokeWidth=1.5).encode(y="y")
    RaceGenderDegreeChngChart = (
        (line1 + line2)
        .properties(width=400, height=500, title=title)
        .configure_legend(
            orient="bottom", direction="horizontal", columns=3, columnPadding=25, padding=10, labelFontSize=10
        )
    )

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################
    col7, col8 = st.columns(2, gap="medium")

    with col7:
        st.altair_chart(RaceGenderDegreeChart, theme="streamlit", use_container_width=True)

    with col8:
        st.altair_chart(RaceGenderDegreeChngChart, theme="streamlit", use_container_width=True)
