from multiprocessing import Pool
from multiprocessing import Manager
import sys 
import pickle
from attr_processors import AttProcessors
import pandas as pd
import tabloo
import numpy as np


# Example
# python -m pdb   mlearn/step0_build_attr_tab.py postprocess/master_run_record.pkl

# Functions
def process_year(arg):

    print("Starting year processor")

    # unpack the argument
    (tab, att_functs, year) = arg

    results = []

    years_rows = tab[tab['year'] == year]

    # For every attribute function 
    result_count = -1

    for att_funct in att_functs:

        func = getattr(AttProcessors, 'application_count')

        att_results = [func(row) for i, row in years_rows.iterrows()]

        results.append(att_results)

    print("Completed year %d" % year)
    return (year, np.array(results))


# Main

if __name__ == "__main__":

    #threads = 8
    threads = 4

    # Read in the master record
    file_name = sys.argv[1]

    infile = open(file_name, 'rb')
    tab = pickle.load(infile)

    years = set(tab['year'])

    #att_functs = ['application_count', 'total_irrigation']
    att_functs = ['application_count']

    raw_table = {'year': []}

    # initialize the attribute functions
    for att_funct in att_functs: 
        raw_table[att_funct] = []

    run_results = {}

    # Make a multiprocessing manager to hold the shared data frame
    #mgr = Manager()
    #ns = mgr.Namespace()
    #ns.tab = my_dataframe 

    # pack up arguments
    argz = [(tab, att_functs, year) for year in years]

    print(argz)

    if threads == 1: 
        # Eschew multiprocessing for debugging ease
        results = [process_year(arg) for arg in argz]
    else: 
        with Pool(threads) as p: 
            results = p.map(process_year, argz)

    # unpack results
    for result_by_year in results:
        (year, attrs) = result_by_year
        run_results[year] = attrs

    for year in years:

        result_count = -1

        for (i, att_funct) in enumerate(att_functs): 
            attr = run_results[year]

            new_results = attr[:, i].tolist()
            raw_table[att_funct] = raw_table[att_funct] + new_results

            if result_count == -1:
                result_count = len(new_results)

        raw_table['year'] = raw_table['year'] +  [year] * result_count



    attribute_table = pd.DataFrame(raw_table)

    tabloo.show(attribute_table)

