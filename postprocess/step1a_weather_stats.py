import sys
import pandas as pd
import pickle
import numpy as np
import tabloo

# Example call 
# python postprocess/step1a_weather_stats.py postprocess/yearly_summary.pkl dhome/Weather/CASSREPR.WTH

yearly_summary_file_path = sys.argv[1]
weather_file_path = sys.argv[2]

# Load weather
wth_tab = pd.read_fwf(weather_file_path, skiprows=4)

# Load yearly summary file
infile = open(yearly_summary_file_path, 'rb')
yearly_summary = pickle.load(infile)

total_irr_period_precip = []
total_nit_period_precip = []
total_plant_date_precip = []

for r, row in yearly_summary.iterrows():
  
    year = row['year']

    # Gather data
    irr_start = row['irr period start']
    irr_end = row['irr period end']

    nit_start =  row["nit period start"]
    nit_end =    row["nit period end"]

    plant_date = row['plant date']

    # Convert to the weather file format

    # truncating for the weather file format
    trunc_year = year % 100 # e.g. 1992 -> 92

    irr_start = irr_start + (trunc_year*1e3)
    irr_end = irr_end     + (trunc_year*1e3)

    nit_start = nit_start + (trunc_year*1e3)
    nit_end   = nit_end   + (trunc_year*1e3)

    plant_date = plant_date + (trunc_year*1e3)

    # Filter out the weather data we need 
    irr_period_mask = np.logical_and(wth_tab['@DATE'] >= irr_start, wth_tab['@DATE'] <= irr_end)
    nit_period_mask = np.logical_and(wth_tab['@DATE'] >= nit_start, wth_tab['@DATE'] <= nit_end)
    
    irr_period_precip = wth_tab[irr_period_mask]['RAIN']
    nit_period_precip = wth_tab[nit_period_mask]['RAIN']

    plant_date_mask = (np.logical_and(wth_tab['@DATE'] >= plant_date, wth_tab['@DATE'] <= plant_date + 10))
    total_plant_date_p = np.sum(wth_tab[plant_date_mask]['RAIN'])

    # Sum up results
    total_irr_p = np.sum(irr_period_precip)
    total_nit_p = np.sum(nit_period_precip)

    # Add to total list 
    total_irr_period_precip.append(total_irr_p)   
    total_nit_period_precip.append(total_nit_p)  
    total_plant_date_precip.append(total_plant_date_p)


yearly_summary['total irr period precip (mm)'] = total_irr_period_precip
yearly_summary['total nit period precip (mm)'] = total_nit_period_precip
yearly_summary['total plant date precip (mm)'] = total_plant_date_precip


tabloo.show(yearly_summary)
