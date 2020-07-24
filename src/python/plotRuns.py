import sys
import matplotlib.pyplot as plt
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import numpy as np

objs_to_include = (0,2)

files = sys.argv[1:]

with_files = filter(lambda f : "with_run" in f  ,files)
without_files = filter(lambda f : "without_run" in f  ,files)


plt.figure()

for with_f in with_files:
    objs = np.genfromtxt(with_f, delimiter=',')
    fronts = NonDominatedSorting().do(objs[:,list(objs_to_include)]) 
    objs = objs[fronts[0][..., np.newaxis], objs_to_include]

    plt.scatter(objs[:,1], -objs[:,0], edgecolors="blue", facecolors='none')


for without_f in without_files:
    objs = np.genfromtxt(without_f, delimiter=',')
    fronts = NonDominatedSorting().do(objs[:,list(objs_to_include)]) 
    objs = objs[fronts[0][..., np.newaxis], objs_to_include]

    plt.scatter(objs[:,1], -objs[:,0], edgecolors="red", facecolors='none')



plt.show()

