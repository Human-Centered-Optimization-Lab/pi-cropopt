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

    # unpack the argument
    (tab, att_functs, year, procr) = arg

    results = []

    # For every attribute function 
    result_count = -1

    for att_funct in att_functs:

        func = getattr(procr, att_funct)

        att_results = tab.apply(func, axis=1)

        results.append(att_results)
    
    print("Completed year %d" % year)
    return (year, np.transpose(np.array(results)))


# Main

if __name__ == "__main__":


    threads = 1

    if threads != 1:
        # This somehow prevents this weird error while using multiprocessing
        # AttributeError: module '__main__' has no attribute '__spec__'
        __spec__ = None


    # Read in the master record
    file_name = sys.argv[1]

    infile = open(file_name, 'rb')
    tab = pickle.load(infile)

    # Set up the processing agent 
    procr = AttProcessors(42, 42)

    years = set(tab['year'])

    att_functs = [  'application_count', 
                    'total_irrigation', 
                    'yield_', 
                    'front',
                    'leaching',
                    'minimum_irr',
                    'maximum_irr']


    raw_table = {'year': []}

    # initialize the attribute functions
    for att_funct in att_functs: 
        raw_table[att_funct] = []

    # Split up the data by year, with each thread focusing on a single year
    tab_by_years = {}
    for year in years: 
        tab_by_years[year] = (tab[tab['year'] == year])
    
    # Pack up arguments
    argz = [(tab_by_years[year], att_functs, year, procr) for year in years]

    if threads == 1: 
        # Eschew multiprocessing for debugging ease
        results = [process_year(arg) for arg in argz]
    else: 
        with Pool(threads) as p: 
            results = p.map(process_year, argz)


    # unpack results by year
    run_results = {}
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

    # Build the attribute table    
    attribute_table = pd.DataFrame(raw_table)


    #tabloo.show(attribute_table)

