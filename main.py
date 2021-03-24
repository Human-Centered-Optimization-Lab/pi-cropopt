from pymoo.algorithms.nsga4 import NSGA3
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
import psutil
from SparseSampler import SparseSampler


Configuration.show_compile_hint = False

from cropopt import CropOpt


### Parameters ###

max_run = 10

dateTimeObj = datetime.now()
timestamp = "%d-%02d-%02d_%02d-%02d-%02d" % (dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute, dateTimeObj.second)

seeds = genfromtxt('seeds.csv', delimiter=',')

seeds = seeds.astype(int)

dssat_home = "/mnt/home/kroppian/Projects/cropopt/rundir/"
dssat_exe = "/mnt/home/kroppian/Projects/cropopt/dscsm047"
fileio = "/mnt/home/kroppian/Projects/cropopt/rundir/DSSAT47.INP"
tempdir = "/mnt/scratch/kroppian/"
outputdir = "/mnt/home/kroppian/Projects/cropopt/src/python/output/"
timestamp = "%d-%02d-%02d_%02d-%02d-%02d" % (dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute, dateTimeObj.second)
outputdir = outputdir + "batch" + timestamp
Path(outputdir).mkdir(parents=True, exist_ok=True)
generations = 200

sample_sparsity = 20

pop_size = 100

threads = 20

# 
# Irrigation type 
# Col 1: Period begin date
# Col 2: Period end date
# Col 3: IRR=0,
# Col 4: IRR min
# Col 5: IRR max
# Col 6: 0
# Col 7: 0
#

# 
# Nutrient type 
# Col 1: Period begin date
# Col 2: Period end date
# Col 3: NUT=1,
# Col 4: Nitrogen amount
# Col 5: Phos amount
# Col 6: Pot amount
#
date_ranges = np.array(
        np.matrix("""
        [2017198, 2017299, 0,   0,  10, 0;
         2017190, 2017200, 1, 200,   0, 0 
            ]""")
    )

constant_apps = np.array([[2017135, 0, 70, 10, 4]])

ref_dirs = get_reference_directions("energy", 3, 90, seed=1)

### Functions ###

def startRuns(with_co):

    for run in range(max_run):

        ## START -- Analyze memory 
        mem_avail = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total 
        print("-----------Start Mem sitch:-----------")
        print("Mem_avail %d" % mem_avail)

        print("-----------End mem sitch-----------")
        ## END -- Analyze memory 


        if with_co:
            seed = seeds[run]
            fileName = "with_run"
        else:
            seed = seeds[run + max_run]
            fileName = "without_run"


        gen_dir =  outputdir + "/gendat_%s/" % fileName
        Path(gen_dir).mkdir(parents=True, exist_ok=True)

        nutrient_inds = CropOpt.calc_period_indices(CropOpt, date_ranges)[1]
        nutrient_inds = [a[1] for a in nutrient_inds]

        s_sampler = SparseSampler(sample_sparsity, sampled_mask=nutrient_inds)

        prob = CropOpt(threads, dssat_home,dssat_exe, fileio, tempdir, 
                date_ranges, gen_dir, run, seed=seed, constant_apps=constant_apps)

        cropover = Cropover(eta=30, prob=1.0)

        if with_co:
            algorithm = NSGA3(pop_size=pop_size, 
                    ref_dirs=ref_dirs,
                    eliminate_duplicates=True,
                    crossover=cropover,
                    sampling=s_sampler)
        else: 
            algorithm = NSGA3(pop_size=pop_size, 
                    ref_dirs=ref_dirs,
                    eliminate_duplicates=True,
                    sampling=s_sampler)

        res = minimize(prob,
                       algorithm,
                       ('n_gen', generations),
                       seed=seed,
                       save_history=True,
                       verbose=True)

        paretoFront = res.F
        paretoFront[:,1] = paretoFront[:,1]*-1


        for gen in res.history:

            gen_n = gen.n_gen
           
            objectives = np.array([indiv.F for indiv in gen.pop ])
            x = np.array([indiv.X for indiv in gen.pop ])

            # save generational data 
            np.savetxt("%s/run%04d_gen%04d_obj.csv" % (gen_dir, run, gen_n), objectives, delimiter=",")
            np.savetxt("%s/run%04d_gen%04d_var.csv" % (gen_dir, run, gen_n), x, delimiter=",")
                

        np.savetxt("%s/%s%04d.csv" % (outputdir, fileName, run), paretoFront, delimiter=",")


        print("\n\n========== Run %d complete ==========\n\n" % run)


### Main ###

#print("\n\n========== With CropOpt run starting ==========\n\n" )
#startRuns(True)
#print("\n\n========== With CropOpt run complete ==========\n\n" )
print("\n\n========== Without CropOpt run complete ==========\n\n" )
startRuns(False)
print("\n\n========== Without CropOpt run complete ==========\n\n")


