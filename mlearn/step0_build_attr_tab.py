import sys 
import pickle
from attr_processors import AttProcessors

# Example
# python -m pdb   mlearn/step0_build_attr_tab.py postprocess/master_run_record.pkl

# Read in the master record
file_name = sys.argv[1]

infile = open(file_name, 'rb')
tab = pickle.load(infile)

years = set(tab['year'])

att_functs = ['application_count']

# For every year
for year in years: 

    years_rows = tab[tab['year'] == year]


    # For every attribute function 

    for att_funct in att_functs:

        func = getattr(AttProcessors, 'application_count')

        results = [func(row) for i, row in years_rows.iterrows()]

        print("For year %d and attribute %s" % (year, att_funct))

        print(results)




