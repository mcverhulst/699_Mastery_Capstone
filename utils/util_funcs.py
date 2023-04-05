import pandas as pd
import streamlit as st
import os


@st.cache_resource
def load_data(filename: str):
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

    data = pd.read_csv(path)
    return data
