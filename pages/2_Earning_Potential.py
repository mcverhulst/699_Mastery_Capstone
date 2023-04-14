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

# earn_ratios_df
# earn_ratios_df_melted
final_earn_ratios

###############################################
######### SAVED CODE FOR DOWNLAOD BUTTON ######
###############################################

# csv = convert_df(earn_ratios_df)

# st.download_button("Download the Raw Data", csv, "earn_ratios_2022.csv", "text/csv", key="download-csv")

# # SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv


#########################
####### INPUTS ##########
#########################

######### SET UP RADIO BUTTONS ########

# filters = st.radio("Select a filter: ", ("By Degree", "By Gender & Degree", "By Race & Degree"))

# if filters == "By Degree":
#     data = all_degrees
# elif filters == "By Gender & Degree":
#     data = all_gender_degrees
# elif filters == "By Race & Degree":
#     data = all_race_degrees

##########################################
################ CHARTS ##################
##########################################


##############################
####### PAGE LAYOUT ##########
##############################

## TABS ##
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "By Degree   ",
        "  By Race and Degree   ",
        "  By Gender and Degree   ",
        "  By Gender, Race and Degree   ",
    ]
)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")

        csv = convert_df(earn_ratios_df)
        st.download_button(
            "Download the Raw Data", csv, "earn_ratios_2022.csv", "text/csv", key="download-csv"
        )

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")


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
