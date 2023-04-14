from utils.util_funcs import load_data
import pandas as pd

################################
### FEMALE TO MALE PAY RATIO ###
################################

data = load_data("edu_wages_2022.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

bar_data = data[(data["group"] == "total men") | (data["group"] == "total women")]
bar_data = bar_data.iloc[:, :27]

ratio_df = data[(data.group == "total men") | (data.group == "total women")]

data = pd.melt(data, id_vars=["group"])
data = data.rename(columns={"variable": "year"})
data_only = data[:2340]

data_filtered = data_only[(data_only["group"] == "total men") | (data_only["group"] == "total women")]

ratio_df = ratio_df[["group", "1995", "1996", "1997", "1998", "1999", "2000",
                     "2001", "2002", "2003", "2004", "2005", "2006", "2007",
                     "2008", "2009", "2010", "2011", "2012", "2013", "2014",
                     "2015", "2016", "2017", "2018", "2019", "2020",]]

ratio_df = ratio_df.T
ratio_df = ratio_df.tail(-1)
ratio_df.rename(columns={1: "total men", 2: "total women"}, inplace=True)

# RATIO OF FEMALE PAY TO MALE PAY
ratio_df["ratio"] = ratio_df["total women"] / ratio_df["total men"]

# HOURS WOMEN NEED TO WORK TO MATCH MEN PAY
# https://www.geeksforgeeks.org/applying-lambda-functions-to-pandas-dataframe/#
ratio_df = ratio_df.assign(hours=lambda x: (x["total men"] - x["total women"]) / (x["total women"] / 40))

ratio_df = ratio_df.reset_index()
ratio_df.rename(columns={"index": "year"}, inplace=True)


##########################
### FEMALE PAY BY RACE ###
##########################

data = load_data("edu_wages_2022.csv")
data.set_index("report_name")
data = data.rename(columns={"report_name": "group"})

# male baseline
male = data[(data['male'] == 1) & (data['all_edu'] == 1) & data['all_races'] == 1]
male = male.T
male = male.tail(-1)
male = male.reset_index()
male.rename(columns={"index": "year", 1: "men"}, inplace=True)
male = male.iloc[:26, :]

# female by race
female = data[(data['female'] == 1) & data['all_edu'] == 1]
female = female.T
female = female.tail(-1)
female = female.reset_index()
female.rename(columns={2: "Total women", 42: "White women",
                       43: "Hispanic or Latino women", 66: "Black women",
                       84: "Asian women", "index": 'year'}, inplace=True)
female = female.iloc[:26, :]