import dssat4py
import os


path = "/Users/iankropp/Projects/tryImportingDSSAT/rundir/"
filex = "UFGA8201.MZX"

os.chdir(path)

# 
dssat4py.readfilex(path, filex, 1)

