

# Take in two csvs with Pareto fronts and plot them on the same graph 

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

# Validate the input
if len(sys.argv) != 5:
    print("Usage: python comparePlots.py <label1> <label2> <csv1> <csv2>")
    sys.exit(1)


# Read in the csvs
label1 = sys.argv[1]
label2 = sys.argv[2]
df1 = pd.read_csv(sys.argv[3])
df2 = pd.read_csv(sys.argv[4])



# Plot the data (first column is f1, second column is f2)
plt.scatter(df1.iloc[:,1], df1.iloc[:,0]*-1,  label=label1)
plt.scatter(df2.iloc[:,1], df2.iloc[:,0]*-1,  label=label2)
plt.xlabel("f1")
plt.ylabel("f2")
plt.legend()
plt.show()




