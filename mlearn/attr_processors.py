import numpy as np

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
    def __init__(self, weather_tab, gdd_tab):
        self.weather_tab = weather_tab
        self.gdd_tab = gdd_tab

    # --- Internal methods ---
    @staticmethod
    def _filter_out_n_app(raw_schedule):
        return raw_schedule[raw_schedule[:,AttProcessors.IRR_COL] != 0]

    @staticmethod
    def _filter_out_irr_app(raw_schedule):
        return raw_schedule[raw_schedule[:,AttProcessors.IRR_COL] == 0]

    @staticmethod
    def _add_year_to_doy(doy, year):
        return int((year % 1e2)*1e3 + doy)

    @staticmethod
    def _get_rain_within_period(weather_tab, start, end):
        period_mask = np.logical_and(weather_tab['@DATE'] >= start, weather_tab['@DATE'] <= end)
        rain = weather_tab[period_mask]['RAIN']
        return rain

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
            response = np.min(irr_sched[:,AttProcessors.IRR_COL])

        return response

    def number_of_precipitation_events(self, row):
        year = row['year']
        gdds = self.gdd_tab[self.gdd_tab['Year'] == year]

        plant_doy = gdds['P']
        maturity_doy = gdds['R6']

        plant_date = AttProcessors._add_year_to_doy(plant_doy, year)
        maturity_date = AttProcessors._add_year_to_doy(maturity_doy, year)

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


if __name__ == "__main__":
    AttProcessors.foobar(blah)







