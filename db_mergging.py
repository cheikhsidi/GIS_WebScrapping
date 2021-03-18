import geopy.distance
import pandas as pd
import re

# Merging all databses into one 
folder = r"C:\Users\cheikh_Moctar\Documents\Upwork\Theaters_project\Theater_GIS_Project\GIS_Theaters_3rd\scratch\\"
def Merging():
    yelp = pd.read_excel(folder + 'yelp.xls')
    atom = pd.read_excel(folder + 'Atom_nyc.xls')[['Name', 'Address', 'Latitude', 'Longitude']]
    bigSc = pd.read_excel(
        folder + 'BigScreen.xls')[['Name', 'Address', 'Latitude', 'Longitude']]
    IntsShow = pd.read_excel(
        folder + 'International_NYC.xls')[['Name', 'Address', 'Latitude', 'Longitude']]

    # Adding Source Column
    yelp['Source'] = 'Yelp'
    atom['Source'] = 'Atom'
    bigSc['Source'] = 'Big Screen'
    IntsShow['Source'] = 'International Showtime'

    for i, item in yelp['Name'].items():
        if item in IntsShow['Name'].to_list():
            yelp.loc[i, 'Source'] = 'Yelp, IntShow'
        if item in atom['Name'].to_list():
            yelp.loc[i, 'Source'] = 'Yelp, Atom'
        if item in bigSc['Name'].to_list():
            yelp.loc[i, 'Source'] = 'Yelp, Big Screen'  

    for i, item in atom['Name'].items():
        if item in IntsShow['Name'].to_list():
            atom.loc[i, 'Source'] = 'Atom, IntShow'
        if item in yelp['Name'].to_list():
            atom.loc[i, 'Source'] = 'Atom, Yelp'
        if item in bigSc['Name'].to_list():
            atom.loc[i, 'Source'] = 'Atom, Big Screen'    

    for i, item in bigSc['Name'].items():
        if item in IntsShow['Name'].to_list():
            bigSc.loc[i, 'Source'] = 'Big Screen, IntShow'
        if item in yelp['Name'].to_list():
            bigSc.loc[i, 'Source'] = 'Big Screen, Yelp'
        if item in atom['Name'].to_list():
            bigSc.loc[i, 'Source'] = 'Big Screen, Atom' 

    dr_atom = atom[atom['Name'].isin(yelp['Name'].to_list())].index
    dr_bc = bigSc[bigSc['Name'].isin(yelp['Name'].to_list())].index
    dr_int = IntsShow[IntsShow['Name'].isin(yelp['Name'].to_list())].index

    yelp.drop_duplicates('Name', keep='first', inplace=True)
    atom.drop(dr_atom, axis=0, inplace=True)
    bigSc.drop(dr_bc, axis=0, inplace=True)
    IntsShow.drop(dr_int, axis=0, inplace=True)
    print(len(dr_atom), len(dr_bc), len(dr_int))


    db_NYC = yelp.append([atom, bigSc, IntsShow], sort=False)
    db_NYC.drop_duplicates('Name', keep='first', inplace=True)
    db_NYC.to_excel('merged_db_NYC.xlsx')
    print(len(db_NYC[db_NYC['Source'] == 'Yelp']), len(db_NYC[db_NYC['Source'] == 'Atom']), len(db_NYC[db_NYC['Source'] == 'Big Screen']), len(db_NYC[db_NYC['Source'] == 'International Showtime']), len(db_NYC))

# # Calculating the minimum closest cinema distance from each cineam site
df = pd.read_excel('merged_db_NYC_0322.xlsx')

# # Creating  distances
cols = ['Latitude', 'Longitude']
df['location'] = df[cols].apply(
    lambda row: ', '.join(row.values.astype(str)), axis=1)
df['location'] = df['location'].apply(
    lambda row: tuple(map(float, row.split(', '))))

# # Imax dataframe
Imax = df[df['Imax']== 'Imax']
NonImax = df[df['Imax'] != 'Imax']
# looping through each point ans calculating ditance 
for i, coor in df['location'].items():
    df['temp'] = NonImax['location'].apply(
        lambda row: geopy.distance.geodesic(coor, row).miles)
    mindist = df[df['temp']>0].min()['temp']
    print(mindist)
    df.at[i,"NearestIMAX_Name"] = df.loc[df['temp']== mindist, "Name"].iloc[0]
    df.loc[i, 'NearestIMAX_distance'] = round(mindist, 2)
    df.loc[i, 'IMAXAddress'] = df.loc[df['temp']== mindist, "Full Address"].iloc[0]

df[df['Imax'] == 'Imax'].to_excel('IMAX_Proxi.xlsx')
