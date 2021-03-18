import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

df = pd.read_csv("theatersUS.csv")
print(df.head())
# df = df.sort_values("name")
# print(df["name"])
# df = df[df["location.address.state_abbr"] == 'NY']
# print(df)
df = df.drop(['slug', 'chain_id', 'city_id',
              'telephone', 'website', 'booking_type', 'location.address.country'], axis=1)
df = df.drop_duplicates(
    subset=["name", "location.lon", "location.lat", "location.address.display_text"])
df = df.rename(columns={"location.address.street": "address1", "location.address.city": "City", "location.address.state_abbr": "State",
                        "location.address.zipcode": "Zip_Code", "location.address.display_text": "address", "location.lat": "Latitude", 
                        "location.lon": "Longitude", "location.address.country_code": "Country"})
print(len(df))
# df.to_excel('yelp_theaters_nyc.xlsx')

# engine = create_engine(
#     'postgresql://postgres:prayer5subhanallah@localhost:5432/theater_sdb')
# df.to_sql('IntenationalTheaters_US', engine)
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
# print(gdf.head())
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# # We restrict to South America.
ax = world[world.continent == 'North America'].plot(
    color='white', edgecolor='black')

# subset the dataframe
# print(df[df['Longitude'] <= -94])

# Let us create a buffer of 500, 200, 100 meters and plot them
# projecting
gdf.crs = "EPSG:4326"


# Creating buffers 
# gdf_500 = gdf.buffer(500)
# # # We can now plot our ``GeoDataFrame``.s
gdf .plot(ax=ax, color='blue')
# Let us plot
# fig, ax = plt.subplots(figsize=(8, 6))
#vastra.plot(ax=ax)
# gdf_500.plot(ax=ax, color='lightblue')
plt.show()

