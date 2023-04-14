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

#########################
### STACKED BAR CHART ###
#########################

st.write("## Testing2...")
colors = alt.Scale(domain=("Male", "Female"), range=["#31b0a5", "#de8b33"])  # ['#31b0a5', '#de8b33']

values = st.slider("Select a range of years", 1995, 2020, (1995, 2020))

bar2 = (
    alt.Chart(data_filtered).mark_bar().encode(
        x=alt.X("group:N", title=None, axis=None),
        y=alt.Y("value:Q", title="Median Weekly Pay", scale=alt.Scale(domain=(0, 1200))),
        color=alt.Color("group:N", scale=colors),
        column=alt.Column(
            "year:N",
            title=None,
            header=alt.Header(labelAngle=-45, labelFontSize=13, labelOrient="bottom", labelPadding=35)),
        tooltip=["group", "value", "year"],
    ).transform_filter(
        values[0] <= alt.datum.year
    ).transform_filter(
        alt.datum.year <= values[1]
    ).transform_calculate(
        "group", alt.expr.if_(alt.datum.group == "total men", "Male", "Female")
    )
)

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

line2 = line + equal_pay

combo2 = alt.vconcat(bar2, line2).configure_facet(spacing=8)

st.altair_chart(combo2, theme="streamlit", use_container_width=True)

#####################
### WOMEN BY RACE ###
#####################

cuts = ["Total women:Q", "White women:Q", "Hispanic or Lation women:Q", "Black women", "Asian women"]

title = alt.TitleParams("Median Weekly Earnings in 2022 Dollars", anchor='middle')

base = alt.Chart(male, title=title, height=600).mark_line(point=True, strokeDash=[6,1]).encode(
    x = alt.X("year:N", title="Year", axis=alt.Axis(labelAngle=-45)),
    y = alt.Y("men:Q", scale=alt.Scale(domain=(500, 1400)), title="Median Weekly Wages ($2022)"),
    color = alt.value("#31b0a5"),
)

base_women = alt.Chart(female).mark_line(point=True).encode(
    x = alt.X("year:N", axis=alt.Axis(labelAngle=-45)),
    y = alt.Y("Total women:Q", scale=alt.Scale(domain=(500, 1400)), title=""),
    color = alt.value("blue")
)

white_women = base_women.encode(
    y = alt.Y("White women:Q"),
    color = alt.value("red")
)

his_women = base_women.encode(
    y = alt.Y("Hispanic or Latino women:Q"),
    color = alt.value("green")
)

black_women = base_women.encode(
    y = alt.Y("Black women:Q"),
    color = alt.value("orange")
)

asian_women = base_women.encode(
    y = alt.Y("Asian women:Q"),
    color = alt.value("pink")
)

races = base + base_women + white_women + his_women + black_women + asian_women

st.markdown("""### How much do women make by race?""")
st.write("""The median wage for all men is indicated by the black line...
""")
st.altair_chart(races, theme="streamlit", use_container_width=True)