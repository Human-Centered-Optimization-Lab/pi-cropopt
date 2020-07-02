from pymoo.algorithms.nsga3 import NSGA3
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
import numpy as np
from pymoo.configuration import Configuration
from datetime import datetime
import os
from numpy import genfromtxt
from cropover import Cropover
from pathlib import Path
from pymoo.factory import get_reference_directions

Configuration.show_compile_hint = False

from cropopt import CropOpt


### Parameters ###

max_run = 10

dateTimeObj = datetime.now()
timestamp = "%d-%02d-%02d_%02d-%02d-%02d" % (dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute, dateTimeObj.second)

seeds = genfromtxt('seeds.csv', delimiter=',')

seeds = seeds.astype(int)

dssat_home = "/home/ian/Projects/dssat4py/rundir/"
fileio = "/home/ian/Projects/dssat4py/rundir/DSSAT47.INP"
tempdir = "/tmp/"
outputdir = "/home/ian/Projects/dssat4py/src/python/output/"
timestamp = "%d-%02d-%02d_%02d-%02d-%02d" % (dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute, dateTimeObj.second)
outputdir = outputdir + "batch" + timestamp
Path(outputdir).mkdir(parents=True, exist_ok=True)
generations = 200

threads = 4 

date_ranges = np.array(np.matrix("[2017198, 2017299, 0, 10]"))

ref_dirs = get_reference_directions("energy", 3, 90, seed=1)

### Functions ###

def startRuns(with_co):

    for run in range(max_run):

        if with_co:
            seed = seeds[run]
            fileName = "with_run"
        else:
            seed = seeds[run + max_run]
            fileName = "without_run"


        gen_dir =  outputdir + "/gendat_%s/" % fileName
        Path(gen_dir).mkdir(parents=True, exist_ok=True)


        prob = CropOpt(threads, dssat_home, fileio, tempdir, 
                date_ranges, gen_dir, run, seed=seed)

        cropover = Cropover(eta=30, prob=1.0)

        if with_co:
            algorithm = NSGA3(pop_size=100, 
                    ref_dirs=ref_dirs,
                    eliminate_duplicates=True,
                    crossover=cropover)
        else: 
            algorithm = NSGA3(pop_size=100, 
                    ref_dirs=ref_dirs,
                    eliminate_duplicates=True)

        res = minimize(prob,
                       algorithm,
                       ('n_gen', generations),
                       seed=seed,
                       verbose=True)

        paretoFront = res.F
        paretoFront[:,1] = paretoFront[:,1]*-1

        np.savetxt("%s/%s%04d.csv" % (outputdir, fileName, run), paretoFront, delimiter=",")

        print("\n\n========== Run %d complete ==========\n\n" % run)


### Main ###

print("\n\n========== With CropOpt run starting ==========\n\n" )
startRuns(True)
print("\n\n========== With CropOpt run complete ==========\n\n" )
startRuns(False)
print("\n\n========== Without CropOpt run complete ==========\n\n")











