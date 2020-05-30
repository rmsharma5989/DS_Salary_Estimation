- Created a tool that estimates data science salaries (MAE ~ $ 6K) to help data scientists to negotiate their income when they get a job.  
- Scraped over 500 job descriptions from glassdoor using python and selenium  
- Cleaned up the data and Data Engineer using pandas data frame 
- Data engineer on few columns like below
- Did Exploratery data analysis with the help of differnet visualization libraries.  
- Optimized Linear, Lasso, Ridge and Random Forest Regressors using GridsearchCV to reach the best model.  
- Built a client facing API using flask.  

**Python Version**: 3.7  
**Packages**: seaborn, pandas, numpy, matplotlib, seaborn, scikit-learn, pickle, flask, json  
**For Web Framework Requirements**: pip install -r requirements.txt  
**Scraper Github:**:  https://github.com/arapfaik/scraping-glassdoor-selenium  
**Scraper Article:**: https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  
**Flask Productionization:**:https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2  


## Web Scrapping

Tweaked the web scrapper repo available at above github to get the 500 data science vacancies from glassdoor.com, and after scrapping we fetched below data  

* Job title  
* Salary Estimate  
* Job Description  
* Rating  
* Company  
* Location  
* Company Headquarters  
* Company Size  
* Company Founded Date  
* Type of Ownership  
* Industry  
* Sector  
* Revenue  
* Competitors  


## Data Cleaning  

After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes and created the following variables:

* Removed the rows without Salary  
* Removing unncessory columns like where we have exception or NULL values  
* Parsed the numeric data from columns which was containing alpha numeric values like salary column, Rating column  
* Added salary type colum to distinguish the annual and hourly salary  
* converted hourly salaries in annual  
* Separated location by city and state  
* Created company age column from founded year  
* Made columns for if different skills were listed in the job description:  
    - Python
    - R
    - Excel
    - AWS
    - MLE
    - Spark
    - Data Science  
* Column for simplified job title and Seniority  
* Column for description length  



## Exploratory Data Analysis

I looked at the distributions of the data, coorelation and the value counts for the various categorical and numeric variables. Below are a few highlights.

![EDA_Salary_by_Simp](https://raw.githubusercontent.com/rmsharma5989/ds_salary_proj/master/EDA_Salary_by_Simp.png?token=AD2PVLMKHRS66QG4MPMIBEC62JY6E)
![EDA_State](https://raw.githubusercontent.com/rmsharma5989/ds_salary_proj/master/EDA_State.png?token=AD2PVLLIFU6EY2OOGKADUUS62JZC6)
![EDA_Revenue](https://raw.githubusercontent.com/rmsharma5989/ds_salary_proj/master/EDA_Revenue.png?token=AD2PVLPWQX5YBNATW26SZVS62JZFU)
Word cloud for salary description column  
![EDA_wordcloud](https://raw.githubusercontent.com/rmsharma5989/ds_salary_proj/master/EDA_wordcloud.png?token=AD2PVLPZDLOC6GEDEITZBLS62JZJQ)  



## Model building

First, I transformed the categorical variables into dummy variables. I also split the data into train and tests sets with a test size of 20%.  

I tried four different models and evaluated them using Mean Absolute Error. I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.  

I tried four different models:
*  **Multiple Linear Regression**: Baseline for the model
* **Lasso Regression**: Because of the sparse data from the many categorical variables, I thought a normalized regression like lasso would be effective.  
* **Ridge Regression**: Becasue of sparse data i wanted to check if Ridge performs bette than Lasso and i for little improvement with Ridhe.  
* **Random Forest**: Again, with the sparsity associated with the data, I thought that this would be a good fit.

## Model Performance  

The Random Forest model far outperformed the other approaches on the test and validation sets.  



* **Multiple Linear Regression**: MAE = 13.72  
* **Lasso Regression**: MAE = 7.29  
* **Ridge Regression**: MAE = 7.12  
* **Random Forest**: MAE = 6.56  



## Productionization  


In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated salary.


