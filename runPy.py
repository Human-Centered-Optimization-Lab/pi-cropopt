import dssat4py
import os, numpy as np
from functools import reduce

path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
filex = "UFGA8201.MZX"

os.chdir(path)

dssat4py.readfilex(path, filex, 4)

dssat4py.setwsta("WXYZ")

dssat4py.printtest()
dssat4py.writetempx()

# 
#rawout = dssat4py.readfilex(path, filex, 2)

