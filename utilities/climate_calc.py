import pandas as pd
import numpy as np
import sys
import statistics

# Constants
GDD_TAB_CSV = "management_dates.csv"
START_YEAR = 1989
END_YEAR = 2018
STUDY_SITE = "CASS"

output_path = sys.argv[1]
files = sys.argv[2:]
gdd_tab = pd.read_csv(GDD_TAB_CSV)

if output_path[-7:].lower() != "feather":
    print("Usage: %s OUTPUTFILE.feather WEATHER_FILE1.WTH [WEATHER_FILE2.WTH ... WEATHER_FILEN.WTH]" % sys.argv[0])
    sys.exit(1)

# Functions
def get_seasonal_rain(study_site_wth, year, gdd_tab):


    year_modded = int((year  % 1e2) * 1e3) 
    season_start_doy = int(gdd_tab[gdd_tab['Year'] == year].P)
    season_end_doy  = int(gdd_tab[gdd_tab['Year'] == year].R6)

    season_start_date = year_modded + season_start_doy
    season_end_date  = year_modded + season_end_doy

    wth_mask = np.logical_and(study_site_wth['@DATE'] >= season_start_date, study_site_wth['@DATE'] <=  season_end_date)

    return sum(study_site_wth[wth_mask]['RAIN']) 

# Read and store the weather stations
weather_stations = {}
for weather_path in files: 

    station_name = weather_path[-8:-4]

    tab = pd.read_fwf(weather_path, skiprows=4)

    weather_stations[station_name] = tab

# Figure out climate for the study site
total_p = {}
study_site_wth = weather_stations[STUDY_SITE]
for year in range(START_YEAR, END_YEAR+1): 
    total_p[year] = get_seasonal_rain(study_site_wth, year, gdd_tab)


test_total_p = {year: total_p[year] for year in total_p if year >= START_YEAR and year <= END_YEAR }

sorted_p = list(test_total_p.values())

sorted_p.sort()

oneThird = int(len(sorted_p)/3);
twoThird = int((len(sorted_p)*2)/3);

normalThreshold = statistics.mean([sorted_p[oneThird-1], sorted_p[oneThird]])
wetThreshold    = statistics.mean([sorted_p[twoThird-1], sorted_p[twoThird]])

print(normalThreshold)
print(wetThreshold)

# Build climate table for all the sites
raw_tab = {"station": [], "year": [], "clim": []}

for station in weather_stations.keys():
    station_wth = weather_stations[station]
    
    for year in range(START_YEAR, END_YEAR+1):
        
        total_p = get_seasonal_rain(station_wth, year, gdd_tab)

        clim = -1

        if total_p < normalThreshold: 
            clim = 0
        elif total_p < wetThreshold: 
            clim = 1
        else:
            clim = 2

        raw_tab["station"].append(station)
        raw_tab["year"].append(year)
        raw_tab["clim"].append(clim)

       
result = pd.DataFrame(raw_tab)

result.to_feather(output_path)




