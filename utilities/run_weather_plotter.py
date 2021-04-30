import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Example run: python   utilities/run_weather_plotter.py postprocess/master_run_record.pkl dhome/Weather/CASSREPR.WTH 1981 10738
plot_all = False

run_record_path = sys.argv[1]
wth_file_path = sys.argv[2]
year = int(sys.argv[3])
yield_level = float(sys.argv[4])

# Unpickle
infile = open(run_record_path, 'rb')
run_record = pickle.load(infile)

run_mask = np.logical_and(run_record['year'] == year, run_record['yield'] == yield_level)

matching_entries = np.where(run_mask)[0]

# Reformat date information 
year_truncd = year % 100 

# Fetch weather data
wth_tab = pd.read_fwf(wth_file_path, skiprows=4)

    
if plot_all:
    num_sub_plots = np.size(matching_entries)
else:
    num_sub_plots = 1


for (e, entry) in enumerate(matching_entries): 

    sched = run_record.iloc[entry]['scheds']

    # Separate irrigation and nitrogen
    irr_mask = sched[:,1] != 0
    nitro_mask = sched[:,1] == 0

    irr_sched = sched[irr_mask, 0:2]

    nit_sched = sched[nitro_mask,:][:,[0,2]]

    # Find min and max dates to to display and their various formats
    all_dates = irr_sched[:,0].tolist() + nit_sched[:,0].tolist()
    min_date = int(min(all_dates))
    max_date = int(max(all_dates))

    start_doy = int(min_date % 1e3) 
    end_doy = int(max_date % 1e3)

    start_date = int(min_date % 1e5)
    end_date = int(max_date % 1e5)

    # Build the irrigation data

    raw_irr_list = [0] * max_date
    for r in range(np.shape(irr_sched)[0]):
        date = int(irr_sched[r, 0])
        amount = irr_sched[r, 1]
        raw_irr_list[date-1] = amount

    irr_list = raw_irr_list[(min_date-1):]

    raw_nit_list = [0] * max_date
    for r in range(np.shape(nit_sched)[0]):
        date = int(nit_sched[r, 0])
        amount = nit_sched[r, 1]
        raw_nit_list[date-1] = amount

    nit_list = raw_nit_list[(min_date-1):]

    # Pull the observed weather data
    date_mask = np.logical_and(wth_tab['@DATE'] >= start_date, wth_tab['@DATE'] <= end_date )

    rain_ts = wth_tab[date_mask]['RAIN']

    raw_labels = [(d,l) for (d, l) in enumerate(range(start_doy, end_doy)) if l % 5 == 0]

    labels = [r[1] for r in raw_labels]
    label_locales = [r[0] for r in raw_labels]

    ax = plt.subplot(int("%d1%d" % (num_sub_plots, e + 1)))
    ax.set_title(year)
    ax.set_xticks(label_locales)
    ax.set_xticklabels(labels)
    ax.set_xlabel("Day of year")
    ax.set_ylabel("Log(Irrigation/Precipitation (mm))")
    ax.set_yscale('log')

    ax2 = ax.twinx()
    ax2.set_ylabel("Nitrogen applied (kg/ha)")

    width = 0.3
    
    x = np.array(range(len(rain_ts)))
    
    ax.bar(x - width, rain_ts, color='royalblue', alpha=0.7, width=width, label="Precipitation")
    ax.bar(x, np.array(irr_list), color='red', alpha=0.7, width=width, label="Irrigation")
    ax2.bar(x + width, np.array(nit_list), color='black', alpha=0.7, width=width, label="Nitrogen")

    ax.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    ax.legend(loc="upper right")
    ax2.legend(loc="upper center")

    if not plot_all: 
        break

#plt.legend()
plt.show()


