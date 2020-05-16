# -*- coding: utf-8 -*-
"""
Created on Sat May 16 20:51:32 2020

@author: Rohit
"""

    # github pull, push and create new branch
    # git pull
    # git push
    # git checkout -b data_cleanup

import pandas as pd

df = pd.read_csv("glassdoor_jobs.csv")

# 1. drop unnecessory unnammed column
df = df.drop(['Unnamed: 0'], axis = 1)

# 2. remove the salary columns where we got Exception
df = df[~df['Salary Estimate'].str.contains("Exception")]

# 3. which columns contains exception and how many times, ( after replacing the column with -1 if condition is changed in below function)
exception_columns = {}
for cname in df.columns:
    for text in df[cname]:
        if text.strip() == '-1': #if '-1 Exception' in text:
            if cname in exception_columns.keys():
                exception_columns[cname] = (exception_columns[cname]) +1
            else:
                exception_columns[cname] = 1
                
exception_columns


# 4. wherever we got exception we will put -1 ( this you can do with lambda also)
df.loc[df['Job Description'].str.contains('-1 Exception'), 'Job Description'] = '-1'
df.loc[df['Rating'].str.contains('-1 Exception'), 'Rating'] = '-1'
df.loc[df['Headquarters'].str.contains('-1 Exception'), 'Headquarters'] = '-1'
df.loc[df['Founded'].str.contains('-1 Exception'), 'Founded'] = '-1'
df.loc[df['Type of ownership'].str.contains('-1 Exception'), 'Type of ownership'] = '-1'
df.loc[df['Industry'].str.contains('-1 Exception'), 'Industry'] = '-1'
df.loc[df['Sector'].str.contains('-1 Exception'), 'Sector'] = '-1'
df.loc[df['Revenue'].str.contains('-1 Exception'), 'Revenue'] = '-1'
df.loc[df['Competitors'].str.contains('-1 Exception'), 'Competitors'] = '-1'


# 5. Salary parsing
df["Salary_type"] = df['Salary Estimate'].apply(lambda x : 'Glassdoor' 
         if 'glassdoor est.' in x.lower() and 'per hour' not in x.lower()
         else ('Per_hour' if 'per hour' in x.lower() else 'Employer' )
         )
    
    # two days to do add salary type
    #df["Salary_type"] = df.apply(lambda x : 'Glassdoor' 
    #        if 'glassdoor est.' in x['Salary Estimate'].lower() and 'per hour' not in x['Salary Estimate'].lower()
    #         else ('Per_hour' if 'per hour' in x['Salary Estimate'].lower() else 'Employer' )
    #         ,axis =1)


    #df['Salary Estimate'] = df['Salary Estimate'].str.split("(").str[0]
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x : x.split("(")[0])

    #df['Salary Estimate'] = df['Salary Estimate'].str.replace('Per Hour','')
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace('Per Hour',''))

    #df['Salary Estimate'] = df['Salary Estimate'].str.replace('$','')
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace('$',''))

    #df['Salary Estimate'] = df['Salary Estimate'].str.replace('K','')
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace('K',''))

    #df['Salary Estimate'] = df['Salary Estimate'].str.replace(' ','')
df['Salary Estimate'] = df['Salary Estimate'].apply(lambda x: x.replace(' ',''))

df['min_salary'] = df['Salary Estimate'].apply(lambda x : int(x.split('-')[0]))
df['max_salary'] = df['Salary Estimate'].apply(lambda x : int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary + df.max_salary)/2



# 6. From company name remove ratings

df['Company_text'] = df.apply(lambda x : x['Company Name'] if float(x['Rating']) < 0 else x['Company Name'][:-3] ,axis = 1)

    # two ways of droping a column in pandas
    #df = df.drop('Complany_text', axis=1)
    #df = df.drop('Complany Name', axis=1)    
    #df = df.drop(['Complany_text','Complany Name'], axis = 1)



# 7. State field
df['job_city'] = df['Location'].apply(lambda x : x.split(',')[0].strip())
df['job_state'] = df['Location'].apply(lambda x : x.split(',')[1].strip())

    #Work location and headquarters are same location or not
df['same_state'] = df.apply(lambda x : 1 if x['Location'] == x['Headquarters'] else 0, axis=1)



# 8. Age of company
df['company_age'] = df['Founded'].apply(lambda x: 2020 - int(x) if x != '-1' else '-1')


# 9. Job Description

    # Python
    # r studio
    # spark
    # aws
    # excel
    # machine learning
    # data science

df['python_JD'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_JD.value_counts()

df['rstudio_JD'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
df.rstudio_JD.value_counts()

df['spark_JD'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark_JD.value_counts()

df['aws_JD'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws_JD.value_counts()

df['machinelearning_JD'] = df['Job Description'].apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
df.machinelearning_JD.value_counts()

df['datascience_JD'] = df['Job Description'].apply(lambda x: 1 if 'data science' in x.lower() else 0)
df.datascience_JD.value_counts()


df.to_csv('glassdoor_jobs_cleared_data.csv', index = False)

    # git hub push the changes in new branch and merge with master branch by creating new pull request
    # git add . ( make sure you are in newly created branch)
    # git commit -m 'data cleaning task done'
    # git push ( will ask to set  this as upstream)
    # git push --set-upstream origin data_cleanup
    # now create new pull request from browser and merge the changes with master branch




























