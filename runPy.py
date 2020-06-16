import dssat4py
import os, numpy as np
from functools import reduce



path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
pathfull = "%80s" % path
filex = "UFGA8201.MZX"
os.environ["DSSAT_HOME"] = path

os.chdir(path)

dssat4py.mod.PATHEX = pathfull
dssat4py.mod.FILEX = filex
dssat4py.mod.TRTNUM = 4

#dssat4py.mod.readfilex(path, filex, 4)
dssat4py.mod.readfilex()

dssat4py.mod.setwsta("WXYZ")
dssat4py.mod.setlncu(77)
dssat4py.mod.setirramt(3,66)



dssat4py.mod.printtest()
dssat4py.mod.writetempx()

# 
#rawout = dssat4py.readfilex(path, filex, 2)

