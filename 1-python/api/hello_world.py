# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:13:08 2019

@author: Dequan Er
"""

#hello_world.py

print("Hello Git world!")

import requests
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8902'
#r = requests.get(url)

try:
    r = requests.get(url)
except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"

print("Statues code:", r.status_code)

## save to a variable
response_dict = r.json()



# Exp
repo_dicts = response_dict['items']
print("Repositories returned:",len(repo_dicts))
repo_dict = repo_dicts[0]
print('\nKeys:',len(repo_dict))

for key in sorted(repo_dict.keys()):
   print(key)
