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
# st.sidebar.header("Gender Wage Gap")
st.markdown(
    """The gender wage gap is the difference in earnings between men and women. 
    There are a number of factors that have an effect on this statistic including 
    industry, traditional gender norms surrounding family care, and more. Below 
    we chose to examine median pay for men and women at a high level as well as 
    explore how wage outcomes differ for people of different races."""
)

st.markdown("""More information can be found at the following links:
- [Pew Research Center Analysis](https://www.pewresearch.org/social-trends/2023/03/01/the-enduring-grip-of-the-gender-pay-gap/”)
- [Department of Labor Blog](https://blog.dol.gov/2023/03/14/5-fast-facts-the-gender-wage-gap)
- [Government Accountability Office](https://www.gao.gov/products/gao-23-106041)
""")


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

    st.markdown("""Below is a bar chart representing the median weekly pay for 
        men and women between 1995 and 2020. The line chart below denotes the 
        **female to male pay ratio** and the green dotted line indicates the 
        point where men and womens pay would be equal."""
    )

    st.markdown("""
        The ratio between men and womens pay has remained fairly steady over the 
        past 25 years while wages have risen slightly for both groups.
    """)

    values = st.slider("Select a range of years to compare", 1995, 2020, (1995, 2020))

    bars = alt.Chart(data_filtered).mark_bar().encode(
        x = alt.X('group:N', title=None, axis=None),
        y = alt.Y('value:Q', title="Median Weekly Pay", scale=alt.Scale(domain=(0, 1400))),
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
            y=alt.Y("ratio:Q", scale=alt.Scale(domain=(0, 1.2)), title="Female to Male Wage Ratio"),
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
    st.markdown("""This line chart shows median weekly earnings for women of 
        different races as compared to men. Asian women have the highest wages and 
        are the only group to show a significant rise year over year but still fall 
        short of the median pay for men. Hispanic or Latino women fare worse with 
        the lowest wages and hovering around 60\% of men's wages.
    """)

    # https://stackoverflow.com/questions/54015895/altair-default-color-palette-colors-in-hex
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
    races = alt.Chart(new_filt, title=title, height=600).mark_line(point=True).encode(
        x=alt.X('year:N', title='Year',axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('value:Q', title="Median Weekly Wages", scale=alt.Scale(domain=(0, 1400))),
        # color='group'
        color=alt.Color("group:N", scale=colors)
    )

    # PLOT CHART
    st.altair_chart(races, theme="streamlit", use_container_width=True)

######################
### HOURS TO MATCH ###
######################
with tab3:
    title = alt.TitleParams("Hours Women Would Have to Work to Match Men's Pay", anchor='middle')

    hours = alt.Chart(ratio_df, title=title,height=500).mark_bar().encode(
        x = alt.X('year:O', title='Year', axis=alt.Axis(labelAngle=-45)),
        y = alt.Y('hours:Q', title='Hours'),
        color = alt.value("#de8b33")
    )

    ### MONTHS AREA CHART
    title = alt.TitleParams("Proportion of an Additional Year Women Would Have to Work to Match Men's Pay", anchor='middle')

    w_months = alt.Chart(ratio_df,height=500, title=title).mark_area(line=True, point=True).encode(
        alt.X("year:O", axis=alt.Axis(labelAngle=-45), title='Year'),
        alt.Y("f_months:Q", title='Additional Months', scale=alt.Scale(domain=(0, 12))),
        color=alt.value("#de8b33")
    )

    # PLOT CHART
    st.markdown("""### How many hours would women have to work to earn equal pay""")
    st.markdown("""The gender pay gap has significant implications when translated 
        to the number of hours women would need to work to match the pay of men. 
        The bar chart below shows the number of additional hours women would 
        have to work **each week** to make the same amount of money as men."""
    )
    st.altair_chart(hours, theme="streamlit", use_container_width=True)

    # PLOT CHART
    st.markdown("""### How many additional ***months*** into the next year would women have to work to earn equal pay?""")
    st.markdown("""When the additional hours are extrapolated through an entire 
        year, the pay gap is damning. In 1995, women would have needed to work 
        an additional **4.88 months** into the next year to match the annual pay 
        of men. By 2020, that figure had been reduced but still exceeded 
        **3 months**."""
    )
    st.altair_chart(w_months, theme="streamlit", use_container_width=True)