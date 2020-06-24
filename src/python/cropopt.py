
from multiprocessing import Pool


class CropOpt(Problem):


    def __init__(self, threads, dssat_home, dssat_inp, tmp_dir):

        self.threads = 4
        self.dssat_home = dssat_home
        self.dssat_inp = dssat_inp
        self.tmp_dir = tmp_dir

        super().__init__(n_var=self.relay_count*2, # we have a lat and long coordinate for each relay
                         n_obj=2,
                         n_constr=0,
                         xl=self.relay_lower_bounds,
                         xu=self.relay_upper_bounds)

    def _evaluate(self, x, out, *args, **kwargs):


        d_runner = dssat4py(self.dssat_home, self.dssat_inp, self.tmp_dir)


        with Pool(processes=self.threads) as pool:
            objs = pool.map(d_runner.eval_irr, [(variables)])


        out["F"] = objectives





