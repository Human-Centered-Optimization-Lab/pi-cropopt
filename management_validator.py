import pandas as pd
import numpy as np
from dssatmod.robofarmer import RoboFarmer
from dssatmod.robofarmer import MachRecdPractices
from dssatmod.robofarmer import CommonPractice
from dssatmod.dssat4dum import Dssat4Dum

if __name__ == "__main__":

    # Gather weather data
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    gdd_tab_path = "management_dates.csv"

    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)
    gdd_tab = pd.read_csv(gdd_tab_path)

    #wet_years = [2011, 2018, 2019] Bring this back if we GDD on 2018 and 2019
    #wet_years = [2011]
    #normal_years = dates = list(range(2013,2018)) 
    #dry_years = [2012]

    # Excluding 2018 and 2019 because I don't have the gdd data on hand
    year_by_climate = {2011: 2, 2013: 1, 2014: 1, 2015: 1, 2016: 1, 2017: 1, 2012: 0}



    # DSSAT parameters
    home_dir = "/Users/iankropp/"
    #home_dir = "/home/ian/"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    #dssat_exe = "%s/Projects/agovization/dhome/dscsm047-linux" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-macos" % home_dir
    dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/agovization/output/" % home_dir

    tmp_dir = "/tmp/"

    threads = 4

    # Initialize DSSAT runner
    dssat = Dssat4Dum(dssat_home, dssat_inp, dssat_exe, tmp_dir)

    # inputs for DSSAT
    schedules_common_pract = []
    schedules_mech_rec_pract = []
    updates = []


    # Results 
    year_col = [] 
    climates = []

    for year in year_by_climate: 

        climate = year_by_climate[year] 

        # Initialize managers
        com_pract_manager = CommonPractice(wth_tab, gdd_tab, year, climate)
        mach_rec_manager = MachRecdPractices(wth_tab, gdd_tab, year, climate)

        # Initialize robo farmers
        comm_rfarmer = RoboFarmer(com_pract_manager)
        mach_rec_rfarmer = RoboFarmer(mach_rec_manager)

        # Generate schedule for this year
        schedules_common_pract.append(comm_rfarmer.realize_year())
        schedules_mech_rec_pract.append(mach_rec_rfarmer.realize_year())
        
        if year % 4 == 0:
            plant_date = 136
        else:
            plant_date = 135

        updates.append({ 'pdate': year*1e3 + plant_date, 'sdate': year*1e3 + plant_date, 'icdat': year*1e3 + plant_date })
        year_col.append(year)

        climates.append(climate)


    # Run DSSAT 
    com_dssat_result = dssat.run_batch(schedules_common_pract, threads, updates=updates)
    dssat.clean_workspace()
    mach_dssat_result = dssat.run_batch(schedules_mech_rec_pract, threads, updates=updates)

    # Compile results into a dataframe


    com_full_result_mat = np.c_[year_col, climates, com_dssat_result]
    com_result = pd.DataFrame(com_full_result_mat, columns=['year', 'climate', 'yield', 'leaching'])

    mach_full_result_mat = np.c_[year_col, climates, mach_dssat_result]
    mach_result = pd.DataFrame(mach_full_result_mat, columns=['year', 'climate', 'yield', 'leaching'])

    print("Common practices")
    print(com_result)

    print("Mach practices")
    print(mach_result) 





