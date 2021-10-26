import sys
import pandas as pd


def make_management_decision(current_day, wth_tab, gdd_tab):
    
    return (current_day + 5, 10)


class RoboFarmer():


    def __init__(self, wth_tab, gdd_tab, manager):

        self.manager = manager
        self.wth_tab = wth_tab
        self.gdd_tab = gdd_tab


    def simulate_year(year):

        wth_tab_year = wth_tab[wth_tab['year'] == year, :]
        gdd_tab_year = gdd_tab_year[gdd_tab_year['year'] == year, :]

        dssatExp = newExp();

        while current_day < self.R1:
            
            (irr_amount, next_day) = self.manager(current_day, wth_tab_year, gdd_tab_year)

            dssatExp.addIrr(current_day, irr_amount)
       
            current_day = next_day

        (yield_, water_usage, leaching) = dssatExp.run()

        return (yield_, water_usage, leaching)


if __name__ == "__main__":


    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    gdd_tab_path = "management_dates.csv"

    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)
    gdd_tab = pd.read_csv(gdd_tab_path)

    sys.exit(0)
    wet_years = [2011, 2018, 2019]
    normal_years = dates = list(range(2013,2018)) 
    dry_years = [2012]

    rfarmer = RoboFarmer(wth_tab, gdd_tab, make_management_decision)

    sys.exit(0)
    

    results = {year: [], climate: [], yield_: [], leaching: [], water_usage: []}

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















