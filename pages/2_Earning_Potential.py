import streamlit as st
import altair as alt
import pandas as pd
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

# variables to use
# earn_ratios_df
# earn_ratios_df_melted
# final_earn_ratios
all_degrees

###############################################
######### SAVED CODE FOR DOWNLAOD BUTTON ######
###############################################

# csv = convert_df(earn_ratios_df)

# st.download_button("Download the Raw Data", csv, "earn_ratios_2022.csv", "text/csv", key="download-csv")

# # SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv


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
        "  By Race and Degree   ",
        "  By Gender and Degree   ",
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
    title = alt.TitleParams("Median Weekly Earnings in 2022 Dollars", anchor="middle", fontSize=20)
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
    DegreeWageChart = alt.layer(
        line,
        selectors,
        points,
        rules,
        text,
        data=all_degrees,
        width=700,
        height=400,
        title=title,
    ).configure_legend(orient="bottom", columnPadding=25, padding=10)

    ##################################
    ########TAB 1: CHART 2 ###########
    ##################################
    title = alt.TitleParams("Median Weekly Earnings in 2022 Dollars", anchor="middle", fontSize=20)
    line1 = (
        alt.Chart(all_degrees, title=title)
        .mark_line()
        .encode(x="year:T", y="value:Q", color="group:N")
        .properties(
            width=700,
            height=400,
        )
    )

    line2 = (
        alt.Chart(total_median)
        .mark_line(color="black", strokeDash=[5, 1])
        .encode(
            x="year:T",
            y="value:Q",
        )
        .properties(
            width=700,
            height=400,
        )
    )

    degrees_w_total = (line1 + line2).configure_legend(orient="bottom", columnPadding=25, padding=10)

    ##################################
    ######## COLUMN LAYOUT ###########
    ##################################

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(DegreeWageChart, theme="streamlit", use_container_width=True)

    with col2:
        st.altair_chart(degrees_w_total, theme="streamlit", use_container_width=True)


with tab2:
    import numpy as np

    col1, col2 = st.columns([3, 1])
    data = np.random.randn(10, 1)

    col1.subheader("A wide column with a chart")
    col1.line_chart(data)

    col2.subheader("A narrow column with the data")
    col2.write(data)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with tab4:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


## COLUMNS ##
# col1, col2 = st.columns([3, 3], gap="large")

# col1.markdown("**MultiLine Chart**")
# col1.altair_chart(multilineChart, use_container_width=True, theme="streamlit")

# col1.markdown("**Placeholder**")
# col1.altair_chart(highlight_chart, use_container_width=True, theme="streamlit")

# col2.markdown("**Placeholder**")
# # col2.altair_chart(multilineChart, use_container_width=True)

# col2.markdown("**Placeholder**")
# # col2.altair_chart(multilineChart, use_container_width=True)
