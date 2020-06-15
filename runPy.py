import dssat4py
import os, numpy as np
from functools import reduce

path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
filex = "UFGA8201.MZX"

os.chdir(path)

# 
rawout = dssat4py.readfilex(path, filex, 4)

int_vals = rawout[0]
int_names_raw = rawout[1]


int_names = []

for row in range(np.size(int_names_raw, 0)): 
    string = reduce((lambda x, y: x + y ), int_names_raw[row,:]).decode("ascii")
    int_names.append(string.strip())

exp_vars = {}

for ivar in range(len(int_vals)):
    exp_vars[int_names[ivar]] = int_vals[ivar]
    
print(exp_vars)



