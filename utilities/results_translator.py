import sys
import ast
import numpy as np


if len(sys.argv) != 5:
    print("Usage: %s SOLUTION_NUMBER VAR_RESULTS_PATH OBJ_RESULTS_PATH  ENONE_STRUCTURE_PATH" % sys.argv[0])
    sys.exit(1)

sol_no              = int(sys.argv[1])
var_results_path        = sys.argv[2]
obj_results_path        = sys.argv[3]
genome_struct_path  = sys.argv[4]

# Retrieve and unpack genome structure data
with open(genome_struct_path, 'r') as f: genome_struct = ast.literal_eval(f.read())

period_indices = genome_struct['indices']
date_ranges = np.array(genome_struct['date_ranges'])
constant_apps = np.array(genome_struct['constant_apps'])

full_genome = np.loadtxt(var_results_path, delimiter=",")
full_obj = np.loadtxt(obj_results_path, delimiter=",")

genome = full_genome[sol_no,:]
obj = full_obj[sol_no,:]

## -- First process irrigation --
irrigation_periods = period_indices[0]

# isolate irrigation dates 
irrigation_dates = date_ranges[date_ranges[:,2] == 0,:]

print("Irrigation")

total_irrigation = 0
# For each irrigation period
for (period_i, period) in enumerate(irrigation_periods):
    dates = irrigation_dates[period_i, :]
    

    # Iterate through the dates and the genome 
    begindex = period[1]
    endex = period[2]
    date = dates[0]

    for ind in range(begindex, endex):
        value =  round(genome[ind])
        if value != 0:
            print("%d %d" % (date, value))

        total_irrigation += value
        date += 1

## -- Then process nutrients --
nutrient_periods = period_indices[1]

# isolate nutrient dates
nutrient_dates = date_ranges[date_ranges[:,2] == 1,:]

print("Nutrients:")


# For each constant nutrient application
for constant_app in constant_apps:
    value = round(constant_app[2])
    date =  round(constant_app[0])
    print("%d %d" % (date, value))

# For each nutrient period
for (period_i, period) in enumerate(nutrient_periods):
    dates_meta = nutrient_dates[period_i, :]
    value = round(dates_meta[3])
    date = round(genome[period[1]])
    print("%d %d" % (date, value))


if obj.shape[0] == 2:
    print("Objectives")
    print("Yield: %d, total irr: %d" % (-obj[0], obj[1]))
elif obj.shape[0] == 3:
    print("Objectives")
    print("Yield: %d, Leaching: %d, total irr: %d" % (-obj[0], obj[1], obj[2]))
else: 
    print(f"Number of objectives incorrect in {obj_results_path}")
    sys.exit(1)




if obj[-1] != total_irrigation: 
    print("WARNING: objective irrigation doesn't match genome")


