import sys
import ast
import numpy as np
import tabloo
import pickle
from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

directories = sys.argv[1:]

IRR_COL = 1

print("year, plant date, irr period start, irr period end, nit period start, nit period end, max yield (kg/ha), mean I.A.C. (mm), median I.A.C. (mm), mean irr total (mm), median irr total (mm)")

for directory in directories:

    # Get the genome struct info 
    genome_struct_path = "%s/genome_structure.py" % directory

    with open(genome_struct_path, 'r') as f: genome_struct = ast.literal_eval(f.read())

    # Get the pickled run record
    run_record_path = "%s/run_sim_record.pkl" % directory
    infile = open(run_record_path, 'rb')
    run_record = pickle.load(infile)

    # Year 
    path_segments = directory.split("/")
    year = int(path_segments[-1][5:9])

    # Plant date 
    plant_date = 135

    if year % 4 == 0:
        plant_date += 1

    # Irr date info
    periods = genome_struct['date_ranges']
    irr_period = periods[0]
    irr_start = irr_period[0] - (year * 1e3)
    irr_end = irr_period[1] - (year * 1e3)

    # Nit date info
    nit_period = periods[1]
    nit_start = nit_period[0] - (year * 1e3)
    nit_end = nit_period[1] - (year * 1e3)

    # Yield information 
    max_yield = max(run_record['yield'])

    # Irrigation application counts and totals
    run_scheds = run_record['scheds'].tolist()
    #                               Only select the irr applications
    #                               V
    irr_app_count = [np.shape(sched[sched[:,IRR_COL] != 0])[0] for sched in run_scheds]
    #                          Only select the irr applications
    #                          V
    irr_app_total = [sum(sched[sched[:,IRR_COL] != 0][:,IRR_COL]) for sched in run_scheds]

    run_record['irr_app_count'] = irr_app_count
    run_record['irr_total'] = irr_app_total

    # Non-dominated sort
    f1 = -run_record['yield'] # Made this negative because we to maximize yield
    f2 = run_record['leaching']
    f3 = run_record['irr_total']
    F = np.column_stack((f1,f2,f3))

    opt_front_i = NonDominatedSorting().do(F, only_non_dominated_front=True)

    record_count = np.shape(run_record)[0]
    non_dom = [True if i in opt_front_i else False for i in range(record_count)]

    run_record['non_dom'] = non_dom

    # make these only the optimal solutions
    irr_count_mean = np.mean(run_record[run_record['non_dom']]['irr_app_count'])
    irr_count_median = np.median(run_record[run_record['non_dom']]['irr_app_count'])

    irr_total_mean = np.mean(run_record[run_record['non_dom']]['irr_total'])
    irr_total_median = np.median(run_record[run_record['non_dom']]['irr_total'])


    row_vals =  (year, plant_date, irr_start, irr_end, nit_start, nit_end, 
                    max_yield, irr_count_mean, irr_count_median,
                    irr_total_mean, irr_total_median)

    row_str = "%d, %d, %d, %d, %d, %d, %d, %f, %f, %f, %f" % row_vals
   
    print(row_str)

