import numpy as np

# -- Form of processor: 

# Input: Dataframe row (acts like a dictionary)
# Output: single scalar

class AttProcessors: 

    # --- Internal methods ---
    @staticmethod
    def _filter_out_n_app(raw_schedule):
        return raw_schedule[raw_schedule[:,1] != 0]

    @staticmethod
    def _filter_out_irr_app(raw_schedule):
        return raw_schedule[raw_schedule[:,1] == 0]

    # --- Processors ---
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


    @staticmethod
    def growth_period_of_second_N_app(row):
        return 42


if __name__ == "__main__":
    AttProcessors.foobar(blah)







