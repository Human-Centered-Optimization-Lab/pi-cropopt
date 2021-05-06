import itertools as it
import pandas as pd
import sys
import math
import numpy as np
from dssat4dum import Dssat4Dum
import os
import re

IRR_PREAMBLE = """@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME
%2d     1   -99   -99   -99   -99   -99   -99 -99
@I IDATE  IROP IRVAL"""


NIT_PREAMBLE = "@F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME"

NIT_FORMAT_STR = "%2d %05d FE001 AP002    10 %5d   -99   -99   -99   -99   -99 -99"

IRR_FORMAT_STR = "%2d %05d IR001 %5d"

TREAT_FORMAT_STR = "%2d 1 0 0 %25s  1  1  0  1  1 %2d %2d  0  0  0  0  0  1"


IRR_TREATMENTS = [
        {'amount': 10, 'interval': 3, 'start': 'V8', 'end': 'R2'},
        {'amount': 20, 'interval': 3, 'start': 'V8' , 'end': 'R2'},
        {'amount': 10, 'interval': 5, 'start': 'V8' , 'end': 'R2'}, 
        {'amount': 10, 'interval': 5, 'start': 'V8' , 'end': 'R2'},
        {'amount': 10, 'interval': 3, 'start': 'V14', 'end': 'R2'},
        {'amount': 20, 'interval': 3, 'start': 'V14', 'end': 'R2'},
        {'amount': 10, 'interval': 5, 'start': 'V14', 'end': 'R2'},
        {'amount': 10, 'interval': 5, 'start': 'V14', 'end': 'R2'} 
        ]

NIT_APP = [
        {'proportion1':  0.75 , 'date1': 'P', 'proportion2': 0.25, 'date2': 'V6' },
        {'proportion1':  0.75 , 'date1': 'P', 'proportion2': 0.25, 'date2': 'V8' },
        {'proportion1':  0.75 , 'date1': 'P', 'proportion2': 0.25, 'date2': 'V10'},
        {'proportion1':  1    , 'date1': 'P', 'proportion2': 0.0,  'date2': 'V6'  }
    ]

NIT_TOTAL = 200

year = int(sys.argv[1])
temp_file = sys.argv[2]

#open text file in read mode
template_file = open(temp_file, "r")

#read whole file to a string
template = template_file.read()

#close file
template_file.close()

app_man_csv = "management_dates.csv"
app_man = pd.read_csv(app_man_csv)
year_mgt_practices = app_man[app_man['Year'] == year].iloc[0]

treatment_summary_arr = []
irrigation_arr = []
fertilizer_arr = [NIT_PREAMBLE]

trunc_year = int(year % 1e2)
trunc_year = "%02d" % trunc_year

for (i,(irr, nit)) in enumerate(it.product(IRR_TREATMENTS, NIT_APP)):

    ## Generate irrigation applications
    start_day = year_mgt_practices[irr['start']]
    end_day = year_mgt_practices[irr['end']]

    app_count = math.floor((end_day - start_day)/irr['interval'])
  
    irr_apps = np.array([(year_mgt_practices['P']+a*irr['interval'], 0, 0, 0, 0) for a in range(app_count)])

    # Add the year 
    irr_apps[:,0] = irr_apps[:,0] + year*1e3

    # Add the irrigation amount
    irr_apps[:,1] = irr['amount']

    ## Generate nitrogen application
    
    # application one
    nit_apps = np.array([[year_mgt_practices[nit['date1']], 0, nit['proportion1']*NIT_TOTAL, 0, 0],
                         [year_mgt_practices[nit['date2']], 0, nit['proportion2']*NIT_TOTAL, 0, 0]])

    # Filter out zero values 
    nit_apps = nit_apps[nit_apps[:,2] != 0]

    nit_apps[:,0] = nit_apps[:,0] + year*1e3

    treat_no = i + 1

    # Format irrigation
    irr_apps[:,0] = irr_apps[:,0] % 1e5

    irr_lines = [IRR_FORMAT_STR % (treat_no, app[0], app[1]) for app in irr_apps.tolist()] 

    irrigation_arr.append(IRR_PREAMBLE % treat_no)
    irrigation_arr = irrigation_arr + irr_lines

    # Format nitrogen
    nit_apps[:,0] = nit_apps[:,0] % 1e5
     
    nit_lines = [NIT_FORMAT_STR % (treat_no, app[0], app[2]) for app in nit_apps.tolist()] 

    # Format treatment section 
    fertilizer_arr = fertilizer_arr + nit_lines 

    run_description = "%da%di%ds%se%s|%0.2f" % (year,irr['amount'], irr['interval'], irr['start'], irr['end'], nit['proportion1'])

    run_description = run_description.ljust(25, ' ')


    treat_line = TREAT_FORMAT_STR % (treat_no, run_description, treat_no, treat_no)
    treatment_summary_arr.append(treat_line)


treat_section = "\n".join(treatment_summary_arr)
irr_section = "\n".join(irrigation_arr)
nut_section = "\n".join(fertilizer_arr)


template = re.sub(r'TREAT_HERE', treat_section, template)
template = re.sub(r'IRR_HERE', irr_section, template)
template = re.sub(r'FERT_HERE', nut_section, template)


if year % 4 == 0:
    plant_date = "136"
else: 
    plant_date = "135"


template = re.sub(r'ZZ', trunc_year, template)
template = re.sub(r'QQQ', plant_date, template)



print(template)


