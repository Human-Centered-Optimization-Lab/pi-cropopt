import numpy as np
from appCounter import app_counter
import matplotlib.pyplot as plt
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import sys 

# Constants 
offset = [10, 0]

o2exclude = [1]

v2exclude = [102]

if len(sys.argv) != 2 + 1: 
    print("Usage: %s VARIABLE_FILE OBJECTIVE_FILE" % sys.argv[0])
    sys.exit(1)

var_file = sys.argv[1]
obj_file = sys.argv[2]

varz = np.genfromtxt(var_file, delimiter=',')
obj  = np.genfromtxt(obj_file, delimiter=',')

# round the variables 
varz = np.around(varz)

app_count = app_counter(varz, obj, v2exclude, o2exclude)

non_doms = NonDominatedSorting().do(obj[:,(0,2)])[0]

nitro_dates = varz[non_doms, 102]

obj_non_dom = obj[non_doms,:]

plt.figure()

plt.scatter(obj_non_dom[:,2], -obj_non_dom[:,0])


for i, anno in enumerate(app_count):
    plt.annotate(anno, (obj_non_dom[i,2] + offset[0], -obj_non_dom[i,0] + offset[1]))


plt.show()



