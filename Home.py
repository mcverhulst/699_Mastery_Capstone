import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="📚",
)

st.write("# Is education the key to success?")
st.write("#### Analysis by Miranda Cooper and Mike VerHulst")

st.markdown(
    """As young professionals in pursuit of graduate degrees, we are curious to
    investigate the timeworn _"truth"_ that **"Education is the Key to Success"**
    and to analyze wage outcomes and earning potential for individuals at various stages
    of educational attainment."""
)

st.markdown("""The intended audience for this dashboard is undergraduates nearing 
    the end of their bachelor’s degree, young professionals considering an advanced 
    degree, and those considering going back to school as part of a career change."""
)

st.markdown("""##### The Data

For this project we used data from the Bureau of Labor Statistics 
[Current Population Survey](https://www.bls.gov/cps/) ranging from 1995 to 2020. In our analysis we considered 
only workers that were employed full time (35+ hours a week) and have reported 
weekly earnings. All the wage figures in this project represent median weekly 
earnings and have been adjusted to **2022 dollars.**
"""
)

st.markdown("[View the Source Code Here](https://github.com/mleighc/699_Mastery_Capstone)")
