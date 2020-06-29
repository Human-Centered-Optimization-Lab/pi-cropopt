from functools import reduce
from multiprocessing import Pool
import numpy as np
from shutil import copytree, copy, rmtree
from glob import glob
import subprocess as sp
import os, re


class Dssat4Dum():


    def __init__(self, home, fileio, tmp_dir):

        self.home = home
        self.fileio = fileio
        self.tmp_dir = tmp_dir
        self.activeIds = []       
       
        # delete old run directories
        files2del = glob("%s/dssatrun*" % self.tmp_dir) 

        for f in files2del: 
            print("Deleting %s..." % f)
            rmtree(f);
            print("Deleted.")


    # irrsched is a nx2 matrix representing an irrigation schedule of n apps
    def run(self, argz):

        runid = argz[0]
        irrsched = argz[1]

        if runid not in self.activeIds: 
            self._setupDirectory(self.home, self.tmp_dir, runid)

        rundir = self._getRunDir(self.tmp_dir, runid)

        fileio_temp = "%s/DSSAT47.INP" % rundir

        self._editIrr(self.fileio, fileio_temp, irrsched)

        yld = self._runDssat(rundir, fileio_temp)

        return yld

    # irrsched is a jx2xn matrix representing j irrigation schedules of n apps
    def run_batch(self, irrsched, threads=1):


        batch_count = np.size(irrsched, 0)

        # Create the arg list, with the first item being the irrigation 
        # schedule and the second being the run id
        argz = []
        for ind,dat in enumerate(irrsched): 
            argz.append((ind, dat))

        yields = []
        if threads == 1: 
            # Eschew multiprocessing for debugging ease
            for r in range(0, batch_count):
                yields.append(self.run(argz[r]))
        else: 
            with Pool(threads) as p: 
                yields = p.map(self.run, argz)

        return yields

    def _runDssat(self, dssat_path, fileio):
                
        os.chdir(dssat_path)

        res = sp.run(["./dscsm047", "D", "DSSAT47.INP"], check=True)

        # TODO check for errors
       
        # Read output

        reader = open("OVERVIEW.OUT", "r", errors="ignore")

        raw_txt = "".join(reader.readlines())
        
        yld = re.search("\s*\w*\s+YIELD\s+:\s+(\d+)\s+kg/ha",raw_txt).group(1)

        return int(yld)

    def _setupDirectory(self, home, temp_dir, runid):

        # TODO should be cross platform delimiter
        temp_run_dir = self._getRunDir(temp_dir, runid)

        copytree(home, temp_run_dir)

    def _getRunDir(self, temp_dir, runid):

        if temp_dir[-1] == '/':
            return "%sdssatrun%04d" % (temp_dir,runid) 
        else:
            return "%sdssatrun%04d" % (temp_dir,runid) 


    def _editIrr(self, fileio_in, fileio_out, irrsched):

        # Read data 
        reader = open(fileio_in, "r")

        raw_txt = reader.readlines()

        frmdatarr = np.apply_along_axis( (lambda a : "   %d IR001  %f" % (a[0], a[1])), 1,irrsched)

        frmdat = reduce(
                lambda a,b : "%s\n%s" % (a,b) 
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
                raw_result = "%s%s\n" % (raw_result, frmdat)

            if "*FERTILIZERS" in line:
                raw_result = "%s%s" % (raw_result, line)
                irrigation_it = -1

        # Write results to file

        f = open(fileio_out, "w")
       
        f.write(raw_result)

        
dssat_home = "/home/ian/Projects/dssat4py/rundir/"
fileio = "/home/ian/Projects/dssat4py/rundir/DSSAT47.INP"
tmp_dir = "/tmp/"

runner = Dssat4Dum(dssat_home, fileio, tmp_dir)

irrscheds = np.zeros((100, 3, 2))

irrscheds[0] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[1] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[2] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[3] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[4] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[5] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[6] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[7] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[8] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[9] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[10] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[11] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[12] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[13] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[14] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[15] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[16] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[17] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[18] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[19] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[20] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[21] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[22] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[23] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[24] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[25] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[26] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[27] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[28] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[29] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[30] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[31] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[32] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[33] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[34] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[35] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[36] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[37] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[38] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[39] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[40] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[41] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[42] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[43] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[44] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[45] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[46] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[47] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[48] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[49] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[50] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[51] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[52] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[53] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[54] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[55] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[56] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[57] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[58] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[59] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[60] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[61] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[62] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[63] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[64] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[65] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[66] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[67] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[68] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[69] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[70] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[71] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[72] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[73] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[74] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[75] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[76] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[77] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[78] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[79] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[80] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[81] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[82] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[83] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[84] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[85] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[86] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[87] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[88] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[89] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))
irrscheds[90] = np.array(np.matrix('[1982123, 8 ; 1982140, 11; 1982144, 17]'))
irrscheds[91] = np.array(np.matrix('[1982123, 8 ; 1982140, 6 ; 1982144, 3 ]'))
irrscheds[92] = np.array(np.matrix('[1982123, 23; 1982140, 3 ; 1982144, 15]'))
irrscheds[93] = np.array(np.matrix('[1982123, 21; 1982140, 13; 1982144, 4 ]'))
irrscheds[94] = np.array(np.matrix('[1982123, 11; 1982140, 12; 1982144, 13]'))
irrscheds[95] = np.array(np.matrix('[1982123, 12; 1982140, 9 ; 1982144, 9 ]'))
irrscheds[96] = np.array(np.matrix('[1982123, 13; 1982140, 3 ; 1982144, 16]'))
irrscheds[97] = np.array(np.matrix('[1982123, 22; 1982140, 8 ; 1982144, 12]'))
irrscheds[98] = np.array(np.matrix('[1982123, 22; 1982140, 15; 1982144, 19]'))
irrscheds[99] = np.array(np.matrix('[1982123, 10; 1982140, 13; 1982144, 17]'))









irrscheds2 = np.zeros((1, 16, 2))

irrscheds2[0] = np.array(np.matrix('[1982063,13; 1982077,10; 1982094,10; 1982107,13; 1982111,18; 1982122,25; 1982126,25; 1982129,13; 1982132,15; 1982134,19; 1982137,20; 1982141,20; 1982148,15; 1982158,19; 1982161, 4; 1982162,25]'))


print(runner.run_batch(irrscheds, 4))

#print(runner.run(irrscheds[0],0))




