import sys
import numpy as np
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

# Get the file paths
if len(sys.argv) < 3:
    print("Usage: OBJECTIVE_FILE1 ... OBJECTIVE_FILEN OUTPUT_PICKLE_PATH")

input_files = sys.argv[1:-1]
output_path = sys.argv[-1]

# Open the first file to get information on the objective space 

input_files[0]

all_solutions = None

for input_file in input_files: 

    current_objs = np.genfromtxt(input_file, delimiter=',')

    if all_solutions is None:
        all_solutions = current_objs
    else: 
        all_solutions = np.vstack((all_solutions, current_objs))


nds = NonDominatedSorting()
fronts = nds.do(all_solutions, only_non_dominated_front=True)

pf = all_solutions[fronts,:]



