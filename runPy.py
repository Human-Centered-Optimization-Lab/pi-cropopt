import dssat4py
import os, numpy as np
from functools import reduce

path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
filex = "UFGA8201.MZX"

os.chdir(path)

dssat4py.readfilex(path, filex, 4)


dssat4py.printtest()

# 
#rawout = dssat4py.readfilex(path, filex, 2)

