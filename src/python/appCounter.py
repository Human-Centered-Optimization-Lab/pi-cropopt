import numpy as np
from plotHV import get_nondoms

#dat_file = "/Users/iankropp/tempMount/run4/gendat_with_run/run0000_gen0199_var.csv"
var_file = "/Users/iankropp/tempMount/run4/batch2020-07-16_16-23-26/gendat_with_run/run0000_gen0199_var.csv"
obj_file = "/Users/iankropp/tempMount/run4/batch2020-07-16_16-23-26/gendat_with_run/run0000_gen0199_obj.csv"

varz = np.genfromtxt(var_file, delimiter=',')
obj  = np.genfromtxt(obj_file, delimiter=',')

varz = varz[get_nondoms(obj[:,(0,2)]),:]

cols2exclude = [102]

col_count = np.size(varz,1)

cols = set(range(col_count))

for col2ex in cols2exclude: 
    cols.remove(col2ex)

varz = varz[:,list(cols)]

varz[varz != 0] = 1

totals_ones = np.sum(varz,1)    



b = 0

#totals_zeros =  


