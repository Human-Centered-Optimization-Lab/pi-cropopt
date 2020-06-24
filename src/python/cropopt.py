
from multiprocessing import Pool


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
    def __init__(self, threads, dssat_home, dssat_inp, date_ranges):

        self.threads        = threads
        self.dssat_home     = dssat_home
        self.dssat_inp      = dssat_inp
        self.tmp_dir        = tmp_dir
        self.date_ranges    = date_ranges

        # +1 to avoid fencepost error
        day_count = np.sum(
                self.date_ranges[:,MAX_DATE] - self.date_ranges[:,MIN_DATE] + 1
                ) 

        # TODO make sure we don't need any constraints
        super().__init__(n_var=day_count,
                         n_obj=2,
                         n_constr=0,
                         xl=self.date_ranges[:,MIN_APP],
                         xu=self.date_ranges[:,MAX_APP])

    def _evaluate(self, x, out, *args, **kwargs):

        d_runner = dssat4py(self.dssat_home, self.dssat_inp, self.tmp_dir)

        # message x to work in eval_batch

        irrsched = self._format_irrigation(x)

        objectives = d_runner.eval_batch(irrsched, self.threads)

        out["F"] = objectives


    def _format_irrigation(self, x):

        # TODO impelement 

        return x


