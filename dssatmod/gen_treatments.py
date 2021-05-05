import itertools as it
import pandas as pd
import sys
import math
import numpy as np
from dssat4dum import Dssat4Dum
import os

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
        {'proportion1':  1    , 'date1': 'P', 'proportion2': 0.0,  'date2': 'P'  }
    ]

NIT_TOTAL = 200


year = int(sys.argv[1])
app_man_csv = "management_dates.csv"
app_man = pd.read_csv(app_man_csv)
year_mgt_practices = app_man[app_man['Year'] == year].loc[0]


for (irr, nit) in it.product(IRR_TREATMENTS, NIT_APP):
   
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

    nit_apps[:,0] = nit_apps[:,0] + year*1e3

    apps = np.concatenate((irr_apps, nit_apps))

    print(Dssat4Dum.formatIrrSched(apps))
    print(Dssat4Dum.formatNutSched(apps))



