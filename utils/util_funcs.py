import pandas as pd
import streamlit as st
import os


@st.cache_resource
def load_data(filename: str, index_col: int = None):
    """
    Read a csv into a pandas dataframe
    inspiration/source: https://github.com/streamlit/demo-uber-nyc-pickups/blob/main/streamlit_app.py

    params:
        - filename (str): the name of the file to be read in

    returns:
        - df: a pandas dataframe
    """
    if not os.path.isfile(filename):
        path = f"./data/{filename}"

    data = pd.read_csv(path, index_col=index_col)
    return data


@st.cache_data
def convert_df(df):
    """
    Write a csv from a pandas dataframe
    SOURCE: https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv

    params:
        - df (pandas df): the pandas dataframe to be written to csv

    returns:
        - csv: commas separate version of the pandas df"""
    return df.to_csv(index=True).encode("utf-8")
