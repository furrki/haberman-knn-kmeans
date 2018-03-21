import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

file = r'haberman.csv'
df = pd.read_csv(file)
print(df.columns)
print(df.mean())

ex, ey, ez, eres = [], [], [], [] # For Training
elen = 200

tx, ty, tz, tres = [], [], [], [] # For Testing


for i, age in enumerate(df[df.columns[0]]):
    if(i < elen):
        ex.append(age)
    else:
        tx.append(age)

for i, yearofop in enumerate(df[df.columns[1]]):
    if(i < elen):
        ey.append(yearofop)
    else:
        ty.append(yearofop)

for i, nr in enumerate(df[df.columns[2]]):
    if(i < elen):
        ez.append(nr)
    else:
        tz.append(nr)


for i, sur in enumerate(df[df.columns[3]]):
    if(i < elen):
        eres.append(sur)
    else:
        tres.append(sur)

print(df.columns)

def dist(x1, y1, z1, x2, y2, z2):
    return abs(x2-x1)+abs(y2-y1)+abs(z2-z1)
# KNN
def knn(px, py, pz):
    global ex,ey,ez,eres
    k = 3
    dists = []
    for x, y, z, res in zip(ex, ey, ez, eres):
        dists.append([dist(x, y, z, px, py, pz), res])

    dists.sort()
    classes = [0, 0]
    for i in range(k):
        classes[dists[i][1]-1] += 1
    if(classes[0] > classes[1]):
        return 1
    return 2

predicted = 0
n = 0
confmat = [[0,0],[0,0]]


for x, y, z, res in zip(tx, ty, tz, tres):
    pre = knn(x, y, z)
    
    confmat[res-1][pre-1] += 1
    if pre == res:
        predicted += 1
    n += 1
    
    
print("\nSuccess of kNN: "+str(predicted/n))
# K-Means    K = 2

c1 = [52, 62.8, 2.7]
c2 = [53.6, 62.8, 7.4]
c1e = c2.copy()
c2e = c1.copy()
set1 = []
set2 = []

a = 0
while(dist(c1[0],c1[1],c1[2],c1e[0],c1e[1],c1e[2]) + dist(c2[0],c2[1],c2[2],c2e[0],c2e[1],c2e[2]) > 0.01):
    i = 0
    for x, y, z, res in zip(ex, ey, ez, eres):
        d1 = dist(x, y, z, c1[0], c1[1], c1[2])
        d2 = dist(x, y, z, c2[0], c2[1], c2[2])
        if(d1 < d2):
            set1.append(i)
        else:
            set2.append(i)
        i += 1

    n = 0
    nx,ny,nz = 0,0,0
    for i in set1:
        nx += ex[i]
        ny += ey[i]
        nz += ez[i]
        n += 1
    c1e = c1.copy()
    c1 = [nx/n, ny/n, nz/n]


    n = 0
    nx,ny,nz = 0,0,0
    for i in set2:
        nx += ex[i]
        ny += ey[i]
        nz += ez[i]
        n += 1
    c2e = c2.copy()
    c2 = [nx/n, ny/n, nz/n]
    a += 1

ones, twos = [], []
for x, y, z, res in zip(tx, ty, tz, tres):
    d1 = dist(x, y, z, c1[0], c1[1], c1[2])
    d2 = dist(x, y, z, c2[0], c2[1], c2[2])

    if(d1 < d2):
        ones.append(res)
    else:
        twos.append(res)
    n += 1

success = ((ones.count(1)/len(ones))+(twos.count(2)/len(twos)))/2
print("Success of k-means: "+str(success))

ax = plt.axes(projection='3d')
ax.scatter(ex, ey, ez, c=eres, cmap='viridis', linewidth=0.5)

"""
ax = plt.axes(projection='3d')
ax.scatter(tx, ty, tz, c=tres, cmap='viridis', linewidth=0.5)

#print(df[df['Survival'] == 2].mean())
 
AgeAtOperation        52.017778
YearOfOperation       62.862222
NrPosAxillaryNodes     2.791111
Survival               1.000000

AgeAtOperation        53.679012
YearOfOperation       62.827160
NrPosAxillaryNodes     7.456790
Survival               2.000000

"""
