import sys
import pandas as pd
import numpy as np
from dssatmod.dssat4dum import Dssat4Dum
from mlearn.attr_processors import AttProcessors as ap


class Practices(): 

    def __init__(self, wth_tab, gdd_tab, year, climate=-1):
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
        self.climate = climate

    def _get_past_rain_conditions(self, current_day, n):
        current_date_code = self.year_modded + current_day
        rain_ts = ap._get_rain_within_period(self.wth_tab_year, current_date_code - n , current_date_code - 1)
        return sum(rain_ts)
        

    def _get_future_rain_conditions(self, current_day, n):
        current_date_code = self.year_modded + current_day
        rain_ts = ap._get_rain_within_period(self.wth_tab_year, current_date_code + 1, current_date_code + n)
        return sum(rain_ts)


class MachRecdPractices(Practices):

    def make_management_decision(self, current_day):


        STAGE_UPDATES = { 
            'V6': -0.098976109215017,
            'V7': 0.311203319502075,
            'V8': 0.130841121495327,
            'V9': 0.506849315068493,
            'V10': 0.6,
            'V11': -0.00507614213197959,
            'V12': -0.0051282051282052,
            'V13': 0.142857142857143,
            'V14': 0.139705882352941,
            'R1': -0.100830367734282
        }


        #STAGE_UPDATES_DRY = {
        #    'V6': -0.00341296928327638,
        #    'V7': -0.443983402489627,
        #    'V8': 0.0186915887850468,
        #    'V9': 0.780821917808219,
        #    'V10': -0.383333333333333,
        #    'V11': 0.522842639593909,
        #    'V12': 0.117948717948718,
        #    'V13': -0.263157894736842,
        #    'V14': 0.389705882352941,
        #    'R1': -0.513641755634638
        #        }

        #STAGE_UPDATES_NORMAL = {
        #    'V6': -0.52901023890785,
        #    'V7': 0.311203319502075,
        #    'V8': -0.280373831775701,
        #    'V9': 0.287671232876712,
        #    'V10': -0.0666666666666667,
        #    'V11': -0.532994923857868,
        #    'V12': -0.292307692307692,
        #    'V13': -0.293233082706767,
        #    'V14': 0.166666666666667,
        #    'R1': -0.311981020166073
        #    }

        #STAGE_UPDATES_WET = {
        #    'V6': 0.255972696245734,
        #    'V7': 1.79668049792531,
        #    'V8': -0.177570093457944,
        #    'V9': 1.9041095890411,
        #    'V10': 0.7,
        #    'V11': -0.299492385786802,
        #    'V12': 0.0153846153846154,
        #    'V13': 0.338345864661654,
        #    'V14': -0.230392156862745,
        #    'R1': 0.311981020166074,
        #        }



        #if self.climate == 0: 
        #    stage_updates = STAGE_UPDATES_DRY
        #elif self.climate == 1:
        #    stage_updates = STAGE_UPDATES_NORMAL
        #elif self.climate == 2:
        #    stage_updates = STAGE_UPDATES_WET


        stage_updates = STAGE_UPDATES

        period = ap._get_period(self.year, self.gdd_tab_year, current_day)

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

            threshold = 10 + 10*stage_updates[period] 
            
            if past_5day_rain >= 20: 
                # Avoid irrigation in heavy rain period
                irr_amount = 0
                day_delta = 10
            if total_past_fut_rain >= threshold:
                # Skip irrigation if needs already met
                irr_amount = 0 
                day_delta = 5
            else: 
                # Make up for irrigation deficit if needed
                irr_amount = threshold - total_past_fut_rain 
                day_delta = 5


        elif current_day < int(self.gdd_tab_year.R2): 
            # If plant is in the reproductive stages

            threshold = 20  + 20 *stage_updates[period]
            if past_5day_rain >= 20: 
                # Avoid irrigation in heavy rain period
                irr_amount = 0
                day_delta = 10
            elif total_past_fut_rain >= threshold:
                # Skip irrigation if needs already met
                irr_amount = 0
                day_delta = 5
            else:
                # Make up for irrigation deficit if needed
                irr_amount = threshold - total_past_fut_rain
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


class CommonPractice(Practices):
        
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

            year_code = self.manager.year*1e3 + current_day

            if irr_amount != 0:
                raw_management.append([year_code, irr_amount, 0, 0, 0])

            if nitro_amount != 0: 
                raw_management.append([year_code, 0, nitro_amount, 0, 0])


            current_day = next_day
            

        management = np.array(raw_management)

        return management


