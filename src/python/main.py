from pymoo.algorithms.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
import numpy as np
from pymoo.configuration import Configuration
from datetime import datetime
import os
from numpy import genfromtxt
from cropover import Cropover
from pathlib import Path

Configuration.show_compile_hint = False

from cropopt import CropOpt


max_run = 50 

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

threads = 4 

date_ranges = np.array(np.matrix("[2017135, 2017140, 1, 20; 2017200, 2017204, 0, 19]"))


# Runs with cropover
for run in range(max_run):

    seed = seeds[run + max_run]



    prob = CropOpt(threads, dssat_home, fileio, tempdir, 
            date_ranges, outputdir, run, seed=seed)

    cropover = Cropover(eta=30, prob=1.0)

    algorithm = NSGA2(pop_size=100, 
            eliminate_duplicates=True,
            #sampling=s_sampler,
            crossover=cropover)

    res = minimize(prob,
                   algorithm,
                   ('n_gen', 200),
                   seed=seed,
                   verbose=True)

    print("Optima with regards to yield: %d" % prob.get_optimal())

    paretoFront = res.F
    paretoFront[:,1] = paretoFront[:,1]*-1
    
    dir_name = "results/%s" % timestamp

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    np.savetxt("%s/with_run%04d.csv" % (dir_name,run), paretoFront, delimiter=",")


# Runs without cropover
for run in range(max_run):

    seed = seeds[run]

    prob = Cropover(seed=seed)
    cropover = Cropover(eta=30, prob=1.0)

    algorithm = NSGA2(pop_size=100, 
            eliminate_duplicates=True)#,
            #sampling=s_sampler)

    res = minimize(prob,
                   algorithm,
                   ('n_gen', 200),
                   seed=seed,
                   verbose=True)

    print("Optima with regards to yield: %d" % prob.get_optimal())

    paretoFront = res.F
    paretoFront[:,1] = paretoFront[:,1]*-1
    
    dir_name = "results/%s" % timestamp
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    np.savetxt("%s/without_run%04d.csv" % (dir_name,run), paretoFront, delimiter=",")










