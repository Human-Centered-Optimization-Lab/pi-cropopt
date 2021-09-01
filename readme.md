# Agricultural Innovization

## Overview

This project contains an innovization framework, which entails: 

1. Optimization of crop management practices over many years of climate data (1980 - 2010) (the `optimization` folder)
2. Converting data into a single data table (`postprocess` folder) 
3. Converting run information into human readable attributes (`step0_build_attr_tab.py`)
4. Run machine learning routines on human readable attributes (to do)


## File summary


```
 dhome                          # Where DSSAT is ran from
├── dssatmod
│   ├── createexp.sh
│   ├── dssat4dum.py            # Simple dssat wrapper
│   ├── exp_gens                # Means of generating DSSAT-formatted fert. and irr. applications for result validation 
│   │   ├── fertilizer.py     
│   │   └── irrigation.py
│   ├── genallexp.sh            # ???    ┐
│   ├── genexp.py               # ???    ├  I believe I used these script to validate DSSAT runs
│   ├── parse_bmp.py            # ???    │
│   └── printEXPFile.py         # ???    ┘
├── management_dates.csv
├── mlearn
│   ├── attr_processors.py      # Module with all of the attribute processing routines
│   └── step0_build_attr_tab.py
├── optimization
│   ├── appCounter.py           # Takes the genome of an irrigation optimization run and returns the number of applications in each solution. 
│   ├── cropopt.py              # The optimization problem fed into pymoo, including objective function 
│   ├── cropover.py             # Implementation of the cropover routine
│   ├── main.py                 # The main file for the optimization portion of agricultural innovization
│   ├── main_cropverVsSPS.py    # Script I used to compare the performance of cropover and sparse population sampling
│   └── sps.py
├── plotting
│   ├── plotAnnotatedPF.py      # Plots a Pareto front that also shows the number of applications in each solution
│   ├── plotHV.py               # Plots the hyper-volume of a given run
│   └── plotRuns.py             # Plots irrigation, yield, and number of applications in each solution
├── postprocess
│   ├── step0_run_summary.py    # Aggregates multiple runs into a single data table (run_results.xlsx)
│   ├── step1_plotPareto.py     # Plots... global pareto front? 
│   └── step1a_weather_stats.py # Plots... weather stats?? 
├── seeds.csv
└── utilities
    ├── print_table.py          # Prints tables to standard out. Only good for small tables
    ├── results_translator.py   # Pulls a solution from the results table and prints it out...?
    ├── run_weather_plotter.py  # Plots irrigation and precipitation for a given year and solution
    ├── show_table.py           # For showing pkl'd tables
    └── weather_plotter.py      # Plots precipation for a given year
```



## Installing

```
conda create --name my_project_env
pip install -r requirements.txt
```

