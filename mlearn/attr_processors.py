import numpy as np
import sys

# -- Form of processor: 

# Input: Dataframe row (acts like a dictionary)
# Output: single scalar

class AttProcessors: 

    # --- Constants ---
    DATE_COL = 0
    IRR_COL = 1
    N_COL = 2
    GROWTH_STAGES = ['P', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 
                        'V13', 'V14', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    

    # --- Constructor ---
    def __init__(self, weather_tab, gdd_tab, total_p_, normalThreshold, wetThreshold):
        self.weather_tab = weather_tab
        self.gdd_tab = gdd_tab
        self.total_p_ = total_p_
        self.normalThreshold = normalThreshold
        self.wetThreshold = wetThreshold
        

    # --- Internal methods ---


    @staticmethod
    def _filter_out_n_app(raw_schedule):
        return raw_schedule[raw_schedule[:,AttProcessors.IRR_COL] != 0]

    @staticmethod
    def _filter_out_irr_app(raw_schedule):
        return raw_schedule[raw_schedule[:,AttProcessors.IRR_COL] == 0]

    @staticmethod
    def _add_year_to_doy_2dig(doy, year):
        return int((year % 1e2)*1e3 + doy)

    @staticmethod
    def _add_year_to_doy_4dig(doy, year):
        return int(year*1e3 + doy)

    @staticmethod
    def _get_rain_within_period(weather_tab, start, end):
        period_mask = np.logical_and(weather_tab['@DATE'] >= start, weather_tab['@DATE'] <= end)
        rain = weather_tab[period_mask]['RAIN']
        return rain

    @staticmethod
    def _get_period_doys(period, year, gdd_tab):
        end_of_period_ind = AttProcessors.GROWTH_STAGES.index(period) + 1
        end_of_period = AttProcessors.GROWTH_STAGES[end_of_period_ind]
  
        gdds = gdd_tab[gdd_tab['Year'] == year]

        start_date_doy = gdds[period]
        end_date_doy = gdds[end_of_period]

        return (int(start_date_doy), int(end_date_doy))

    @staticmethod
    def _get_irr_period(period, year, gdd_tab, sched):

        sched = AttProcessors._filter_out_n_app(sched)

        # Get the DOY of the period in question
        (start_doy, end_doy) = AttProcessors._get_period_doys(period,  year, gdd_tab)

        start_doy = AttProcessors._add_year_to_doy_4dig(start_doy, year)
        end_doy = AttProcessors._add_year_to_doy_4dig(end_doy, year)

        # filter out the irrigation during the period
        irr_mask = np.logical_and(sched[:,0] >= start_doy, sched[:,0] < end_doy)
        return sched[irr_mask, AttProcessors.IRR_COL]


    @staticmethod
    def _calc_total_irr_per_period(period, year, gdd_tab, sched):
        return np.sum(AttProcessors._get_irr_period(period, year, gdd_tab, sched))

    @staticmethod
    def _calc_freq_irr_per_period(period, year, gdd_tab, sched):
        result = AttProcessors._get_irr_period(period, year, gdd_tab, sched)
        return len(result)

    @staticmethod
    def _get_precip_period(period, year, gdd_tab, weather):

        # Get the DOY of the period in question
        (start_doy, end_doy) = AttProcessors._get_period_doys(period,  year, gdd_tab)

        start_doy = AttProcessors._add_year_to_doy_2dig(start_doy, year)
        end_doy = AttProcessors._add_year_to_doy_2dig(end_doy, year)

        # filter out the irrigation during the period
        p_mask = np.logical_and(weather['@DATE'] >= start_doy, weather['@DATE'] < end_doy)

        return weather['RAIN'][p_mask]

    def _get_period(year, gdd_tab, doy):
        date = AttProcessors._add_year_to_doy_2dig(doy, year)

        gdd_tab_year = gdd_tab[gdd_tab['Year'] == year]
        stages = gdd_tab_year.iloc[[0]].to_numpy()[0][1:]

        # filter out which period we're in 
        matching_stage = [i for (i, s) in  enumerate(stages) if s <= doy and stages[i+1] > doy][0]
     
        # since the first column is the year
        matching_stage = matching_stage + 1

        return gdd_tab_year.columns[matching_stage]


    @staticmethod
    def _calc_total_precip_per_period(period, year, gdd_tab, weather):
        return np.sum(AttProcessors._get_precip_period(period, year, gdd_tab, weather))

    @staticmethod
    def _calc_freq_precip_per_period(period, year, gdd_tab, weather):
        return len(AttProcessors._get_precip_period(period, year, gdd_tab, weather))

    @staticmethod
    def _calc_total_precip_per_period_til(period, year, gdd_tab, weather, doy): 
        date = AttProcessors._add_year_to_doy_2dig(doy, year)
        weather_filtered = weather[weather['@DATE'] <= date]
        return AttProcessors._calc_total_precip_per_period(period, year, gdd_tab, weather_filtered)

    # --- Transfered attributes ---
    # Or attributes that we're just copying from the main table
    def application_count(self, row):
        return row['irr_app_count']

    def total_irrigation(self, row):
        return row['irr_total']

    def yield_(self, row):
        return row['yield']

    def front(self, row):
        return row['front']

    def leaching(self, row):
        return row['leaching']

    # --- Processed attributes ---


    def climate(self, row):

        if self.total_p_ < self.normalThreshold:
            return 0
        elif self.total_p_ < self.wetThreshold:
            return 1
        else:
            return 2

    def total_p(self, row):
        return self.total_p_

    def minimum_irr(self, row):
        irr_sched = AttProcessors._filter_out_n_app(row['scheds'])
        
        if np.size(irr_sched[:,AttProcessors.IRR_COL]) == 0:
            response = None
        else:
            response = np.min(irr_sched[:,AttProcessors.IRR_COL])

        return response

    def maximum_irr(self, row):
        irr_sched = AttProcessors._filter_out_n_app(row['scheds'])

        if np.size(irr_sched[:,AttProcessors.IRR_COL]) == 0:
            response = None
        else:
            response = np.max(irr_sched[:,AttProcessors.IRR_COL])

        return response

    def number_of_precipitation_events(self, row):
        year = row['year']
        gdds = self.gdd_tab[self.gdd_tab['Year'] == year]

        plant_doy = gdds['P']
        maturity_doy = gdds['R6']

        plant_date = AttProcessors._add_year_to_doy_2dig(plant_doy, year)
        maturity_date = AttProcessors._add_year_to_doy_2dig(maturity_doy, year)

        rain = AttProcessors._get_rain_within_period(self.weather_tab, plant_date, maturity_date)

        return np.sum(rain != 0.0)

    def growth_period_of_second_N_app(self, row):

        n_app = AttProcessors._filter_out_irr_app(row['scheds'])
        
        second_app_date = max(n_app[:, AttProcessors.DATE_COL])

        second_app_doy = second_app_date % 1000

        result = None 

        for (s, this_stage) in enumerate(AttProcessors.GROWTH_STAGES[0:-1]): 

            next_stage = AttProcessors.GROWTH_STAGES[s+1]

            this_stage_date = self.gdd_tab[this_stage]
            next_stage_date = self.gdd_tab[next_stage]

            if np.logical_and(second_app_doy >= this_stage_date, second_app_doy <= next_stage_date).any():
                result = this_stage

        return result

    # Physiological properties

    def total_irr_during_v6(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V6', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v7(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V7', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v8(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V8', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v9(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V9', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v10(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V10', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v11(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V11', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v12(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V12', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v13(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V13', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_v14(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('V14', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_R1(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('R1', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_R2(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('R2', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_R3(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('R3', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_irr_during_R4(self, row):
        total_irr = AttProcessors._calc_total_irr_per_period('R4', row['year'], self.gdd_tab, row['scheds'])
        return total_irr

    def total_precip_during_v6(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V6', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v7(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V7', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v8(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V8', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v9(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V9', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v10(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V10', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v11(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V11', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v12(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V12', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v13(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V13', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_v14(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('V14', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_R1(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('R1', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_R2(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('R2', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_R3(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('R3', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def total_precip_during_R4(self, row):
        total_precip = AttProcessors._calc_total_precip_per_period('R4', row['year'], self.gdd_tab, self.weather_tab)
        return total_precip

    def freq_irr_during_v6(self, row):
        return AttProcessors._calc_freq_irr_per_period('V6', row['year'], self.gdd_tab, row['scheds']) 
    
    def freq_irr_during_v7(self, row):
        return AttProcessors._calc_freq_irr_per_period('V7', row['year'], self.gdd_tab, row['scheds']) 
    
    def freq_irr_during_v8(self, row):
        return AttProcessors._calc_freq_irr_per_period('V8', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_v9(self, row):
        return AttProcessors._calc_freq_irr_per_period('V9', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_v10(self, row):
        return AttProcessors._calc_freq_irr_per_period('V10', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_v11(self, row):
        return AttProcessors._calc_freq_irr_per_period('V11', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_v12(self, row):
        return AttProcessors._calc_freq_irr_per_period('V12', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_v13(self, row):
        return AttProcessors._calc_freq_irr_per_period('V13', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_v14(self, row):
        return AttProcessors._calc_freq_irr_per_period('V14', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_R1(self, row):
        return AttProcessors._calc_freq_irr_per_period('R1', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_R2(self, row):
        return AttProcessors._calc_freq_irr_per_period('R2', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_R3(self, row):
        return AttProcessors._calc_freq_irr_per_period('R3', row['year'], self.gdd_tab, row['scheds']) 

    def freq_irr_during_R4(self, row):
        return AttProcessors._calc_freq_irr_per_period('R4', row['year'], self.gdd_tab, row['scheds']) 

    def freq_precip_during_v6(self, row):
        return AttProcessors._calc_freq_precip_per_period('V6', row['year'], self.gdd_tab, self.weather_tab) 
    
    def freq_precip_during_v7(self, row):
        return AttProcessors._calc_freq_precip_per_period('V7', row['year'], self.gdd_tab, self.weather_tab) 
    
    def freq_precip_during_v8(self, row):
        return AttProcessors._calc_freq_precip_per_period('V8', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_v9(self, row):
        return AttProcessors._calc_freq_precip_per_period('V9', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_v10(self, row):
        return AttProcessors._calc_freq_precip_per_period('V10', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_v11(self, row):
        return AttProcessors._calc_freq_precip_per_period('V11', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_v12(self, row):
        return AttProcessors._calc_freq_precip_per_period('V12', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_v13(self, row):
        return AttProcessors._calc_freq_precip_per_period('V13', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_v14(self, row):
        return AttProcessors._calc_freq_precip_per_period('V14', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_R1(self, row):
        return AttProcessors._calc_freq_precip_per_period('R1', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_R2(self, row):
        return AttProcessors._calc_freq_precip_per_period('R2', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_R3(self, row):
        return AttProcessors._calc_freq_precip_per_period('R3', row['year'], self.gdd_tab, self.weather_tab) 

    def freq_precip_during_R4(self, row):
        return AttProcessors._calc_freq_precip_per_period('R4', row['year'], self.gdd_tab, self.weather_tab) 




if __name__ == "__main__":
    AttProcessors.foobar(blah)







