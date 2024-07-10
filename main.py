import pandas as pd
import numpy as np
from pico.cropopt.cropopt import CropOpt
from pico.cropopt.vssps import VSSPS
from pico.dash.Dashboard import Dashboard
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import FloatRandomSampling
import sys
from pathlib import Path
from datetime import datetime
import pickle
from pymoo.visualization.scatter import Scatter

from pico.pinsga2.pinsga2 import PINSGA2
from pico.pinsga2 import value_functions as mvf



def plot_eta_F(context, algorithm):

   
    # Next highlight the eta selctions
    if len(algorithm.eta_F) > 0:

        # Plot the historical PO fronts
        plot = Scatter().add(algorithm.historical_F * -1, facecolors= '#f5f5f5', edgecolors='#f5f5f5')

        # The current PO front 
        plot.add(algorithm.paused_F * -1)

        # Starred items for the DM
        plot.add(algorithm.eta_F * -1, s=500, marker='*', facecolors='red')
        

    else: 
        F = algorithm.pop.get("F")
        plot = Scatter().add(F * -1)


    plot.plot_if_not_done_yet()

    return plot.fig
 

def running_plot_vf(context, algorithm):

    if not algorithm.vf_plot_flag and algorithm.vf_plot: 
        return algorithm.vf_plot

    elif len(algorithm.eta_F) > 0 and (algorithm.vf_res is not None) and algorithm.vf_plot_flag:

        plot = mvf.plot_vf(algorithm.eta_F * -1, algorithm.vf_res.vf, show=False)
        
        algorithm.vf_plot_flag = False;
        
        algorithm.vf_plot = plot.gcf()

        return plot.gcf()
    
    else: 

        # Plot empty axis
        plot = Scatter().add(np.array([[10000, -50]]), facecolors="#ffffff", edgecolors="#ffffff")
        plot.plot_if_not_done_yet()
        
        algorithm.vf_plot = plot.fig

        return plot.fig

 

def current_plot_vf(context, algorithm):

    if not algorithm.current_vf_plot_flag and algorithm.current_vf_plot: 
        return algorithm.current_vf_plot

    elif len(algorithm.eta_F) > 0 and (algorithm.current_vf_res is not None) and algorithm.current_vf_plot_flag:

        plot = mvf.plot_vf(algorithm.eta_F * -1, algorithm.current_vf_res.vf, show=False)
        
        algorithm.current_vf_plot_flag = False;
        
        algorithm.current_vf_plot = plot.gcf()

        return plot.gcf()
    
    else: 

        # Plot empty axis
        plot = Scatter().add(np.array([[10000, -50]]), facecolors="#ffffff", edgecolors="#ffffff")
        plot.plot_if_not_done_yet()
        
        algorithm.vf_plot = plot.fig

        return plot.fig



if __name__ == "__main__":

    ## Parameters: 

    dateTimeObj = datetime.now()
    timestamp = "%d-%02d-%02d_%02d-%02d-%02d" % (dateTimeObj.year, dateTimeObj.month, dateTimeObj.day, dateTimeObj.hour, dateTimeObj.minute, dateTimeObj.second)

    # Agricultural parameters
    app_man_csv = "management_dates.csv"
    app_man = pd.read_csv(app_man_csv)

    if len(sys.argv) != 3: 
        print("Usage: %s YEAR [nsga2|pinsga2]" % sys.argv[0])
        sys.exit(1)

    year = int(sys.argv[1])
    method = sys.argv[2]

    reps = 1
    plant_date = 135

    total_nitro = 200

    # dssat parameters 
    home_dir = "/home/ian/"

    dssat_home = "%s/Projects/pi-cropopt/dhome" % home_dir
    dssat_exe  = "%s/Projects/pi-cropopt/dhome/dscsm047-linux" % home_dir
    dssat_inp  = "%s/Projects/pi-cropopt/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/pi-cropopt/output/" % home_dir

    tmp_dir = "/dev/shm/"

    # Runtime optimization parameters
    threads = 20
    initial_sparsity = 0.2
    generations = 200
    if method == "nsga2": 
        pop_size = 120
    elif method == "pinsga2": 
        pop_size = 30
    else: 
        print("Unrecognized method")
        sys.exit(1)



    ## Derived parameters 
    first_nut_app = plant_date

    # Calcualte irrigation bounds
    # (between the 30-year minimum of V6 and maximum of R2)
    irr_date_lb = min(app_man[app_man.Year < 2010].V8)  
    irr_date_ub = max(app_man[app_man.Year < 2010].R2)

    nitro_date_lb = min(app_man[app_man.Year < 2010].V6)  
    nitro_date_ub = max(app_man[app_man.Year < 2010].V14)

    # Reformat the mins and maxes for the given year
    # 
    irr_date_lb += int(year * 1e3)
    irr_date_ub += int(year * 1e3)
    nitro_date_lb += int(year * 1e3)
    nitro_date_ub += int(year * 1e3)
    plant_date += int(year * 1e3)

    if year % 4 == 0: 
        plant_date += 1
        irr_date_lb += 1
        irr_date_ub += 1
        nitro_date_lb += 1
        nitro_date_ub += 1

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
            [irr_date_lb,   irr_date_ub,    0,                     0, 30, 0], # Irrigation period 
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

        vssps = VSSPS(FloatRandomSampling, nz_indices=nutrient_inds)

        algorithm = None
        dashboard = None
        if method == "nsga2": 
            algorithm = NSGA2(pop_size=pop_size, 
                              eliminate_duplicates=True,
                              sampling=vssps)

            dashboard = Dashboard()
        elif method == "pinsga2":
            algorithm = PINSGA2(pop_size=pop_size, 
                              eliminate_duplicates=True,
                              sampling=vssps)

            dashboard = Dashboard(plot_eta_F=plot_eta_F, running_plot_vf=running_plot_vf, current_plot_vf=current_plot_vf)


        else: 
            print("Unrecognized method")
            sys.exit(1)


        res = minimize(prob,
                       algorithm,
                       ('n_gen', generations),
                       seed=seed,
                       callback=dashboard,
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

    report = prob.get_report()

    output = open('%s/run_sim_record.pkl' % full_output_dir, 'wb')
    pickle.dump(report, output)



    #print("Copy the following statement into the script")

    #print("period_indices=%s" % statement_str)



