import pandas as pd
import numpy as np
from dssatmod.robofarmer import *
from dssatmod.dssat4dum import Dssat4Dum
import matplotlib.pyplot as plt

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
    year_by_climate = {1980:  0, 1981:  2, 1982:  0, 1983:  0, 1984:  1, 1985:  1, 1986:  2, 1987:  2, 1988:  0, 1989:  1, 1990:  2, 1991:  0, 1992:  1, 1993:  2, 1994:  1, 1995:  1, 1996:  2, 1997:  2, 1998:  0, 1999:  0, 2000:  1, 2001:  2, 2002:  0, 2003:  0, 2004:  1, 2005:  0, 2006:  2, 2007:  1, 2008:  2, 2009:  1}
    year_by_climate = {2011: 2, 2013: 1, 2014: 1, 2015: 1, 2016: 1, 2017: 1, 2012: 0, 2010: 1, 2018: 2}



    # DSSAT parameters
    #home_dir = "/Users/iankropp/"
    home_dir = "/home/ian/"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-linux" % home_dir
    #dssat_exe = "%s/Projects/agovization/dhome/dscsm047-macos" % home_dir
    dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/agovization/output/" % home_dir

    tmp_dir = "/tmp/"

    threads = 8

    # Initialize DSSAT runner
    dssat = Dssat4Dum(dssat_home, dssat_inp, dssat_exe, tmp_dir)

    # inputs for DSSAT
    schedules_common_pract = []
    schedules_irr_only_pract = []
    schedules_nitro_only_pract = []

    updates = []


    # Results 
    year_col = [] 
    climates = []
    total_wat_common_pract = [] 
    total_wat_irr_only= [] 
    total_wat_nitro_only = []

    for year in year_by_climate: 

        climate = year_by_climate[year] 

        # Initialize managers
        com_pract_manager = Practices(wth_tab, gdd_tab, year, climate)
        irr_only_manager = RecIrrOnly(wth_tab, gdd_tab, year, climate)
        nitro_only_manager = RecNitroOnly(wth_tab, gdd_tab, year, climate)

        # Initialize robo farmers
        comm_rfarmer = RoboFarmer(com_pract_manager)
        irr_only_rfarmer = RoboFarmer(irr_only_manager)
        nitro_only_rfarmer = RoboFarmer(nitro_only_manager)

        # Generate schedule for this year
        comm_sched = comm_rfarmer.realize_year()
        irr_only_sched = irr_only_rfarmer.realize_year()
        nitro_only_sched = nitro_only_rfarmer.realize_year()
        
        schedules_common_pract.append(comm_sched)
        schedules_irr_only_pract.append(irr_only_sched)
        schedules_nitro_only_pract.append(nitro_only_sched)

        if year % 4 == 0:
            plant_date = 136
        else:
            plant_date = 135

        updates.append({ 'pdate': year*1e3 + plant_date, 'sdate': year*1e3 + plant_date, 'icdat': year*1e3 + plant_date })

        total_wat_common_pract.append(sum(comm_sched[:, 1]))
        total_wat_irr_only.append(sum(irr_only_sched[:, 1]))
        total_wat_nitro_only.append(sum(nitro_only_sched[:, 1]))

        year_col.append(year)

        climates.append(climate)


    # Run DSSAT 
    com_dssat_result = dssat.run_batch(schedules_common_pract, threads, updates=updates)
    dssat.clean_workspace()
    irr_only_dssat_result = dssat.run_batch(schedules_irr_only_pract, threads, updates=updates)
    dssat.clean_workspace()
    nitro_only_dssat_result = dssat.run_batch(schedules_nitro_only_pract, threads, updates=updates)


    # Compile results into a dataframe
    com_full_result_mat = np.c_[year_col, climates, com_dssat_result, total_wat_common_pract]
    com_result = pd.DataFrame(com_full_result_mat, columns=['year', 'climate', 'yield', 'leaching', 'total_wat'])

    irr_only_full_result_mat = np.c_[year_col, climates, irr_only_dssat_result, total_wat_irr_only]
    irr_only_result = pd.DataFrame(irr_only_full_result_mat, columns=['year', 'climate', 'yield', 'leaching', 'total_wat'])

    nitro_only_full_result_mat = np.c_[year_col, climates, nitro_only_dssat_result, total_wat_nitro_only]
    nitro_only_result = pd.DataFrame(nitro_only_full_result_mat, columns=['year', 'climate', 'yield', 'leaching', 'total_wat'])
    

    print("Common practices")
    print(com_result)

    print("Irr only practices")
    print(irr_only_result) 

    print("Nitro only practices")
    print(nitro_only_result) 
   

