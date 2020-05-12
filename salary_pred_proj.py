import glassdoor_scrapper as gs
#import pandas as pd

path ="E:/OneDrive/DS Journey/DS_Projects/ds_salary_proj/chromedriver"
sleep_time = 15
City = 'United States'

df = gs.get_jobs("Data Scientist",20,False,path,City,sleep_time)

# parse out the salary info
# remove rating part from company name
# Location by State, rather than by City
