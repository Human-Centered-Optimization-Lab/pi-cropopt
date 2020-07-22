import numpy as np
from appCounter import app_counter
import matplotlib.pyplot as plt
from plotHV import get_nondoms

var_file = "/Users/iankropp/tempMount/run4/batch2020-07-16_16-23-26/gendat_with_run/run0000_gen0199_var.csv"
obj_file = "/Users/iankropp/tempMount/run4/batch2020-07-16_16-23-26/gendat_with_run/run0000_gen0199_obj.csv"

varz = np.genfromtxt(var_file, delimiter=',')
obj  = np.genfromtxt(obj_file, delimiter=',')

o2exclude = [1]

v2exclude = [102]

app_count = app_counter(varz, obj, v2exclude, o2exclude)

non_doms = get_nondoms(obj[:,(0,2)])

nitro_dates = varz[non_doms, 102]

print(app_count)
print(nitro_dates)

print(obj[non_doms, :])

plt.figure()
plt.scatter(obj[non_doms,2], -obj[non_doms,0])
plt.show()

