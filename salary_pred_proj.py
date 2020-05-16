import glassdoor_scrapper as gs
#import pandas as pd

path ="E:/OneDrive/DS Journey/DS_Projects/ds_salary_proj/chromedriver"
sleep_time = 5
location = 'us'

df = gs.get_jobs("Data-Scientist",850,False,path,location,sleep_time)

df.to_csv("glassdoor_jobs.csv")

# parse out the salary info
# remove rating part from company name
# Location by State, rather than by City

