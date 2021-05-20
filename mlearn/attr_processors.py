import numpy as np

# -- Form of processor: 

# Input: Dataframe row (acts like a dictionary)
# Output: single scalar

class AttProcessors: 

    # Internal methods 
    @staticmethod
    def _filter_out_n_app(raw_schedule):
        return raw_schedule[raw_schedule[:,1] != 0]

    @staticmethod
    def _filter_out_irr_app(raw_schedule):
        return raw_schedule[raw_schedule[:,1] == 0]

    # Processors 
    @staticmethod
    def application_count(row):
        sched = AttProcessors._filter_out_n_app(row['scheds'])
        app_count = np.shape(sched)[0]

        return app_count

    @staticmethod
    def total_irrigation(row):
        sched = AttProcessors._filter_out_n_app(row['scheds']) 

        return np.sum(sched[:,1])

    def growth_period_of_second_N_app(row):
        return 42


if __name__ == "__main__":
    AttProcessors.foobar(blah)







