import sys
import pandas as pd
import numpy as np
from dssat4dum import Dssat4Dum

def make_common_practices_decision(current_day, wth_tab, gdd_tab):

    if current_day < int(gdd_tab.V6):
        # If before V6
        day_delta = 1
        irr_amount = 0
    elif current_day < int(gdd_tab.R1): 
        day_delta = 5
        irr_amount = 10
    elif current_day < int(gdd_tab.R2): 
        day_delta = 5
        irr_amount = 20
    else: 
        day_delta = 1
        irr_amount = 0


    return (irr_amount, current_day + day_delta)


class RoboFarmer():


    def __init__(self, wth_tab, gdd_tab, manager):

        self.manager = manager
        self.wth_tab = wth_tab
        self.gdd_tab = gdd_tab


    def realize_year(self, year):

        year_modded = int((year  % 1e2) * 1e3) 
       
        wth_mask = np.logical_and(wth_tab['@DATE'] >= year_modded, wth_tab['@DATE'] < (year_modded + 366))

        wth_tab_year = self.wth_tab[wth_mask]
        gdd_tab_year = gdd_tab[self.gdd_tab['Year'] == year]


        # To become a 2D array 
        raw_management = []

        current_day = int(gdd_tab_year.P) 

        while current_day < int(gdd_tab_year.R4):

            (irr_amount, next_day) = self.manager(current_day, wth_tab_year, gdd_tab_year)

            year_code = year*1e3 + current_day

            if irr_amount != 0:
                raw_management.append([year_code, irr_amount, 0, 0, 0])

            current_day = next_day
            

        management = np.array(raw_management)

        return management


if __name__ == "__main__":

    # Gather weather data
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    gdd_tab_path = "management_dates.csv"

    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)
    gdd_tab = pd.read_csv(gdd_tab_path)

    #wet_years = [2011, 2018, 2019] Bring this back if we GDD on 2018 and 2019
    wet_years = [2011]
    normal_years = dates = list(range(2013,2018)) 
    dry_years = [2012]

    # DSSAT parameters
    #home_dir = "/Users/iankropp/"
    home_dir = "/home/ian/"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-linux" % home_dir
    dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/agovization/output/" % home_dir

    tmp_dir = "/tmp/"

    threads = 1

    dssat = Dssat4Dum(dssat_home, dssat_inp, dssat_exe, tmp_dir)

    rfarmer = RoboFarmer(wth_tab, gdd_tab, make_common_practices_decision)

    # inputs for DSSAT
    schedules = []
    updates = []

    # Results 
    year_col = [] 
    climate = []

    for year in wet_years: 
        print("Year: %s" % year)
        schedules.append(rfarmer.realize_year(year))
        updates.append({ 'pdate': year*1e3 + 135, 'sdate': year*1e3 + 135, 'icdat': year*1e3 + 135 })
        year_col.append(year)
        climate.append(2)

    for year in normal_years: 
        print("Year: %s" % year)
        schedules.append(rfarmer.realize_year(year))
        updates.append({ 'pdate': year*1e3 + 135, 'sdate': year*1e3 + 135, 'icdat': year*1e3 + 135 })
        year_col.append(year)
        climate.append(1)
        

    for year in dry_years: 
        print("Year: %s" % year)
        schedules.append(rfarmer.realize_year(year))
        updates.append({ 'pdate': year*1e3 + 135, 'sdate': year*1e3 + 135, 'icdat': year*1e3 + 135 })
        year_col.append(year)
        climate.append(0)


    dssat_result = dssat.run_batch(schedules, threads, updates=updates)


    full_result_mat = np.c_[year_col, climate, dssat_result]


    result = pd.DataFrame(full_result_mat, columns=['year', 'climate', 'yield', 'leaching'])


    print(result)




































