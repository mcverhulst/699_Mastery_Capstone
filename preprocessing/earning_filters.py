import pandas as pd
import numpy as np
from utils.util_funcs import load_data

#####################################
####### READ RAW DATA ###############
#####################################
data_raw = load_data("edu_wages_2022.csv")

##########################################
####### READ IN AND MELT DATA ############
##########################################

# READ IN AND MELT DATASET - MEDIAN WAGES
data = data_raw.rename(columns={"report_name": "group"})

data = pd.melt(data, id_vars="group")
data = data.rename(columns={"variable": "year"})
data_only = data[:2340]

###############################################
## FILTER MEDIAN WAGES BY GENDER/RACE/DEGREE ##
###############################################

total_median = data_only[data_only["group"] == "total"]
all_degrees = data_only[
    data_only["group"].isin(
        [
            "High School",
            "Some College",
            "Bachelors Degree",
            "Advanced Degree",
        ]
    )
]

all_gender_degrees = data_only[
    data_only["group"].isin(
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
male_degrees = data_only[
    data_only["group"].isin(
        [
            "Male + High School",
            "Male + Some College",
            "Male + Bachelors Degree",
            "Male + Advanced Degree",
        ]
    )
]
female_degrees = data_only[
    data_only["group"].isin(
        [
            "Female + High School",
            "Female + Some College",
            "Female + Bachelors Degree",
            "Female + Advanced Degree",
        ]
    )
]
all_races = data_only[data_only["group"].isin(["Asian", "Black", "Hispanic or Latino", "White"])]
all_race_degrees = data_only[
    data_only["group"].isin(
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
all_races_advan = data_only[
    data_only["group"].isin(
        [
            "Asian + Advanced Degree",
            "Black + Advanced Degree",
            "Hispanic or Latino + Advanced Degree",
            "White + Advanced Degree",
        ]
    )
]
all_races_bach = data_only[
    data_only["group"].isin(
        [
            "Asian + Bachelors Degree",
            "Black + Bachelors Degree",
            "Hispanic or Latino + Bachelors Degree",
            "White + Bachelors Degree",
        ]
    )
]
asian_degrees = data_only[
    data_only["group"].isin(
        ["Asian + Bachelors Degree", "Asian + Advanced Degree", "Asian + Some College", "Asian + High School"]
    )
]
black_degrees = data_only[
    data_only["group"].isin(
        ["Black + Bachelors Degree", "Black + Advanced Degree", "Black + Some College", "Black + High School"]
    )
]
white_degrees = data_only[
    data_only["group"].isin(
        ["White + Bachelors Degree", "White + Advanced Degree", "White + Some College", "White + High School"]
    )
]
latino_degrees = data_only[
    data_only["group"].isin(
        [
            "Hispanic or Latino + Bachelors Degree",
            "Hispanic or Latino + Advanced Degree",
            "Hispanic or Latino + Some College",
            "Hispanic or Latino + High School",
        ]
    )
]

all_race_gender_degrees = data_only[
    data_only["group"].isin(
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
            "Hispanic or Latino + Female + Advanced Degree",
            "Hispanic or Latino + Female + Some College",
            "Hispanic or Latino + Female + High School",
        ]
    )
]

# LIST OF FILTERED SELECTIONS
# filters = [
#     "By Gender and Education Level",
#     "Male By Education Level",
#     "Female By Education Level",
#     "By Race",
#     "Bachelors Degrees By Race",
#     "Advanced Degrees By Race",
#     "Asian By Education Level",
#     "Black By Education Level",
#     "White By Education Level",
#     "Hispanic or Latino By Education Level",
# ]

################################################
####### % DIFF CALCULATIONS BY FILTER ##########
################################################
# SOURCE: https://www.indeed.com/career-advice/career-development/how-to-calculate-percentage-difference
# SOURCE: https://www.oracle.com/webfolder/technetwork/data-quality/edqhelp/Content/processor_library/matching/comparisons/percent_difference.htm
data_raw = data_raw.rename(columns={"report_name": "group"})
data_raw = data_raw[
    [
        "group",
        "1995",
        "1996",
        "1997",
        "1998",
        "1999",
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
    ]
]

data_raw = data_raw.T
data_raw.columns = data_raw.iloc[0]
data_raw = data_raw[1:]
data_raw = data_raw.reset_index()
data_raw = data_raw.rename(columns={"index": "year"})
data_raw

# https://www.investopedia.com/terms/p/percentage-change.asp
# CREATE NEW DF WITH PERCNT CHANGE VALUES
earn_perc_chng_df = pd.DataFrame()
earn_perc_chng_df["year"] = data_raw["year"]


## Total % change for comparison to the rest below:
earn_perc_chng_df["diff_%_total_total"] = (data_raw["total"] - data_raw["total"]) / data_raw["total"]


## BY DEGREE
earn_perc_chng_df["diff_%_HS_total"] = (data_raw["High School"] - data_raw["total"]) / data_raw["total"]
earn_perc_chng_df["diff_%_SC_total"] = (data_raw["Some College"] - data_raw["total"]) / data_raw["total"]
earn_perc_chng_df["diff_%_BA_total"] = (data_raw["Bachelors Degree"] - data_raw["total"]) / data_raw["total"]
earn_perc_chng_df["diff_%_AD_total"] = (data_raw["Advanced Degree"] - data_raw["total"]) / data_raw["total"]

## BY DEGREE + RACE
# Asian
earn_perc_chng_df["diff_%_A_BA_total"] = (
    data_raw["Asian + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_AD_total"] = (data_raw["Asian + Advanced Degree"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_A_SC_total"] = (data_raw["Asian + Some College"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_A_HS_total"] = (data_raw["Asian + High School"] - data_raw["total"]) / data_raw[
    "total"
]


# Black
earn_perc_chng_df["diff_%_B_BA_total"] = (
    data_raw["Black + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_AD_total"] = (data_raw["Black + Advanced Degree"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_B_SC_total"] = (data_raw["Black + Some College"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_B_HS_total"] = (data_raw["Black + High School"] - data_raw["total"]) / data_raw[
    "total"
]


# White
earn_perc_chng_df["diff_%_W_BA_total"] = (
    data_raw["White + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_AD_total"] = (data_raw["White + Advanced Degree"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_W_SC_total"] = (data_raw["White + Some College"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_W_HS_total"] = (data_raw["White + High School"] - data_raw["total"]) / data_raw[
    "total"
]


# Latino
earn_perc_chng_df["diff_%_L_BA_total"] = (
    data_raw["Hispanic or Latino + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_AD_total"] = (
    data_raw["Hispanic or Latino + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_SC_total"] = (
    data_raw["Hispanic or Latino + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_HS_total"] = (
    data_raw["Hispanic or Latino + High School"] - data_raw["total"]
) / data_raw["total"]


## BY DEGREE + GENDER
# Male
earn_perc_chng_df["diff_%_M_HS_total"] = (data_raw["Male + High School"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_M_SC_total"] = (data_raw["Male + Some College"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_M_BA_total"] = (data_raw["Male + Bachelors Degree"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_M_AD_total"] = (data_raw["Male + Advanced Degree"] - data_raw["total"]) / data_raw[
    "total"
]


# Female
earn_perc_chng_df["diff_%_F_HS_total"] = (data_raw["Female + High School"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_F_SC_total"] = (data_raw["Female + Some College"] - data_raw["total"]) / data_raw[
    "total"
]
earn_perc_chng_df["diff_%_F_BA_total"] = (
    data_raw["Female + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_F_AD_total"] = (
    data_raw["Female + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


## BY DEGREE + RACE + GENDER
# W + M + Degrees
earn_perc_chng_df["diff_%_W_M_HS_total"] = (
    data_raw["White + Male + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_M_SC_total"] = (
    data_raw["White + Male + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_M_BA_total"] = (
    data_raw["White + Male + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_M_AD_total"] = (
    data_raw["White + Male + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# W + F + Degrees
earn_perc_chng_df["diff_%_W_F_HS_total"] = (
    data_raw["White + Female + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_F_SC_total"] = (
    data_raw["White + Female + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_F_BA_total"] = (
    data_raw["White + Female + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_W_F_AD_total"] = (
    data_raw["White + Female + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# L + M + Degrees
earn_perc_chng_df["diff_%_L_M_HS_total"] = (
    data_raw["Hispanic or Latino + Male + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_M_SC_total"] = (
    data_raw["Hispanic or Latino + Male + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_M_BA_total"] = (
    data_raw["Hispanic or Latino + Male + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_M_AD_total"] = (
    data_raw["Hispanic or Latino + Male + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# L + F + Degrees
earn_perc_chng_df["diff_%_L_F_HS_total"] = (
    data_raw["Hispanic or Latino + Female + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_F_SC_total"] = (
    data_raw["Hispanic or Latino + Female + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_F_BA_total"] = (
    data_raw["Hispanic or Latino + Female + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_L_F_AD_total"] = (
    data_raw["Hispanic or Latino + Female + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# B + M + Degrees
earn_perc_chng_df["diff_%_B_M_HS_total"] = (
    data_raw["Black + Male + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_M_SC_total"] = (
    data_raw["Black + Male + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_M_BA_total"] = (
    data_raw["Black + Male + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_M_AD_total"] = (
    data_raw["Black + Male + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# B + F + Degrees
earn_perc_chng_df["diff_%_B_F_HS_total"] = (
    data_raw["Black + Female + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_F_SC_total"] = (
    data_raw["Black + Female + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_F_BA_total"] = (
    data_raw["Black + Female + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_B_F_AD_total"] = (
    data_raw["Black + Female + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# A + M + Degrees
earn_perc_chng_df["diff_%_A_M_HS_total"] = (
    data_raw["Asian + Male + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_M_SC_total"] = (
    data_raw["Asian + Male + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_M_BA_total"] = (
    data_raw["Asian + Male + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_M_AD_total"] = (
    data_raw["Asian + Male + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


# A + F + Degrees
earn_perc_chng_df["diff_%_A_F_HS_total"] = (
    data_raw["Asian + Female + High School"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_F_SC_total"] = (
    data_raw["Asian + Female + Some College"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_F_BA_total"] = (
    data_raw["Asian + Female + Bachelors Degree"] - data_raw["total"]
) / data_raw["total"]
earn_perc_chng_df["diff_%_A_F_AD_total"] = (
    data_raw["Asian + Female + Advanced Degree"] - data_raw["total"]
) / data_raw["total"]


##########################################
########## MELT THE RATIOS DF ############
##########################################
earn_perc_chng_df_melted = pd.melt(earn_perc_chng_df, id_vars=["year"])
earn_perc_chng_df_melted = earn_perc_chng_df_melted.rename(
    columns={"variable": "group", "value": "earn_perc_chng_from_total"}
)


## CREATE LEGEND FRIENDLY COLUMN
earn_perc_chng_df_melted["group_legend"] = earn_perc_chng_df_melted.loc[:, "group"]

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_total_total", "group_legend"
] = "total"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_HS_total", "group_legend"
] = "High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_SC_total", "group_legend"
] = "Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_BA_total", "group_legend"
] = "Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_AD_total", "group_legend"
] = "Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_BA_total", "group_legend"
] = "Asian + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_AD_total", "group_legend"
] = "Asian + Advanced Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_SC_total", "group_legend"
] = "Asian + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_HS_total", "group_legend"
] = "Asian + High School"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_BA_total", "group_legend"
] = "Black + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_AD_total", "group_legend"
] = "Black + Advanced Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_SC_total", "group_legend"
] = "Black + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_HS_total", "group_legend"
] = "Black + High School"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_BA_total", "group_legend"
] = "White + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_AD_total", "group_legend"
] = "White + Advanced Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_SC_total", "group_legend"
] = "White + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_HS_total", "group_legend"
] = "White + High School"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_BA_total", "group_legend"
] = "Hispanic or Latino + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_AD_total", "group_legend"
] = "Hispanic or Latino + Advanced Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_SC_total", "group_legend"
] = "Hispanic or Latino + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_HS_total", "group_legend"
] = "Hispanic or Latino + High School"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_M_HS_total", "group_legend"
] = "Male + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_M_SC_total", "group_legend"
] = "Male + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_M_BA_total", "group_legend"
] = "Male + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_M_AD_total", "group_legend"
] = "Male + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_F_HS_total", "group_legend"
] = "Female + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_F_SC_total", "group_legend"
] = "Female + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_F_BA_total", "group_legend"
] = "Female + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_F_AD_total", "group_legend"
] = "Female + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_M_HS_total", "group_legend"
] = "White + Male + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_M_SC_total", "group_legend"
] = "White + Male + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_M_BA_total", "group_legend"
] = "White + Male + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_M_AD_total", "group_legend"
] = "White + Male + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_F_HS_total", "group_legend"
] = "White + Female + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_F_SC_total", "group_legend"
] = "White + Female + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_F_BA_total", "group_legend"
] = "White + Female + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_W_F_AD_total", "group_legend"
] = "White + Female + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_M_HS_total", "group_legend"
] = "Hispanic or Latino + Male + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_M_SC_total", "group_legend"
] = "Hispanic or Latino + Male + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_M_BA_total", "group_legend"
] = "Hispanic or Latino + Male + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_M_AD_total", "group_legend"
] = "Hispanic or Latino + Male + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_F_HS_total", "group_legend"
] = "Hispanic or Latino + Female + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_F_SC_total", "group_legend"
] = "Hispanic or Latino + Female + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_F_BA_total", "group_legend"
] = "Hispanic or Latino + Female + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_L_F_AD_total", "group_legend"
] = "Hispanic or Latino + Female + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_M_HS_total", "group_legend"
] = "Black + Male + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_M_SC_total", "group_legend"
] = "Black + Male + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_M_BA_total", "group_legend"
] = "Black + Male + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_M_AD_total", "group_legend"
] = "Black + Male + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_F_HS_total", "group_legend"
] = "Black + Female + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_F_SC_total", "group_legend"
] = "Black + Female + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_F_BA_total", "group_legend"
] = "Black + Female + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_B_F_AD_total", "group_legend"
] = "Black + Female + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_M_HS_total", "group_legend"
] = "Asian + Male + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_M_SC_total", "group_legend"
] = "Asian + Male + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_M_BA_total", "group_legend"
] = "Asian + Male + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_M_AD_total", "group_legend"
] = "Asian + Male + Advanced Degree"

earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_F_HS_total", "group_legend"
] = "Asian + Female + High School"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_F_SC_total", "group_legend"
] = "Asian + Female + Some College"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_F_BA_total", "group_legend"
] = "Asian + Female + Bachelors Degree"
earn_perc_chng_df_melted.loc[
    earn_perc_chng_df_melted["group_legend"] == "diff_%_A_F_AD_total", "group_legend"
] = "Asian + Female + Advanced Degree"
