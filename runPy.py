import dssat4py as d
import os, numpy as np
from functools import reduce



path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
pathfull = "%80s" % path
filex = "UFGA8201.MZX"
os.environ["DSSAT_HOME"] = path

os.chdir(path)

d.dssatwrap.PATHEX = pathfull
d.dssatwrap.FILEX = filex
d.dssatwrap.TRTNUM = 4

d.dssatwrap.readfilex()

d.dssatwrap.setirramt(3,66.0)

d.dssatwrap.printtest()
d.dssatwrap.writetempx()



