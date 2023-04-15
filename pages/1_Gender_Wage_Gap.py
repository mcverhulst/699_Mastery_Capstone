import streamlit as st
import altair as alt

st.set_page_config(page_title="Gender Wage Gap",
                   page_icon="⚖️",
                   layout="wide",
                   initial_sidebar_state="collapsed",
)

### IMPORT FILTERED DATA
from preprocessing.gender_ratios import *

st.markdown("# Education and the gender wage gap")
st.sidebar.header("Gender Wage Gap")
st.write(
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
    quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum."""
)

### ESTABLISH TAB STRUCTURE
tab1, tab2, tab3 = st.tabs(
    [
        "Men and Womens' Pay Compared   ",
        "  Female Pay by Race   ",
        "  Hours Needed to Match Mens' Pay   ",
    ]
)

#########################
### STACKED BAR CHART ###
#########################
with tab1:
    colors = alt.Scale(domain=("Male", "Female"), range=["#31b0a5", "#de8b33"])  # ['#31b0a5', '#de8b33']

    st.markdown("""### How does median pay for women and men compare?""")
    st.write("""Lorem ipsum...""")

    values = st.slider("Select a range of years", 1995, 2020, (1995, 2020))

    bars = alt.Chart(data_filtered).mark_bar().encode(
        x = alt.X('group:N', title=None, axis=None),
        y = alt.Y('value:Q', title="Median Weekly Pay", scale=alt.Scale(domain=(0, 1200))),
        color=alt.Color("group:N", scale=alt.Scale(range=["#31b0a5", "#de8b33"])),
        column=alt.Column(
                "year:O",
                title=None,
                header=alt.Header(labelAngle=-45, labelFontSize=13, labelOrient="bottom", labelPadding=35))
        ).transform_filter(
            values[0] <= alt.datum.year
        ).transform_filter(
            alt.datum.year <= values[1]
        ).transform_calculate(
            "group", alt.expr.if_(alt.datum.group == "total men", "Male", "Female")
        ).properties(width=30)

    # RATIO LINE CHART
    line = alt.Chart(ratio_df).mark_line(point=True).encode(
            x=alt.X("year:N", title="Year", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("ratio:Q", scale=alt.Scale(domain=(0, 1.2)), title="Female to male wage ratio"),
            color = alt.value("#de8b33")
    ).transform_filter(
        values[0] <= alt.datum.year
    ).transform_filter(
        alt.datum.year <= values[1]
    )

    # MALE BASELINE
    equal_pay = alt.Chart(pd.DataFrame({'y': [1]})).mark_rule(
        strokeWidth=3,
        strokeDash=[7,2]
    ).encode(
        y='y',
        color = alt.value("#31b0a5")
    )

    line2 = (line + equal_pay)

    combo2 = alt.vconcat(bars, line2).configure_facet(spacing=8)

    # PLOT CHART
    st.altair_chart(combo2, theme="streamlit", use_container_width=True)

######################################
### LAYERED RACE CHART WITH SELECT ###
######################################
with tab2:
    st.markdown("""### How much do women make by race?""")
    st.write("""The median wage for all men is indicated by the black line...
    """)

    # DEFINE CHECKBOX OPTIONS
    cuts = ["total men", "total women", "White + Female", "Hispanic or Latino + Female",
            "Black + Female", "Asian + Female"]
    # DEFINING COLOR SCALE
    alt_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    colors = alt.Scale(domain=(cuts), range=alt_colors)

    new = data_only[data_only['group'].isin(cuts)]

    race_checkboxes = new.group.unique()

    # COLLECT CHECKBOX VALUES
    # https://stackoverflow.com/questions/74243710/how-can-we-create-this-type-of-filter-checkbox-in-streamlit-python
    # https://discuss.streamlit.io/t/horizontal-checkbox/32751
    val = [None]* len(race_checkboxes)

    checks = st.columns(6)
    with checks[0]:
        val[0] = st.checkbox(cuts[0], value=True)
    with checks[1]:
        val[1] = st.checkbox(cuts[1], value=True)
    with checks[2]:
        val[2] = st.checkbox(cuts[2], value=True)
    with checks[3]:
        val[3] = st.checkbox(cuts[3], value=True)
    with checks[4]:
        val[4] = st.checkbox(cuts[4], value=True)
    with checks[5]:
        val[5] = st.checkbox(cuts[5], value=True)

    # FILTER DATAFRAME TO ONLY CHECKED BOXES
    new_filt = new[new.group.isin(race_checkboxes[val])].reset_index(drop=True)



    title = alt.TitleParams("Median Weekly Earnings in 2022 Dollars", anchor='middle')
    races = alt.Chart(new_filt, title=title).mark_line(point=True).encode(
        x=alt.X('year:N', title='Year',axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('value:Q', title="Median Weekly Wages", scale=alt.Scale(domain=(500, 1400))),
        # color='group'
        color=alt.Color("group:N", scale=colors)
    )

    # PLOT CHART
    st.altair_chart(races, theme="streamlit", use_container_width=True)

######################
### HOURS TO MATCH ###
######################
with tab3:
    title = alt.TitleParams("Hours Women Would Have to Work to Match Mens' Pay", anchor='middle')

    hours = alt.Chart(ratio_df, title=title,height=500).mark_bar().encode(
        x = alt.X('year:O', title='Year', axis=alt.Axis(labelAngle=-45)),
        y = alt.Y('hours:Q', title='Hours'),
        color = alt.value("#de8b33")
    )

    dummy_years = ["1995", "1996", "1997", "1998", "1999", "2000",
                     "2001", "2002", "2003", "2004", "2005", "2006", "2007",
                     "2008", "2009", "2010", "2011", "2012", "2013", "2014",
                     "2015", "2016", "2017", "2018", "2019", "2020"]

    dummy_weeks = {'weeks': 52, 'year': dummy_years}
    d_weeks = pd.DataFrame(data=dummy_weeks)

    dummy_months = {'months': 12, 'year': dummy_years}
    d_months = pd.DataFrame(data=dummy_months)

    ### MONTHS AREA CHART
    m_months = alt.Chart(d_months, height=500).mark_area().encode(
        alt.X("year:O", title="", axis=alt.Axis(labelAngle=-45)),
        alt.Y('months:Q', title="", scale=alt.Scale(domain=(0, 12))),
        color=alt.value("#1f77b4"),
        tooltip=[]
    )

    w_months = alt.Chart(ratio_df,height=500).mark_area().encode(
        alt.X("year:O", axis=alt.Axis(labelAngle=-45), title='Year'),
        alt.Y("f_months:Q", title='Additional Months', scale=alt.Scale(domain=(0, 12))),
        color=alt.value("#ff7f0e")
    )

    mw_months = m_months + w_months

    st.markdown("""### How many hours would women have to work to earn equal pay""")
    st.write("""Lorem ipsum...""")

    # PLOT CHART
    st.altair_chart(hours, theme="streamlit", use_container_width=True)

    st.markdown("""### How many ***months*** into the next year would women have to work to earn equal pay?""")
    st.altair_chart(mw_months, theme="streamlit", use_container_width=True)