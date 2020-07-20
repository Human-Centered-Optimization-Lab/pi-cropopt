import numpy as np
from pymoo.model.problem import Problem
import sys

from dssat4dum import Dssat4Dum

class CropOpt(Problem):

    MIN_DATE    = 0
    MAX_DATE    = 1
    APP_TYPE    = 2

    # Irrigation params
    MIN_IRR_APP = 3
    MAX_IRR_APP = 4
   
    # Nutrient params
    N_APP = 3
    PHOS_APP = 4
    POT_APP = 5
    


    IRR_APP_TYPE = 0
    NUT_APP_TYPE = 1

    #
    # threads       -- Number of threads for optimization
    # dssat_home    -- Where all of your dssat files are
    # tmp_dir       -- Where to set up the run directories 
    # date_ranges   -- 4xn array of period beginnings, period endings, period 
    #                   minimums, and period maximums
    # 
    def __init__(self, threads, dssat_home, dssat_inp, 
            tmp_dir, date_ranges, output_dir, run, seed=0, constant_apps=None):

        self.threads     = threads
        self.dssat_home  = dssat_home
        self.dssat_inp   = dssat_inp
        self.tmp_dir     = tmp_dir
        self.date_ranges = date_ranges
        self.output_dir  = output_dir
        self.run         = run
        self.generation  = 0
        self.constant_apps = constant_apps

        # Separate the nutrient apps from the irrigation apps
        irrigation_ranges = date_ranges[date_ranges[:,2] == self.IRR_APP_TYPE]
        nutrient_ranges   = date_ranges[date_ranges[:,2] == self.NUT_APP_TYPE]


        # Count irrigation dates
        # +1 to avoid fencepost error
        day_count = irr_count = np.sum(
                irrigation_ranges[:,self.MAX_DATE] - irrigation_ranges[:,self.MIN_DATE] + 1
                ) 

        # Count nutrient applications 
        nutrient_app_count = np.size(nutrient_ranges,0)
        day_count += nutrient_app_count

        mins = np.ones(day_count) * -1
        maxs = np.ones(day_count) * -1

       
        (irr_period_indices, nutrient_period_indices) = self.calc_period_indices(date_ranges)

        for period in irr_period_indices:

            (periodInd, minindex, maxindex) = period

            mins[minindex:maxindex] = date_ranges[periodInd, self.MIN_IRR_APP]
            maxs[minindex:maxindex] = date_ranges[periodInd, self.MAX_IRR_APP]
        
        for period in nutrient_period_indices:

            (periodInd, indx) = period

            mins[indx] = date_ranges[periodInd, self.MIN_DATE]
            maxs[indx] = date_ranges[periodInd, self.MAX_DATE]


        # TODO constraints? 
        super().__init__(n_var=day_count,
                         n_obj=3,           # (Yield, leaching, total irrigation)
                         n_constr=0,
                         xl=mins,
                         xu=maxs)

    def _evaluate(self, x, out, *args, **kwargs):

        # Round the genome to the nearest mm
        x_rounded = np.around(x)

        # Put into application format
        irrapps = self._build_applications(x_rounded, self.date_ranges)

        # Set up a dssat runner that will handle the batch
        runner = Dssat4Dum(self.dssat_home, self.dssat_inp, self.tmp_dir, constant_apps=self.constant_apps)
    
        # Run batch 
        yield_and_leaching = runner.run_batch(irrapps, self.threads)
 
        yld = yield_and_leaching[:,0][np.newaxis]

        leaching = yield_and_leaching[:,1][np.newaxis]

        # Calc irrigation indices 

        ranges = self.calc_period_indices(self.date_ranges)[0]

        ranges = np.array(ranges)

        ranges = ranges[:,1:3]

        irr_indices = []

        for row in range(np.size(ranges,0)):
              irr_indices += list(range(ranges[row,0], ranges[row,1]))


        # Sum up irrigation
        #irr_totals = np.sum(x_rounded[irr_indices],1)[np.newaxis]
        irr_totals = np.sum(x_rounded[:,irr_indices],1)[np.newaxis]

        # First column of results are yield, second is leaching
        objectives = np.concatenate((-yld, leaching, irr_totals), axis=0).T

        np.savetxt("%s/run%04d_gen%04d_obj.csv" % (self.output_dir, self.run, self.generation), objectives, delimiter=",")
        np.savetxt("%s/run%04d_gen%04d_var.csv" % (self.output_dir, self.run, self.generation), x_rounded, delimiter=",")
        
        self.generation = self.generation + 1

        out["F"] = objectives


    # Returns (a, b, c)
    #
    # a -> original date range index
    # b -> Beginning of range in genome
    # c -> End of range in genome
    #
    def calc_period_indices(self, date_ranges):
        
        res_irr = []  
        res_nut = []  
       
        offset = 0 
        for period in range(0, np.size(date_ranges, 0)):


            minDate = date_ranges[period,self.MIN_DATE]
            maxDate = date_ranges[period,self.MAX_DATE]

            minindex = offset
            maxindex = minindex + (maxDate - minDate)  + 1

            if date_ranges[period, self.APP_TYPE] == self.IRR_APP_TYPE:
                res_irr.append((period,minindex, maxindex))
                offset = (maxDate - minDate) + 1
            else:
                res_nut.append((period, offset))
                offset += 1
            

        return (res_irr, res_nut)


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
    #   [[2018102, 2018103, 0, 0, 10],
    #     2018110, 2018110, 0, 0, 10]]
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

        scheds = np.ones((pop_size, app_count, 5)) * -1

        (irr_period_inds, nut_period_inds) = self.calc_period_indices(date_ranges)

        # plug in the genome for irrigation
        #scheds[:, :, 1 ] = x[]

        # Plug in the irrigation dates
        for period in irr_period_inds: 

            (periodInd, startInd, endInd) = period

            # Plug in the genome for this irrigation period
            scheds[:, startInd:endInd,1] = x[:, startInd:endInd]

            startDate = date_ranges[periodInd][0]
            endDate = date_ranges[periodInd][1]
            scheds[:,startInd:endInd, 0 ] = np.array(range(startDate,endDate+1))    

            # Empty nutrient values
            scheds[:,startInd:endInd, 2 ] = 0
            scheds[:,startInd:endInd, 3 ] = 0
            scheds[:,startInd:endInd, 4 ] = 0


        # Translate the nutrient dates 
        for period in nut_period_inds:

            (periodInd, indx) = period
           
            date = np.around(x[:,indx])
            n_amount = date_ranges[periodInd, self.N_APP]
            phos_amount = date_ranges[periodInd, self.PHOS_APP]
            pot_amount = date_ranges[periodInd, self.POT_APP]

            # Empty irrigation value
            scheds[:, indx, 1]  = 0

            if np.sum(np.isnan(date)) != 0:
                sys.exit("Whoops")

            # Fill in nutrient values
            scheds[:, indx, 0]  = date
            scheds[:, indx, 2]  = n_amount
            scheds[:, indx, 3]  = phos_amount
            scheds[:, indx, 4]  = pot_amount

        if np.sum(scheds == -1) != 0:
            sys.exit("Schedule not properly built")


        if np.sum(scheds == None) != 0:
            sys.exit("Schedule not properly built")


        return scheds     


