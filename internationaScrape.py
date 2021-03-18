#Importing the dependencies

from pandas.io.json import json_normalize
import numpy as np
import pandas as pd
import requests

cin = pd.read_excel('cinemasIds.xlsx')['Cinema'].to_list()
print(cin)
cit = pd.read_excel('CinemasIds.xlsx')['city'].to_list()
dfs = []
for c in cin:
    apikey = 'E4SFHaGawXf9UFrEFrSbnf40saXVOSiy'
    headers = {'X-API-Key': apikey}

    url = 'https://api.internationalshowtimes.com/v4/movies/?countries=US'

    # Adding Parameters to filter the search results like {'city_ids': '2215'}
    params = {'cinema_id': c, 'all_fields': True}

    # Making a get request to the API
    req = requests.get(url, params=params, headers=headers).json()

    # Creating a Dataframe of the json response 
    df = pd.json_normalize(req, 'movies')
    dfs.append(df)

df = pd.concat(dfs)
filename = 'showtimesUS.csv'
df = pd.DataFrame(df)
# df.to_csv(filename, encoding='utf-8', index=False)
# for dt in theaters:
print (len(df))

