# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:13:55 2019

@author: cheikh_Moctar
"""
import pandas as pd
#import geopandas
from geopy.geocoders import Nominatim

def geocode(x, y):
    theater1 = {}
    df = pd.read_excel(x)
    #print(df.columns)
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    #locations = geopandas.tools.geocode(df['Address'])

    from geopy.extra.rate_limiter import RateLimiter
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df['location'] = df['Address'].apply(geocode)

    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    df.to_excel(y)

geocode('../bigscreenbiz_NY.xlsx', 'bigsb_geocoded.xlsx')