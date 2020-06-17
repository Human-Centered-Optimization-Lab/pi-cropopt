import dssat4py as d
import os, numpy as np
from functools import reduce


class Experiment: 

    def __init__(self, path, filex, treatment):

        pathfull = "%80s" % path
        os.environ["DSSAT_HOME"] = path

        os.chdir(path)

        d.dssatwrap.PATHEX = pathfull
        d.dssatwrap.FILEX = filex
        d.dssatwrap.TRTNUM = treatment

        d.dssatwrap.readfilex()

        d.dssatwrap.printtest()
        d.dssatwrap.writetempx()

   
        self._setup_irrigation()
            

    def _setup_irrigation(self):
       
        self.irrigation_count = d.dssatwrap.getnirr()

        self.irrigation_amounts = d.dssatwrap.getirramts(self.irrigation_count)
        self.irrigation_dates = d.dssatwrap.getirrdates(self.irrigation_count)
        self.irrigation_operations = d.dssatwrap.getirrops(self.irrigation_count)

        # Conver the byte strings to strings
        self.irrigation_operations = np.apply_along_axis(
                lambda a : a.tostring().decode("ascii"), 1, 
                self.irrigation_operations)

        




path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
filex = "UFGA8201.MZX"

exp = Experiment(path, filex, 4)

fa = 3

