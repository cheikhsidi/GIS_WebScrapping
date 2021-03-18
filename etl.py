import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

df = pd.read_csv("theaters_NewYork2.csv")
print(df.head())
# df = df.sort_values("name")
# print(df["name"])
df = df[df["location.state"] == 'NY']
# print(df)
df = df.drop_duplicates(
    subset=["name", "coordinates.longitude", "coordinates.latitude"])
df = df[["name", "location.address1", "location.city", "location.state",
         "location.zip_code", "location.display_address", "coordinates.latitude",
         "coordinates.longitude", "review_count", "rating"]].rename(columns={"location.address1":"address1",
                                                                    "location.city": "City", "location.state":"State", "location.zip_code":"Zip_Code",
                                                                    "location.display_address":"address", "coordinates.latitude":"Latitude", "coordinates.longitude":"Longitude"})
print(len(df))
# df.to_excel('yelp_theaters_nyc.xlsx')

engine = create_engine('postgresql://postgres:prayer5subhanallah@localhost:5432/theater_sdb')
df.to_sql('Yelp_NY_scrape', engine)
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
print(gdf.head())
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# # We restrict to South America.
ax = world[world.continent == 'North America'].plot(
    color='white', edgecolor='black')

# # We can now plot our ``GeoDataFrame``.s
gdf.plot(ax=ax, color='red')
print (df.columns)
# plt.show()
