import numpy as np 
from sklearn.neighbors import NearestNeighbors
import pandas as pd

def nn(x):
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='auto', metric='euclidean').fit(x)
    distances, indices = nbrs.kneighbors(x)
    return distances, indices

df = pd.read('db_merged)nyc.xlsx')

#This has the index of the nearest neighbor in the group, as well as the distance
nns = df.drop('car', 1).groupby('time').apply(lambda x: nn(x.as_matrix()))

groups = df.groupby('time')
nn_rows = []
for i, nn_set in enumerate(nns):
    group = groups.get_group(i)
    for j, tup in enumerate(zip(nn_set[0], nn_set[1])):
        nn_rows.append({'time': i,
                        'car': group.iloc[j]['car'],
                        'nearest_neighbour': group.iloc[tup[1][1]]['car'],
                        'euclidean_distance': tup[0][1]})

nn_df = pd.DataFrame(nn_rows).set_index('time')