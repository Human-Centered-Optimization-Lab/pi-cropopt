
import sys
import numpy as np

# Convert this 
#
# Solution 1 [-10256.     54.]
# Solution 2 [-9810.    35.]
# Solution 3 [-9329.    22.]
# Solution 4 [-8421.     0.]
# Ranks (e.g., 3, 2, ..., 1): 2 1 3 4

# into 
# [9810 35 1; 10256   54    2; 9329    22    3; 8421  0 4]

# Read a multi-line string from from console

lines = sys.stdin.readlines()
lines = [line.strip() for line in lines]
 
# Extract the numbers from the lines
solutions = []
ranks = []
for line in lines:
    if line.startswith('Solution'):
        solution = line.split('[')[1].split(']')[0].split()
        
        # remove trailing dot
        if solution[0].endswith('.'):
            solution[0] = solution[0][:-1]

        if solution[1].endswith('.'):
            solution[1] = solution[1][:-1]

        solutions.append([int(solution[0]), int(solution[1])])
        
    elif line.startswith('Ranks'):
        ranks = line.split(': ')[1].split()
        ranks = [int(rank) for rank in ranks]

solutions = np.array(solutions)

solutions[:,0]  = -solutions[:,0]

# Make the ranks the third column 
solutions = np.c_[solutions, ranks]

# Sort the solutions by the ranks
solutions = solutions[solutions[:,2].argsort()]


# Convert the solutions to a string
sol_str = solutions.__str__()
sol_str = sol_str.replace('\n', '')

print(sol_str)

sol_str = sol_str.replace('[[', '[')
sol_str = sol_str.replace(' [', '')
sol_str = sol_str.replace(']', ';')
sol_str = sol_str.replace(';;', '];')

# Remove newlines


print("obj = " + sol_str)



