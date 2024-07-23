

# Take in two csvs with Pareto fronts and plot them on the same graph 
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys


if len(sys.argv) < 2:
    print("Usage: python comparePlots.py [GEN] <LABEL1> <LABEL2> <CSV1> <CSV2>")
    sys.exit(1)
# Validate the input
elif len(sys.argv) % 2 == 1:
    output_format = "show"
else:
    output_format = "save"


labels = []
dfs = []
facecolors = ['none', 'green', 'purple', 'orange']
edgecolors = ['black', 'green', 'purple', 'orange']
markers = ['s', 'o', 'o', 'o']


if output_format == "save": 
    gen = sys.argv[1]    
    args = sys.argv[2:]
else: 
    args = sys.argv[1:]


for (a, arg) in enumerate(args):
    
    if a < (len(args)/2):
        labels.append(arg)
    else:
        dfs.append(pd.read_csv(arg))



for (d, df) in enumerate(dfs): 

    # Perform non-dominated sorting
    nds = NonDominatedSorting()
    fronts = nds.do(df.values, only_non_dominated_front=True)

    # Get the Pareto front      
    pf = df.iloc[fronts,:]
    
    # Plot the data (first column is f1, second column is f2) 
    plt.scatter(pf.iloc[:,1], pf.iloc[:,0]*-1,  
                label=labels[d], 
                facecolors=facecolors[d], 
                edgecolors=edgecolors[d], 
                marker=markers[d])
    

    
plt.xlabel("Irrigation (mm)")
plt.ylabel("Yield (kg/ha)")
plt.legend()

if output_format == "save":

    # turn gen into a string padded with four zeros
    gen = gen.zfill(4)

    # Save plot to /tmp
    plt.savefig("/tmp/pareto%s.png" % gen)

else: 

    plt.show()


