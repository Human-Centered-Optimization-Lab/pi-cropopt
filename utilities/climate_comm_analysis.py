import pandas as pd
import numpy as np
from dssatmod.robofarmer import RoboFarmer
from dssatmod.robofarmer import MachRecdPractices
from dssatmod.robofarmer import CommonPractice
from dssatmod.dssat4dum import Dssat4Dum
from mlearn.attr_processors import AttProcessors as ap

if __name__ == "__main__":

    # Gather weather data
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    gdd_tab_path = "management_dates.csv"

    output_path = "/Volumes/data/Gilgamesh/kroppian/agovization_results/mlearning/recommended_practices.feather"

    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)
    gdd_tab = pd.read_csv(gdd_tab_path)

    year_by_climate = {
            1980: 0,
            1981: 2,
            1982: 0,
            1983: 0,
            1984: 1,
            1985: 1,
            1986: 2,
            1987: 2,
            1988: 0,
            1989: 1,
            1990: 2,
            1991: 0,
            1992: 1,
            1993: 2,
            1994: 1,
            1995: 1,
            1996: 2,
            1997: 2,
            1998: 0,
            1999: 0,
            2000: 1,
            2001: 2,
            2002: 0,
            2003: 0,
            2004: 1,
            2005: 0,
            2006: 2,
            2007: 1,
            2008: 2,
            2009: 1}

    growth_stages = ['P', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 
                        'V13', 'V14', 'R1']


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
    schedules = {}
    updates = []

    # Results 
    year_col = [] 
    climates = []

    for year in year_by_climate: 

        climate = year_by_climate[year]

        # Initialize managers
        com_pract_manager = CommonPractice(wth_tab, gdd_tab, year, climate)

        # Initialize robo farmers
        comm_rfarmer = RoboFarmer(com_pract_manager)

        # Generate schedule for this year
        schedules[year] = comm_rfarmer.realize_year()
        
        climates.append(climate)


    raw_table = {'stages': [], 'year': [], 'irr': [], 'climate': []}
      
    for year in year_by_climate:

        for stage in growth_stages:

            total_precip = ap._calc_total_precip_per_period(stage, year, gdd_tab, wth_tab)

            total_irr = ap._calc_total_irr_per_period(stage, year, gdd_tab, schedules[year])

            #print("Year: %d, stage: %s, Precip %f, irr %f" % (year, stage, total_precip, total_irr))

            raw_table['year'].append(year)
            raw_table['irr'].append(total_precip + total_irr)
            raw_table['climate'].append(year_by_climate[year])
            raw_table['stages'].append(stage)

            


    result = pd.DataFrame(raw_table)

    result.to_feather(output_path)

    print(result)


    



