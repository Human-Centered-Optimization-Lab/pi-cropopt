from multiprocessing import Pool
import numpy as np
from shutil import copytree, copy, rmtree
from glob import glob
import subprocess as sp
import os, re, sys
import json
import pandas as pd

class DssatCode():

    def __init__(self, section, row, col):
        self.section = section
        self.row = row 
        self.col = col

class Dssat4Dum():

    def __init__(self, home, fileio, exe_path, tmp_dir, constant_apps=None):

        self.home = home
        self.fileio = fileio
        self.tmp_dir = tmp_dir
        self.activeIds = []       
        self.constant_apps = constant_apps 
        self.exe_path = exe_path
        self.exe_setup = False

        self.code_lookup = {
                'pdate' : DssatCode("PLANTING DETAILS", 0, 0),
                'sdate' : DssatCode("SIMULATION CONTROL", 0, 3),
                'icdat' : DssatCode("INITIAL CONDITIONS", 0, 1),
            }


        self._run_record = {}
        
        self.clean_workspace()


    def clean_workspace(self):

        # delete old run directories
        files2del = glob("%s/dssatrun*" % self.tmp_dir) 

        for f in files2del: 
            rmtree(f);


    # irrsched is a nx2 matrix representing an irrigation schedule of n apps
    def _run(self, argz):

        runid = argz[0]
        appsched = argz[1]
        updates = argz[2]

        if self.constant_apps is not None:
            appsched = np.concatenate((appsched, self.constant_apps))

        if runid not in self.activeIds: 
            self._setupDirectory(self.home, self.tmp_dir, runid)

        rundir = self._getRunDir(self.tmp_dir, runid)

        fileio_temp = "%s/DSSAT47.INP" % rundir

        run_key = self._editExp(self.fileio, fileio_temp, appsched, updates= updates)

        appsched_list = appsched.tolist()

        # Remove any days that have no applications
        appsched_list_cleaned = [r for r in appsched_list if (r[1] + r[2] + r[3] + r[4] != 0)]

        sched_key = json.dumps(appsched_list_cleaned)

        (yld, leaching) = self._runDssat(rundir, fileio_temp)

        return (yld, leaching, sched_key)

    def _dump_run_record(self):
        return self._run_record

    def generate_report(self):
     
        yields   = []
        leaching = []
        scheds   = []
        
        for k in self._run_record.keys():

            sched_raw = json.loads(k)
            sched = np.array(sched_raw)

            scheds.append(sched)
            yields.append(self._run_record[k][0])
            leaching.append(self._run_record[k][1])

        raw_report = {  'yield': yields , 
                        'leaching': leaching,
                        'scheds': scheds}

        report = pd.DataFrame(raw_report)

        return report


    # appsched is a jx5xn matrix representing j schedules of n apps 
    # with date, irrigation, nitrogen, phosphorus, and potassium
    def run_batch(self, appsched, threads=1, updates={}):

        if isinstance(appsched, np.ndarray) :
            batch_count = np.size(appsched, 0)
        else:
            batch_count = len(appsched)

        # Create the arg list, with the first item being the runid,
        # the second being the irrigation schedule, and the thid 
        # being updates
        argz = []
        for ind,dat in enumerate(appsched): 

            # Check if the user submitted a...
            if isinstance(updates, dict):
                # single update, 
                argz.append((ind, dat, updates))
            else:
                # or one update per schedule
                argz.append((ind, dat, updates[ind]))


        results = []
        if threads == 1: 
            # Eschew multiprocessing for debugging ease
            for r in range(0, batch_count):
                results.append(self._run(argz[r]))
        else: 
            with Pool(threads) as p: 
                results = p.map(self._run, argz)

        # Save the most recent runs
        for result in results:
            sched_key = result[2]
            yield_ = result[0]
            leaching = result[1]
            self._run_record[sched_key] = (yield_, leaching)

        # Remove the run records from the simple results
        results_cleaned = [(a[0], a[1]) for a in results]
        return np.array(results_cleaned)

    @staticmethod 
    def _replace_txt(string, field_no, value):

        chunks = re.findall(r"\s*\S+", string)

        zones = []
        prev_chunk_end = 0
        for chunk in chunks:
            chunk_length = len(chunk)
            zones.append((prev_chunk_end, prev_chunk_end+chunk_length-2))
            prev_chunk_end =  prev_chunk_end+chunk_length

        replace_str_len = len(chunks[field_no])

        replace_str_frmt = "{:>%d}" % (replace_str_len)

        replace_str = replace_str_frmt.format(value)

        chunks[field_no] = replace_str

        return "%s\n" % "".join(chunks)


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

    @staticmethod
    def formatIrrSched(appSched):

        # Filter out the non-irrigation rows
        irr_rows = appSched[:,1] != 0
        irr_apps = appSched[irr_rows]

        # Sort the irrigation rows
        irr_apps = irr_apps[irr_apps[:,0].argsort()]
        
        formatted_irr_list = ["   %d IR001  %f" % (r[0], r[1]) for r in irr_apps if len(r) > 0 ]

        formatted_irr = "\n".join(formatted_irr_list)

        return formatted_irr + "\n"

    @staticmethod
    def formatNutSched(appSched):

        # Build lines of nutrient applications
        formatStr = "   %d FE001 AP001   10. % 4d. % 4d. % 4d.    0.    0.   -99"

        # Filter out the non-nutrient rows
        nitro_rows = np.logical_or(appSched[:,2] != 0, appSched[:,3] != 0, appSched[:,4] != 0) 
        nitroSched = appSched[nitro_rows]
       
        # Sort the nitrogen applications
        nitroSched = nitroSched[nitroSched[:,0].argsort()]

        formattedNutAppList =  [formatStr % (r[0], r[2], r[3], r[4]) for r in nitroSched if len(r) > 0]

        formattedNutApp = "\n".join(formattedNutAppList)


        if formattedNutApp == '':
           formattedNutApp = formatStr % (99001, 0, 0, 0)

        return formattedNutApp + "\n"

    def _editExp(self, fileio_in, fileio_out, irrsched, updates={}):

        # Read data 
        reader = open(fileio_in, "r")

        raw_txt = reader.readlines()

        # Work around https://github.com/numpy/numpy/issues/8352

        formattedIrr = self.formatIrrSched(irrsched)

        formattedNutrients = self.formatNutSched(irrsched)

        if "None" in  formattedIrr : 
            sys.exit("Unexpected 'None' found in output ")

        # Parse file and insert values 

        raw_result = ""
        irrigation_iter = -1
        nutrient_iter = -1

        progress = [("IRRIGATION", -1), ("FERTILIZERS", -1)] 

        NAME = 0
        ITER = 1

        progress_new = [["FILES", -1], ["SIMULATION CONTROL", -1], 
                ["EXP.DETAILS", -1], ["TREATMENTS", -1], ["CULTIVARS", -1],
                ["FIELDS", -1], ["INITIAL CONDITIONS", -1], 
                ["PLANTING DETAILS", -1], ["IRRIGATION", -1], 
                ["FERTILIZERS", -1], ["RESIDUES", -1], ["CHEMICALS", -1],
                ["TILLAGE", -1], ["ENVIRONMENT", -1], ["HARVEST", -1],
                ["SOIL", -1], ["CULTIVAR", -1]]

        curr_field = -1

        raw_result_new = []

        for line in raw_txt:

            # Check if the next field has arrived
            # TODO index out of range? 
            if (curr_field + 1) < len(progress_new) and ("*%s" % progress_new[curr_field+1][NAME]) in line:
                curr_field += 1
                progress_new[curr_field][ITER] = 0

            curr_iter = progress_new[curr_field][ITER]
            curr_name = progress_new[curr_field][NAME]
          
            if curr_iter == 0:
                # Print the section header by default
                raw_result_new.append(line)
            elif curr_name == "IRRIGATION" and curr_iter > 1: 
                # Print the special irrigation section
                if curr_iter == 2:
                    raw_result_new.append(formattedIrr)
            elif curr_name == "FERTILIZERS":    
                # Print the special fertilizer section
                if curr_iter == 1: 
                    raw_result_new.append(formattedNutrients)
            else:

                no_replace_found = True
                #print(updates)
                for code in updates.keys():
                    value = int(updates[code])
                    section = self.code_lookup[code].section
                    row = self.code_lookup[code].row
                    col = self.code_lookup[code].col
                    if curr_name == section and row == (curr_iter-1):
                        edited_line = self._replace_txt(line, col, value)
                        raw_result_new.append(edited_line)
                        no_replace_found = False
                        break 
               
                if no_replace_found: 
                    raw_result_new.append(line)

            progress_new[curr_field][ITER] += 1

                # Perform the find and replace
                #if _needs_replace(self.code_lookup, updates):
                #    raw_result_new.append(formattedNutrients)
                #    # Update line
                #    #_replace_txt(line, )

        raw_result = "".join(raw_result_new)
        # Write results to file
        f = open(fileio_out, "w")
       
        f.write(raw_result)

if __name__ == "__main__":
            
    appsched1 = np.zeros((100, 3, 5))

    appsched1[0] = np.array(np.matrix('[1980123,  8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[1] = np.array(np.matrix('[1980123,  8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[2] = np.array(np.matrix('[1980123,  23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[3] = np.array(np.matrix('[1980123,  21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[4] = np.array(np.matrix('[1980123,  11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[5] = np.array(np.matrix('[1980123,  12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[6] = np.array(np.matrix('[1980123,  13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[7] = np.array(np.matrix('[1980123,  22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[8] = np.array(np.matrix('[1980123,  22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[9] = np.array(np.matrix('[1980123,  10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[10] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[11] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[12] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[13] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[14] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[15] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[16] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[17] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[18] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[19] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[20] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[21] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[22] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[23] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[24] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[25] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[26] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[27] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[28] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[29] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[30] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[31] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[32] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[33] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[34] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[35] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[36] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[37] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[38] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[39] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[40] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[41] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[42] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[43] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[44] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[45] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[46] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[47] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[48] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[49] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[50] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[51] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[52] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[53] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[54] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[55] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[56] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[57] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[58] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[59] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[60] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[61] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[62] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[63] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[64] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[65] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[66] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[67] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[68] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[69] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[70] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[71] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[72] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[73] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[74] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[75] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[76] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[77] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[78] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[79] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[80] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[81] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[82] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[83] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[84] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[85] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[86] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[87] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[88] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[89] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[90] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 11, 0, 0, 0; 1980144, 17, 0, 0, 0]'))
    appsched1[91] = np.array(np.matrix('[1980123, 8 , 0, 0, 0; 1980140, 6 , 0, 0, 0; 1980144, 3 , 0, 0, 0]'))
    appsched1[92] = np.array(np.matrix('[1980123, 23, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 15, 0, 0, 0]'))
    appsched1[93] = np.array(np.matrix('[1980123, 21, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 4 , 0, 0, 0]'))
    appsched1[94] = np.array(np.matrix('[1980123, 11, 0, 0, 0; 1980140, 12, 0, 0, 0; 1980144, 13, 0, 0, 0]'))
    appsched1[95] = np.array(np.matrix('[1980123, 12, 0, 0, 0; 1980140, 9 , 0, 0, 0; 1980144, 9 , 0, 0, 0]'))
    appsched1[96] = np.array(np.matrix('[1980123, 13, 0, 0, 0; 1980140, 3 , 0, 0, 0; 1980144, 16, 0, 0, 0]'))
    appsched1[97] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 8 , 0, 0, 0; 1980144, 12, 0, 0, 0]'))
    appsched1[98] = np.array(np.matrix('[1980123, 22, 0, 0, 0; 1980140, 15, 0, 0, 0; 1980144, 19, 0, 0, 0]'))
    appsched1[99] = np.array(np.matrix('[1980123, 10, 0, 0, 0; 1980140, 13, 0, 0, 0; 1980144, 17, 0, 0, 0]'))

    appsched2 = np.zeros((1, 18, 5))

    appsched2[0] = np.array(np.matrix("""
       [1980063,13,  0, 0, 0; 
        1980077,10,  0, 0, 0; 
        1980094,10,  0, 0, 0; 
        1980107,13,  0, 0, 0; 
        1980111,18,  0, 0, 0; 
        1980122,25,  0, 0, 0; 
        1980126,25,  0, 0, 0; 
        1980129,13,  0, 0, 0; 
        1980132,15,  0, 0, 0; 
        1980134,19,  0, 0, 0; 
        1980137,20,  0, 0, 0; 
        1980141,20,  0, 0, 0; 
        1980148,15,  0, 0, 0; 
        1980158,19,  0, 0, 0; 
        1980161, 4,  0, 0, 0; 
        1980162,25,  0, 0, 0; 
        1980135, 0, 71,11, 4; 
        1980196, 0,201, 0, 0  
        ]"""))


    appsched3 = np.zeros((3, 18, 5))

    appsched3[0] = np.array(np.matrix("""
       [2000063,13,  0, 0, 0; 
        2000077,10,  0, 0, 0; 
        2000094,10,  0, 0, 0; 
        2000107,13,  0, 0, 0; 
        2000111,18,  0, 0, 0; 
        2000122,25,  0, 0, 0; 
        2000126,25,  0, 0, 0; 
        2000129,13,  0, 0, 0; 
        2000132,15,  0, 0, 0; 
        2000134,19,  0, 0, 0; 
        2000137,20,  0, 0, 0; 
        2000141,20,  0, 0, 0; 
        2000148,15,  0, 0, 0; 
        2000158,19,  0, 0, 0; 
        2000161, 4,  0, 0, 0; 
        2000162,25,  0, 0, 0; 
        2000135, 0, 71,11, 4; 
        2000196, 0,201, 0, 0  
        ]"""))
      

    appsched3[1] = np.array(np.matrix("""
       [2000063,13,  0, 0, 0; 
        2000077,10,  0, 0, 0; 
        2000094,10,  0, 0, 0; 
        2000107,13,  0, 0, 0; 
        2000111,18,  0, 0, 0; 
        2000122,25,  0, 0, 0; 
        2000126,25,  0, 0, 0; 
        2000129,13,  0, 0, 0; 
        2000132,15,  0, 0, 0; 
        2000134,19,  0, 0, 0; 
        2000137,20,  0, 0, 0; 
        2000141,20,  0, 0, 0; 
        2000148,15,  0, 0, 0; 
        2000158,19,  0, 0, 0; 
        2000161, 4,  0, 0, 0; 
        2000162,25,  0, 0, 0; 
        2000135, 0, 71,11, 4; 
        2000196, 0,201, 0, 0  
        ]"""))

    appsched3[2] = np.array(np.matrix("""
       [2000063,13,  0, 0, 0; 
        2000077, 0,  0, 0, 0; 
        2000107,13,  0, 0, 0; 
        2000111,18,  0, 0, 0; 
        2000094,10,  0, 0, 0; 
        2000122,25,  0, 0, 0; 
        2000126,25,  0, 0, 0; 
        2000129,13,  0, 0, 0; 
        2000132,15,  0, 0, 0; 
        2000134,19,  0, 0, 0; 
        2000137,20,  0, 0, 0; 
        2000141,20,  0, 0, 0; 
        2000148,15,  0, 0, 0; 
        2000158,19,  0, 0, 0; 
        2000161, 4,  0, 0, 0; 
        2000162,25,  0, 0, 0; 
        2000196, 0,201, 0, 0;
        2000135, 0, 71,11, 4 
        ]"""))

       

    home_dir = "/Users/iankropp"

    dssat_home = "%s/Projects/agovization/dhome" % home_dir
    dssat_exe = "%s/Projects/agovization/dhome/dscsm047-macos" % home_dir
    fileio = "%s/Projects/agovization/dhome/DSSAT47.INP" % home_dir
    tmp_dir = "/tmp/"

    runner = Dssat4Dum(dssat_home, fileio, dssat_exe, tmp_dir)

    threads = 1

    updates = { 'pdate': 1980136, 'sdate': 1980135, 'icdat': 1980135 }


    print(runner.run_batch(appsched3, threads, updates=updates))

    
    #print(runner.generate_report())








