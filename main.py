import pandas as pd
import numpy as np
from cropopt import CropOpt
from sps import SPS

## Parameters: 

# Agricultural parameters
app_man_csv = "management_dates.csv"
app_man = pd.read_csv(app_man_csv)

reps = 20
year = 2000
plant_date = 135 

total_nitro = 200

# dssat parameters 
home_dir = "/Users/iankropp"

dssat_home = "%s/Projects/agovization/dhome" % home_dir
dssat_exe = "%s/Projects/agovization/dhome/dscsm047" % home_dir
dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
output_dir = "%s/Projects/agovization/output/" % home_dir

tmp_dir = "/tmp/"

# Runtime parameters
seed = 20210401
threads = 1

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
                           updates=year_updates, constant_apps=None)


    print("Starting run %d" % run)


