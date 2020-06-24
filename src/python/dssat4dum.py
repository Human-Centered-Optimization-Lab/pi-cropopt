from functools import reduce
from multiprocessing import Pool
import numpy as np
from shutil import copytree, copy
import errno

class Dssat4Dum():


    def __init__(self, home, fileio, tmp_dir):

        self.home = home
        self.fileio = fileio
        self.tmp_dir = tmp_dir
        self.activeIds = []       

    # irrsched is a nx2 matrix representing an irrigation schedule of n apps

    def run(self, irrsched, runid=0):

        if runid not in self.activeIds: 
            self._setupDirectory(self.home, self.tmp_dir, runid)

        # self._editIrr(self.fileio, irrsched)

        return 
      
    # irrsched is a nx2xy matrix representing j irrigation schedules of n apps
    def run_batch(self, irrsched, threads=1):

        batch_count = np.size(irrsched, 0)

        # Create the arg list, with the first item being the irrigation 
        # schedule and the second being the run id
        args = list(map((lambda a, ind : (a, ind)), irrsched, range(0,batch_count)))

        yields = []
        with Pool(threads) as p: 
            yields = p.map(run, args)

        return yields

    def _setupDirectory(self, home, temp_dir, runid):

        # TODO should be cross platform delimiter
        temp_run_dir = "%s/dssatrun%04d" % (temp_dir,runid) 

        copytree(home, temp_run_dir)

        

    def _editIrr(self, fileio_in, fileio_out, irrsched):

        # Read data 
        reader = open(fileio_in, "r")

        raw_txt = reader.readlines()

        frmdatarr = np.apply_along_axis( (lambda a : "   %d IR001  %f" % (a[0], a[1])), 1,irrsched)

        frmdat = reduce(
                lambda a,b : "%s\n\r%s" % (a,b) 
                ,frmdatarr
                )

        # Parse file and insert values 

        raw_result = ""
        irrigation_it = -1

        for line in raw_txt:

            if "*IRRIGATION" in line:
                irrigation_it += 1

            if irrigation_it >= 0: 
                irrigation_it += 1        

            if irrigation_it <= 2 :
                raw_result = "%s%s" % (raw_result, line)

            if irrigation_it == 3:
                raw_result = "%s%s\n\r" % (raw_result, frmdat)

            if "*FERTILIZERS" in line:
                raw_result = "%s%s" % (raw_result, line)
                irrigation_it = -1


        return raw_result

        
dssat_home = "../../rundir/"
fileio = "../../rundir/DSSAT47.INP"
tmp_dir = "/tmp/"

runner = Dssat4Dum(dssat_home, fileio, tmp_dir)

irrsched = np.array(np.matrix('[2017123, 22; 2017140, 4]'))

print(runner.run(irrsched))




