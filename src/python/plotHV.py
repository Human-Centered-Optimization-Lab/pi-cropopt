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

    #ideal_point = np.array([-100000, 0, 2017000])
    ideal_point = np.array([0, 1000, 3000000])

    hv = get_performance_indicator("hv", ref_point=ideal_point)

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

all_run_files = sys.argv[1:]

get_run_no = lambda a : int(re.search("run(\d{4})",a).group(1))

runs_raw = list(map(get_run_no, all_run_files))

runs = set(runs_raw)

colors = ["red", "blue", "pink"]

plt.figure()

for (indx, run) in enumerate(runs): 

    files = list(filter(lambda a : ("run%04d" % run) in a , all_run_files))

    hv_vals = get_hv(files)

    plt.plot(hv_vals)

plt.show()




