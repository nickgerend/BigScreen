# Written by: Nick Gerend, @dataoutsider
# Viz: "Big Screen", enjoy!

from math import sqrt, sin, cos, pi

class point:
    def __init__(self, index, row, column, item, x, y, path = -1, value = -1): 
        self.index = index
        self.row = row
        self.column = column
        self.item = item
        self.x = x
        self.y = y
        self.path = path
        self.value = value
    def to_dict(self):
        return {
            'index' : self.index,
            'row' : self.row,
            'column' : self.column,
            'item' : self.item,
            'x' : self.x,
            'y' : self.y,
            'path' : self.path,
            'value' : self.value }

def fan(points):

    if points % 2 != 0:
        points += 1

    x = []
    y = []
    path = []
    angle = -90.
    path_i = 1

    for i in range(points+1):
        x.append(sin(angle*pi/180.))
        y.append(cos(angle*pi/180.))
        path.append(path_i)
        angle += 1./points*180.
        path_i += 1

    path_i = int(points*2-points/2)+1
    for i in range(int(points/2)):
        x.append(x[i]+1.)  
        y.append(y[i]-1.)
        path.append(path_i)
        path_i -= 1

    path_i = int(points*2-1)+1
    for i in range(int(points/2)-1):
            x.append(x[i+(int(points/2)+1)]-1.)
            y.append(y[i+(int(points/2)+1)]-1.)
            path.append(path_i)
            path_i -= 1
    
    x.append(x[0])  
    y.append(y[0])
    path.append(points*2+1)

    return x,y,path

#region algorithm

x,y,p = fan(50)

r_c = 50
resolution = 50
list_xy = []
ix = 0
item = 1
x,y,p = fan(resolution)
xt = 0
yt = 0
offset = 0
for i in range(r_c):
    for j in range(r_c):      
        for k in range(resolution*2+1):
            list_xy.append(point(ix, j, i, item, x[k]+xt+offset, y[k]+yt, p[k]))
            ix +=1
        item += 1
        xt += 2
    xt = 0
    if offset == 0:
        offset = 1
    else:
        offset = 0
    yt -= 1
#endregion

#region output
import csv
import os
with open(os.path.dirname(__file__) + '/fan_test.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile, lineterminator = '\n')
    writer.writerow(['index', 'row', 'column', 'item', 'x', 'y', 'path'])
    for i in range(len(list_xy)):
        writer.writerow([list_xy[i].index, list_xy[i].row, list_xy[i].column, list_xy[i].item, list_xy[i].x, list_xy[i].y, list_xy[i].path])
#endregion