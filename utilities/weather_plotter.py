import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Process parameters
if len(sys.argv) != 3 and len(sys.argv) != 5:
    print("USEAGE: %s WTH_PATH YEAR1[,YEAR2,...,YEARN] [START_DOY END_DOY]" % sys.argv[0])
    sys.exit(1)

wth_file_path = sys.argv[1]
years_raw = sys.argv[2].split(",")
years = [int(raw_year) for raw_year in years_raw]

if len(sys.argv) == 5:
    start_doy = int(sys.argv[3])
    end_doy = int(sys.argv[4])
else:
    start_doy = 1 
    end_doy = 365

# Fetch weather data
wth_tab = pd.read_fwf(wth_file_path, skiprows=4)

for (y, year) in enumerate(years): 

    # Reformat date information 
    year_truncd = year % 100 

    start_date = start_doy + int(year_truncd*1e3)
    end_date = end_doy + int(year_truncd*1e3)

    date_mask = np.logical_and(wth_tab['@DATE'] >= start_date, wth_tab['@DATE'] <= end_date )

    rain_ts = wth_tab[date_mask]['RAIN']

    raw_labels = [(d,l) for (d, l) in enumerate(range(start_doy, end_doy)) if l % 5 == 0]

    labels = [r[1] for r in raw_labels]
    label_locales = [r[0] for r in raw_labels]


    ax = plt.subplot(int("%d1%d" % (len(years), y + 1)))
    ax.set_title(year)
    #ax.set_xticks(labels, label_locales)
    ax.set_xticks(label_locales)
    ax.set_xticklabels(labels)


    ax.bar(range(len(rain_ts)), rain_ts, color='royalblue', alpha=0.7)
    ax.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)


plt.show()


