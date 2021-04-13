import pandas as pd
import numpy as np
from cropopt import CropOpt
from sps import SPS
from pymoo.algorithms.nsga3 import NSGA3
from pymoo.factory import get_reference_directions
from pymoo.optimize import minimize
import sys
from pathlib import Path
from datetime import datetime

if __name__ == "__main__":

    ## Parameters: 

    dateTimeObj = datetime.now()
    timestamp = "%d-%02d-%02d_%02d-%02d-%02d" % (dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute, dateTimeObj.second)

    # Agricultural parameters
    app_man_csv = "management_dates.csv"
    app_man = pd.read_csv(app_man_csv)

    if len(sys.argv) != 2: 
        print("Usage: %s YEAR" % sys.argv[0])
        sys.exit(1)

    year = int(sys.argv[1])

    reps = 30
    plant_date = 136

    total_nitro = 200

    # dssat parameters 
    home_dir = "/work/ian/"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-linux" % home_dir
    dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/agovization/output/" % home_dir

    tmp_dir = "/tmp/"

    # Runtime optimization parameters
    threads = 20
    initial_sparsity = 0.1
    pop_size = 100
    ref_dirs = get_reference_directions("energy", 3, 90, seed=1)
    generations = 200

    ## Derived parameters 

    if year % 4 == 0: 
        plant_date += 1

    first_nut_app = plant_date

    # Calcualte irrigation bounds
    # (between the 30-year minimum of V6 and maximum of R2)
    irr_date_lb = min(app_man[app_man.Year < 2010].V8)  # TODO change to V6 when data is available
    irr_date_ub = max(app_man[app_man.Year < 2010].R2)

    nitro_date_lb = min(app_man[app_man.Year < 2010].V8)  # TODO change to V6 when data is available
    nitro_date_ub = max(app_man[app_man.Year < 2010].V14)

    # Reformat the mins and maxes for the given year
    # 
    irr_date_lb += int(year * 1e3)
    irr_date_ub += int(year * 1e3)
    nitro_date_lb += int(year * 1e3)
    nitro_date_ub += int(year * 1e3)
    plant_date += int(year * 1e3)

    #
    # Irrigation type            Nutrient type
    # Col 1: Period begin date   Col 1: Period begin date  
    # Col 2: Period end date     Col 2: Period end date    
    # Col 3: IRR=0,              Col 3: NUT=1,             
    # Col 4: IRR min             Col 4: Nitrogen amount    
    # Col 5: IRR max             Col 5: Phos amount        
    # Col 6: 0                   Col 6: Pot amount         
    #

    date_ranges = [
            [irr_date_lb,   irr_date_ub,    0,                     0, 10, 0], # Irrigation period 
            [nitro_date_lb, nitro_date_ub,  1, int(total_nitro*0.25),  0, 0]] # 

    # Preplant incorporation 
    constant_apps = np.array([[plant_date, 0, int(total_nitro*0.75), 0, 0]])

    date_ranges = np.array(date_ranges)

    year_updates = { 'pdate': plant_date, 'sdate': plant_date, 'icdat': plant_date }

    ## Main 


    for run in range(reps):

        print("Initializing Run %d" % run)

        seed = year + plant_date + run

        prob = CropOpt(threads, dssat_home, dssat_exe, dssat_inp,
                               tmp_dir, date_ranges, output_dir, run, seed=0, 
                               updates=year_updates, constant_apps=constant_apps)


        print("Starting run %d" % run)

        nutrient_inds = CropOpt.calc_period_indices(CropOpt, date_ranges)[1]

        nutrient_inds = [a[1] for a in nutrient_inds]

        sps_sampler = SPS(initial_sparsity, sampled_mask=nutrient_inds)

        algorithm = NSGA3(pop_size=pop_size, 
                ref_dirs=ref_dirs,
                eliminate_duplicates=True,
                sampling=sps_sampler)

        res = minimize(prob,
                       algorithm,
                       ('n_gen', generations),
                       seed=seed,
                       save_history=True,
                       verbose=True)

        paretoFront = res.F
        paretoFront[:,1] = paretoFront[:,1]*-1

        print("Recording run %d" % run)

        for gen in res.history:

            gen_n = gen.n_gen
           
            objectives = np.array([indiv.F for indiv in gen.pop ])
            x = np.array([indiv.X for indiv in gen.pop ])

            full_output_dir = "%s/year_%s_%s" % (output_dir, str(year), timestamp)

            Path(full_output_dir).mkdir(parents=True, exist_ok=True)

            # save generational data 
            np.savetxt("%s/run%04d_gen%04d_obj.csv" % (full_output_dir, run, gen_n), objectives, delimiter=",")
            np.savetxt("%s/run%04d_gen%04d_var.csv" % (full_output_dir, run, gen_n), x, delimiter=",")

            np.savetxt("%s/run%04d_finalgen.csv" % (full_output_dir, run), paretoFront, delimiter=",")

    # metadata on the genome structure
    statement = {
                'indices': CropOpt.calc_period_indices(CropOpt, date_ranges),
                'date_ranges': date_ranges.tolist(),
                'constant_apps': constant_apps.tolist()
            }



    with open("%s/genome_structure.py" % full_output_dir, 'w') as f:f.write(repr(statement))
    

    #print("Copy the following statement into the script")

    #print("period_indices=%s" % statement_str)



