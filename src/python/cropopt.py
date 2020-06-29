import numpy as np
from pymoo.model.problem import Problem
from dssat4dum import Dssat4Dum

class CropOpt(Problem):

    MIN_DATE    = 0
    MAX_DATE    = 1
    MIN_APP     = 2
    MAX_APP     = 3

    #
    # threads       -- Number of threads for optimization
    # dssat_home    -- Where all of your dssat files are
    # tmp_dir       -- Where to set up the run directories 
    # date_ranges   -- 4xn array of period beginnings, period endings, period 
    #                   minimums, and period maximums
    # 
    def __init__(self, threads, dssat_home, dssat_inp, tmp_dir, date_ranges, seed=0):

        self.threads        = threads
        self.dssat_home     = dssat_home
        self.dssat_inp      = dssat_inp
        self.tmp_dir        = tmp_dir
        self.date_ranges    = date_ranges

        # +1 to avoid fencepost error
        day_count = np.sum(
                self.date_ranges[:,self.MAX_DATE] - self.date_ranges[:,self.MIN_DATE] + 1
                ) 

        mins = np.ones(day_count) * -1
        maxs = np.ones(day_count) * -1


        offset = 0 
        for period in range(0, np.size(self.date_ranges, 0)):

            minDate = date_ranges[period,self.MIN_DATE]
            maxDate = date_ranges[period,self.MAX_DATE]

            minindex = offset
            maxindex = minindex + (maxDate - minDate)  + 1

            mins[minindex:maxindex] = date_ranges[period, self.MIN_APP]
            maxs[minindex:maxindex] = date_ranges[period, self.MAX_APP]
            
            offset = (maxDate - minDate) + 1

        # TODO make sure we don't need any constraints
        print("in")
        super().__init__(n_var=day_count,
                         n_obj=2,
                         n_constr=0,
                         xl=mins,
                         xu=maxs)

        print("done")
        return  

    def _evaluate(self, x, out, *args, **kwargs):

        print("******")
        print(np.shape(x))
        print("******")

        #d_runner = dssat4dum(self.dssat_home, self.dssat_inp, self.tmp_dir)


        # message x to work in eval_batch

        irrsched = self._format_irrigation(x)

        objectives = d_runner.eval_batch(irrsched, self.threads)

        out["F"] = objectives


    def _format_irrigation(self, x):

        # TODO impelement 

        return x


