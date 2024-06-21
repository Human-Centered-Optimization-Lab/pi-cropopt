

# Take in two csvs with Pareto fronts and plot them on the same graph 

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

# Validate the input
if len(sys.argv) == 5 or len(sys.argv) == 3:
    output_format = "show"
elif len(sys.argv) == 4 or len(sys.argv) == 2:
    output_format = "save"
else: 
    print("Usage: python comparePlots.py [GEN] <LABEL1> <LABEL2> <CSV1> <CSV2>")
    sys.exit(1)


labels = []
dfs = []

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

    # Plot the data (first column is f1, second column is f2)
    plt.scatter(df.iloc[:,1], df.iloc[:,0]*-1,  label=labels[d])


    
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


