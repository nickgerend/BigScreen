# Written by: Nick Gerend, @dataoutsider
# Viz: "Big Screen", enjoy!

from scipy import interpolate
import pandas as pd
import numpy as np
import os
from math import isnan, pi, sin, cos, exp

def sig_h(x1, y1, x2, y2, points):
    x = []
    y = []
    limit = 6.
    amin = 1./(1.+exp(limit))
    amax = 1./(1.+exp(-limit))
    da = amax-amin
    for i in range(points):
        i += 1
        xi = (i-1.)*((2.*limit)/(points-1.))-limit
        yi = ((1.0/(1.0+exp(-xi)))-amin)/da
        x.append((xi-(-limit))/(2.*limit)*(x2-x1)+x1)
        y.append((yi-(0.))/(1.)*(y2-y1)+y1)
    return list(zip(x,y))

class data:
    def __init__(self, index, item, time, value): 
        self.index = index
        self.item = item
        self.time = time
        self.value = value
    def to_dict(self):
        return {
            'index' : self.index,
            'item' : self.item,
            'time' : self.time,
            'value' : self.value }

class point:
    def __init__(self, index, item, x, y, path = -1, value = -1): 
        self.index = index
        self.item = item
        self.x = x
        self.y = y
        self.path = path
        self.value = value
    def to_dict(self):
        return {
            'index' : self.index,
            'item' : self.item,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value }

#region load data
dataset = 'multi'
cutoff = 2020

df = pd.read_csv(os.path.dirname(__file__) + '/imdb_12_30_2020_movie.csv')
df = df.loc[df['startYear']!='\\N']
df["startYear"] = pd.to_numeric(df["startYear"])
df = df.loc[df['language']=='en']

if dataset == 'multi':
    df = df.set_index(['tconst','startYear','language','label'])['genres'].str.split(',', expand=True).stack().reset_index(name='genre').drop('level_4',1)
    df['movie_id'] = df['tconst']+'_'+df['genre']
    df = df.groupby(['startYear', 'genre']).agg({'movie_id':pd.Series.nunique}).rename(columns={'movie_id':'count'}).reset_index()
    df = df.loc[df['startYear']<=cutoff]
    df = df.loc[df['genre'].isin(['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Musical','Mystery','Romance','Sci-Fi','Sport','Thriller','Undefined','War','Western'])]
    df.rename(columns={'genre': 'Item', 'startYear': 'Time', 'count': 'Value'}, inplace=True)
else:
    df = df.groupby(['startYear', 'label']).agg({'tconst':pd.Series.nunique}).rename(columns={'tconst':'count'}).reset_index()
    df = df.loc[df['startYear']<=cutoff]
    df = df.loc[df['label'].isin(['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Multiple','Music','Musical','Mystery','Romance','Sci-Fi','Sport','Thriller','Undefined','War','Western'])]
    df.rename(columns={'label': 'Item', 'startYear': 'Time', 'count': 'Value'}, inplace=True)
#endregion

#region time fill
t_min = df['Time'].min()
t_max = df['Time'].max()
val_min = 0.
df_group = df.groupby('Item')
data_list = []
ix = 0
for item, group in df_group:
    for i in range(t_max-t_min+1):
        i += t_min
        if i in list(group['Time']):
            value = group['Value'].loc[group['Time'] == i]
            data_list.append(data(ix, item, i, value._values[0]))
        else:
            data_list.append(data(ix, item, i, val_min))
        ix += 1
df_tf = pd.DataFrame.from_records([s.to_dict() for s in data_list])
df_tf.to_csv(os.path.dirname(__file__) + '/movie_genres.csv', encoding='utf-8', index=False)
#endregion

#region sigmoid fill
xy_list = []
df_group = df_tf.groupby('item')
ix = 0
j = 0
resolution = 31
for item, group in df_group:
    group_sort = group.sort_values(by=['time'], ascending=[True])
    for i, row in group_sort.iterrows():
        if ix > 0:
            x2 = group_sort['time'][i]
            y2 = group_sort['value'][i]
            
            #region reduced points
            # if y2 == y1:
            #     xy_list.append(point(x1, item, x1,  y1, 0, y1))
            #     xy_list.append(point(x2, item, x2,  y2, 0, y2))
            # else:
            #     xy_group_list = sig_h(x1, y1, x2, y2, resolution)
            #     for j in range(len(xy_group_list)):
            #         xy_list.append(point(x2, item, xy_group_list[j][0],  xy_group_list[j][1], 0, y2))
            #endregion

            xy_group_list = sig_h(x1, y1, x2, y2, resolution)
            for j in range(len(xy_group_list)):
                xy_list.append(data(j, item, xy_group_list[j][0],  xy_group_list[j][1]))

            x1 = x2
            y1 = y2
        else:
            x1 = group_sort['time'][i]
            y1 = group_sort['value'][i]
            ix += 1
            j += 0
    ix = 0
df_sf = pd.DataFrame.from_records([s.to_dict() for s in xy_list])
df_sf = df_sf.drop_duplicates(subset=['item', 'time', 'value'], keep='first')
#endregion

df_sf.to_csv(os.path.dirname(__file__) + '/movie_sig.csv', encoding='utf-8', index=False)