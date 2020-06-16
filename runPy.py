import dssat4py
import os, numpy as np
from functools import reduce



path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
pathfull = "%80s" % path
filex = "UFGA8201.MZX"
os.environ["DSSAT_HOME"] = path

os.chdir(path)

dssat4py.dssatwrap.PATHEX = pathfull
dssat4py.dssatwrap.FILEX = filex
dssat4py.dssatwrap.TRTNUM = 4

dssat4py.dssatwrap.readfilex()

dssat4py.dssatwrap.setirramt(3,66)

dssat4py.dssatwrap.printtest()
dssat4py.dssatwrap.writetempx()



