# Is Education the Key to Success?
#### Analysis by Miranda Cooper and Mike VerHulst

**Our Project**
You can find our dashboard by clicking the button below:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ed-dash.streamlit.app/)

### Table of Contents
- [Project Statement](#project-statement)
- [Challenges of Being an Embedded Data Scientist](#challenges-of-being-an-embedded-data-scientist-mike)
- [Methodology](#methodology)
- [Building the Dashboard](#building-the-dashboard)
- [Findings](#findings)
- [Broader Impacts](#broader-impacts)
- [Future Work](#future-work)
- [Statement of Work](#statement-of-work)
- [Data Access Statement](#data-access-statement)

### Project Statement
##### Choosing a topic
When looking for inspiration for our data science project, both of us remembered seeing articles from news outlets, blogs, and other sources stating that over the last several decades productivity in the United States had grown considerably while wages for workers have remained relatively stagnant. After doing some quick searches online we were curious to examine two questions:
1. Was this claim true?
2. If so, what was causing the gap to grow?

<img src="https://drive.google.com/uc?id=131m1xdJCfaBmS5qYauNfMN0ndH-EGZlj"
     alt="EPI Disclaimer"
     style="display: block; margin-right: auto; margin-left: auto; width: 50%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
     border:1px solid black;" />

Answering these questions was an exciting challenge for us because neither of us studied economics in our undergraduate careers and we were curious to see if we could come to similar conclusions after our analysis.

##### Our goal
After some discussion, we decided that the ultimate goal for our project would be to build a dashboard that could convey our findings in a way that is accessible and easy to understand for the general public. We found that some of the academic and news articles we had come across in our preliminary search required a significant background in economics to understand and we wanted to build a tool that would help normal people understand how they are affected by the broader economic forces at play in the U.S.

To achieve this goal, we framed our approach as data scientists embedded within a team of economists that wanted to educate the general public. This approach led to some significant challenges and as we’ll explain below.

### Challenges of Being an Embedded Data Scientist
##### Learning a new domain on your own
Perhaps the biggest challenge we faced while assuming the role of embedded data scientists was coming into a field that was completely foreign to us and having to teach ourselves the ins and outs of that field. After choosing to study productivity and wages we spent the following 2-3 weeks reading articles from various academic journals and news outlets as well as papers published by economic think tanks such as the [Economic Policy Institute](https://www.epi.org/) and the [Cato Institute](https://www.cato.org/) and found that every topic related to economics is very complicated and will have major differences of opinions based on who you talk to.

For example, at the start of our research we believed that there was likely one generally accepted standard for how to measure productivity but that assumption turned out to be wrong. On a basic level, productivity is the amount of goods and services produced (output) with the amount of inputs used to produce those goods and services ([Bureau of Labor Statistics](https://www.bls.gov/k12/productivity-101/content/what-is-productivity/home.htm)), but there is debate among economists as to which output and input measures most accurately reflect the market. As a non-expert in the field, it became very difficult to parse which measures were most accurate.

Choosing a dataset was not a straightforward task either. There are multiple federal datasets that track the metrics that we were interested in but they are conducted by different organizations and had different survey methodologies. The primary datasets we considered were the Bureau of Labor Statistics’ (BLS) [Current Population Survey](https://www.bls.gov/cps/) and the U.S. Census Bureau’s [American Community Survey](https://www.census.gov/programs-surveys/acs). Experts who have been familiar with these datasets may be able to quickly explain which dataset would be best for a given task but detailed breakdowns of the strengths and weaknesses of each dataset don’t seem to exist. As a result, we made our data choices based on the available documentation for each survey.

##### Unclear methodologies
In addition to challenges posed by choosing the best metrics, many of the analysis methodologies we encountered were not reproducible. In many cases, methodology sections were incomplete or vague which prevented us from reproducing the same analysis even if we had access to the same data. In other cases, analysis was done using proprietary or unpublished data. In fact, one of the initial [articles](https://www.epi.org/productivity-pay-gap/) that inspired us to examine productivity was written by the Economic Policy Institute but used unpublished data from the BLS so we could not reproduce it.

<img src="https://drive.google.com/uc?id=1lk3rvGABmKElLRLintUR6tnfmIqKP7fE"
     alt="EPI Disclaimer"
     style="display: block; margin-right: auto; margin-left: auto; width: 60%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
     border:1px solid black;" />

##### The pivot
After weeks of research, we realized that it would not be feasible to reproduce the analysis we initially wanted to do in the span of just a couple months. We also realized that a common theme in our research was related to differing wage outcomes for full time workers based on their demographics (primarily gender and race) and their level of educational attainment. With that in mind, we decided to still create a public facing dashboard but to shift our analysis away from productivity and towards how education and demographics can affect a person’s earnings over time.

### Methodology
##### The data and preprocessing
With our focus shifted, we chose to use the Current Population Survey (CPS) from BLS and began to collect our data. We downloaded the data for this project from the National Bureau of Economic Research (NBER) which had merged the CPS Outgoing Rotation Group data going back to 1979. The Outgoing Rotation Group data contains responses to the survey at the individual level and has been pre-filtered to contain only responses from those 18 years or older. The number of responses for each year ranged from 271,000 to nearly 330,000. The data for this project can be found in the preprocessing folder of our [GitHib repository](https://github.com/mcverhulst/699_Mastery_Capstone/tree/main/preprocessing/CPS_ORG) or in our data access statement [below](#data-access).

Since we were interested in studying earnings we filtered each year to just those that were working full time (35+ hours a week). We further filtered the results to just the rows that had reported weekly earnings. Once filtered to the rows with relevant data, we converted the earnings to 2022 dollars to accommodate for inflation and allow for fair comparisons across the years. The conversion rates we used were sourced from an [online calculator](https://www.in2013dollars.com/) that uses inflation figures published by the U.S. Department of Labor to make its calculations.

##### Limitations of the data
One of the major factors that limits how well this data represents different demographic groups is how the survey is designed. For example, individuals are not able to self-identify their gender and are instead limited to the binary of male and female. Additionally, between 1996 and 2002 there were only 4 options for race (White, Black, American Indian, and Asian). According to the [documentation](https://data.nber.org/morg/docs/cpsx.pdf) for the data we used, after 1996 if a respondent marked their race as “other” they were placed in one of the other 4 existing categories.

As a result of these limitations, our results may not be directly applicable to individuals that do not fall neatly into these pre-defined groups.

##### The dashboard goals/audience

### Building the Dashboard

### Findings
##### The gender age gap

##### Earning potential


### Broader Impacts

### Future Work

### Statement of Work

### Data Access Statement
The data for this project was sourced from the National Bureau of Economic 
Research (NBER). NBER compiled monthly data from the Bureau of Labor 
Statistic's Current Population Survey, which in turn gets its data by querying more than 50,000 households within the U.S. each month. More information and the data itself can be found on [NBER's website](https://www.nber.org/research/data/current-population-survey-cps-merged-outgoing-rotation-group-earnings-data).
