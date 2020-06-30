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


        
        for indx, period in enumerate(self._calc_period_indices(date_ranges)):

            minindex = period[0]
            maxindex = period[1]

            mins[minindex:maxindex] = date_ranges[indx, self.MIN_APP]
            maxs[minindex:maxindex] = date_ranges[indx, self.MAX_APP]
           
#        offset = 0 
#        for period in range(0, np.size(self.date_ranges, 0)):

#            minDate = date_ranges[period,self.MIN_DATE]
#            maxDate = date_ranges[period,self.MAX_DATE]

#            minindex = offset
#            maxindex = minindex + (maxDate - minDate)  + 1

#            mins[minindex:maxindex] = date_ranges[period, self.MIN_APP]
#            maxs[minindex:maxindex] = date_ranges[period, self.MAX_APP]
            
#            offset = (maxDate - minDate) + 1


        # TODO make sure we don't need any constraints
        super().__init__(n_var=day_count,
                         n_obj=2,
                         n_constr=0,
                         xl=mins,
                         xu=maxs)

        return  

    def _evaluate(self, x, out, *args, **kwargs):

        # Put into application format
        irrapps = self._build_applications(x, self.date_ranges)

        # Set up a dssat runner that will handle the batch
        runner = Dssat4Dum(self.dssat_home, self.dssat_inp, self.tmp_dir)
    
        # Run batch 
        yields = runner.run_batch(irrapps, self.threads)
  
        # Sum up irrigation
        irr_totals = np.sum(x,1)[np.newaxis]

        out["F"] = np.concatenate((-yields, irr_totals), axis=0).T


    def _calc_period_indices(self, date_ranges):
        
        res = []  
        
        offset = 0 
        for period in range(0, np.size(date_ranges, 0)):

            minDate = date_ranges[period,self.MIN_DATE]
            maxDate = date_ranges[period,self.MAX_DATE]

            minindex = offset
            maxindex = minindex + (maxDate - minDate)  + 1

            res.append((minindex, maxindex))
            
            offset = (maxDate - minDate) + 1
        return res


    # Reformat the genome to irrigation applications for each of the 
    # population's individuals.
    #
    # Input x (dimensions p x k) 
    #           s.t. p is the # of individuals
    #           and k is the dimension of the genome 
    #
    # Input date_ranges (see comments above)
    #
    # Output (dimension p x k x 2)
    #
    # e.g. for one individaul:
    #
    #  x = [23.2, 3.5, 67]
    #   and  
    #  date_ranges = 
    #   [[2018102, 2018103, 0, 10],
    #     2018110, 2018110, 0, 10]]
    #
    # is transformed into 
    #
    #  [[2018102,23.2],
    #   [2018103,3.5],
    #   [2018110,67]]
    #
    def _build_applications(self, x, date_ranges): 

        app_count = np.size(x, 1)

        pop_size = np.size(x, 0)

        irrscheds = np.ones((pop_size, app_count, 2)) * -1

        period_inds = self._calc_period_indices(date_ranges)

        # plug in the genome
        irrscheds[:, :, 1 ] = x

        # Plug in the dates
        for periodInd, period in enumerate(period_inds): 

            startInd = period[0]
            endInd = period[1]

            startDate = date_ranges[periodInd][0]
            endDate = date_ranges[periodInd][1]
            irrscheds[:,startInd:endInd, 0 ] = np.array(range(startDate,endDate+1))    


        return irrscheds     



