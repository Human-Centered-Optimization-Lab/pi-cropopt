import sys
import pandas as pd
import numpy as np

# SDAT -- Simulation date Simulation start date (YrDoy) 
# HWAH -- Harvested yield (kg [dm]/ha)
# NLCM -- N leached during season (kg [N]/ha)

file_path = sys.argv[1]

summary = pd.read_fwf(file_path, skiprows=3)

all_dates = summary['SDAT']

available_years = [int(i) for i in set(np.floor_divide(all_dates, 1e3))]

raw_table = {
        'year': [],
        'max_yield' : [],
        'Mean leaching': []
        }

for year in available_years:


    lbound = int(year * 1e3)
    ubound = int((year * 1e3) + 366)

    time_mask = np.logical_and(summary['SDAT'] > lbound, summary['SDAT'] <= ubound)

    max_yield = max(summary[time_mask]['HWAH'])

    mean_leaching = np.mean(summary[time_mask]['NLCM'])

    raw_table['year'].append(year)
    raw_table['max_yield'].append(max_yield)
    raw_table['Mean leaching'].append(mean_leaching)
    

tab = pd.DataFrame(raw_table)



