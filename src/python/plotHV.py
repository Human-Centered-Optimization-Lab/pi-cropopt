import sys
import numpy as np
from pymoo.factory import get_performance_indicator
import matplotlib.pyplot as plt
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import re


def get_hv(files):

    files.sort()

    ref_point = np.array([0, 3000])

    hv = get_performance_indicator("hv", ref_point=ref_point)

    hv_vals = []

    for f in files: 

        print("processing %s..." % f)
        solutions = np.genfromtxt(f, delimiter=',')

        objs_to_include = (0,2)
        non_doms = NonDominatedSorting().do(solutions[:,objs_to_include])[0]

        nd_sols = solutions[non_doms[np.newaxis].T,objs_to_include]

        hv_vals.append(hv.calc(nd_sols))

    return hv_vals

#
# Main
#

if __name__ == "__main__":

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

    



