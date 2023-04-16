import streamlit as st
from utils.util_funcs import convert_df, load_data

st.set_page_config(
    page_title="Earning Potential",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("# About the Data")

###############################################
################ READ IN DATA #################
earn_percent = load_data("earn_perc_chng.csv")
edu_wages = load_data("edu_wages_2022.csv")

###############################################
############# DOWNLOAD BUTTONS ################
###############################################
# SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv

csv1 = convert_df(edu_wages)
st.download_button(
    "Download the Median Weekly Wage Data", csv1, "edu_wages_2022.csv", "text/csv", key="download-csv1"
)

csv2 = convert_df(earn_percent)
st.download_button(
    "Download the Percent Change Data", csv2, "earn_perc_chng.csv", "text/csv", key="download-csv2"
)
