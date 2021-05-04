import matplotlib.pyplot as plt
import numpy as np
import sys
import pickle

year = int(sys.argv[1])
file_name = sys.argv[2]

infile = open(file_name, 'rb')
tab = pickle.load(infile)

# Grab non-dominated solutions for this given year 
selection_mask = np.logical_and(tab['front'] == 0, tab['year'] == year)

x = tab[selection_mask]['irr_total'] 
y = tab[selection_mask]['leaching'] 
z = tab[selection_mask]['yield'] 

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

## For each set of style and range settings, plot n random points in the box
## defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
#for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
#    xs = randrange(n, 23, 32)
#    ys = randrange(n, 0, 100)
#    zs = randrange(n, zlow, zhigh)
ax.scatter(x, y, z)

ax.set_xlabel('Total irrigation')
ax.set_ylabel('Leaching')
ax.set_zlabel('Yield')

plt.title(year)
plt.show()

