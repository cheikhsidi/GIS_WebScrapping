import folium
import pandas as pd


m = folium.Map(location=[42.36, -71.34], zoom_start=12)
df = pd.read_excel("nearest.xlsx")
tooltip = 'click for more info'
for i, d in df['location'].items():
    print(type(d))
    name = df.loc[df['location']== d, "Name"].iloc[0]
    marker = [df.loc[i, 'Latitude'], df.loc[i, 'Longitude']]
    folium.Marker(marker,radius=500, popup=f'<Strong>{name}</strong>', tooltip=tooltip).add_to(m)

m.save("map.html")
