import numpy as np

# -- Form of processor: 

# Input: Dataframe row (acts like a dictionary)
# Output: single scalar

class AttProcessors: 

    # --- Constants ---
    DATE_COL = 0
    IRR_COL = 1
    N_ROW = 2

    # --- Internal methods ---
    @staticmethod
    def _filter_out_n_app(raw_schedule):
        return raw_schedule[raw_schedule[:,AttProcessors.IRR_COL] != 0]

    @staticmethod
    def _filter_out_irr_app(raw_schedule):
        return raw_schedule[raw_schedule[:,AttProcessors.IRR_COL] == 0]

    # --- Transfered attributes ---
    # Or attributes that we're just copying from the main table
    @staticmethod
    def application_count(row):
        return row['irr_app_count']

    @staticmethod
    def total_irrigation(row):
        return row['irr_total']

    @staticmethod
    def yield_(row):
        return row['yield']

    @staticmethod
    def front(row):
        return row['front']

    @staticmethod
    def leaching(row):
        return row['leaching']

    # --- Processed attributes ---

    @staticmethod
    def minimum_irr(row):
        irr_sched = AttProcessors._filter_out_n_app(row['scheds'])
        
        if np.size(irr_sched[:,AttProcessors.IRR_COL]) == 0:
            response = None
        else:
            response = np.min(irr_sched[:,AttProcessors.IRR_COL])

        return response

    @staticmethod
    def maximum_irr(row):
        irr_sched = AttProcessors._filter_out_n_app(row['scheds'])

        if np.size(irr_sched[:,AttProcessors.IRR_COL]) == 0:
            response = None
        else:
            response = np.min(irr_sched[:,AttProcessors.IRR_COL])

        return response

    @staticmethod
    def growth_period_of_second_N_app(row):
        # TODO implement
        return 42


if __name__ == "__main__":
    AttProcessors.foobar(blah)







