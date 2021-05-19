import numpy as np

# -- Form of processor: 

# Input: Dataframe row (acts like a dictionary)
# Output: single scalar

class AttProcessors: 



    @staticmethod
    def application_count(row):
        sched = row['scheds']
        app_count = np.shape(sched)[0]

        return app_count





if __name__ == "__main__":
    AttProcessors.foobar(blah)







