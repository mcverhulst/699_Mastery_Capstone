import pandas as pd
from utils.util_funcs import load_data

#####################################
####### READ RAW DATA ###############
#####################################
data_raw = load_data("edu_wages_2022.csv")

##########################################
####### READ IN AND MELT DATA ############
##########################################

# READ IN AND MELT DATASET
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

###############################################
####### RATIO CALCULATIONS BY FILTER ##########
###############################################
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
data_raw

# CREATE NEW DF WITH RATIO VALUES
earn_ratios_df = pd.DataFrame()

## BY DEGREE
earn_ratios_df["ratio_HS_total"] = data_raw["High School"] / data_raw["total"]
earn_ratios_df["ratio_SC_total"] = data_raw["Some College"] / data_raw["total"]
earn_ratios_df["ratio_BA_total"] = data_raw["Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_AD_total"] = data_raw["Advanced Degree"] / data_raw["total"]

## BY DEGREE + RACE
# Asian
earn_ratios_df["ratio_A_BA_total"] = data_raw["Asian + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_A_AD_total"] = data_raw["Asian + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_A_SC_total"] = data_raw["Asian + Some College"] / data_raw["total"]
earn_ratios_df["ratio_A_HS_total"] = data_raw["Asian + High School"] / data_raw["total"]

# Black
earn_ratios_df["ratio_B_BA_total"] = data_raw["Black + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_B_AD_total"] = data_raw["Black + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_B_SC_total"] = data_raw["Black + Some College"] / data_raw["total"]
earn_ratios_df["ratio_B_HS_total"] = data_raw["Black + High School"] / data_raw["total"]

# White
earn_ratios_df["ratio_W_BA_total"] = data_raw["White + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_W_AD_total"] = data_raw["White + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_W_SC_total"] = data_raw["White + Some College"] / data_raw["total"]
earn_ratios_df["ratio_W_HS_total"] = data_raw["White + High School"] / data_raw["total"]

# Latino
earn_ratios_df["ratio_L_BA_total"] = data_raw["Hispanic or Latino + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_L_AD_total"] = data_raw["Hispanic or Latino + Advanced Degree"] / data_raw["total"]
earn_ratios_df["ratio_L_SC_total"] = data_raw["Hispanic or Latino + Some College"] / data_raw["total"]
earn_ratios_df["ratio_L_HS_total"] = data_raw["Hispanic or Latino + High School"] / data_raw["total"]

## BY DEGREE + GENDER
# Male
earn_ratios_df["ratio_M_HS_total"] = data_raw["Male + High School"] / data_raw["total"]
earn_ratios_df["ratio_M_SC_total"] = data_raw["Male + Some College"] / data_raw["total"]
earn_ratios_df["ratio_M_BA_total"] = data_raw["Male + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_M_AD_total"] = data_raw["Male + Advanced Degree"] / data_raw["total"]

# Female
earn_ratios_df["ratio_F_HS_total"] = data_raw["Female + High School"] / data_raw["total"]
earn_ratios_df["ratio_F_SC_total"] = data_raw["Female + Some College"] / data_raw["total"]
earn_ratios_df["ratio_F_BA_total"] = data_raw["Female + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_F_AD_total"] = data_raw["Female + Advanced Degree"] / data_raw["total"]

## BY DEGREE + RACE + GENDER
# W + M + Degrees
earn_ratios_df["ratio_W_M_HS_total"] = data_raw["White + Male + High School"] / data_raw["total"]
earn_ratios_df["ratio_W_M_SC_total"] = data_raw["White + Male + Some College"] / data_raw["total"]
earn_ratios_df["ratio_W_M_BA_total"] = data_raw["White + Male + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_W_M_AD_total"] = data_raw["White + Male + Advanced Degree"] / data_raw["total"]

# W + F + Degrees
earn_ratios_df["ratio_W_F_HS_total"] = data_raw["White + Female + High School"] / data_raw["total"]
earn_ratios_df["ratio_W_F_SC_total"] = data_raw["White + Female + Some College"] / data_raw["total"]
earn_ratios_df["ratio_W_F_BA_total"] = data_raw["White + Female + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_W_F_AD_total"] = data_raw["White + Female + Advanced Degree"] / data_raw["total"]

# L + M + Degrees
earn_ratios_df["ratio_L_M_HS_total"] = data_raw["Hispanic or Latino + Male + High School"] / data_raw["total"]
earn_ratios_df["ratio_L_M_SC_total"] = (
    data_raw["Hispanic or Latino + Male + Some College"] / data_raw["total"]
)
earn_ratios_df["ratio_L_M_BA_total"] = (
    data_raw["Hispanic or Latino + Male + Bachelors Degree"] / data_raw["total"]
)
earn_ratios_df["ratio_L_M_AD_total"] = (
    data_raw["Hispanic or Latino + Male + Advanced Degree"] / data_raw["total"]
)

# L + F + Degrees
earn_ratios_df["ratio_L_F_HS_total"] = (
    data_raw["Hispanic or Latino + Female + High School"] / data_raw["total"]
)
earn_ratios_df["ratio_L_F_SC_total"] = (
    data_raw["Hispanic or Latino + Female + Some College"] / data_raw["total"]
)
earn_ratios_df["ratio_L_F_BA_total"] = (
    data_raw["Hispanic or Latino + Female + Bachelors Degree"] / data_raw["total"]
)
earn_ratios_df["ratio_L_F_AD_total"] = (
    data_raw["Hispanic or Latino + Female + Advanced Degree"] / data_raw["total"]
)

# B + M + Degrees
earn_ratios_df["ratio_B_M_HS_total"] = data_raw["Black + Male + High School"] / data_raw["total"]
earn_ratios_df["ratio_B_M_SC_total"] = data_raw["Black + Male + Some College"] / data_raw["total"]
earn_ratios_df["ratio_B_M_BA_total"] = data_raw["Black + Male + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_B_M_AD_total"] = data_raw["Black + Male + Advanced Degree"] / data_raw["total"]

# B + F + Degrees
earn_ratios_df["ratio_B_F_HS_total"] = data_raw["Black + Female + High School"] / data_raw["total"]
earn_ratios_df["ratio_B_F_SC_total"] = data_raw["Black + Female + Some College"] / data_raw["total"]
earn_ratios_df["ratio_B_F_BA_total"] = data_raw["Black + Female + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_B_F_AD_total"] = data_raw["Black + Female + Advanced Degree"] / data_raw["total"]

# A + F + Degrees
earn_ratios_df["ratio_A_M_HS_total"] = data_raw["Asian + Male + High School"] / data_raw["total"]
earn_ratios_df["ratio_A_M_SC_total"] = data_raw["Asian + Male + Some College"] / data_raw["total"]
earn_ratios_df["ratio_A_M_BA_total"] = data_raw["Asian + Male + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_A_M_AD_total"] = data_raw["Asian + Male + Advanced Degree"] / data_raw["total"]

# A + F + Degrees
earn_ratios_df["ratio_A_F_HS_total"] = data_raw["Asian + Female + High School"] / data_raw["total"]
earn_ratios_df["ratio_A_F_SC_total"] = data_raw["Asian + Female + Some College"] / data_raw["total"]
earn_ratios_df["ratio_A_F_BA_total"] = data_raw["Asian + Female + Bachelors Degree"] / data_raw["total"]
earn_ratios_df["ratio_A_F_AD_total"] = data_raw["Asian + Female + Advanced Degree"] / data_raw["total"]


earn_ratios_df = earn_ratios_df.reset_index()
earn_ratios_df = earn_ratios_df.rename(columns={"index": "year"})


##########################################
########## MELT THE RATIOS DF ############
##########################################
earn_ratios_df_melted = pd.melt(earn_ratios_df, id_vars=["year"])
earn_ratios_df_melted = earn_ratios_df_melted.rename(columns={"variable": "group", "value": "earn_ratios_%"})
earn_ratios_df_melted["earn_ratios_%"] = earn_ratios_df_melted["earn_ratios_%"].astype(float)
# earn_ratios_df_melted["earn_ratios_%"] = round(earn_ratios_df_melted["earn_ratios_%"])
earn_ratios_df_melted["earn_ratios_%"] = round(earn_ratios_df_melted["earn_ratios_%"] * 100, 2)

## READ IN UPDATED MELTED DF FROM CSV/.ipynb file
final_earn_ratios = load_data("earning_ratios_melted.csv", index_col=0)
