# -*- coding: utf-8 -*-
"""
Created on Sat May 30 17:19:50 2020

@author: 44QRQZ1
"""

from model_building import 

import requests
from input_file import input_data

url ='http://127.0.0.1:5000/predict'
head = {'Content-Type': 'application/json'}
data = {'input_data':input_data}


res = requests.get(url,headers=head, json=data)

res.json()


#import sys
#import os
#os.getcwd()
#sys.path.append('E:\\OneDrive\\DS Journey\\DS_Projects\\ds_salary_proj')
#sys.path
#sys.path.append('/path/to/the/example_file.py')
