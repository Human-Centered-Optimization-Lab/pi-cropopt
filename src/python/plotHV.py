import sys
import numpy as np
from pymoo.factory import get_performance_indicator
import matplotlib.pyplot as plt
import re

#
# Functions
#
def get_nondoms(solutions):

    paretoFront = []
    for solution_inner in solutions: 
        non_dominated = True
        for solution_outer in solutions: 
            if solution_inner[0] > solution_outer[0] and solution_inner[1] > solution_outer[1]:
                non_dominated = False

        if non_dominated:
            paretoFront.append(solution_inner.tolist())

    paretoFront = np.array(paretoFront)

    return paretoFront


def get_hv(files):

    files.sort()

    #nadir_point = np.array([-100000, 0, 2017000])
    ref_point = np.array([0, 1000, 3000])

    hv = get_performance_indicator("hv", ref_point=ref_point)

    hv_vals = []

    for f in files: 

        print("processing %s..." % f)
        solutions = np.genfromtxt(f, delimiter=',')

        nd_sols = get_nondoms(solutions)

        hv_vals.append(hv.calc(nd_sols))

    return hv_vals

#
# Main
#

file_list = sys.argv[1]

with open(file_list) as f:
    all_run_files = [line[0:-1] for line in f.readlines()  ]

#all_run_files = open(argv[1], "")

get_run_no = lambda a : int(re.search("run(\d{4})",a).group(1))

runs_raw = list(map(get_run_no, all_run_files))

runs = set(runs_raw)

plt.figure()


for run_type in ("with_run", "without_run"):

    for (indx, run) in enumerate(runs): 

        print("*********************")
        print("Run type: %s, run %s" % (run_type, run))
        print("*********************")

        # Only pull runs of the same type and number
        run_filter = lambda a : (("run%04d" % run) in a) and (run_type in a) and (int(re.search("run0(\d{3})",a).group(1)) < 250) 

        files = list(filter(run_filter, all_run_files))

        hv_vals = get_hv(files)

        if run_type == "with_run":
            color = "red"
        else: 
            color = "blue"

        plt.plot(hv_vals, color=color)




plt.show()




