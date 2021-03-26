from functools import reduce
from multiprocessing import Pool
import numpy as np
from shutil import copytree, copy, rmtree
from glob import glob
import subprocess as sp
import os, re, sys


class Dssat4Dum():


    def __init__(self, home, fileio, exe_path, tmp_dir, constant_apps=None):

        self.home = home
        self.fileio = fileio
        self.tmp_dir = tmp_dir
        self.activeIds = []       
        self.constant_apps = constant_apps 
        self.exe_path = exe_path
        self.exe_setup = False

        # delete old run directories
        files2del = glob("%s/dssatrun*" % self.tmp_dir) 

        for f in files2del: 
            rmtree(f);


    # irrsched is a nx2 matrix representing an irrigation schedule of n apps
    def run(self, argz):

        runid = argz[0]
        appsched = argz[1]

        if self.constant_apps is not None:
            appsched = np.concatenate((appsched, self.constant_apps))

        if runid not in self.activeIds: 
            self._setupDirectory(self.home, self.tmp_dir, runid)

        rundir = self._getRunDir(self.tmp_dir, runid)

        fileio_temp = "%s/DSSAT47.INP" % rundir

        self._editApp(self.fileio, fileio_temp, appsched)

        (yld, leaching) = self._runDssat(rundir, fileio_temp)

        return (yld, leaching)

    # appsched is a jx5xn matrix representing j schedules of n apps 
    # with date, irrigation, nitrogen, phosphorus, and potassium
    def run_batch(self, appsched, threads=1):


        batch_count = np.size(appsched, 0)

        # Create the arg list, with the first item being the irrigation 
        # schedule and the second being the run id
        argz = []
        for ind,dat in enumerate(appsched): 
            argz.append((ind, dat))

        results = []
        if threads == 1: 
            # Eschew multiprocessing for debugging ease
            for r in range(0, batch_count):
                results.append(self.run(argz[r]))
        else: 
            with Pool(threads) as p: 
                results = p.map(self.run, argz)

        return np.array(results)

    def _runDssat(self, dssat_path, fileio):
                
        os.chdir(dssat_path)

        res = sp.run([self.exe_path, "D", "DSSAT47.INP"], check=True)

        # TODO check for errors
       
        # Read yield
        reader = open("OVERVIEW.OUT", "r", errors="ignore")

        raw_txt = "".join(reader.readlines())
        
        yld = re.search("\s*\w*\s+YIELD\s+:\s+(\d+)\s+kg/ha",raw_txt).group(1)

        # Read yield
        
        reader = open("SoilNiBal.OUT", "r", errors="ignore")
        raw_txt = "".join(reader.readlines())
        leaching = re.search("N leached\s+(\d+\.?\d*)",raw_txt).group(1)


        return (float(yld), float(leaching))

    def _setupDirectory(self, home, temp_dir, runid):

        # TODO should be cross platform delimiter
        temp_run_dir = self._getRunDir(temp_dir, runid)
        copytree(home, temp_run_dir)


    def _getRunDir(self, temp_dir, runid):

        if temp_dir[-1] == '/':
            return "%sdssatrun%04d" % (temp_dir,runid) 
        else:
            return "%sdssatrun%04d" % (temp_dir,runid) 

    def formatIrrSched(self, irrSched):

        blank = np.array("", object)
        # Build lines of irrigation applications
        formattedIrrApp = np.apply_along_axis( 
                (lambda a : "   %d IR001  %f" % (a[0], a[1]) if a[1] != 0 else blank
            ), 1,irrSched)
              
        nonZeros = list(filter(
                (lambda x : x != "" ), 
                formattedIrrApp
            ))

        if len(nonZeros) != 0:
            # Convert array of irrigation application to a string
            formattedIrr = reduce(
                lambda a,b : "%s\n%s" % (a,b),
                # remove None values (nutrient applications)
                nonZeros               
            )
        else: 
            formattedIrr = ""

        return formattedIrr

    def formatNutSched(self, nitroSched):

        blank = np.array("", object)
        # Build lines of nutrient applications
        formatStr = "   %d FE001 AP001   10. % 4d. % 4d. % 4d.    0.    0.   -99"

        formattedNutApp = np.apply_along_axis( 
                (lambda a : formatStr % (a[0], a[2], a[3], a[4]) if (a[2] != 0 or a[3] != 0 or a[4] != 0) else blank 
            ), 1, nitroSched)
       
        nonZeros = list(filter(
            (lambda x : x != "" ), 
            formattedNutApp
        ))

        # If there were no valid nutrient applications, return a application with zero amounts
        if len(nonZeros) != 0:
            formattedNutrients = reduce(
                lambda a,b : "%s\n%s" % (a,b),
                # remove None values (nutrient applications)
                nonZeros
            )
        else:
            formattedNutrients = formatStr % (99001, 0, 0, 0)



        return formattedNutrients

    def _editApp(self, fileio_in, fileio_out, irrsched):

        # Read data 
        reader = open(fileio_in, "r")

        raw_txt = reader.readlines()

        # Work around https://github.com/numpy/numpy/issues/8352

        formattedIrr = self.formatIrrSched(irrsched)

        formattedNutrients = self.formatNutSched(irrsched)

        if "None" in  formattedIrr : 
            sys.exit("Unexpected 'None' found in output ")

        #print("-----\n%s\n-----" % formattedIrr)
        #print("-----\n%s\n-----" % formattedNutrients)

        # Parse file and insert values 

        raw_result = ""
        irrigation_iter = -1
        nutrient_iter = -1

        for line in raw_txt:

            # If irrigation is reached, mark that we've start processing 
            if "*IRRIGATION" in line:
                irrigation_iter += 1

            # If processing irrigation, mark another line of irrigation processed
            if irrigation_iter >= 0: 
                irrigation_iter += 1        

            # If not processing irrigation data, concat to result
            if irrigation_iter <= 2 and nutrient_iter <= 0 :
                raw_result = "%s%s" % (raw_result, line)

            # Process the last line after irrigation
            if irrigation_iter == 3:
                raw_result = "%s%s\n" % (raw_result, formattedIrr)

            # If we've reached fertilizer, stop process irrigation  
            # and start processing fertilizer
            if "*FERTILIZERS" in line:
                raw_result = "%s%s" % (raw_result, line)
                irrigation_iter = -1
                nutrient_iter += 1

            # If processing nutrients, mark another line of nutrient processed
            if nutrient_iter >= 0: 
                nutrient_iter += 1

            # Process the last line after irrigation
            if nutrient_iter == 1:
                raw_result = "%s%s\n" % (raw_result, formattedNutrients)

            
            if "*RESIDUES" in line:
                raw_result = "%s%s" % (raw_result, line)
                nutrient_iter = -1


        # Write results to file

        f = open(fileio_out, "w")
       
        f.write(raw_result)


if __name__ == "__main__":
            
    appsched1 = np.zeros((100, 3, 5))

    appsched1[0] = np.array(np.matrix('[2017123,  8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[1] = np.array(np.matrix('[2017123,  8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[2] = np.array(np.matrix('[2017123,  23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[3] = np.array(np.matrix('[2017123,  21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[4] = np.array(np.matrix('[2017123,  11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[5] = np.array(np.matrix('[2017123,  12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[6] = np.array(np.matrix('[2017123,  13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[7] = np.array(np.matrix('[2017123,  22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[8] = np.array(np.matrix('[2017123,  22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[9] = np.array(np.matrix('[2017123,  10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[10] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[11] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[12] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[13] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[14] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[15] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[16] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[17] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[18] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[19] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[20] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[21] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[22] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[23] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[24] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[25] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[26] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[27] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[28] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[29] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[30] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[31] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[32] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[33] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[34] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[35] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[36] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[37] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[38] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[39] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[40] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[41] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[42] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[43] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[44] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[45] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[46] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[47] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[48] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[49] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[50] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[51] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[52] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[53] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[54] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[55] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[56] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[57] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[58] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[59] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[60] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[61] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[62] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[63] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[64] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[65] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[66] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[67] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[68] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[69] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[70] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[71] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[72] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[73] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[74] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[75] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[76] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[77] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[78] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[79] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[80] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[81] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[82] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[83] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[84] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[85] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[86] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[87] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[88] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[89] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[90] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 11, 0, 0, 0; 2017144, 17, 0, 0, 0]'))
    appsched1[91] = np.array(np.matrix('[2017123, 8 , 0, 0, 0; 2017140, 6 , 0, 0, 0; 2017144, 3 , 0, 0, 0]'))
    appsched1[92] = np.array(np.matrix('[2017123, 23, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 15, 0, 0, 0]'))
    appsched1[93] = np.array(np.matrix('[2017123, 21, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 4 , 0, 0, 0]'))
    appsched1[94] = np.array(np.matrix('[2017123, 11, 0, 0, 0; 2017140, 12, 0, 0, 0; 2017144, 13, 0, 0, 0]'))
    appsched1[95] = np.array(np.matrix('[2017123, 12, 0, 0, 0; 2017140, 9 , 0, 0, 0; 2017144, 9 , 0, 0, 0]'))
    appsched1[96] = np.array(np.matrix('[2017123, 13, 0, 0, 0; 2017140, 3 , 0, 0, 0; 2017144, 16, 0, 0, 0]'))
    appsched1[97] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 8 , 0, 0, 0; 2017144, 12, 0, 0, 0]'))
    appsched1[98] = np.array(np.matrix('[2017123, 22, 0, 0, 0; 2017140, 15, 0, 0, 0; 2017144, 19, 0, 0, 0]'))
    appsched1[99] = np.array(np.matrix('[2017123, 10, 0, 0, 0; 2017140, 13, 0, 0, 0; 2017144, 17, 0, 0, 0]'))

    appsched2 = np.zeros((1, 18, 5))

    appsched2[0] = np.array(np.matrix("""
       [2017063,13,  0, 0, 0; 
        2017077,10,  0, 0, 0; 
        2017094,10,  0, 0, 0; 
        2017107,13,  0, 0, 0; 
        2017111,18,  0, 0, 0; 
        2017122,25,  0, 0, 0; 
        2017126,25,  0, 0, 0; 
        2017129,13,  0, 0, 0; 
        2017132,15,  0, 0, 0; 
        2017134,19,  0, 0, 0; 
        2017137,20,  0, 0, 0; 
        2017141,20,  0, 0, 0; 
        2017148,15,  0, 0, 0; 
        2017158,19,  0, 0, 0; 
        2017161, 4,  0, 0, 0; 
        2017162,25,  0, 0, 0; 
        2017135, 0, 70,10, 4; 
        2017196, 0,200, 0, 0  
        ]"""))

    home_dir = "/Users/iankropp"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047" % home_dir
    fileio = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    tmp_dir = "/tmp/"

    runner = Dssat4Dum(dssat_home, fileio, dssat_exe, tmp_dir)


    threads = 1

    print(runner.run_batch(appsched1, threads))

    #print(runner.run_batch(irrscheds,1))




