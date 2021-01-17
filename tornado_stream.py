# Written by: Nick Gerend, @dataoutsider
# Viz: "Big Screen", enjoy!

from scipy import interpolate
import pandas as pd
import numpy as np
import os
from math import isnan, pi, sin, cos

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
df = pd.read_csv(os.path.dirname(__file__) + '/interp.csv')
#endregion

#region alogrithm
list_xy = []
df_group_e = df.groupby('Entity').count()
df_group_e['Path'] = 0
df_group_y = df.groupby('Entity')['Year'].min()
df = pd.merge(df, df_group_y, on=['Entity'], how='left')
df_group = df.groupby('Year_x')
ix = 0
for year, group in df_group:
    group_sort = group.sort_values(by=['Year_y','Entity'], ascending=[True,True])
    half_value = group_sort['Hybrid_Value'].sum()/2
    moving_min = -half_value
    for i, row in group_sort.iterrows():
        min_value = moving_min
        max_value = group_sort['Hybrid_Value'][i]+moving_min
        entity = row['Entity']
        e_count = df_group_e['Year'][entity]
        
        path_min = e_count*2-df_group_e['Path'][entity]
        path_max = df_group_e['Path'][entity]
        value = group_sort['Hybrid_Value'][i]
        
        list_xy.append(point(ix, entity, year, min_value, path_min, value))
        list_xy.append(point(ix, entity, year, max_value, path_max, value))

        moving_min += group_sort['Hybrid_Value'][i]
        ix += 1
        df_group_e.at[entity, 'Path'] += 1
        #print(df_group_e['Path'][entity])
#endregion

#region tornado
df_out = pd.DataFrame.from_records([s.to_dict() for s in list_xy])
print(df_out)
#df_out.to_csv(os.path.dirname(__file__) + '/stream.csv', encoding='utf-8', index=False)
N = 80 #years
offset = 4.
min_year = df_out['x'].min()
import csv
import os
with open(os.path.dirname(__file__) + '/ts.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'entity', 'year', 'year_value', 'value', 'x', 'y', 'path'])
    for i in range(len(list_xy)):
        t = list_xy[i].x
        v = list_xy[i].y
        angle = (2.*pi)*(((t-min_year)%N)/N)
        angle_deg = angle * 180./pi
        angle_rotated = (abs(angle_deg-360.)+90.) % 360.
        angle_new = angle_rotated * pi/180.

        o = offset + 2.*offset*(t-min_year)/N
        #o = offset

        x = (o+v)*cos(angle_new)
        y = (o+v)*sin(angle_new)

        writer.writerow([i+1, list_xy[i].item, t, v, list_xy[i].value, x, y, list_xy[i].path])
#endregion

print('finished')