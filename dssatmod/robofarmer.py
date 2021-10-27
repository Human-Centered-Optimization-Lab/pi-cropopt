import sys
import pandas as pd
import numpy as np
from dssat4dum import Dssat4Dum

class CommonPractice():

    def __init__(self, wth_tab, gdd_tab, year):
        self.not_applied_n = True
        wth_tab = wth_tab
        gdd_tab = gdd_tab 

        self.year = year

        self.year_modded = int((year  % 1e2) * 1e3) 
        wth_mask = np.logical_and(wth_tab['@DATE'] >= self.year_modded, wth_tab['@DATE'] < (self.year_modded + 366))
        
        self.wth_tab_year = wth_tab[wth_mask]
        self.gdd_tab_year = gdd_tab[gdd_tab['Year'] == year]
        self.total_nitro = 200
        self.irrigation_record = {}
        

    def _get_past_rain_conditions(self, current_day, n):
        # Get previous n days of irrigation and precipitation

        current_date_code = self.year_modded + current_day

        # Tally up total past rain
        total_rain = 0.0
        for prev_days in range(n):
            day = current_date_code - prev_days - 1
            rain = float(self.wth_tab_year[self.wth_tab_year['@DATE'] == day].RAIN) 
            total_rain = total_rain + rain
        
        return total_rain
        

    def _get_future_rain_conditions(self, current_day, n):

        current_date_code = self.year_modded + current_day

        total_rain = 0.0
        # Tally up the total rain for next few days
        for next_day in range(n):
            day = current_date_code + next_day + 1
            rain = float(self.wth_tab_year[self.wth_tab_year['@DATE'] == day].RAIN) 
            total_rain = total_rain + rain

        return total_rain


    def make_management_decision(self, current_day):


        past_3day_rain = self._get_past_rain_conditions(current_day, 3)
        past_5day_rain = self._get_past_rain_conditions(current_day, 5)
        future_rain = self._get_future_rain_conditions(current_day, 2)

        total_past_fut_rain = past_3day_rain + future_rain



        # Irrigation logic
        if current_day < int(self.gdd_tab_year.V6) or current_day >= int(self.gdd_tab_year.R2):
            # If out of irrigation window, do nothing and move forward a day
            day_delta = 1
            irr_amount = 0
        elif current_day < int(self.gdd_tab_year.R1): 
            # If plant still in vegetative stage

            if past_5day_rain >= 20: 
                # Avoid irrigation in heavy rain period
                irr_amount = 0
                day_delta = 10
            if total_past_fut_rain >= 10:
                # Skip irrigation if needs already met
                irr_amount = 0 
                day_delta = 5
            else: 
                # Make up for irrigation deficit if needed
                irr_amount = 10 - total_past_fut_rain 
                day_delta = 5


        elif current_day < int(self.gdd_tab_year.R2): 
            # If plant is in the reproductive stages

            if past_5day_rain >= 20: 
                # Avoid irrigation in heavy rain period
                irr_amount = 0
                day_delta = 10
            elif total_past_fut_rain >= 20:
                # Skip irrigation if needs already met
                irr_amount = 0
                day_delta = 5
            else:
                # Make up for irrigation deficit if needed
                irr_amount = 20 - total_past_fut_rain
                day_delta = 5

        if irr_amount != 0:
            self.irrigation_record[self.year_modded + current_day] = irr_amount



        # Nitrogen logic
        if current_day == int(self.gdd_tab_year.P): 
            nitro_amount = self.total_nitro*0.75
        elif current_day > int(self.gdd_tab_year.V6) and self.not_applied_n: 
            nitro_amount = self.total_nitro*0.25
            self.not_applied_n = False
        else: 
            nitro_amount = 0

        return (irr_amount, nitro_amount, current_day + day_delta)


class RoboFarmer():


    def __init__(self, manager):

        self.manager = manager


    def realize_year(self):


        # To become a 2D array 
        raw_management = []

        current_day = int(self.manager.gdd_tab_year.P) 

        while current_day < int(self.manager.gdd_tab_year.R4):

            (irr_amount, nitro_amount, next_day) = self.manager.make_management_decision(current_day)

            year_code = year*1e3 + current_day

            if irr_amount != 0:
                raw_management.append([year_code, irr_amount, 0, 0, 0])

            if nitro_amount != 0: 
                raw_management.append([year_code, 0, nitro_amount, 0, 0])


            current_day = next_day
            

        management = np.array(raw_management)

        return management


if __name__ == "__main__":

    # Gather weather data
    wth_file_path = "dhome/Weather/CASSREPR.WTH"
    gdd_tab_path = "management_dates.csv"

    wth_tab = pd.read_fwf(wth_file_path, skiprows=4)
    gdd_tab = pd.read_csv(gdd_tab_path)

    #wet_years = [2011, 2018, 2019] Bring this back if we GDD on 2018 and 2019
    wet_years = [2011]
    normal_years = dates = list(range(2013,2018)) 
    dry_years = [2012]

    # DSSAT parameters
    #home_dir = "/Users/iankropp/"
    home_dir = "/home/ian/"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-linux" % home_dir
    dssat_inp = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    output_dir = "%s/Projects/agovization/output/" % home_dir

    tmp_dir = "/tmp/"

    threads = 8

    # Initialize DSSAT runner
    dssat = Dssat4Dum(dssat_home, dssat_inp, dssat_exe, tmp_dir)

    # inputs for DSSAT
    schedules = []
    updates = []

    # Results 
    year_col = [] 
    climate = []

    for year in wet_years: 

        # Initialize robo farmer
        com_pract_manager = CommonPractice(wth_tab, gdd_tab, year)
        rfarmer = RoboFarmer(com_pract_manager)

        # Generate schedule for this year
        schedules.append(rfarmer.realize_year())
       
        
        if year % 4 == 0:
            plant_date = 136
        else:
            plant_date = 135

        updates.append({ 'pdate': year*1e3 + plant_date, 'sdate': year*1e3 + plant_date, 'icdat': year*1e3 + plant_date })
        year_col.append(year)
        climate.append(2)

    for year in normal_years: 

        # Initialize robo farmer
        com_pract_manager = CommonPractice(wth_tab, gdd_tab, year)
        rfarmer = RoboFarmer(com_pract_manager)

        schedules.append(rfarmer.realize_year())

        if year % 4 == 0:
            plant_date = 136
        else:
            plant_date = 135

        updates.append({ 'pdate': year*1e3 + plant_date, 'sdate': year*1e3 + plant_date, 'icdat': year*1e3 + plant_date })
        year_col.append(year)
        climate.append(1)
        

    for year in dry_years: 


        # Initialize robo farmer
        com_pract_manager = CommonPractice(wth_tab, gdd_tab, year)
        rfarmer = RoboFarmer(com_pract_manager)
        
        if year % 4 == 0:
            plant_date = 136
        else:
            plant_date = 135

        schedules.append(rfarmer.realize_year())
        updates.append({ 'pdate': year*1e3 + plant_date, 'sdate': year*1e3 + plant_date, 'icdat': year*1e3 + plant_date })
        year_col.append(year)
        climate.append(0)


    dssat_result = dssat.run_batch(schedules, threads, updates=updates)


    full_result_mat = np.c_[year_col, climate, dssat_result]


    result = pd.DataFrame(full_result_mat, columns=['year', 'climate', 'yield', 'leaching'])


    print(result)




































