# Is Education the Key to Success?
#### Analysis by Miranda Cooper and Mike VerHulst

**Our Project**
You can find our dashboard by clicking the button below:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ed-dash.streamlit.app/)

### Table of Contents
- [Project Statement](#project-statement)
- [Challenges of Being an Embedded Data Scientist](#challenges-of-being-an-embedded-data-scientist)
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

Answering these questions posed an exciting challenge for us because neither of us studied economics in our undergraduate careers and we were curious to see if we could come to similar conclusions with our own analysis.

##### Our goal
After some discussion, we decided that the ultimate goal for our project would be to build a dashboard that could convey our findings in a way that is accessible and easy to understand for the general public. We found that some of the academic and news articles we had come across in our preliminary search required a significant background in economics to understand and we wanted to build a tool that would help normal people learn  how they may be affected by broader economic forces at play in the U.S.

To achieve this goal, we framed our approach as data scientists embedded within a team of economists that wanted to educate the general public. This approach led to some significant challenges and as we’ll explain below.

### Challenges of Being an Embedded Data Scientist
##### Learning a new domain on your own
Perhaps the biggest challenge we faced while assuming the role of embedded data scientists was coming into a field that was completely foreign to us and having to teach ourselves the ins and outs of economics. After choosing to study productivity and wages we spent the following 2-3 weeks reading articles from various academic journals and news outlets as well as papers published by economic think tanks such as the [Economic Policy Institute](https://www.epi.org/) and the [Cato Institute](https://www.cato.org/) and found that practically every topic related to economics is extremely complicated and experts will have major differences of opinions based on their backgrounds and beliefs.

For example, at the start of our research we believed that there was likely just one generally accepted standard for how to measure productivity but that assumption turned out to be wrong. On a basic level, productivity is the comparison of the amount of goods and services produced (output) with the amount of inputs used to produce those goods and services [Bureau of Labor Statistics](https://www.bls.gov/k12/productivity-101/content/what-is-productivity/home.htm), but there is debate among economists as to which output and input measures most accurately reflect the market. As a non-expert in the field, it became very difficult to parse which measures were most accurate.

Choosing a dataset was not a straightforward task either. There are multiple federal datasets that track the metrics that we were interested in but they are conducted by different organizations and had different survey methodologies. The primary datasets we considered were the Bureau of Labor Statistics’ (BLS) [Current Population Survey](https://www.bls.gov/cps/) and the U.S. Census Bureau’s [American Community Survey](https://www.census.gov/programs-surveys/acs). Experts who have been using these datasets for years now may be able to quickly explain which dataset would be best for a given task but detailed breakdowns of the strengths and weaknesses of each dataset don’t seem to exist. As a result, we made our data choices based on the available documentation for each survey, ultimately choosing to go with the BLS’ Current Population Survey.

##### Unclear methodologies
In addition to challenges posed by choosing the best metrics, many of the analysis methodologies we encountered were not reproducible. In many cases, methodology sections were incomplete or vague in terms of which industries, ages, or other criteria they were considering which prevented us from reproducing the same analysis even if we had access to the same data. In other cases, analysis was done using proprietary or unpublished data. In fact, one of the initial [articles](https://www.epi.org/productivity-pay-gap/) that inspired us to examine productivity was written by the Economic Policy Institute but used unpublished data from the BLS so we could not reproduce it.

<img src="https://drive.google.com/uc?id=1lk3rvGABmKElLRLintUR6tnfmIqKP7fE"
     alt="EPI Disclaimer"
     style="display: block; margin-right: auto; margin-left: auto; width: 60%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
     border:1px solid black;" />

##### The pivot
After weeks of research, we realized that it would not be feasible to reproduce the analysis we initially wanted to do in the span of just a couple months. We also realized that a common theme in our research was related to differing wage outcomes for full time workers based on their demographics (primarily gender and race) and their level of educational attainment. With that in mind, we decided to still create a public facing dashboard but to shift our analysis away from productivity and towards how education and demographics can affect a person’s earnings over time.

### Methodology
##### The data and preprocessing
With our focus shifted, we chose to use the Current Population Survey (CPS) from BLS and began to collect our data. We downloaded the data for this project from the National Bureau of Economic Research (NBER) which had merged the CPS Outgoing Rotation Group data for each year going back to 1979. The Outgoing Rotation Group data contains responses to the survey at the individual level and has been pre-filtered to contain only responses from those 18 years or older. The number of responses for each year ranged from 271,000 to nearly 330,000. The data for this project can be found in the preprocessing folder of our [GitHib repository](https://github.com/mcverhulst/699_Mastery_Capstone/tree/main/preprocessing/CPS_ORG) or in our data access statement [below](#data-access).

Since we were interested in studying earnings we filtered each year to just those that were working full time (35+ hours a week). We further filtered the results to just the rows that had reported weekly earnings. Once filtered to the rows with relevant data, we converted the earnings to 2022 dollars to accommodate for inflation and allow for fair comparisons across the years. The conversion rates we used were sourced from an [online calculator](https://www.in2013dollars.com/) that uses inflation figures published by the U.S. Department of Labor to make its calculations.

##### Limitations of the data
One of the major factors that limits how well this data represents different demographic groups is how the survey is designed. For example, individuals are not able to self-identify their gender and are instead limited to the binary of male and female. Additionally, between 1996 and 2002 there were only 4 options for race (White, Black, American Indian, and Asian). According to the [documentation](https://data.nber.org/morg/docs/cpsx.pdf) for the data we used, after 1996 if a respondent marked their race as “other” they were placed in one of the other 4 existing categories.

As a result of these limitations, our results may not be directly applicable to individuals that do not fall neatly into these pre-defined groups.

##### The dashboard goals and audience
In the design stage of our project, we recognized the need to bring focus to the most pertinent questions that had been swirling through our minds as we dove head first into our research. Narrowing our focus proved challenging, but we found inspiration in the work of Elsie Lee-Robbins and Eytan Adar who discuss [Affective Learning Objectives for Communicative Visualizations](https://arxiv.org/abs/2208.04078), and with the help of a tool derived from [Anderson and Krathwol's Revised Bloom Taxonomy (2001)](http://visualobjectives.net/learnobj-cog.html), we developed learning objectives unique to each of our final questions, which would in turn become tabs of our final dashboard. While time only afforded us the ability to develop two of the planned four tabs of our final dashboard, we developed the following learning objectives in alignment with each:
1. The viewer will compare outcomes for different groups of people based on race, gender, and education.
2. The viewer will evaluate their earning potential based on educational attainment.
3. The viewer will conclude if obtaining an advanced degree will reduce their chances of being underemployed.
4. The viewer will differentiate between the value of union coverage or no union coverage based on educational attainment.

In bringing focus to our learning objectives, it was also our goal to keep a particular audience or viewer in mind during the development process. Our target audience was young professionals or students much like Mike and I. Individuals who perhaps had an undergraduate degree and some years of work experience, but were considering returning to school for higher education. Individuals who recently graduated and considering entering the job market or individuals looking to gain an understanding of how their current median wage aligns with that of the broader population. In essence, we wanted to ensure that our synthesis of this information was accessible to a broad audience, not just those with deep economic or data science expertise.



### Building the Dashboard
In early stages of planning our project, we researched and considered various tools for development of our dashboard with the initial goal of challenging ourselves to work with Python libraries and web frameworks that were unfamiliar to us. For this reason, the early prototypes of our project were developed in FastAPI and Bokeh, utilizing a personal cloud-computing platform, called Deta Space, to deploy publicly. We were successful in developing a backend database infrastructure on a test dataset with SQLite, as well as, setting up basic landing pages that included some of the necessary layout functionality for our dashboard. However, in assessing the scope of our semester-long project and considering the time constraints we had due to research and data-related decision-making on the frontend of the semester, we opted to pivot our tech stack to tools we’d leveraged in prior course projects. In addition, while the raw data acquired from the Current Population Survey was cumulatively quite large when stored in separate files, we were also able to drastically reduce the data size after preprocessing. To that end, instead of requiring a SQLite database, we were able to store the data in individual CSV files and read them into pandas for further manipulation prior to visualizing in Altair. We developed and deployed the front-end dashboard interactions using Streamlit and its free Community Cloud. Many decisions were made in the design process to ensure that we were presenting the data in a clear and accessible manner.

### Findings
After processing our data (including adjusting all figures to 2022 dollars) and creating our visualizations we had some interesting findings. The bulk of our analysis focused on examining the gender wage gap and the effect different levels of education can have on earnings.

##### The gender age gap
Our first step in examining the gender wage gap was comparing the median pay of men and women side by side over the years. When shown in a grouped bar chart, the difference of median pay between men and women is clear: **women do make significantly less money than men**. As part of this analysis we also calculated the female-to-male pay ratio over that same period and there is good and bad news. The good news is that the ratio has gotten better for women since 1995 but the bad news is that it only improved from **.727 in 1995 to .807 in 2020**.

<img src="https://drive.google.com/uc?id=1wT9QuvEPw0oBS5r7wh984OUvo7HhgxEa"
     alt="EPI Disclaimer"
     style="display: block; margin-right: auto; margin-left: auto; width: 90%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
     border:1px solid black;" />

When looking at the outcomes for women of different races we see that no group matches the median pay of men but Asian women do come the closest. Black and Hispanic or Latino women fare far worse with Hispanic or Latino making a mere 60% of men while working the same number of hours.

<img src="https://drive.google.com/uc?id=1t3bht11qMi7qGhkH5P6dfWn49_hkTm5O"
     alt="EPI Disclaimer"
     style="display: block; margin-right: auto; margin-left: auto; width: 90%;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
     border:1px solid black;" />

When calculating how many hours a woman would need to work to match the pay of a man the wage gap ratio becomes staggering. Fortunately, this figure has declined over the years but in 1995, women had to work an additional **15 hours into the next week** to make the same pay as men. By 2020 this figure had only dropped 36\% to 9.56 hours. However, when you extrapolate these results to account for a full 52 week work year, even in 2020 women would have to work **3.11 months** into the next year before they matched the pay of men.

<img src="https://drive.google.com/uc?id=1aUyrYZ0C0lKNz8HJHUEJEIzepNAOoI0a"
alt="EPI Disclaimer"
style="display: block; margin-right: auto; margin-left: auto; width: 90%;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
border:1px solid black;" />

It is worth noting again that the analysis in this project cannot account for all factors that affect the gender pay gap. According to Rakesh Kochhar, a Senior Researcher at the Pew Research Center, gender stereotypes and discrimination can have an effect on wages but societal norms (such as women being more likely to be caretakers for children or other family members) also play a role in perpetuating the gender wage gap ([The Enduring Grip of the Gender Pay Gap](https://www.pewresearch.org/social-trends/2023/03/01/the-enduring-grip-of-the-gender-pay-gap/)). Kochhar goes on to state that although the wage gap had closed significantly in the 1980s and 1990s, progress has stalled within the last 25 years. The results of our analysis are similar although it is important to distinguish that his analysis also included part time workers as well as workers who are 16 and 17 years old.

##### Earning potential
As [Elka Torpey (2018)](https://www.bls.gov/careeroutlook/2018/data-on-display/education-pays.htm), an economist in the Office of Occupational Statistics and Employment Projections at the Bureau of Labor Statistics, states, “It’s hard to quantify the full value of an education. But U.S. Bureau of Labor Statistics (BLS) data consistently show that, in terms of dollars, education makes sense”. As might be expected, we can also safely say based on our analysis that a higher education degree can lead to a higher earning potential. However, along with that, we can recognize the earning gap that materializes as additional degrees are attained. Between 1995 and 2020, the median weekly wage for individuals completing the Current Population Survey who reported their education level as Bachelor’s was consistently between 20-40% higher than the total median. In contrast, for individuals who reported their education level as Advanced Degree, including master’s, doctoral, or professional degree recipients, the median weekly wage was consistently even higher than the total median by about 60-80%, and initially peaked back in 1997 at 87%.

<img src="https://drive.google.com/uc?id=1SBUvuP5DWrz5WHZxRShQp1y_wGMW-aHS"
alt="EPI Disclaimer"
style="display: block; margin-right: auto; margin-left: auto; width: 90%;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
border:1px solid black;" />

At this high level of analysis, though, we lose the insight that can be gained from further parsing the data by Gender and Race. And in breaking down the data by individuals who identified themselves as Male or Female, Black, White, Hispanic or Latino, or Asian, we start to recognize additional earning gaps that materialize when we compare the median weekly wage not only by degree levels, but cross-sectioned with these various gender and racial identities. At this time also, we want to acknowledge the limitations of these categories, which result from limitations of the original survey design. But in moving forward with these limited categories, we see, for example, that the median weekly wage between 1995 and 2020 for men reporting an Advanced Degree was about 90-100% higher than the total median, while the median weekly wage for women reporting the same degree was only about 40-60% higher than the total median.

<img src="https://drive.google.com/uc?id=1JaN1sJFAME2jSxZADmYdzkcVFTd8z2y7"
alt="EPI Disclaimer"
style="display: block; margin-right: auto; margin-left: auto; width: 90%;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
border:1px solid black;" />

<img src="https://drive.google.com/uc?id=1Q6VIu9Id3RwR0GSG-7SIiNu2qBN670qH"
alt="EPI Disclaimer"
style="display: block; margin-right: auto; margin-left: auto; width: 90%;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
border:1px solid black;" />

As another example, we also saw that individuals who identified as Asian with an Advanced degree reported median weekly earnings from 1995 through 2020 between 75-100% higher than the total median, while individuals who identified as Black with an Advanced degree reported median weekly wages only about 40-60% higher than the total median. While there are many other factors that would likely need to be considered when analyzing these median weekly wages, we can recognize an obvious earning gap as it relates to gender and race.

<img src="https://drive.google.com/uc?id=1LF4Lw1kg9wJYYU294LswIzd6zTijzjNe"
alt="EPI Disclaimer"
style="display: block; margin-right: auto; margin-left: auto; width: 90%;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
border:1px solid black;" />

<img src="https://drive.google.com/uc?id=1qm4JcBaQDMg9kpweZjjdF5_mpNfjANaT"
alt="EPI Disclaimer"
style="display: block; margin-right: auto; margin-left: auto; width: 90%;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
border:1px solid black;" />

In returning to two of our many research inquiries
1. Does a higher education degree give you a better chance at wage growth?
2. Does any particular degree create one advantage of earning potential over another?

In response to these inquiries, we can state a resounding, “yes”! But we must also recognize the significant gaps and inequalities in earning potential as the data is further parsed and analyzed by both gender and race.


### Broader Impacts
Our intended impact for our project was to synthesize a complicated issue for a broader audience. We hoped that our dashboard would support young professionals and students like ourselves in making informed decisions related to education and career. Despite this well-intentioned goal, we do recognize the likelihood of oversimplification and potential erasure of certain parties as a result of limitations in the initial collection of our chosen data, as well as, general categorizing and parsing of the available data. There are, indeed, systematic social factors at play in how data is collected through surveys, like the Current Population Survey, and we view our dashboard as an exploration of the data that is currently available, as well as, an insight into the potential changes that should be made to its design.

### Future Work
In the future, we hope to expand on the topics for analysis that are currently represented by the tabs listed as “under construction” in our deployed dashboard. These topics include bringing focus to the impact of union coverage on an individual’s income, as well as, the impact of higher education degrees on an individual’s likelihood of underemployment (which we, like the [EPI](https://www.epi.org/data/#?subject=underemp), define as individuals who are unemployed, working part-time but wanting to work full-time, or wanting to work and looking for work but have recently stopped job seeking). In addition to these analyses, we would hope to return to our prototype, full stack infrastructure that would include developing a REST API via FastAPI and storing the data in a database, like SQLite or PostrgeSQL. As we explore additional topics, we will also be introducing additional datasets that increase the complexity of the relationships in our data.

### Statement of Work
##### Miranda’s Contributions
- Conducted research in topics related to gender wage gap, earning potential, and underemployment
- Researched tools and methods of dashboard development, including JavaScript, Altair, Streamlit, Plotly Dash, FastAPI, Bokeh, and Flask.
- Developed prototype SQLite database with test dataset and deployed a REST API via FastAPI and Deta Space
- Set up GitHub repository with dependencies and deployed Streamlit application via Streamlit Community Cloud
- Developed Earning Potential tab, including data manipulation, visualization, and page layout
- Wrote final report

##### Mike’s Contributions
- Conducted research on topics related to gender pay gap, and union coverage
- Researched and selected relevant datasets
- Collected data
- Conducted preprocessing including parsing multiple changes in survey coding to obtain consistent results over all years of the data
- Developed Gender Wage Gap tab, including data manipulation, visualization, and page layout
- Wrote final report

### Data Access Statement
The data for this project was sourced from the National Bureau of Economic Research (NBER). NBER compiled monthly data from the Bureau of Labor Statistic's Current Population Survey, which in turn gets its data by querying more than 50,000 households within the U.S. each month. More information and the data itself can be found on [NBER's website](https://www.nber.org/research/data/current-population-survey-cps-merged-outgoing-rotation-group-earnings-data).
