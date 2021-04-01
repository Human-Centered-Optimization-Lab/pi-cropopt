import pandas as pd

## Parameters: 

#app_man_xlxs = "/Users/iankropp/OneDrive - Michigan State University/Documents/Shared/todo/paper1Innovization/management/original_Cass_Irrigation_Nitrogen_Application_Climatology_1980_2017.xlsx"
app_man_csv = "management_dates.csv"
app_man = pd.read_csv(app_man_csv)

reps = 20
year = 2000
plant_date = 135 



## Derived parameters 

if year % 4 == 0: 
    plant_date += 1

first_nut_app = plant_date

# Calcualte irrigation bounds
# (between the 30-year minimum of V6 and maximum of R2)
irr_lb = min(app_man[app_man.Year < 2010].V8)  # TODO change to V6 when data is available
irr_up = max(app_man[app_man.Year < 2010].R2)

nitro_lb = min(app_man[app_man.Year < 2010].V8)  # TODO change to V6 when data is available
nitro_up = max(app_man[app_man.Year < 2010].V14)


# 1: Year
# 2: Irrigation period 
# 3: Nitrogen timing (determined by weather properties)
# 4: Plant date (determined by weather properties)


## Objective function

    # Parameters: irrigation days for this 



## Main -- Run setup

# Optimization params:
# Objectives -- 
#   maximize yield
#   minimize irrigation





dssat_home = "/home/ian/Projects/dssat4py/rundir"
fileio = "/home/ian/Projects/dssat4py/rundir/DSSAT47.INP"
tmp_dir = "/tmp/"

#runner = Dssat4Dum(dssat_home, fileio, tmp_dir)
#
#threads = 7
#
#print(runner.run_batch(appscheds2, threads))
#
#
#updates = { 'pdate': 2000135, 'sdate': 2000135, 'icdat': 2000135 }
#
#
#print(runner.run_batch(appsched1[:10], threads, updates=updates))


#print(runner.run(irrscheds[0],0))





# Decision variables --
#   x --> (period end) - (period start)
#   




