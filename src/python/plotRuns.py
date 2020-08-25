import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import numpy as np

objs_to_include = (0,1,2)

files = sys.argv[1:]

with_files = filter(lambda f : "with_run" in f  ,files)
without_files = filter(lambda f : "without_run" in f  ,files)


fig = plt.figure()

ax = fig.add_subplot(111,projection='3d')

x =[1,2,3,4,5,6,7,8,9,10]
y =[5,6,2,3,13,4,1,2,4,8]
z =[2,3,3,3,5,7,9,11,9,10]

#ax.scatter(x, y, z, c='r', marker='o')

#ax.set_xlabel('X Label')
#ax.set_ylabel('Y Label')
#ax.set_zlabel('Z Label')

#plt.show()

#sys.exit(0)

for with_f in with_files:
    objs = np.genfromtxt(with_f, delimiter=',')
    fronts = NonDominatedSorting().do(objs[:,list(objs_to_include)]) 
    objs = objs[fronts[0][..., np.newaxis], objs_to_include]

    ax.scatter(objs[:,1], objs[:,2], -objs[:,0], c='b', marker='o')

for without_f in without_files:
    objs = np.genfromtxt(without_f, delimiter=',')
    fronts = NonDominatedSorting().do(objs[:,list(objs_to_include)]) 
    objs = objs[fronts[0][..., np.newaxis], objs_to_include]

    ax.scatter(objs[:,1], objs[:,2],  -objs[:,0], c='r', marker='o')

ax.set_xlabel('App count')
ax.set_ylabel('Total irrigation')
ax.set_zlabel('Yield')



plt.show()

