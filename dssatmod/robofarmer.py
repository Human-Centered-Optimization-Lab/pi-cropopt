import sys
import pandas as pd
import numpy as np
from dssat4dum import Dssat4Dum

def make_management_decision(current_day, wth_tab, gdd_tab):
    
    return (current_day + 5, 10)


class RoboFarmer():


    def __init__(self, dssat, wth_tab, gdd_tab, manager):

        self.manager = manager
        self.wth_tab = wth_tab
        self.gdd_tab = gdd_tab
        self.dssat = dssat 


    def simulate_year(self, year):

        year_modded = int((year  % 1e2) * 1e3) 
       
        wth_mask = np.logical_and(wth_tab['@DATE'] >= year_modded, wth_tab['@DATE'] < (year_modded + 366))

        wth_tab_year = self.wth_tab[wth_mask]
        gdd_tab_year = gdd_tab[self.gdd_tab['Year'] == year]

        sys.exit(0)
        dssatExp = newExp();

        while current_day < self.R1:
            
            (irr_amount, next_day) = self.manager(current_day, wth_tab_year, gdd_tab_year)

            dssatExp.addIrr(current_day, irr_amount)
       
            current_day = next_day

        (yield_, water_usage, leaching) = dssatExp.run()

        return (yield_, water_usage, leaching)


if __name__ == "__main__":

    # Gather weather data
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    gdd_tab_path = "management_dates.csv"

    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)
    gdd_tab = pd.read_csv(gdd_tab_path)

    wet_years = [2011, 2018, 2019]
    normal_years = dates = list(range(2013,2018)) 
    dry_years = [2012]

    # DSSAT parameters
    home_dir = "/work/ian/"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-linux" % home_dir
    dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/agovization/output/" % home_dir

    tmp_dir = "/tmp/"

    dssat = Dssat4Dum(dssat_home, dssat_inp, dssat_exe, tmp_dir)


    rfarmer = RoboFarmer(dssat, wth_tab, gdd_tab, make_management_decision)

    

    results = {'year': [], 'climate': [], 'yield_': [], 'leaching': [], 'water_usage': []}

    for wet_year in wet_years: 
        (yield_, water_usage, leaching) = rfarmer.simulate_year(wet_year)
        results['year'].append(wet_year)
        results['climate'].append(2)
        results['yield_'].append(yield_)
        results['leaching'].append(leaching)
        results['water_usage'].append(water_usage)

    for normal_year in normal_years: 
        (yield_, water, leaching) = rfarmer.simulate_year(normal_year)
        results['year'].append(normal_year)
        results['climate'].append(1)
        results['yield_'].append(yield_)
        results['leaching'].append(leaching)
        results['water_usage'].append(water_usage)
        


    for dry_year in dry_years: 
        (yield_, water, leaching) = rfarmer.simulate_year(dry_year)
        results['year'].append(dry_year)
        results['climate'].append(0)
        results['yield_'].append(yield_)
        results['leaching'].append(leaching)
        results['water_usage'].append(water_usage)















