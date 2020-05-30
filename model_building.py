# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:21:08 2020

@author: Rohit Sharma
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('data_eda.csv')

# 1. choose relavent columns
df.columns
df_model = df[['Rating','Size', 'Type of ownership', 'Industry', 'Sector', 
               'Revenue','Salary_type','avg_salary','job_state', 'same_state', 
               'company_age','python_JD','rstudio_JD', 'spark_JD', 'aws_JD',
               'machinelearning_JD','datascience_JD', 'data_simp', 'seniority',
               'job_desc_len']]



# 2. get dummy data
df_dummy = pd.get_dummies(df_model)







# 3. train test split
from sklearn.model_selection import train_test_split

X = df_dummy.drop('avg_salary', axis=1)
y = df_dummy.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=1)








# 4. mutiple linear regression
    # 4.1 we are going to do the linear regression in statsmodels and will use their package in sklearn
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()  # it will give the compelte statistical modeling calculation summary

    # 4.2 linear regresion in sklearn
from sklearn.linear_model import LinearRegression, Lasso, Ridge
lm = LinearRegression()
lm.fit(X_train,y_train)

    # 4.3 cross validtion score in sklearn

from sklearn.model_selection import cross_val_score
np.mean(cross_val_score(lm,X_train,y_train,scoring="neg_mean_absolute_error", cv=3)) # -13.71838259998843








# 5. lasso regression

lm_l = Lasso(0.03) # best result given by alpha 0.03
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))

    # in lasso regression alpha is parameter and it's default value is 1, its value 0 is equal to linear
    # regression, and so we are going to check with different values of alpha, which value will give us 
    # best result

alpha = []
error= []

for i in range(1,100):
    alpha_val = i/100
    alpha.append(alpha_val)
    lml = Lasso(alpha=alpha_val)
    error.append(np.mean(cross_val_score(lm_l,X_train,y_train,scoring="neg_mean_absolute_error",cv=3)))

plt.cla()
plt.plot(alpha,error)    
    
    # when we plotted, it gaves us alpha value between 0.0 and 0.2 gaves us the better result. 
error = tuple(zip(alpha,error))
df_err = pd.DataFrame(error,columns=['alpha','error'])
df_err[df_err.error == max(df_err.error)] # 0.03(alpha) -7.287518(error)








# 6. Ridge Regression

lm_r = Ridge(0.54) # best result given by alpha 0.54
lm_r.fit(X_train,y_train)
np.mean(cross_val_score(lm_r,X_train,y_train,scoring="neg_mean_absolute_error",cv=3))

    
    # check same with ridge if we can improve our model accuracy by decreasing the our error
alpha = []
error= []

for i in range(1,100):
    alpha_val = i/100
    alpha.append(alpha_val)
    rm = Ridge(alpha=alpha_val)
    error.append(np.mean(cross_val_score(lm_r,X_train,y_train,scoring="neg_mean_absolute_error",cv=3)))


error = tuple(zip(alpha,error))
df_err = pd.DataFrame(error,columns=['alpha','error'])
df_err[df_err.error == max(df_err.error)] # 0.54(alpha) -6.557390(error)








# 7. random forest
from sklearn.ensemble import RandomForestRegressor 
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring="neg_mean_absolute_error", cv=3))









# 8. tune the models using GridSearchCV

from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)

gs.fit(X_train,y_train)  #11.48.31 - 12.00.56 : took 13 minutes 25 seconds

gs.best_score_ # -6.329449340379722
gs.best_estimator_ # n_estimators=30, min_samples_leaf=1,ccp_alpha=0.0, criterion='mse'

'''
RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=None, max_features='sqrt', max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_impurity_split=None, min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=30, n_jobs=None, oob_score=False,
                      random_state=None, verbose=0, warm_start=False)
'''







# 9. test ensamples

# so we prepared below all models, and lets test them with test data
    # Linear Regression model(lm) -13.71838259998843
    # Lasso Regression model (lm_l) -7.287518
    # Ridge Regresion model (lm_r) -7.12288779770865
    # Random forest (rf) - 6.55739028864096

predict_lm = lm.predict(X_test)
predict_lm_l = lm_l.predict(X_test)
predict_lm_r = lm_r.predict(X_test)
predict_rf = gs.best_estimator_.predict(X_test)


from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, predict_lm) # 10.718073779336335
mean_absolute_error(y_test, predict_lm_l) # 6.067613024518437
mean_absolute_error(y_test, predict_lm_r) # 6.29068653115861
mean_absolute_error(y_test, predict_rf) # 4.711064678004536


mean_absolute_error(y_test,(predict_lm+predict_rf)/2) # 6.60354896258138



##*********************************************************************************##
##****** Productionize a Machine Learning model with Flask and Heroku *************##
##https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2##
##*********************************************************************************##

# lets first pickle the model : Pickling converts the object into a byte stream which can
# be stored, transferred, and converted back to the original model at a later time. 
# Pickles are one of the ways python lets you save just about any object out of the box.

import pickle

pkl = {'model': gs.best_estimator_}
pickle.dump(pkl,open('model_file' + ".p", "wb"))


file_name ='model_file.p'
with open(file_name, 'rb') as pickled:
    data = pickle.load(pickled)
    model = data['model']

model.predict(X_test.iloc[1,:].values.reshape(1,-1))

# list(X_test.iloc[1,:]) #this was to take the first row input from our test set

################################################################
# Now we are gonna build a simple fask api, for that we need separate environment
# in comda prompt go to project folder
# >mkdir FlaskAPI
# >cd FlaskAPI
# >conda create -n flask_env python=3.7
# >conda activate flask_env
# >conda install flask
# >conda install pandas
# >conda install scikit-learn
# >pip freeze requirement.txt
# Inside the last directory we created, create a few files and another directory with the command line.
# >touch app.py ( type nul > app.py)
# >touch procfile ( type nul > procfile)
# >touch wsgi.py ( type nul > wsgi.py)
# >mkdit models




################################################################







