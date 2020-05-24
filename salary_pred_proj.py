# -*- coding: utf-8 -*-
"""
Created on Sat May 16 20:51:32 2020

@author: Rohit
"""

#-- create new folder from git bash
#$ cd Documents
#$ mkdir ds_salary_proj
#$ cd ds_salary_proj
#$ git init

#then create a new reposatory in your account from browser, now after doing all the work link your folder with this repo as below.
#(make sure the project folder name and repo name is same)

import glassdoor_scrapper as gs
#import pandas as pd

path ="E:/OneDrive/DS Journey/DS_Projects/ds_salary_proj/chromedriver"
sleep_time = 5
location = 'us'

df = gs.get_jobs("Data-Scientist",1000,False,path,location,sleep_time)

df.to_csv("glassdoor_jobs2.csv")




#$ cd ds_salary_proj
#echo "# ds_salary_proj" >> README.md
#git add .
#git commit -m "uploaded scrapper and run code"
#git remote add origin https://github.com/rmsharma5989/ds_salary_proj.git
#git push -u origin master
                
#######################  extra info  ##########################
#git push -u origin master
#(this command gave me error, then i ran below command and then )

#git remote -v
#git push origin master
#(this command opened a popup window to enter credentials and then all pushed, received an email about "A personal access token has been added to your account")

